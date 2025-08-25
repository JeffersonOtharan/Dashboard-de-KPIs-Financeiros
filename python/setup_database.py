#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 Configuração Automática do Banco de Dados
Monitoramento de KPIs Financeiros - Nível Avançado

Este script configura automaticamente o banco de dados
e cria as tabelas necessárias para o sistema de KPIs.
"""

import mysql.connector
from mysql.connector import Error
import os
import sys
from datetime import datetime
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('setup_database.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class DatabaseSetup:
    """Classe para configuração automática do banco de dados"""
    
    def __init__(self, host='localhost', user='root', password=None, database='kpis_financeiros_avancado'):
        """Inicializa a conexão com o banco de dados"""
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        
    def connect(self):
        """Estabelece conexão com o MySQL"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci'
            )
            logger.info("✅ Conexão com MySQL estabelecida com sucesso!")
            return True
        except Error as e:
            logger.error(f"❌ Erro ao conectar com MySQL: {e}")
            return False
    
    def create_database(self):
        """Cria o banco de dados se não existir"""
        try:
            cursor = self.connection.cursor()
            
            # Criar banco de dados
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            logger.info(f"✅ Banco de dados '{self.database}' criado/verificado com sucesso!")
            
            # Selecionar o banco
            cursor.execute(f"USE {self.database}")
            logger.info(f"✅ Banco de dados '{self.database}' selecionado!")
            
            cursor.close()
            return True
            
        except Error as e:
            logger.error(f"❌ Erro ao criar banco de dados: {e}")
            return False
    
    def execute_sql_file(self, file_path):
        """Executa um arquivo SQL"""
        try:
            if not os.path.exists(file_path):
                logger.error(f"❌ Arquivo SQL não encontrado: {file_path}")
                return False
            
            cursor = self.connection.cursor()
            
            with open(file_path, 'r', encoding='utf-8') as file:
                sql_content = file.read()
                
            # Dividir o conteúdo em comandos individuais
            commands = sql_content.split(';')
            
            for command in commands:
                command = command.strip()
                if command and not command.startswith('--'):
                    try:
                        cursor.execute(command)
                        logger.info(f"✅ Comando SQL executado com sucesso")
                    except Error as e:
                        if "already exists" not in str(e).lower():
                            logger.warning(f"⚠️ Aviso ao executar comando: {e}")
            
            cursor.close()
            logger.info(f"✅ Arquivo SQL '{file_path}' executado com sucesso!")
            return True
            
        except Error as e:
            logger.error(f"❌ Erro ao executar arquivo SQL '{file_path}': {e}")
            return False
    
    def verify_setup(self):
        """Verifica se a configuração foi bem-sucedida"""
        try:
            cursor = self.connection.cursor()
            
            # Verificar tabelas
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            logger.info(f"📊 Tabelas encontradas: {len(tables)}")
            
            for table in tables:
                logger.info(f"   - {table[0]}")
            
            # Verificar views
            cursor.execute("SHOW FULL TABLES WHERE Table_type = 'VIEW'")
            views = cursor.fetchall()
            logger.info(f"🔍 Views encontradas: {len(views)}")
            
            for view in views:
                logger.info(f"   - {view[0]}")
            
            cursor.close()
            return True
            
        except Error as e:
            logger.error(f"❌ Erro ao verificar configuração: {e}")
            return False
    
    def close(self):
        """Fecha a conexão com o banco"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("🔌 Conexão com banco de dados fechada")

def main():
    """Função principal de configuração"""
    logger.info("🚀 Iniciando configuração automática do banco de dados...")
    
    # Solicitar credenciais
    print("\n📊 CONFIGURAÇÃO DO BANCO DE DADOS")
    print("=" * 50)
    
    host = input("Host MySQL (padrão: localhost): ").strip() or 'localhost'
    user = input("Usuário MySQL (padrão: root): ").strip() or 'root'
    password = input("Senha MySQL (deixe em branco se não houver): ").strip() or None
    
    # Criar instância da classe
    db_setup = DatabaseSetup(host=host, user=user, password=password)
    
    try:
        # Conectar ao MySQL
        if not db_setup.connect():
            logger.error("❌ Falha na conexão. Verifique as credenciais e tente novamente.")
            return
        
        # Criar banco de dados
        if not db_setup.create_database():
            logger.error("❌ Falha na criação do banco de dados.")
            return
        
        # Executar scripts SQL em ordem
        scripts = [
            '../database/01_create_database.sql',
            '../database/02_populate_data.sql',
            '../database/03_create_views.sql'
        ]
        
        for script in scripts:
            logger.info(f"📋 Executando script: {script}")
            if not db_setup.execute_sql_file(script):
                logger.error(f"❌ Falha na execução do script: {script}")
                return
        
        # Verificar configuração
        logger.info("🔍 Verificando configuração...")
        if not db_setup.verify_setup():
            logger.error("❌ Falha na verificação da configuração.")
            return
        
        logger.info("🎉 CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
        logger.info("📋 Próximos passos:")
        logger.info("   1. Execute: python load_sample_data.py")
        logger.info("   2. Execute: streamlit run dashboard/main.py")
        
    except Exception as e:
        logger.error(f"❌ Erro inesperado: {e}")
    
    finally:
        db_setup.close()

if __name__ == "__main__":
    main()
