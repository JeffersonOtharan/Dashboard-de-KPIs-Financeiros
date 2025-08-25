#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 Dashboard Executivo de KPIs Financeiros
Monitoramento de KPIs Financeiros - Nível Avançado

Este dashboard fornece uma visão executiva dos principais
indicadores financeiros da empresa.
"""

import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import logging

# Configuração da página
st.set_page_config(
    page_title="📊 Dashboard KPIs Financeiros",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DashboardKPIs:
    """Classe principal do dashboard de KPIs"""
    
    def __init__(self):
        """Inicializa o dashboard"""
        self.connection = None
        self.setup_connection()
    
    def setup_connection(self):
        """Configura conexão com o banco de dados"""
        try:
            # Configurações do banco (em produção, usar variáveis de ambiente)
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',  # Configurar conforme necessário
                database='kpis_financeiros_avancado',
                charset='utf8mb4'
            )
            logger.info("✅ Conexão com banco estabelecida")
        except Error as e:
            logger.error(f"❌ Erro na conexão: {e}")
            st.error("❌ Erro na conexão com o banco de dados")
    
    def execute_query(self, query):
        """Executa uma query e retorna DataFrame"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.setup_connection()
            
            df = pd.read_sql(query, self.connection)
            return df
        except Exception as e:
            logger.error(f"❌ Erro na query: {e}")
            st.error(f"❌ Erro na execução da query: {e}")
            return pd.DataFrame()
    
    def get_resumo_executivo(self):
        """Obtém resumo executivo dos KPIs"""
        query = """
        SELECT * FROM vw_resumo_financeiro_executivo 
        WHERE ano = 2024 
        ORDER BY ano DESC, mes DESC
        """
        return self.execute_query(query)
    
    def get_margem_lucro(self):
        """Obtém dados de margem de lucro"""
        query = """
        SELECT * FROM vw_analise_margem_lucro 
        ORDER BY margem_lucro_percentual DESC
        """
        return self.execute_query(query)
    
    def get_receita_vs_meta(self):
        """Obtém dados de receita vs meta"""
        query = """
        SELECT * FROM vw_receita_vs_meta 
        WHERE ano = 2024 
        ORDER BY mes DESC, tipo, nome_categoria
        """
        return self.execute_query(query)
    
    def get_despesas_categoria(self):
        """Obtém dados de despesas por categoria"""
        query = """
        SELECT * FROM vw_despesas_por_categoria 
        ORDER BY total_despesas DESC
        """
        return self.execute_query(query)
    
    def get_tendencias(self):
        """Obtém dados de tendências financeiras"""
        query = """
        SELECT * FROM vw_tendencias_financeiras 
        WHERE ano = 2024 
        ORDER BY ano, mes
        """
        return self.execute_query(query)
    
    def render_header(self):
        """Renderiza o cabeçalho do dashboard"""
        st.title("📊 Dashboard Executivo de KPIs Financeiros")
        st.markdown("---")
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="🏢 Empresa",
                value="Empresa Exemplo Ltda",
                delta="Tecnologia"
            )
        
        with col2:
            st.metric(
                label="📅 Período",
                value="2024",
                delta="Ano Atual"
            )
        
        with col3:
            st.metric(
                label="🔄 Status",
                value="Ativo",
                delta="Sistema Funcionando"
            )
        
        with col4:
            st.metric(
                label="📊 Última Atualização",
                value=datetime.now().strftime("%d/%m/%Y"),
                delta="Tempo Real"
            )
    
    def render_kpi_cards(self):
        """Renderiza cards de KPIs principais"""
        st.subheader("🎯 KPIs Principais")
        
        # Obter dados
        df_resumo = self.get_resumo_executivo()
        
        if df_resumo.empty:
            st.warning("⚠️ Nenhum dado encontrado")
            return
        
        # Calcular métricas do ano
        receita_total = df_resumo['total_receitas'].sum()
        despesa_total = df_resumo['total_despesas'].sum()
        lucro_total = receita_total - despesa_total
        margem_media = df_resumo['margem_lucro_percentual'].mean()
        
        # Cards de métricas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="💰 Receita Total 2024",
                value=f"R$ {receita_total:,.2f}",
                delta=f"R$ {df_resumo['total_receitas'].iloc[0]:,.2f} (último mês)"
            )
        
        with col2:
            st.metric(
                label="💸 Despesa Total 2024",
                value=f"R$ {despesa_total:,.2f}",
                delta=f"R$ {df_resumo['total_despesas'].iloc[0]:,.2f} (último mês)"
            )
        
        with col3:
            st.metric(
                label="📈 Lucro Total 2024",
                value=f"R$ {lucro_total:,.2f}",
                delta=f"R$ {df_resumo['lucro_bruto'].iloc[0]:,.2f} (último mês)"
            )
        
        with col4:
            st.metric(
                label="🎯 Margem Média 2024",
                value=f"{margem_media:.1f}%",
                delta=f"{df_resumo['margem_lucro_percentual'].iloc[0]:.1f}% (último mês)"
            )
    
    def render_grafico_evolucao(self):
        """Renderiza gráfico de evolução temporal"""
        st.subheader("📈 Evolução Financeira - 2024")
        
        df_resumo = self.get_resumo_executivo()
        
        if df_resumo.empty:
            st.warning("⚠️ Nenhum dado encontrado")
            return
        
        # Gráfico de linha
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_resumo['mes_ano'],
            y=df_resumo['total_receitas'],
            mode='lines+markers',
            name='Receitas',
            line=dict(color='#28a745', width=3),
            marker=dict(size=8)
        ))
        
        fig.add_trace(go.Scatter(
            x=df_resumo['mes_ano'],
            y=df_resumo['total_despesas'],
            mode='lines+markers',
            name='Despesas',
            line=dict(color='#dc3545', width=3),
            marker=dict(size=8)
        ))
        
        fig.add_trace(go.Scatter(
            x=df_resumo['mes_ano'],
            y=df_resumo['lucro_bruto'],
            mode='lines+markers',
            name='Lucro Bruto',
            line=dict(color='#17a2b8', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title="Evolução de Receitas, Despesas e Lucro",
            xaxis_title="Mês",
            yaxis_title="Valor (R$)",
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_grafico_margem(self):
        """Renderiza gráfico de margem de lucro"""
        st.subheader("📊 Margem de Lucro por Categoria")
        
        df_margem = self.get_margem_lucro()
        
        if df_margem.empty:
            st.warning("⚠️ Nenhum dado encontrado")
            return
        
        # Filtrar apenas receitas para margem
        df_receitas = df_margem[df_margem['tipo'] == 'receita']
        
        if df_receitas.empty:
            st.warning("⚠️ Nenhuma categoria de receita encontrada")
            return
        
        # Gráfico de barras
        fig = px.bar(
            df_receitas,
            x='nome_categoria',
            y='margem_lucro_percentual',
            color='margem_lucro_percentual',
            color_continuous_scale='RdYlGn',
            title="Margem de Lucro por Categoria de Receita",
            labels={'margem_lucro_percentual': 'Margem (%)', 'nome_categoria': 'Categoria'}
        )
        
        fig.update_layout(
            height=500,
            xaxis_tickangle=-45
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_grafico_despesas(self):
        """Renderiza gráfico de despesas por categoria"""
        st.subheader("💸 Despesas por Categoria")
        
        df_despesas = self.get_despesas_categoria()
        
        if df_despesas.empty:
            st.warning("⚠️ Nenhum dado encontrado")
            return
        
        # Gráfico de pizza
        fig = px.pie(
            df_despesas,
            values='total_despesas',
            names='nome_categoria',
            title="Distribuição de Despesas por Categoria",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    def render_tabela_metas(self):
        """Renderiza tabela de metas vs realizado"""
        st.subheader("🎯 Metas vs Realizado - Dezembro 2024")
        
        df_metas = self.get_receita_vs_meta()
        
        if df_metas.empty:
            st.warning("⚠️ Nenhum dado encontrado")
            return
        
        # Filtrar apenas dezembro
        df_dezembro = df_metas[df_metas['mes'] == 12]
        
        if df_dezembro.empty:
            st.warning("⚠️ Nenhum dado para dezembro encontrado")
            return
        
        # Preparar dados para exibição
        df_display = df_dezembro[['nome_categoria', 'tipo', 'meta_receita', 'receita_realizada', 
                                 'percentual_atingimento_receita', 'status_meta']].copy()
        
        # Formatar valores monetários
        df_display['meta_receita'] = df_display['meta_receita'].apply(lambda x: f"R$ {x:,.2f}" if pd.notna(x) else "R$ 0,00")
        df_display['receita_realizada'] = df_display['receita_realizada'].apply(lambda x: f"R$ {x:,.2f}" if pd.notna(x) else "R$ 0,00")
        df_display['percentual_atingimento_receita'] = df_display['percentual_atingimento_receita'].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "0.0%")
        
        # Renomear colunas
        df_display.columns = ['Categoria', 'Tipo', 'Meta', 'Realizado', 'Atingimento', 'Status']
        
        st.dataframe(df_display, use_container_width=True)
    
    def render_tendencias_analise(self):
        """Renderiza análise de tendências"""
        st.subheader("📊 Análise de Tendências")
        
        df_tendencias = self.get_tendencias()
        
        if df_tendencias.empty:
            st.warning("⚠️ Nenhum dado encontrado")
            return
        
        # Métricas de tendência
        col1, col2, col3 = st.columns(3)
        
        with col1:
            ultima_tendencia = df_tendencias['tendencia_receita'].iloc[-1]
            st.metric(
                label="📈 Tendência Receitas",
                value=ultima_tendencia,
                delta="Último mês"
            )
        
        with col2:
            ultima_tendencia = df_tendencias['tendencia_despesa'].iloc[-1]
            st.metric(
                label="💸 Tendência Despesas",
                value=ultima_tendencia,
                delta="Último mês"
            )
        
        with col3:
            ultima_tendencia = df_tendencias['tendencia_lucro'].iloc[-1]
            st.metric(
                label="💰 Tendência Lucro",
                value=ultima_tendencia,
                delta="Último mês"
            )
        
        # Gráfico de variação percentual
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_tendencias['mes_ano'],
            y=df_tendencias['variacao_receita_percentual'],
            mode='lines+markers',
            name='Variação Receitas (%)',
            line=dict(color='#28a745', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=df_tendencias['mes_ano'],
            y=df_tendencias['variacao_despesa_percentual'],
            mode='lines+markers',
            name='Variação Despesas (%)',
            line=dict(color='#dc3545', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=df_tendencias['mes_ano'],
            y=df_tendencias['variacao_lucro_percentual'],
            mode='lines+markers',
            name='Variação Lucro (%)',
            line=dict(color='#17a2b8', width=3)
        ))
        
        fig.update_layout(
            title="Variação Percentual Mensal",
            xaxis_title="Mês",
            yaxis_title="Variação (%)",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_sidebar(self):
        """Renderiza a barra lateral"""
        st.sidebar.title("⚙️ Configurações")
        
        # Filtros
        st.sidebar.subheader("🔍 Filtros")
        
        ano_selecionado = st.sidebar.selectbox(
            "Ano",
            [2024, 2023, 2022],
            index=0
        )
        
        mes_selecionado = st.sidebar.selectbox(
            "Mês",
            list(range(1, 13)),
            index=datetime.now().month - 1,
            format_func=lambda x: datetime(2024, x, 1).strftime("%B")
        )
        
        # Informações do sistema
        st.sidebar.subheader("ℹ️ Informações")
        st.sidebar.info("""
        **Dashboard de KPIs Financeiros**
        
        Este sistema fornece uma visão executiva dos principais indicadores financeiros da empresa.
        
        **Desenvolvido com:**
        - Python + Streamlit
        - MySQL
        - Plotly
        """)
        
        # Botão de atualização
        if st.sidebar.button("🔄 Atualizar Dados"):
            st.rerun()
        
        return ano_selecionado, mes_selecionado
    
    def render_footer(self):
        """Renderiza o rodapé"""
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666;'>
        <p>📊 Dashboard de KPIs Financeiros - Nível Avançado</p>
        <p>Desenvolvido com foco em solução real para problemas reais de negócio</p>
        <p>Última atualização: {}</p>
        </div>
        """.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")), unsafe_allow_html=True)
    
    def run(self):
        """Executa o dashboard"""
        try:
            # Header
            self.render_header()
            
            # Sidebar
            ano, mes = self.render_sidebar()
            
            # KPIs principais
            self.render_kpi_cards()
            
            # Gráficos
            col1, col2 = st.columns(2)
            
            with col1:
                self.render_grafico_evolucao()
            
            with col2:
                self.render_grafico_margem()
            
            # Despesas e metas
            col1, col2 = st.columns(2)
            
            with col1:
                self.render_grafico_despesas()
            
            with col2:
                self.render_tabela_metas()
            
            # Análise de tendências
            self.render_tendencias_analise()
            
            # Footer
            self.render_footer()
            
        except Exception as e:
            logger.error(f"❌ Erro no dashboard: {e}")
            st.error(f"❌ Erro no dashboard: {e}")
        
        finally:
            if self.connection and self.connection.is_connected():
                self.connection.close()

def main():
    """Função principal"""
    st.title("📊 Dashboard Executivo de KPIs Financeiros")
    
    # Verificar se o banco está acessível
    try:
        dashboard = DashboardKPIs()
        dashboard.run()
    except Exception as e:
        st.error(f"❌ Erro ao inicializar dashboard: {e}")
        st.info("💡 Verifique se o banco de dados está configurado e acessível")

if __name__ == "__main__":
    main()
