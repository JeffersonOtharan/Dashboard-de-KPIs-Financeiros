#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 Carregamento Automático de Dados CSV
Monitoramento de KPIs Financeiros - Nível Avançado

Este script carrega automaticamente dados de CSVs para
o banco de dados, permitindo atualização em lote.
"""

import mysql.connector
from mysql.connector import Error
import pandas as pd
import os
import sys
from datetime import datetime
import logging
import argparse
from pathlib import Path

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('load_csv_data.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class CSVDataLoader:
    """Classe para carregamento automático de dados CSV"""
    
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
                database=self.database,
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci'
            )
            logger.info("✅ Conexão com banco de dados estabelecida com sucesso!")
            return True
        except Error as e:
            logger.error(f"❌ Erro ao conectar com banco de dados: {e}")
            return False
    
    def validate_csv_structure(self, df, expected_columns, table_name):
        """Valida a estrutura do CSV"""
        missing_columns = set(expected_columns) - set(df.columns)
        extra_columns = set(df.columns) - set(expected_columns)
        
        if missing_columns:
            logger.error(f"❌ Colunas obrigatórias ausentes em {table_name}: {missing_columns}")
            return False
        
        if extra_columns:
            logger.warning(f"⚠️ Colunas extras em {table_name}: {extra_columns}")
        
        logger.info(f"✅ Estrutura do CSV {table_name} validada com sucesso!")
        return True
    
    def load_receitas_from_csv(self, csv_path):
        """Carrega dados de receitas do CSV"""
        try:
            logger.info(f"📊 Carregando receitas do arquivo: {csv_path}")
            
            # Ler CSV
            df = pd.read_csv(csv_path)
            logger.info(f"📋 {len(df)} registros de receitas encontrados")
            
            # Colunas esperadas para receitas
            expected_columns = [
                'id_empresa', 'id_categoria', 'codigo_transacao', 'descricao',
                'valor', 'valor_liquido', 'data_receita', 'data_recebimento',
                'status', 'fonte_receita', 'cliente', 'forma_recebimento'
            ]
            
            # Validar estrutura
            if not self.validate_csv_structure(df, expected_columns, 'receitas'):
                return False
            
            # Preparar dados
            df['data_receita'] = pd.to_datetime(df['data_receita']).dt.date
            df['data_recebimento'] = pd.to_datetime(df['data_recebimento']).dt.date
            df['parcelado'] = df.get('parcelado', False)
            df['num_parcelas'] = df.get('num_parcelas', 1)
            
            # Inserir no banco
            cursor = self.connection.cursor()
            
            for _, row in df.iterrows():
                sql = """
                INSERT INTO receitas (
                    id_empresa, id_categoria, codigo_transacao, descricao,
                    valor, valor_liquido, data_receita, data_recebimento,
                    status, fonte_receita, cliente, forma_recebimento,
                    parcelado, num_parcelas
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                values = (
                    row['id_empresa'], row['id_categoria'], row['codigo_transacao'],
                    row['descricao'], row['valor'], row['valor_liquido'],
                    row['data_receita'], row['data_recebimento'], row['status'],
                    row['fonte_receita'], row['cliente'], row['forma_recebimento'],
                    row['parcelado'], row['num_parcelas']
                )
                
                cursor.execute(sql, values)
            
            self.connection.commit()
            cursor.close()
            
            logger.info(f"✅ {len(df)} receitas carregadas com sucesso!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao carregar receitas: {e}")
            return False
    
    def load_despesas_from_csv(self, csv_path):
        """Carrega dados de despesas do CSV"""
        try:
            logger.info(f"📊 Carregando despesas do arquivo: {csv_path}")
            
            # Ler CSV
            df = pd.read_csv(csv_path)
            logger.info(f"📋 {len(df)} registros de despesas encontrados")
            
            # Colunas esperadas para despesas
            expected_columns = [
                'id_empresa', 'id_categoria', 'codigo_transacao', 'descricao',
                'valor', 'valor_liquido', 'data_despesa', 'data_pagamento',
                'status', 'fornecedor', 'forma_pagamento'
            ]
            
            # Validar estrutura
            if not self.validate_csv_structure(df, expected_columns, 'despesas'):
                return False
            
            # Preparar dados
            df['data_despesa'] = pd.to_datetime(df['data_despesa']).dt.date
            df['data_pagamento'] = pd.to_datetime(df['data_pagamento']).dt.date
            df['parcelado'] = df.get('parcelado', False)
            df['num_parcelas'] = df.get('num_parcelas', 1)
            
            # Inserir no banco
            cursor = self.connection.cursor()
            
            for _, row in df.iterrows():
                sql = """
                INSERT INTO despesas (
                    id_empresa, id_categoria, codigo_transacao, descricao,
                    valor, valor_liquido, data_despesa, data_pagamento,
                    status, fornecedor, forma_pagamento,
                    parcelado, num_parcelas
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                values = (
                    row['id_empresa'], row['id_categoria'], row['codigo_transacao'],
                    row['descricao'], row['valor'], row['valor_liquido'],
                    row['data_despesa'], row['data_pagamento'], row['status'],
                    row['fornecedor'], row['forma_pagamento'],
                    row['parcelado'], row['num_parcelas']
                )
                
                cursor.execute(sql, values)
            
            self.connection.commit()
            cursor.close()
            
            logger.info(f"✅ {len(df)} despesas carregadas com sucesso!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao carregar despesas: {e}")
            return False
    
    def load_metas_from_csv(self, csv_path):
        """Carrega dados de metas do CSV"""
        try:
            logger.info(f"📊 Carregando metas do arquivo: {csv_path}")
            
            # Ler CSV
            df = pd.read_csv(csv_path)
            logger.info(f"📋 {len(df)} registros de metas encontrados")
            
            # Colunas esperadas para metas
            expected_columns = [
                'id_empresa', 'ano', 'mes', 'id_categoria',
                'meta_receita', 'meta_despesa', 'meta_lucro', 'meta_margem'
            ]
            
            # Validar estrutura
            if not self.validate_csv_structure(df, expected_columns, 'metas'):
                return False
            
            # Inserir no banco
            cursor = self.connection.cursor()
            
            for _, row in df.iterrows():
                sql = """
                INSERT INTO metas_mensais (
                    id_empresa, ano, mes, id_categoria,
                    meta_receita, meta_despesa, meta_lucro, meta_margem
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    meta_receita = VALUES(meta_receita),
                    meta_despesa = VALUES(meta_despesa),
                    meta_lucro = VALUES(meta_lucro),
                    meta_margem = VALUES(meta_margem)
                """
                
                values = (
                    row['id_empresa'], row['ano'], row['mes'], row['id_categoria'],
                    row['meta_receita'], row['meta_despesa'], row['meta_lucro'], row['meta_margem']
                )
                
                cursor.execute(sql, values)
            
            self.connection.commit()
            cursor.close()
            
            logger.info(f"✅ {len(df)} metas carregadas com sucesso!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao carregar metas: {e}")
            return False
    
    def process_csv_directory(self, csv_dir):
        """Processa todos os CSVs de um diretório"""
        try:
            csv_dir = Path(csv_dir)
            if not csv_dir.exists():
                logger.error(f"❌ Diretório não encontrado: {csv_dir}")
                return False
            
            logger.info(f"📁 Processando diretório: {csv_dir}")
            
            # Processar cada tipo de CSV
            csv_files = {
                'receitas': list(csv_dir.glob('*receitas*.csv')),
                'despesas': list(csv_dir.glob('*despesas*.csv')),
                'metas': list(csv_dir.glob('*metas*.csv'))
            }
            
            success_count = 0
            
            for csv_type, files in csv_files.items():
                for csv_file in files:
                    logger.info(f"📋 Processando arquivo: {csv_file}")
                    
                    if csv_type == 'receitas':
                        if self.load_receitas_from_csv(csv_file):
                            success_count += 1
                    elif csv_type == 'despesas':
                        if self.load_despesas_from_csv(csv_file):
                            success_count += 1
                    elif csv_type == 'metas':
                        if self.load_metas_from_csv(csv_file):
                            success_count += 1
            
            logger.info(f"✅ Processamento concluído! {success_count} arquivos processados com sucesso!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar diretório: {e}")
            return False
    
    def close(self):
        """Fecha a conexão com o banco"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("🔌 Conexão com banco de dados fechada")

def main():
    """Função principal de carregamento"""
    parser = argparse.ArgumentParser(description='Carregamento automático de dados CSV')
    parser.add_argument('--csv-dir', default='../data', help='Diretório com arquivos CSV')
    parser.add_argument('--host', default='localhost', help='Host MySQL')
    parser.add_argument('--user', default='root', help='Usuário MySQL')
    parser.add_argument('--password', help='Senha MySQL')
    parser.add_argument('--database', default='kpis_financeiros_avancado', help='Nome do banco')
    
    args = parser.parse_args()
    
    logger.info("🚀 Iniciando carregamento automático de dados CSV...")
    
    # Criar instância da classe
    loader = CSVDataLoader(
        host=args.host,
        user=args.user,
        password=args.password,
        database=args.database
    )
    
    try:
        # Conectar ao banco
        if not loader.connect():
            logger.error("❌ Falha na conexão. Verifique as credenciais e tente novamente.")
            return
        
        # Processar diretório CSV
        if not loader.process_csv_directory(args.csv_dir):
            logger.error("❌ Falha no processamento dos CSVs.")
            return
        
        logger.info("🎉 CARREGAMENTO CONCLUÍDO COM SUCESSO!")
        logger.info("📋 Próximos passos:")
        logger.info("   1. Execute: streamlit run dashboard/main.py")
        logger.info("   2. Verifique os dados no dashboard")
        
    except Exception as e:
        logger.error(f"❌ Erro inesperado: {e}")
    
    finally:
        loader.close()

if __name__ == "__main__":
    main()
