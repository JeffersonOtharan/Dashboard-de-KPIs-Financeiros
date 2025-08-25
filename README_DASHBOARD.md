# Dashboard de KPIs Financeiros - Guia de Execução

## Visão Geral

Este é um sistema completo de monitoramento de KPIs financeiros com dashboard interativo, desenvolvido em Python usando Streamlit e SQLite. O sistema foi projetado para fornecer uma visão executiva centralizada dos resultados financeiros empresariais.

## Funcionalidades

- **Métricas Principais**: Receitas, despesas, lucro líquido e margem
- **Evolução de Receitas**: Gráfico de linha temporal
- **Despesas por Categoria**: Gráfico de pizza com detalhamento
- **Receita vs Meta**: Comparação entre metas e realizados
- **Análise de Clientes**: Top 10 clientes por valor
- **Análise de Fornecedores**: Top 10 fornecedores por valor
- **Resumo Executivo**: Tabela consolidada dos últimos 6 meses

## Tecnologias

- **Backend**: Python + SQLite
- **Frontend**: Streamlit
- **Visualizações**: Plotly
- **Processamento**: Pandas + NumPy

## Como Executar

### Opção 1: Script Python (Recomendado)

```bash
python iniciar_dashboard.py
```

### Opção 2: Script Batch (Windows)

```bash
iniciar_dashboard.bat
```

### Opção 3: Comando Direto

```bash
python -m streamlit run dashboard_app.py --server.port 8501
```

## Acesso

Após executar, abra seu navegador em:
```
http://localhost:8501
```

## Pré-requisitos

1. **Python 3.8+** instalado
2. **Dependências** instaladas:
   ```bash
   python -m pip install streamlit plotly pandas numpy
   ```
3. **Banco de dados** configurado:
   ```bash
   python python/setup_sqlite_database.py
   ```

## Estrutura do Projeto

```
Monitoramento de KPIs Financeiros/
├── dashboard_app.py          # Dashboard principal (RAIZ)
├── iniciar_dashboard.py      # Script de inicialização
├── iniciar_dashboard.bat     # Script batch para Windows
├── kpis_financeiros.db      # Banco SQLite
├── python/                   # Scripts Python
├── dashboard/                # Dashboards originais
├── database/                 # Scripts SQL
└── scripts/                  # Scripts de teste
```

## Testando o Sistema

Para verificar se tudo está funcionando:

```bash
python scripts/test_sqlite_system.py
```

## Solução de Problemas

### Erro: "streamlit não é reconhecido"
**Solução**: Instale o Streamlit:
```bash
python -m pip install streamlit
```

### Erro: "Banco não encontrado"
**Solução**: Configure o banco:
```bash
python python/setup_sqlite_database.py
```

### Erro: "Porta 8501 em uso"
**Solução**: Use outra porta:
```bash
python -m streamlit run dashboard_app.py --server.port 8502
```

### Erro: "Módulo não encontrado"
**Solução**: Instale as dependências:
```bash
python -m pip install -r requirements.txt
```

## Dados de Exemplo

O sistema inclui dados de exemplo para:
- 1 empresa (TechCorp Solutions)
- 7 categorias (receitas e despesas)
- 10 receitas (Janeiro a Junho 2024)
- 10 despesas (Janeiro a Março 2024)
- 6 metas mensais (2024)

## Personalização

Para personalizar o dashboard:
1. Edite `dashboard_app.py`
2. Modifique as queries SQL
3. Ajuste os gráficos Plotly
4. Adicione novas métricas

## Atualização de Dados

Para atualizar dados:
1. Use o botão "Atualizar Dados" no dashboard
2. Ou execute o script de configuração novamente
3. Ou carregue novos CSVs via `python/load_csv_data.py`

## Suporte

Se encontrar problemas:
1. Verifique os logs no terminal
2. Execute o script de teste
3. Confirme se todas as dependências estão instaladas
4. Verifique se o banco foi configurado corretamente

## Próximos Passos

- [ ] Adicionar autenticação de usuários
- [ ] Implementar filtros por período
- [ ] Adicionar exportação de relatórios
- [ ] Integrar com APIs externas
- [ ] Implementar cache de dados
- [ ] Adicionar notificações automáticas

---

**Sistema pronto para uso. Execute `python iniciar_dashboard.py` e comece a monitorar seus KPIs financeiros.**
