#!/usr/bin/env python3
"""
Dashboard de KPIs Financeiros - Versão SQLite
Versão simplificada para funcionar sem MySQL
"""

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import logging

# Configuração da página
st.set_page_config(
    page_title="📊 Dashboard KPIs Financeiros (SQLite)",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DashboardKPIsSQLite:
    """Classe principal do dashboard de KPIs com SQLite"""
    
    def __init__(self):
        """Inicializa o dashboard"""
        self.db_path = "kpis_financeiros.db"
        self.connection = None
        self.setup_connection()
    
    def setup_connection(self):
        """Configura conexão com o banco SQLite"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            logger.info("✅ Conexão com banco SQLite estabelecida")
        except Exception as e:
            logger.error(f"❌ Erro na conexão: {e}")
            st.error("❌ Erro na conexão com o banco de dados SQLite")
    
    def execute_query(self, query, params=None):
        """Executa uma query e retorna DataFrame"""
        try:
            if not self.connection:
                self.setup_connection()
            
            if params:
                df = pd.read_sql_query(query, self.connection, params=params)
            else:
                df = pd.read_sql_query(query, self.connection)
            return df
        except Exception as e:
            logger.error(f"❌ Erro na query: {e}")
            st.error(f"❌ Erro na execução da query: {e}")
            return pd.DataFrame()
    
    def get_resumo_financeiro(self):
        """Obtém resumo financeiro executivo"""
        query = """
            SELECT 
                e.nome_empresa,
                e.setor,
                strftime('%Y', r.data_receita) as ano,
                strftime('%m', r.data_receita) as mes,
                strftime('%Y-%m', r.data_receita) as mes_ano,
                COALESCE(SUM(r.valor), 0) as total_receitas,
                COALESCE(SUM(d.valor), 0) as total_despesas,
                COALESCE(SUM(r.valor), 0) - COALESCE(SUM(d.valor), 0) as lucro_bruto,
                CASE 
                    WHEN COALESCE(SUM(r.valor), 0) > 0 
                    THEN ROUND(((COALESCE(SUM(r.valor), 0) - COALESCE(SUM(d.valor), 0)) / COALESCE(SUM(r.valor), 0)) * 100, 2)
                    ELSE 0 
                END as margem_lucro_percentual,
                COALESCE(SUM(r.valor_liquido), 0) as total_receitas_liquido,
                COALESCE(SUM(d.valor_liquido), 0) as total_despesas_liquido,
                COALESCE(SUM(r.valor_liquido), 0) - COALESCE(SUM(d.valor_liquido), 0) as lucro_liquido,
                CASE 
                    WHEN COALESCE(SUM(r.valor_liquido), 0) > 0 
                    THEN ROUND(((COALESCE(SUM(r.valor_liquido), 0) - COALESCE(SUM(d.valor_liquido), 0)) / COALESCE(SUM(r.valor_liquido), 0)) * 100, 2)
                    ELSE 0 
                END as margem_liquida_percentual
            FROM empresas e
            LEFT JOIN receitas r ON e.id_empresa = r.id_empresa
            LEFT JOIN despesas d ON e.id_empresa = d.id_empresa 
                AND strftime('%Y', r.data_receita) = strftime('%Y', d.data_despesa)
                AND strftime('%m', r.data_receita) = strftime('%m', d.data_despesa)
            WHERE e.ativo = 1
            GROUP BY e.nome_empresa, strftime('%Y', r.data_receita), strftime('%m', r.data_receita)
            ORDER BY e.nome_empresa, ano DESC, mes DESC
        """
        return self.execute_query(query)
    
    def get_evolucao_receitas(self):
        """Obtém evolução de receitas por mês"""
        query = """
            SELECT 
                strftime('%Y-%m', data_receita) as mes_ano,
                strftime('%Y', data_receita) as ano,
                strftime('%m', data_receita) as mes,
                SUM(valor) as total_receitas,
                SUM(valor_liquido) as total_receitas_liquido,
                COUNT(*) as num_transacoes
            FROM receitas
            GROUP BY strftime('%Y-%m', data_receita)
            ORDER BY ano DESC, mes DESC
        """
        return self.execute_query(query)
    
    def get_despesas_por_categoria(self):
        """Obtém despesas por categoria"""
        query = """
            SELECT 
                c.nome_categoria,
                SUM(d.valor) as total_despesas,
                COUNT(*) as num_transacoes,
                ROUND((SUM(d.valor) / (SELECT SUM(valor) FROM despesas)) * 100, 2) as percentual
            FROM despesas d
            JOIN categorias c ON d.id_categoria = c.id_categoria
            WHERE c.tipo = 'despesa'
            GROUP BY c.id_categoria, c.nome_categoria
            ORDER BY total_despesas DESC
        """
        return self.execute_query(query)
    
    def get_receita_vs_meta(self):
        """Obtém comparação receita vs meta"""
        query = """
            SELECT 
                m.ano,
                m.mes,
                strftime('%Y-%m', date(m.ano || '-' || printf('%02d', m.mes) || '-01')) as mes_ano,
                m.meta_receita,
                COALESCE(SUM(r.valor), 0) as receita_realizada,
                m.meta_receita - COALESCE(SUM(r.valor), 0) as diferenca,
                CASE 
                    WHEN m.meta_receita > 0 
                    THEN ROUND((COALESCE(SUM(r.valor), 0) / m.meta_receita) * 100, 2)
                    ELSE 0 
                END as percentual_realizado
            FROM metas_mensais m
            LEFT JOIN receitas r ON m.id_empresa = r.id_empresa 
                AND m.ano = CAST(strftime('%Y', r.data_receita) AS INTEGER)
                AND m.mes = CAST(strftime('%m', r.data_receita) AS INTEGER)
            GROUP BY m.ano, m.mes, m.meta_receita
            ORDER BY m.ano DESC, m.mes DESC
        """
        return self.execute_query(query)
    
    def get_analise_clientes(self):
        """Obtém análise de clientes"""
        query = """
            SELECT 
                cliente,
                COUNT(*) as num_transacoes,
                SUM(valor) as total_recebido,
                AVG(valor) as ticket_medio,
                MAX(data_receita) as ultima_transacao
            FROM receitas
            WHERE cliente IS NOT NULL AND cliente != ''
            GROUP BY cliente
            ORDER BY total_recebido DESC
            LIMIT 10
        """
        return self.execute_query(query)
    
    def get_analise_fornecedores(self):
        """Obtém análise de fornecedores"""
        query = """
            SELECT 
                fornecedor,
                COUNT(*) as num_transacoes,
                SUM(valor) as total_pago,
                AVG(valor) as ticket_medio,
                MAX(data_despesa) as ultima_despesa
            FROM despesas
            WHERE fornecedor IS NOT NULL AND fornecedor != ''
            GROUP BY fornecedor
            ORDER BY total_pago DESC
            LIMIT 10
        """
        return self.execute_query(query)
    
    def render_dashboard(self):
        """Renderiza o dashboard completo"""
        
        # Título principal
        st.title("📊 Dashboard de KPIs Financeiros")
        st.markdown("**Versão SQLite** - Monitoramento Executivo de Resultados")
        
        # Sidebar com filtros
        st.sidebar.header("🔧 Configurações")
        
        # Informações do sistema
        st.sidebar.subheader("ℹ️ Informações do Sistema")
        st.sidebar.info(f"**Banco:** SQLite\n**Arquivo:** {self.db_path}")
        
        # Status da conexão
        if self.connection:
            st.sidebar.success("✅ Conectado ao banco")
        else:
            st.sidebar.error("❌ Sem conexão")
        
        # Botão para atualizar dados
        if st.sidebar.button("🔄 Atualizar Dados"):
            st.rerun()
        
        # Métricas principais
        st.header("📈 Métricas Principais")
        
        try:
            # Resumo financeiro
            df_resumo = self.get_resumo_financeiro()
            if not df_resumo.empty:
                # KPIs principais
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        label="💰 Receita Total",
                        value=f"R$ {df_resumo['total_receitas'].sum():,.2f}",
                        delta=f"R$ {df_resumo['total_receitas'].iloc[0]:,.2f}"
                    )
                
                with col2:
                    st.metric(
                        label="💸 Despesa Total",
                        value=f"R$ {df_resumo['total_despesas'].sum():,.2f}",
                        delta=f"R$ {df_resumo['total_despesas'].iloc[0]:,.2f}"
                    )
                
                with col3:
                    st.metric(
                        label="💵 Lucro Líquido",
                        value=f"R$ {df_resumo['lucro_liquido'].sum():,.2f}",
                        delta=f"R$ {df_resumo['lucro_liquido'].iloc[0]:,.2f}"
                    )
                
                with col4:
                    margem_media = df_resumo['margem_liquida_percentual'].mean()
                    st.metric(
                        label="📊 Margem Média",
                        value=f"{margem_media:.1f}%",
                        delta=f"{margem_media:.1f}%"
                    )
            else:
                st.warning("⚠️ Nenhum dado encontrado para exibir métricas")
        
        except Exception as e:
            st.error(f"❌ Erro ao carregar métricas: {e}")
        
        # Gráficos
        st.header("📊 Análises Gráficas")
        
        # Evolução de receitas
        st.subheader("📈 Evolução de Receitas")
        try:
            df_evolucao = self.get_evolucao_receitas()
            if not df_evolucao.empty:
                fig = px.line(
                    df_evolucao, 
                    x='mes_ano', 
                    y='total_receitas',
                    title='Evolução de Receitas por Mês',
                    labels={'total_receitas': 'Receitas (R$)', 'mes_ano': 'Mês/Ano'}
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("📊 Nenhum dado de evolução disponível")
        except Exception as e:
            st.error(f"❌ Erro ao gerar gráfico de evolução: {e}")
        
        # Despesas por categoria
        st.subheader("💸 Despesas por Categoria")
        try:
            df_despesas_cat = self.get_despesas_por_categoria()
            if not df_despesas_cat.empty:
                fig = px.pie(
                    df_despesas_cat,
                    values='total_despesas',
                    names='nome_categoria',
                    title='Distribuição de Despesas por Categoria'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                # Tabela de detalhes
                st.dataframe(
                    df_despesas_cat[['nome_categoria', 'total_despesas', 'percentual']].round(2),
                    use_container_width=True
                )
            else:
                st.info("📊 Nenhum dado de despesas por categoria disponível")
        except Exception as e:
            st.error(f"❌ Erro ao gerar gráfico de despesas: {e}")
        
        # Receita vs Meta
        st.subheader("🎯 Receita vs Meta")
        try:
            df_receita_meta = self.get_receita_vs_meta()
            if not df_receita_meta.empty:
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    x=df_receita_meta['mes_ano'],
                    y=df_receita_meta['meta_receita'],
                    name='Meta',
                    marker_color='lightblue'
                ))
                
                fig.add_trace(go.Bar(
                    x=df_receita_meta['mes_ano'],
                    y=df_receita_meta['receita_realizada'],
                    name='Realizado',
                    marker_color='green'
                ))
                
                fig.update_layout(
                    title='Comparação: Meta vs Receita Realizada',
                    barmode='group',
                    height=400,
                    xaxis_title='Mês/Ano',
                    yaxis_title='Valor (R$)'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Tabela de detalhes
                st.dataframe(
                    df_receita_meta[['mes_ano', 'meta_receita', 'receita_realizada', 'percentual_realizado']].round(2),
                    use_container_width=True
                )
            else:
                st.info("📊 Nenhum dado de meta vs realizado disponível")
        except Exception as e:
            st.error(f"❌ Erro ao gerar gráfico de meta vs realizado: {e}")
        
        # Análise de clientes
        st.subheader("👥 Top 10 Clientes")
        try:
            df_clientes = self.get_analise_clientes()
            if not df_clientes.empty:
                fig = px.bar(
                    df_clientes.head(10),
                    x='cliente',
                    y='total_recebido',
                    title='Top 10 Clientes por Valor Recebido',
                    labels={'total_recebido': 'Total Recebido (R$)', 'cliente': 'Cliente'}
                )
                fig.update_layout(height=400, xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("📊 Nenhum dado de clientes disponível")
        except Exception as e:
            st.error(f"❌ Erro ao gerar gráfico de clientes: {e}")
        
        # Análise de fornecedores
        st.subheader("🏢 Top 10 Fornecedores")
        try:
            df_fornecedores = self.get_analise_fornecedores()
            if not df_fornecedores.empty:
                fig = px.bar(
                    df_fornecedores.head(10),
                    x='fornecedor',
                    y='total_pago',
                    title='Top 10 Fornecedores por Valor Pago',
                    labels={'total_pago': 'Total Pago (R$)', 'fornecedor': 'Fornecedor'}
                )
                fig.update_layout(height=400, xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("📊 Nenhum dado de fornecedores disponível")
        except Exception as e:
            st.error(f"❌ Erro ao gerar gráfico de fornecedores: {e}")
        
        # Resumo executivo
        st.header("📋 Resumo Executivo")
        
        try:
            if not df_resumo.empty:
                # Filtrar apenas os últimos 6 meses
                df_resumo['mes_ano'] = pd.to_datetime(df_resumo['mes_ano'] + '-01')
                df_resumo = df_resumo.sort_values('mes_ano').tail(6)
                
                st.dataframe(
                    df_resumo[[
                        'mes_ano', 'total_receitas', 'total_despesas', 
                        'lucro_bruto', 'margem_lucro_percentual'
                    ]].round(2),
                    use_container_width=True
                )
            else:
                st.info("📊 Nenhum resumo executivo disponível")
        except Exception as e:
            st.error(f"❌ Erro ao carregar resumo executivo: {e}")
        
        # Footer
        st.markdown("---")
        st.markdown(
            "**Dashboard de KPIs Financeiros** | "
            "Desenvolvido com Streamlit e SQLite | "
            f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        )

def main():
    """Função principal"""
    try:
        dashboard = DashboardKPIsSQLite()
        dashboard.render_dashboard()
    except Exception as e:
        st.error(f"❌ Erro crítico no dashboard: {e}")
        st.info("💡 Verifique se o banco SQLite foi configurado corretamente")

if __name__ == "__main__":
    main()
