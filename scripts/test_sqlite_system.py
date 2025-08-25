#!/usr/bin/env python3
"""
Script de teste para o sistema de KPIs Financeiros com SQLite
Sistema de monitoramento executivo de resultados
"""

import sqlite3
import pandas as pd
import sys
import os

# Adicionar diretório pai ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_database_connection():
    """Testa conexão com o banco SQLite"""
    print("Testando conexão com banco SQLite...")
    
    try:
        db_path = "kpis_financeiros.db"
        if not os.path.exists(db_path):
            print(f"ERRO: Banco não encontrado: {db_path}")
            return False
        
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        
        # Testar se consegue executar uma query simples
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"STATUS: Conectado ao banco: {db_path}")
        print(f"INFO: Tabelas encontradas: {len(tables)}")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"ERRO na conexão: {e}")
        return False

def test_tables_existence():
    """Testa se as tabelas principais existem"""
    print("\nTestando existência das tabelas...")
    
    try:
        connection = sqlite3.connect("kpis_financeiros.db")
        cursor = connection.cursor()
        
        expected_tables = [
            'empresas', 'categorias', 'receitas', 'despesas', 
            'metas_mensais', 'kpis_calculados'
        ]
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        missing_tables = []
        for table in expected_tables:
            if table in existing_tables:
                print(f"STATUS: Tabela {table}: OK")
            else:
                print(f"ERRO: Tabela {table}: FALTANDO")
                missing_tables.append(table)
        
        connection.close()
        
        if missing_tables:
            print(f"AVISO: Tabelas faltando: {missing_tables}")
            return False
        else:
            print("STATUS: Todas as tabelas principais existem")
            return True
            
    except Exception as e:
        print(f"ERRO ao testar tabelas: {e}")
        return False

def test_data_counts():
    """Testa contagens básicas de dados"""
    print("\nTestando contagens de dados...")
    
    try:
        connection = sqlite3.connect("kpis_financeiros.db")
        
        # Contar registros em cada tabela
        tables_data = {
            'empresas': 'SELECT COUNT(*) FROM empresas',
            'categorias': 'SELECT COUNT(*) FROM categorias',
            'receitas': 'SELECT COUNT(*) FROM receitas',
            'despesas': 'SELECT COUNT(*) FROM despesas',
            'metas_mensais': 'SELECT COUNT(*) FROM metas_mensais'
        }
        
        for table, query in tables_data.items():
            count = pd.read_sql_query(query, connection)
            count_value = count.iloc[0, 0]
            print(f"INFO: {table}: {count_value} registros")
            
            if count_value == 0:
                print(f"AVISO: Tabela {table} está vazia")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"ERRO ao testar contagens: {e}")
        return False

def test_basic_queries():
    """Testa queries básicas do sistema"""
    print("\nTestando queries básicas...")
    
    try:
        connection = sqlite3.connect("kpis_financeiros.db")
        
        # Teste 1: Resumo financeiro
        print("Testando resumo financeiro...")
        query_resumo = """
            SELECT 
                e.nome_empresa,
                COUNT(r.id_receita) as num_receitas,
                COUNT(d.id_despesa) as num_despesas
            FROM empresas e
            LEFT JOIN receitas r ON e.id_empresa = r.id_empresa
            LEFT JOIN despesas d ON e.id_empresa = d.id_empresa
            GROUP BY e.id_empresa, e.nome_empresa
        """
        
        df_resumo = pd.read_sql_query(query_resumo, connection)
        if not df_resumo.empty:
            print("STATUS: Query de resumo financeiro funcionando")
            print(df_resumo)
        else:
            print("AVISO: Query de resumo retornou dados vazios")
        
        # Teste 2: Evolução de receitas
        print("\nTestando evolução de receitas...")
        query_evolucao = """
            SELECT 
                strftime('%Y-%m', data_receita) as mes_ano,
                SUM(valor) as total_receitas
            FROM receitas
            GROUP BY strftime('%Y-%m', data_receita)
            ORDER BY mes_ano DESC
            LIMIT 5
        """
        
        df_evolucao = pd.read_sql_query(query_evolucao, connection)
        if not df_evolucao.empty:
            print("STATUS: Query de evolução funcionando")
            print(df_evolucao)
        else:
            print("AVISO: Query de evolução retornou dados vazios")
        
        # Teste 3: Despesas por categoria
        print("\nTestando despesas por categoria...")
        query_despesas = """
            SELECT 
                c.nome_categoria,
                SUM(d.valor) as total_despesas
            FROM despesas d
            JOIN categorias c ON d.id_categoria = c.id_categoria
            WHERE c.tipo = 'despesa'
            GROUP BY c.id_categoria, c.nome_categoria
            ORDER BY total_despesas DESC
        """
        
        df_despesas = pd.read_sql_query(query_despesas, connection)
        if not df_despesas.empty:
            print("STATUS: Query de despesas por categoria funcionando")
            print(df_despesas)
        else:
            print("AVISO: Query de despesas por categoria retornou dados vazios")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"ERRO ao testar queries: {e}")
        return False

def test_python_dependencies():
    """Testa dependências Python"""
    print("\nTestando dependências Python...")
    
    dependencies = [
        'streamlit', 'plotly', 'pandas', 'numpy', 'sqlite3'
    ]
    
    missing_deps = []
    for dep in dependencies:
        try:
            if dep == 'sqlite3':
                import sqlite3
                print(f"STATUS: {dep}: OK (built-in)")
            else:
                __import__(dep)
                print(f"STATUS: {dep}: OK")
        except ImportError:
            print(f"ERRO: {dep}: FALTANDO")
            missing_deps.append(dep)
    
    if missing_deps:
        print(f"AVISO: Dependências faltando: {missing_deps}")
        return False
    else:
        print("STATUS: Todas as dependências Python estão instaladas")
        return True

def main():
    """Função principal de teste"""
    print("TESTE DO SISTEMA DE KPIs FINANCEIROS (SQLite)")
    print("=" * 60)
    
    # Executar todos os testes
    tests = [
        ("Conexão com Banco", test_database_connection),
        ("Existência de Tabelas", test_tables_existence),
        ("Contagens de Dados", test_data_counts),
        ("Queries Básicas", test_basic_queries),
        ("Dependências Python", test_python_dependencies)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"ERRO no teste {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumo dos resultados
    print("\n" + "=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASSOU" if result else "FALHOU"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nRESULTADO: {passed}/{total} testes passaram")
    
    if passed == total:
        print("TODOS OS TESTES PASSARAM")
        print("\nPRÓXIMOS PASSOS:")
        print("   1. Execute o dashboard: python -m streamlit run dashboard_app.py")
        print("   2. Ou configure o banco MySQL se preferir")
    else:
        print("ALGUNS TESTES FALHARAM")
        print("\nVERIFICAÇÕES NECESSÁRIAS:")
        print("   1. Se o banco SQLite foi criado corretamente")
        print("   2. Se todas as dependências estão instaladas")
        print("   3. Os logs de erro para mais detalhes")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    exit(main())
