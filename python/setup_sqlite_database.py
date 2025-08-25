#!/usr/bin/env python3
"""
Script para configurar banco SQLite como alternativa ao MySQL
Sistema de monitoramento de KPIs financeiros
"""

import sqlite3
import os
import logging
from datetime import datetime, timedelta
import json

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SQLiteSetup:
    """Classe para configurar banco SQLite"""
    
    def __init__(self, db_path="kpis_financeiros.db"):
        """Inicializa com caminho do banco"""
        self.db_path = db_path
        self.connection = None
        
    def create_database(self):
        """Cria o banco e todas as tabelas"""
        try:
            # Conecta ao banco (cria se não existir)
            self.connection = sqlite3.connect(self.db_path)
            cursor = self.connection.cursor()
            
            logger.info(f"Banco SQLite criado/conectado: {self.db_path}")
            
            # Criar tabelas
            self._create_tables(cursor)
            
            # Inserir dados de exemplo
            self._insert_sample_data(cursor)
            
            # Criar views (SQLite não suporta views complexas, mas podemos criar tabelas auxiliares)
            self._create_auxiliary_tables(cursor)
            
            self.connection.commit()
            logger.info("Banco configurado com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao criar banco: {e}")
            raise
        finally:
            if self.connection:
                self.connection.close()
    
    def _create_tables(self, cursor):
        """Cria todas as tabelas necessárias"""
        
        # Tabela empresas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS empresas (
                id_empresa INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_empresa TEXT NOT NULL,
                setor TEXT,
                ativo BOOLEAN DEFAULT 1,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabela categorias
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categorias (
                id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_categoria TEXT NOT NULL,
                tipo TEXT CHECK(tipo IN ('receita', 'despesa')) NOT NULL,
                ativo BOOLEAN DEFAULT 1
            )
        """)
        
        # Tabela receitas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS receitas (
                id_receita INTEGER PRIMARY KEY AUTOINCREMENT,
                id_empresa INTEGER NOT NULL,
                id_categoria INTEGER NOT NULL,
                codigo_transacao TEXT UNIQUE,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL CHECK (valor > 0),
                valor_liquido REAL NOT NULL CHECK (valor_liquido > 0),
                data_receita DATE NOT NULL,
                data_recebimento DATE,
                status TEXT DEFAULT 'pendente',
                fonte_receita TEXT,
                cliente TEXT,
                forma_recebimento TEXT NOT NULL,
                parcelado BOOLEAN DEFAULT 0,
                num_parcelas INTEGER DEFAULT 1,
                observacoes TEXT,
                tags TEXT,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY (id_empresa) REFERENCES empresas (id_empresa),
                FOREIGN KEY (id_categoria) REFERENCES categorias (id_categoria)
            )
        """)
        
        # Tabela despesas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS despesas (
                id_despesa INTEGER PRIMARY KEY AUTOINCREMENT,
                id_empresa INTEGER NOT NULL,
                id_categoria INTEGER NOT NULL,
                codigo_transacao TEXT UNIQUE,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL CHECK (valor > 0),
                valor_liquido REAL NOT NULL CHECK (valor_liquido > 0),
                data_despesa DATE NOT NULL,
                data_pagamento DATE,
                status TEXT DEFAULT 'pendente',
                fornecedor TEXT,
                forma_pagamento TEXT NOT NULL,
                parcelado BOOLEAN DEFAULT 0,
                num_parcelas INTEGER DEFAULT 1,
                observacoes TEXT,
                tags TEXT,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY (id_empresa) REFERENCES empresas (id_empresa),
                FOREIGN KEY (id_categoria) REFERENCES categorias (id_categoria)
            )
        """)
        
        # Tabela metas mensais
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metas_mensais (
                id_meta INTEGER PRIMARY KEY AUTOINCREMENT,
                id_empresa INTEGER NOT NULL,
                ano INTEGER NOT NULL,
                mes INTEGER NOT NULL CHECK (mes >= 1 AND mes <= 12),
                meta_receita REAL NOT NULL CHECK (meta_receita > 0),
                meta_despesa REAL NOT NULL CHECK (meta_despesa > 0),
                meta_lucro REAL,
                observacoes TEXT,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY (id_empresa) REFERENCES empresas (id_empresa),
                UNIQUE(id_empresa, ano, mes)
            )
        """)
        
        # Tabela KPIs calculados (cache)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS kpis_calculados (
                id_kpi INTEGER PRIMARY KEY AUTOINCREMENT,
                id_empresa INTEGER NOT NULL,
                ano INTEGER NOT NULL,
                mes INTEGER NOT NULL,
                tipo_kpi TEXT NOT NULL,
                valor_kpi REAL NOT NULL,
                data_calculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY (id_empresa) REFERENCES empresas (id_empresa),
                UNIQUE(id_empresa, ano, mes, tipo_kpi)
            )
        """)
        
        logger.info("Tabelas criadas com sucesso")
    
    def _insert_sample_data(self, cursor):
        """Insere dados de exemplo"""
        
        # Inserir empresa
        cursor.execute("""
            INSERT OR IGNORE INTO empresas (id_empresa, nome_empresa, setor) 
            VALUES (1, 'TechCorp Solutions', 'Tecnologia')
        """)
        
        # Inserir categorias
        categorias = [
            (1, 'Vendas de Software', 'receita'),
            (2, 'Consultoria', 'receita'),
            (3, 'Suporte Técnico', 'receita'),
            (4, 'Salários', 'despesa'),
            (5, 'Infraestrutura', 'despesa'),
            (6, 'Marketing', 'despesa'),
            (7, 'Impostos', 'despesa')
        ]
        
        for cat in categorias:
            cursor.execute("""
                INSERT OR IGNORE INTO categorias (id_categoria, nome_categoria, tipo) 
                VALUES (?, ?, ?)
            """, cat)
        
        # Inserir receitas de exemplo (2024)
        receitas = [
            (1, 1, 'REC001', 'Licença Software Enterprise', 50000.00, 47500.00, '2024-01-15', '2024-01-15', 'recebido', 'Venda Direta', 'Empresa ABC', 'transferencia', 0, 1, 'Licença anual'),
            (1, 2, 'REC002', 'Consultoria Projeto X', 25000.00, 23750.00, '2024-01-20', '2024-02-15', 'recebido', 'Consultoria', 'Empresa XYZ', 'pix', 0, 1, 'Projeto de 3 meses'),
            (1, 3, 'REC003', 'Suporte Premium', 15000.00, 14250.00, '2024-02-01', '2024-02-01', 'recebido', 'Suporte', 'Empresa ABC', 'cartao_credito', 0, 1, 'Suporte mensal'),
            (1, 1, 'REC004', 'Licença Software Pro', 30000.00, 28500.00, '2024-02-15', '2024-03-01', 'recebido', 'Venda Direta', 'Empresa DEF', 'boleto', 0, 1, 'Licença semestral'),
            (1, 2, 'REC005', 'Consultoria Projeto Y', 35000.00, 33250.00, '2024-03-01', '2024-03-15', 'recebido', 'Consultoria', 'Empresa GHI', 'transferencia', 0, 1, 'Projeto de 4 meses'),
            (1, 3, 'REC006', 'Suporte Premium', 15000.00, 14250.00, '2024-03-01', '2024-03-01', 'recebido', 'Suporte', 'Empresa ABC', 'cartao_credito', 0, 1, 'Suporte mensal'),
            (1, 1, 'REC007', 'Licença Software Enterprise', 60000.00, 57000.00, '2024-04-01', '2024-04-15', 'recebido', 'Venda Direta', 'Empresa JKL', 'transferencia', 0, 1, 'Licença anual'),
            (1, 2, 'REC008', 'Consultoria Projeto Z', 40000.00, 38000.00, '2024-05-01', '2024-05-15', 'recebido', 'Consultoria', 'Empresa MNO', 'pix', 0, 1, 'Projeto de 6 meses'),
            (1, 3, 'REC009', 'Suporte Premium', 15000.00, 14250.00, '2024-05-01', '2024-05-01', 'recebido', 'Suporte', 'Empresa ABC', 'cartao_credito', 0, 1, 'Suporte mensal'),
            (1, 1, 'REC010', 'Licença Software Pro', 35000.00, 33250.00, '2024-06-01', '2024-06-15', 'recebido', 'Venda Direta', 'Empresa PQR', 'boleto', 0, 1, 'Licença semestral')
        ]
        
        for rec in receitas:
            cursor.execute("""
                INSERT OR IGNORE INTO receitas 
                (id_empresa, id_categoria, codigo_transacao, descricao, valor, valor_liquido, 
                 data_receita, data_recebimento, status, fonte_receita, cliente, 
                 forma_recebimento, parcelado, num_parcelas, observacoes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, rec)
        
        # Inserir despesas de exemplo (2024)
        despesas = [
            (1, 4, 'DESP001', 'Salários Janeiro', 25000.00, 25000.00, '2024-01-31', '2024-01-31', 'pago', 'RH', 'dinheiro', 0, 1, 'Folha de pagamento'),
            (1, 5, 'DESP002', 'Servidor Cloud', 5000.00, 5000.00, '2024-01-15', '2024-01-15', 'pago', 'AWS', 'cartao_credito', 0, 1, 'Serviços de infraestrutura'),
            (1, 6, 'DESP003', 'Google Ads', 3000.00, 3000.00, '2024-01-20', '2024-01-20', 'pago', 'Google', 'cartao_credito', 0, 1, 'Campanha de marketing'),
            (1, 7, 'DESP004', 'Impostos Janeiro', 8000.00, 8000.00, '2024-01-31', '2024-02-20', 'pago', 'Receita Federal', 'boleto', 0, 1, 'Impostos federais'),
            (1, 4, 'DESP005', 'Salários Fevereiro', 25000.00, 25000.00, '2024-02-29', '2024-02-29', 'pago', 'RH', 'dinheiro', 0, 1, 'Folha de pagamento'),
            (1, 5, 'DESP006', 'Servidor Cloud', 5000.00, 5000.00, '2024-02-15', '2024-02-15', 'pago', 'AWS', 'cartao_credito', 0, 1, 'Serviços de infraestrutura'),
            (1, 6, 'DESP007', 'Google Ads', 3000.00, 3000.00, '2024-02-20', '2024-02-20', 'pago', 'Google', 'cartao_credito', 0, 1, 'Campanha de marketing'),
            (1, 7, 'DESP008', 'Impostos Fevereiro', 8000.00, 8000.00, '2024-02-29', '2024-03-20', 'pago', 'Receita Federal', 'boleto', 0, 1, 'Impostos federais'),
            (1, 4, 'DESP009', 'Salários Março', 25000.00, 25000.00, '2024-03-31', '2024-03-31', 'pago', 'RH', 'dinheiro', 0, 1, 'Folha de pagamento'),
            (1, 5, 'DESP010', 'Servidor Cloud', 5000.00, 5000.00, '2024-03-15', '2024-03-15', 'pago', 'AWS', 'cartao_credito', 0, 1, 'Serviços de infraestrutura')
        ]
        
        for desp in despesas:
            cursor.execute("""
                INSERT OR IGNORE INTO despesas 
                (id_empresa, id_categoria, codigo_transacao, descricao, valor, valor_liquido, 
                 data_despesa, data_pagamento, status, fornecedor, 
                 forma_pagamento, parcelado, num_parcelas, observacoes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, desp)
        
        # Inserir metas mensais (2024)
        metas = [
            (1, 2024, 1, 100000.00, 50000.00, 50000.00),
            (1, 2024, 2, 120000.00, 55000.00, 65000.00),
            (1, 2024, 3, 110000.00, 52000.00, 58000.00),
            (1, 2024, 4, 130000.00, 60000.00, 70000.00),
            (1, 2024, 5, 125000.00, 58000.00, 67000.00),
            (1, 2024, 6, 140000.00, 65000.00, 75000.00)
        ]
        
        for meta in metas:
            cursor.execute("""
                INSERT OR IGNORE INTO metas_mensais 
                (id_empresa, ano, mes, meta_receita, meta_despesa, meta_lucro)
                VALUES (?, ?, ?, ?, ?, ?)
            """, meta)
        
        logger.info("Dados de exemplo inseridos com sucesso")
    
    def _create_auxiliary_tables(self, cursor):
        """Cria tabelas auxiliares para simular views do MySQL"""
        
        # Tabela resumo financeiro executivo
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resumo_financeiro_executivo (
                id_resumo INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_empresa TEXT NOT NULL,
                setor TEXT,
                ano INTEGER NOT NULL,
                mes INTEGER NOT NULL,
                mes_ano TEXT NOT NULL,
                total_receitas REAL DEFAULT 0,
                total_despesas REAL DEFAULT 0,
                lucro_bruto REAL DEFAULT 0,
                margem_lucro_percentual REAL DEFAULT 0,
                total_receitas_liquido REAL DEFAULT 0,
                total_despesas_liquido REAL DEFAULT 0,
                lucro_liquido REAL DEFAULT 0,
                margem_liquida_percentual REAL DEFAULT 0,
                status_financeiro TEXT,
                classificacao_margem TEXT,
                data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabela análise de margem de lucro
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analise_margem_lucro (
                id_analise INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_empresa TEXT NOT NULL,
                ano INTEGER NOT NULL,
                mes INTEGER NOT NULL,
                receita_bruta REAL DEFAULT 0,
                despesa_bruta REAL DEFAULT 0,
                lucro_bruto REAL DEFAULT 0,
                margem_bruta_percentual REAL DEFAULT 0,
                receita_liquida REAL DEFAULT 0,
                despesa_liquida REAL DEFAULT 0,
                lucro_liquido REAL DEFAULT 0,
                margem_liquida_percentual REAL DEFAULT 0,
                data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabela receita vs meta
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS receita_vs_meta (
                id_comparacao INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_empresa TEXT NOT NULL,
                ano INTEGER NOT NULL,
                mes INTEGER NOT NULL,
                meta_receita REAL DEFAULT 0,
                receita_realizada REAL DEFAULT 0,
                diferenca_absoluta REAL DEFAULT 0,
                percentual_realizado REAL DEFAULT 0,
                status_meta TEXT,
                data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabela despesas por categoria
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS despesas_por_categoria (
                id_despesa_cat INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_empresa TEXT NOT NULL,
                ano INTEGER NOT NULL,
                mes INTEGER NOT NULL,
                categoria TEXT NOT NULL,
                total_despesas REAL DEFAULT 0,
                percentual_categoria REAL DEFAULT 0,
                data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        logger.info("Tabelas auxiliares criadas com sucesso")
    
    def get_connection(self):
        """Retorna conexão com o banco"""
        return sqlite3.connect(self.db_path)

def main():
    """Função principal"""
    print("CONFIGURANDO BANCO SQLITE PARA KPIs FINANCEIROS")
    print("=" * 60)
    
    try:
        # Criar instância e configurar banco
        setup = SQLiteSetup()
        setup.create_database()
        
        print("\nSTATUS: Banco SQLite configurado com sucesso")
        print(f"LOCALIZAÇÃO: {os.path.abspath(setup.db_path)}")
        print("\nPRÓXIMOS PASSOS:")
        print("   1. Execute o dashboard: python -m streamlit run dashboard_app.py")
        print("   2. Ou teste o sistema: python scripts/test_sqlite_system.py")
        
    except Exception as e:
        print(f"\nERRO ao configurar banco: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
