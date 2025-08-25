# 📚 Guia de Execução Detalhado - Monitoramento de KPIs Financeiros

## 🎯 **Visão Geral do Projeto**

Este projeto implementa um **sistema completo de monitoramento de KPIs financeiros** em nível intermediário → avançado, focado na **solução real** de visualização centralizada para a diretoria.

### 🏆 **O que foi implementado:**

✅ **Banco de dados SQL robusto** com tabelas: despesas, receitas, metas mensais  
✅ **Consultas avançadas** para cálculo de: margem de lucro, receita x meta, despesas por categoria  
✅ **Automação Python** para carregamento de CSVs de vendas e gastos  
✅ **Dashboard executivo** com lucro líquido, evolução de receitas, comparação meta x realizado  
✅ **Sistema profissional** seguindo as melhores práticas do mercado de dados  

## 🚀 **Passo a Passo de Execução**

### **1️⃣ PREPARAÇÃO DO AMBIENTE**

#### **1.1 Instalar MySQL**
```bash
# Windows - Baixar MySQL Community Server
# https://dev.mysql.com/downloads/mysql/

# Linux Ubuntu/Debian
sudo apt-get update
sudo apt-get install mysql-server

# macOS
brew install mysql
```

#### **1.2 Instalar Python 3.8+**
```bash
# Verificar versão
python --version

# Se necessário, baixar de: https://www.python.org/downloads/
```

#### **1.3 Instalar dependências Python**
```bash
# Navegar para o diretório do projeto
cd "Monitoramento de KPIs Financeiros"

# Instalar dependências
pip install -r requirements.txt
```

### **2️⃣ CONFIGURAÇÃO DO BANCO DE DADOS**

#### **2.1 Executar script de configuração automática**
```bash
# Navegar para pasta python
cd python

# Executar configuração automática
python setup_database.py
```

**Durante a execução, você será solicitado a informar:**
- Host MySQL (padrão: localhost)
- Usuário MySQL (padrão: root)
- Senha MySQL (deixe em branco se não houver)

#### **2.2 Verificar configuração**
O script irá:
1. ✅ Conectar ao MySQL
2. ✅ Criar banco `kpis_financeiros_avancado`
3. ✅ Executar scripts SQL em ordem:
   - `01_create_database.sql` - Estrutura das tabelas
   - `02_populate_data.sql` - Dados de exemplo
   - `03_create_views.sql` - Views analíticas
4. ✅ Verificar se tudo foi criado corretamente

### **3️⃣ CARREGAMENTO DE DADOS CSV (OPCIONAL)**

#### **3.1 Preparar arquivos CSV**
Crie arquivos CSV na pasta `data/` com os seguintes nomes:
- `receitas_*.csv` - Para dados de receitas
- `despesas_*.csv` - Para dados de despesas  
- `metas_*.csv` - Para metas mensais

#### **3.2 Estrutura dos CSVs**

**receitas.csv:**
```csv
id_empresa,id_categoria,codigo_transacao,descricao,valor,valor_liquido,data_receita,data_recebimento,status,fonte_receita,cliente,forma_recebimento
1,1,REC-2025-001,Venda Software,50000.00,47500.00,2025-01-15,2025-01-20,recebido,Vendas,TechCorp,transferencia
```

**despesas.csv:**
```csv
id_empresa,id_categoria,codigo_transacao,descricao,valor,valor_liquido,data_despesa,data_pagamento,status,fornecedor,forma_pagamento
1,5,DES-2025-001,Salários,45000.00,45000.00,2025-01-05,2025-01-05,pago,Folha de Pagamento,transferencia
```

**metas.csv:**
```csv
id_empresa,ano,mes,id_categoria,meta_receita,meta_despesa,meta_lucro,meta_margem
1,2025,1,1,60000.00,0.00,45000.00,75.00
```

#### **3.3 Carregar dados CSV**
```bash
# Executar carregamento automático
python load_csv_data.py --csv-dir ../data

# Ou com parâmetros específicos
python load_csv_data.py --host localhost --user root --database kpis_financeiros_avancado
```

### **4️⃣ EXECUTAR DASHBOARD EXECUTIVO**

#### **4.1 Iniciar dashboard**
```bash
# Navegar para pasta dashboard
cd ../dashboard

# Executar dashboard
streamlit run main.py
```

#### **4.2 Acessar dashboard**
- O dashboard abrirá automaticamente no navegador
- URL padrão: `http://localhost:8501`
- Interface responsiva e profissional

## 📊 **Funcionalidades do Dashboard**

### **🎯 KPIs Principais**
- **Margem de Lucro** - Rentabilidade por período
- **Receita vs Meta** - Performance de vendas
- **Despesas por Categoria** - Controle de custos
- **Lucro Líquido** - Resultado final
- **Evolução de Receitas** - Tendências temporais

### **📈 Visualizações**
- **Gráficos de evolução** - Receitas, despesas e lucro ao longo do tempo
- **Análise de margem** - Por categoria de receita
- **Distribuição de despesas** - Gráfico de pizza por categoria
- **Tabela de metas** - Comparação meta vs realizado
- **Análise de tendências** - Variação percentual mensal

### **⚙️ Recursos Avançados**
- **Filtros dinâmicos** - Por ano e mês
- **Atualização em tempo real** - Botão de refresh
- **Responsivo** - Funciona em desktop e mobile
- **Exportação** - Dados podem ser exportados

## 🔧 **Configurações Avançadas**

### **Personalizar Conexão com Banco**
Editar arquivo `dashboard/main.py`:
```python
self.connection = mysql.connector.connect(
    host='localhost',           # Seu host MySQL
    user='root',                # Seu usuário MySQL
    password='sua_senha',       # Sua senha MySQL
    database='kpis_financeiros_avancado',
    charset='utf8mb4'
)
```

### **Adicionar Novas Categorias**
```sql
-- Conectar ao banco e executar:
INSERT INTO categorias (id_empresa, nome_categoria, tipo, nivel_hierarquia, cor_hex, icone) 
VALUES (1, 'Nova Categoria', 'receita', 1, '#FF6B6B', 'star');
```

### **Configurar Metas Mensais**
```sql
-- Inserir metas para 2025
INSERT INTO metas_mensais (id_empresa, ano, mes, id_categoria, meta_receita, meta_despesa, meta_lucro, meta_margem) 
VALUES (1, 2025, 1, 1, 70000.00, 0.00, 52500.00, 75.00);
```

## 🧪 **Testes e Validação**

### **Verificar Banco de Dados**
```sql
-- Conectar ao MySQL e executar:
USE kpis_financeiros_avancado;

-- Verificar tabelas
SHOW TABLES;

-- Verificar views
SHOW FULL TABLES WHERE Table_type = 'VIEW';

-- Verificar dados
SELECT COUNT(*) FROM receitas WHERE YEAR(data_receita) = 2024;
SELECT COUNT(*) FROM despesas WHERE YEAR(data_despesa) = 2024;
SELECT COUNT(*) FROM metas_mensais WHERE ano = 2024;
```

### **Testar Views**
```sql
-- Testar cada view criada
SELECT * FROM vw_resumo_financeiro_executivo LIMIT 5;
SELECT * FROM vw_analise_margem_lucro WHERE tipo = 'receita';
SELECT * FROM vw_receita_vs_meta WHERE ano = 2024 AND mes = 12;
```

## 🚨 **Solução de Problemas**

### **Erro de Conexão com MySQL**
```bash
# Verificar se MySQL está rodando
# Windows
net start mysql

# Linux
sudo systemctl status mysql

# macOS
brew services list | grep mysql
```

### **Erro de Dependências Python**
```bash
# Atualizar pip
python -m pip install --upgrade pip

# Reinstalar dependências
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### **Erro no Dashboard**
```bash
# Verificar logs
tail -f setup_database.log
tail -f load_csv_data.log

# Verificar permissões do banco
# Garantir que o usuário tem acesso ao banco kpis_financeiros_avancado
```

## 📈 **Próximos Passos**

### **Implementações Futuras**
- [ ] **Deploy em produção** - Servidor dedicado
- [ ] **Integração com ERPs** - SAP, Oracle, etc.
- [ ] **Machine Learning** - Previsões financeiras
- [ ] **API REST** - Para integrações externas
- [ ] **Alertas automáticos** - Email/SMS para metas
- [ ] **Backup automático** - Dados e configurações

### **Melhorias Técnicas**
- [ ] **Cache Redis** - Para performance
- [ ] **Docker** - Containerização
- [ ] **CI/CD** - Pipeline de deploy
- [ ] **Monitoramento** - Logs e métricas
- [ ] **Segurança** - Autenticação e autorização

## 🏆 **Resultado Esperado**

Ao final da execução, você terá:

1. **✅ Banco de dados robusto** com estrutura profissional
2. **✅ Sistema de automação** para carregamento de dados
3. **✅ Dashboard executivo** com KPIs em tempo real
4. **✅ Análises avançadas** de performance financeira
5. **✅ Solução escalável** para crescimento da empresa

## 📞 **Suporte**

### **Documentação Adicional**
- `README.md` - Visão geral do projeto
- `database/` - Scripts SQL e estrutura
- `python/` - Scripts de automação
- `dashboard/` - Interface visual

### **Logs e Debug**
- `setup_database.log` - Logs de configuração
- `load_csv_data.log` - Logs de carregamento
- Console do Streamlit - Logs do dashboard

---

**🎉 Parabéns! Você implementou um sistema profissional de monitoramento de KPIs financeiros que resolve problemas reais de negócio!**
