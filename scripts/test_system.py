#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Teste Rápido do Sistema
Monitoramento de KPIs Financeiros - Nível Avançado

Este script testa rapidamente se todos os componentes
do sistema estão funcionando corretamente.
"""

import sys
import os
import mysql.connector
from mysql.connector import Error
import pandas as pd

def test_database_connection():
    """Testa conexão com o banco de dados"""
    print("🔍 Testando conexão com banco de dados...")
    
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='kpis_financeiros_avancado',
            charset='utf8mb4'
        )
        
        if connection.is_connected():
            print("✅ Conexão com banco estabelecida com sucesso!")
            
            # Testar queries básicas
            cursor = connection.cursor()
            
            # Testar tabelas
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"📊 Tabelas encontradas: {len(tables)}")
            
            # Testar views
            cursor.execute("SHOW FULL TABLES WHERE Table_type = 'VIEW'")
            views = cursor.fetchall()
            print(f"🔍 Views encontradas: {len(views)}")
            
            # Testar dados
            cursor.execute("SELECT COUNT(*) FROM empresas")
            empresas_count = cursor.fetchone()[0]
            print(f"🏢 Empresas: {empresas_count}")
            
            cursor.execute("SELECT COUNT(*) FROM categorias")
            categorias_count = cursor.fetchone()[0]
            print(f"📋 Categorias: {categorias_count}")
            
            cursor.execute("SELECT COUNT(*) FROM receitas WHERE YEAR(data_receita) = 2024")
            receitas_count = cursor.fetchone()[0]
            print(f"💰 Receitas 2024: {receitas_count}")
            
            cursor.execute("SELECT COUNT(*) FROM despesas WHERE YEAR(data_despesa) = 2024")
            despesas_count = cursor.fetchone()[0]
            print(f"💸 Despesas 2024: {despesas_count}")
            
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        print(f"❌ Erro na conexão: {e}")
        return False

def test_views():
    """Testa as views principais"""
    print("\n🔍 Testando views principais...")
    
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='kpis_financeiros_avancado',
            charset='utf8mb4'
        )
        
        # Testar view de resumo executivo
        df_resumo = pd.read_sql("SELECT * FROM vw_resumo_financeiro_executivo LIMIT 5", connection)
        print(f"✅ View Resumo Executivo: {len(df_resumo)} registros")
        
        # Testar view de margem de lucro
        df_margem = pd.read_sql("SELECT * FROM vw_analise_margem_lucro LIMIT 5", connection)
        print(f"✅ View Margem de Lucro: {len(df_margem)} registros")
        
        # Testar view de receita vs meta
        df_meta = pd.read_sql("SELECT * FROM vw_receita_vs_meta LIMIT 5", connection)
        print(f"✅ View Receita vs Meta: {len(df_meta)} registros")
        
        # Testar view de despesas por categoria
        df_despesas = pd.read_sql("SELECT * FROM vw_despesas_por_categoria LIMIT 5", connection)
        print(f"✅ View Despesas por Categoria: {len(df_despesas)} registros")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar views: {e}")
        return False

def test_kpis():
    """Testa os principais KPIs"""
    print("\n🎯 Testando principais KPIs...")
    
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='kpis_financeiros_avancado',
            charset='utf8mb4'
        )
        
        # KPI 1: Margem de Lucro
        df_margem = pd.read_sql("""
            SELECT * FROM vw_resumo_financeiro_executivo 
            WHERE ano = 2024 
            ORDER BY ano DESC, mes DESC
        """, connection)
        
        if not df_margem.empty:
            margem_media = df_margem['margem_lucro_percentual'].mean()
            print(f"✅ KPI Margem de Lucro: {margem_media:.1f}% (média)")
        
        # KPI 2: Receita vs Meta
        df_meta = pd.read_sql("""
            SELECT * FROM vw_receita_vs_meta 
            WHERE ano = 2024 AND mes = 12
        """, connection)
        
        if not df_meta.empty:
            print(f"✅ KPI Receita vs Meta: {len(df_meta)} categorias analisadas")
        
        # KPI 3: Despesas por Categoria
        df_despesas = pd.read_sql("""
            SELECT * FROM vw_despesas_por_categoria 
            ORDER BY total_despesas DESC
        """, connection)
        
        if not df_despesas.empty:
            total_despesas = df_despesas['total_despesas'].sum()
            print(f"✅ KPI Despesas por Categoria: R$ {total_despesas:,.2f} (total)")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar KPIs: {e}")
        return False

def test_python_dependencies():
    """Testa dependências Python"""
    print("\n🐍 Testando dependências Python...")
    
    try:
        import streamlit
        print("✅ Streamlit instalado")
        
        import plotly
        print("✅ Plotly instalado")
        
        import pandas
        print("✅ Pandas instalado")
        
        import numpy
        print("✅ Numpy instalado")
        
        return True
        
    except ImportError as e:
        print(f"❌ Dependência não encontrada: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🧪 TESTE RÁPIDO DO SISTEMA DE KPIs FINANCEIROS")
    print("=" * 60)
    
    tests = [
        ("Conexão com Banco", test_database_connection),
        ("Views do Sistema", test_views),
        ("Cálculo de KPIs", test_kpis),
        ("Dependências Python", test_python_dependencies)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erro no teste {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumo dos testes
    print("\n📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 RESULTADO: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 SISTEMA FUNCIONANDO PERFEITAMENTE!")
        print("\n📋 Próximos passos:")
        print("   1. Execute: streamlit run dashboard/main.py")
        print("   2. Acesse o dashboard no navegador")
        print("   3. Monitore seus KPIs financeiros!")
    else:
        print("⚠️ ALGUNS TESTES FALHARAM!")
        print("\n🔧 Verifique:")
        print("   1. Se o MySQL está rodando")
        print("   2. Se o banco foi criado corretamente")
        print("   3. Se as dependências Python estão instaladas")
        print("   4. Os logs de erro para mais detalhes")

if __name__ == "__main__":
    main()
