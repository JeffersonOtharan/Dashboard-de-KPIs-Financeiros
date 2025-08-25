#!/usr/bin/env python3
"""
Script para iniciar o dashboard de KPIs Financeiros
Sistema de monitoramento executivo de resultados
"""

import subprocess
import sys
import os
import time

def main():
    """Função principal"""
    print("INICIANDO DASHBOARD DE KPIs FINANCEIROS")
    print("=" * 50)
    
    # Verificar se o banco existe
    if not os.path.exists("kpis_financeiros.db"):
        print("ERRO: Banco de dados não encontrado!")
        print("SOLUÇÃO: Execute primeiro: python python/setup_sqlite_database.py")
        return 1
    
    print("STATUS: Banco de dados encontrado")
    
    # Verificar se o Streamlit está instalado
    try:
        import streamlit
        print("STATUS: Streamlit instalado")
    except ImportError:
        print("ERRO: Streamlit não está instalado!")
        print("SOLUÇÃO: Execute: python -m pip install streamlit")
        return 1
    
    # Verificar se o dashboard existe
    if not os.path.exists("dashboard_app.py"):
        print("ERRO: Arquivo do dashboard não encontrado!")
        return 1
    
    print("STATUS: Arquivo do dashboard encontrado")
    print("\nINICIANDO DASHBOARD...")
    print("ACESSO: Abra seu navegador em: http://localhost:8501")
    print("CONTROLE: Para parar, pressione Ctrl+C")
    print("-" * 50)
    
    try:
        # Iniciar o dashboard
        cmd = [sys.executable, "-m", "streamlit", "run", "dashboard_app.py", "--server.port", "8501"]
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n\nDASHBOARD INTERROMPIDO PELO USUÁRIO")
    except Exception as e:
        print(f"\nERRO ao iniciar dashboard: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
