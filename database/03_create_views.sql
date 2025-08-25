-- =====================================================
-- 📊 SCRIPT DE CRIAÇÃO DE VIEWS EXECUTIVAS
-- Monitoramento de KPIs Financeiros - Nível Avançado
-- =====================================================
--
-- Este script cria views estratégicas para análise
-- executiva e cálculo de KPIs financeiros
--
-- 🎯 OBJETIVOS:
-- 1. Criar views para análise executiva
-- 2. Facilitar cálculo de KPIs complexos
-- 3. Otimizar consultas de dashboard
-- 4. Padronizar métricas de negócio
-- =====================================================

USE kpis_financeiros_avancado;

-- =====================================================
-- 📊 VIEW: RESUMO FINANCEIRO EXECUTIVO
-- =====================================================
-- Propósito: Visão consolidada para diretoria
-- Boa prática: View materializada para consultas frequentes

CREATE OR REPLACE VIEW vw_resumo_financeiro_executivo AS
SELECT 
    e.nome_empresa,
    e.setor,
    ano,
    mes,
    CONCAT(ano, '-', LPAD(mes, 2, '0')) as mes_ano,
    total_receitas,
    total_despesas,
    (total_receitas - total_despesas) as lucro_bruto,
    ROUND(((total_receitas - total_despesas) / total_receitas) * 100, 2) as margem_lucro_percentual,
    total_receitas_liquido,
    total_despesas_liquido,
    (total_receitas_liquido - total_despesas_liquido) as lucro_liquido,
    ROUND(((total_receitas_liquido - total_despesas_liquido) / total_receitas_liquido) * 100, 2) as margem_liquida_percentual,
    CASE 
        WHEN (total_receitas - total_despesas) > 0 THEN 'Positivo'
        WHEN (total_receitas - total_despesas) < 0 THEN 'Negativo'
        ELSE 'Neutro'
    END as status_financeiro,
    CASE 
        WHEN ROUND(((total_receitas - total_despesas) / total_receitas) * 100, 2) >= 30 THEN '🟢 Excelente'
        WHEN ROUND(((total_receitas - total_despesas) / total_receitas) * 100, 2) >= 20 THEN '🟡 Bom'
        WHEN ROUND(((total_receitas - total_despesas) / total_receitas) * 100, 2) >= 10 THEN '🟠 Regular'
        ELSE '🔴 Crítico'
    END as classificacao_margem
FROM empresas e
CROSS JOIN (
    SELECT DISTINCT YEAR(data_receita) as ano, MONTH(data_receita) as mes
    FROM receitas 
    WHERE id_empresa = e.id_empresa
) periodos
LEFT JOIN (
    SELECT 
        id_empresa,
        YEAR(data_receita) as ano,
        MONTH(data_receita) as mes,
        SUM(valor) as total_receitas,
        SUM(valor_liquido) as total_receitas_liquido
    FROM receitas 
    GROUP BY id_empresa, YEAR(data_receita), MONTH(data_receita)
) r ON e.id_empresa = r.id_empresa AND periodos.ano = r.ano AND periodos.mes = r.mes
LEFT JOIN (
    SELECT 
        id_empresa,
        YEAR(data_despesa) as ano,
        MONTH(data_despesa) as mes,
        SUM(valor) as total_despesas,
        SUM(valor_liquido) as total_despesas_liquido
    FROM despesas 
    GROUP BY id_empresa, YEAR(data_despesa), MONTH(data_despesa)
) d ON e.id_empresa = d.id_empresa AND periodos.ano = d.ano AND periodos.mes = d.mes
WHERE e.ativo = TRUE
ORDER BY e.nome_empresa, ano DESC, mes DESC;

-- =====================================================
-- 📊 VIEW: ANÁLISE DE MARGEM DE LUCRO
-- =====================================================
-- Propósito: Análise detalhada de rentabilidade
-- Boa prática: View para análise de performance

CREATE OR REPLACE VIEW vw_analise_margem_lucro AS
SELECT 
    c.id_categoria,
    c.nome_categoria,
    c.tipo,
    c.cor_hex,
    c.icone,
    COALESCE(SUM(r.valor), 0) as total_receitas,
    COALESCE(SUM(d.valor), 0) as total_despesas,
    (COALESCE(SUM(r.valor), 0) - COALESCE(SUM(d.valor), 0)) as lucro_bruto,
    CASE 
        WHEN COALESCE(SUM(r.valor), 0) > 0 THEN 
            ROUND(((COALESCE(SUM(r.valor), 0) - COALESCE(SUM(d.valor), 0)) / COALESCE(SUM(r.valor), 0)) * 100, 2)
        ELSE 0
    END as margem_lucro_percentual,
    COALESCE(SUM(r.valor_liquido), 0) as total_receitas_liquido,
    COALESCE(SUM(d.valor_liquido), 0) as total_despesas_liquido,
    (COALESCE(SUM(r.valor_liquido), 0) - COALESCE(SUM(d.valor_liquido), 0)) as lucro_liquido,
    CASE 
        WHEN COALESCE(SUM(r.valor_liquido), 0) > 0 THEN 
            ROUND(((COALESCE(SUM(r.valor_liquido), 0) - COALESCE(SUM(d.valor_liquido), 0)) / COALESCE(SUM(r.valor_liquido), 0)) * 100, 2)
        ELSE 0
    END as margem_liquida_percentual,
    COUNT(DISTINCT r.id_receita) as quantidade_receitas,
    COUNT(DISTINCT d.id_despesa) as quantidade_despesas,
    CASE 
        WHEN c.tipo = 'receita' THEN 'Receita'
        WHEN c.tipo = 'despesa' THEN 'Despesa'
        ELSE 'Misto'
    END as tipo_analise
FROM categorias c
LEFT JOIN receitas r ON c.id_categoria = r.id_categoria
LEFT JOIN despesas d ON c.id_categoria = d.id_categoria
WHERE c.ativo = TRUE
GROUP BY c.id_categoria, c.nome_categoria, c.tipo, c.cor_hex, c.icone
ORDER BY c.tipo, margem_lucro_percentual DESC;

-- =====================================================
-- 📊 VIEW: RECEITA VS META
-- =====================================================
-- Propósito: Análise de performance de vendas
-- Boa prática: View para controle de orçamento

CREATE OR REPLACE VIEW vw_receita_vs_meta AS
SELECT 
    mm.ano,
    mm.mes,
    CONCAT(mm.ano, '-', LPAD(mm.mes, 2, '0')) as mes_ano,
    c.nome_categoria,
    c.tipo,
    c.cor_hex,
    c.icone,
    mm.meta_receita,
    mm.meta_despesa,
    mm.meta_lucro,
    mm.meta_margem,
    COALESCE(SUM(r.valor), 0) as receita_realizada,
    COALESCE(SUM(d.valor), 0) as despesa_realizada,
    (COALESCE(SUM(r.valor), 0) - COALESCE(SUM(d.valor), 0)) as lucro_realizado,
    CASE 
        WHEN mm.meta_receita > 0 THEN 
            ROUND((COALESCE(SUM(r.valor), 0) / mm.meta_receita) * 100, 2)
        ELSE 0
    END as percentual_atingimento_receita,
    CASE 
        WHEN mm.meta_despesa > 0 THEN 
            ROUND((mm.meta_despesa / COALESCE(SUM(d.valor), 0)) * 100, 2)
        ELSE 0
    END as percentual_controle_despesa,
    CASE 
        WHEN mm.meta_lucro > 0 THEN 
            ROUND((COALESCE(SUM(r.valor), 0) - COALESCE(SUM(d.valor), 0)) / mm.meta_lucro * 100, 2)
        ELSE 0
    END as percentual_atingimento_lucro,
    CASE 
        WHEN c.tipo = 'receita' THEN 
            CASE 
                WHEN COALESCE(SUM(r.valor), 0) >= mm.meta_receita THEN '✅ Meta Atingida'
                WHEN COALESCE(SUM(r.valor), 0) >= mm.meta_receita * 0.8 THEN '⚠️ Próximo da Meta'
                ELSE '❌ Meta Não Atingida'
            END
        WHEN c.tipo = 'despesa' THEN 
            CASE 
                WHEN COALESCE(SUM(d.valor), 0) <= mm.meta_despesa THEN '✅ Meta Atingida'
                WHEN COALESCE(SUM(d.valor), 0) <= mm.meta_despesa * 1.2 THEN '⚠️ Atenção'
                ELSE '❌ Meta Excedida'
            END
        ELSE 'N/A'
    END as status_meta
FROM metas_mensais mm
JOIN categorias c ON mm.id_categoria = c.id_categoria
LEFT JOIN receitas r ON mm.id_categoria = r.id_categoria 
    AND YEAR(r.data_receita) = mm.ano AND MONTH(r.data_receita) = mm.mes
LEFT JOIN despesas d ON mm.id_categoria = d.id_categoria 
    AND YEAR(d.data_despesa) = mm.ano AND MONTH(d.data_despesa) = mm.mes
GROUP BY mm.ano, mm.mes, mm.id_categoria, c.nome_categoria, c.tipo, c.cor_hex, c.icone, 
         mm.meta_receita, mm.meta_despesa, mm.meta_lucro, mm.meta_margem
ORDER BY mm.ano DESC, mm.mes DESC, c.tipo, c.nome_categoria;

-- =====================================================
-- 📊 VIEW: DESPESAS POR CATEGORIA
-- =====================================================
-- Propósito: Análise detalhada de custos
-- Boa prática: View para controle de gastos

CREATE OR REPLACE VIEW vw_despesas_por_categoria AS
SELECT 
    c.id_categoria,
    c.nome_categoria,
    c.cor_hex,
    c.icone,
    c.descricao,
    COUNT(d.id_despesa) as quantidade_despesas,
    SUM(d.valor) as total_despesas,
    SUM(d.valor_liquido) as total_despesas_liquido,
    ROUND(AVG(d.valor), 2) as valor_medio_despesa,
    ROUND(AVG(d.valor_liquido), 2) as valor_medio_liquido,
    MIN(d.valor) as menor_despesa,
    MAX(d.valor) as maior_despesa,
    ROUND((SUM(d.valor) / (SELECT SUM(valor) FROM despesas WHERE YEAR(data_despesa) = YEAR(CURDATE()))) * 100, 2) as percentual_total,
    COUNT(CASE WHEN d.status = 'pago' THEN 1 END) as despesas_pagas,
    COUNT(CASE WHEN d.status = 'pendente' THEN 1 END) as despesas_pendentes,
    COUNT(CASE WHEN d.status = 'atrasado' THEN 1 END) as despesas_atrasadas,
    ROUND((COUNT(CASE WHEN d.status = 'pago' THEN 1 END) / COUNT(*)) * 100, 2) as percentual_pago,
    CASE 
        WHEN SUM(d.valor) <= 10000 THEN '🟢 Baixo'
        WHEN SUM(d.valor) <= 50000 THEN '🟡 Médio'
        WHEN SUM(d.valor) <= 100000 THEN '🟠 Alto'
        ELSE '🔴 Crítico'
    END as classificacao_custo
FROM categorias c
LEFT JOIN despesas d ON c.id_categoria = d.id_categoria
WHERE c.tipo = 'despesa' AND c.ativo = TRUE
GROUP BY c.id_categoria, c.nome_categoria, c.cor_hex, c.icone, c.descricao
ORDER BY total_despesas DESC;

-- =====================================================
-- 📊 VIEW: TENDÊNCIAS FINANCEIRAS
-- =====================================================
-- Propósito: Análise de evolução temporal
-- Boa prática: View para análise de tendências

CREATE OR REPLACE VIEW vw_tendencias_financeiras AS
SELECT 
    ano,
    mes,
    mes_ano,
    total_receitas,
    total_despesas,
    lucro_bruto,
    margem_lucro_percentual,
    LAG(total_receitas, 1) OVER (ORDER BY ano, mes) as receita_mes_anterior,
    LAG(total_despesas, 1) OVER (ORDER BY ano, mes) as despesa_mes_anterior,
    LAG(lucro_bruto, 1) OVER (ORDER BY ano, mes) as lucro_mes_anterior,
    LAG(margem_lucro_percentual, 1) OVER (ORDER BY ano, mes) as margem_mes_anterior,
    ROUND(((total_receitas - LAG(total_receitas, 1) OVER (ORDER BY ano, mes)) / 
           NULLIF(LAG(total_receitas, 1) OVER (ORDER BY ano, mes), 0)) * 100, 2) as variacao_receita_percentual,
    ROUND(((total_despesas - LAG(total_despesas, 1) OVER (ORDER BY ano, mes)) / 
           NULLIF(LAG(total_despesas, 1) OVER (ORDER BY ano, mes), 0)) * 100, 2) as variacao_despesa_percentual,
    ROUND(((lucro_bruto - LAG(lucro_bruto, 1) OVER (ORDER BY ano, mes)) / 
           NULLIF(LAG(lucro_bruto, 1) OVER (ORDER BY ano, mes), 0)) * 100, 2) as variacao_lucro_percentual,
    ROUND(((margem_lucro_percentual - LAG(margem_lucro_percentual, 1) OVER (ORDER BY ano, mes)) / 
           NULLIF(LAG(margem_lucro_percentual, 1) OVER (ORDER BY ano, mes), 0)) * 100, 2) as variacao_margem_percentual,
    CASE 
        WHEN total_receitas > LAG(total_receitas, 1) OVER (ORDER BY ano, mes) THEN '📈 Crescimento'
        WHEN total_receitas < LAG(total_receitas, 1) OVER (ORDER BY ano, mes) THEN '📉 Redução'
        ELSE '➡️ Estável'
    END as tendencia_receita,
    CASE 
        WHEN total_despesas > LAG(total_despesas, 1) OVER (ORDER BY ano, mes) THEN '📈 Aumento'
        WHEN total_despesas < LAG(total_despesas, 1) OVER (ORDER BY ano, mes) THEN '📉 Redução'
        ELSE '➡️ Estável'
    END as tendencia_despesa,
    CASE 
        WHEN lucro_bruto > LAG(lucro_bruto, 1) OVER (ORDER BY ano, mes) THEN '📈 Melhoria'
        WHEN lucro_bruto < LAG(lucro_bruto, 1) OVER (ORDER BY ano, mes) THEN '📉 Piora'
        ELSE '➡️ Estável'
    END as tendencia_lucro
FROM vw_resumo_financeiro_executivo
ORDER BY ano, mes;

-- =====================================================
-- 📊 VIEW: ANÁLISE DE CLIENTES
-- =====================================================
-- Propósito: Análise de receita por cliente
-- Boa prática: View para análise comercial

CREATE OR REPLACE VIEW vw_analise_clientes AS
SELECT 
    cliente,
    COUNT(*) as quantidade_transacoes,
    SUM(valor) as total_receita,
    SUM(valor_liquido) as total_receita_liquida,
    ROUND(AVG(valor), 2) as valor_medio_transacao,
    MIN(valor) as menor_transacao,
    MAX(valor) as maior_transacao,
    MIN(data_receita) as primeira_compra,
    MAX(data_receita) as ultima_compra,
    DATEDIFF(MAX(data_receita), MIN(data_receita)) as dias_relacionamento,
    COUNT(CASE WHEN status = 'recebido' THEN 1 END) as transacoes_recebidas,
    COUNT(CASE WHEN status = 'pendente' THEN 1 END) as transacoes_pendentes,
    ROUND((COUNT(CASE WHEN status = 'recebido' THEN 1 END) / COUNT(*)) * 100, 2) as percentual_recebido,
    CASE 
        WHEN SUM(valor) >= 100000 THEN '🟢 Cliente Premium'
        WHEN SUM(valor) >= 50000 THEN '🟡 Cliente Gold'
        WHEN SUM(valor) >= 20000 THEN '🟠 Cliente Silver'
        ELSE '⚪ Cliente Bronze'
    END as classificacao_cliente
FROM receitas
WHERE cliente IS NOT NULL AND cliente != ''
GROUP BY cliente
ORDER BY total_receita DESC;

-- =====================================================
-- 📊 VIEW: ANÁLISE DE FORNECEDORES
-- =====================================================
-- Propósito: Análise de despesas por fornecedor
-- Boa prática: View para controle de custos

CREATE OR REPLACE VIEW vw_analise_fornecedores AS
SELECT 
    fornecedor,
    COUNT(*) as quantidade_transacoes,
    SUM(valor) as total_despesa,
    SUM(valor_liquido) as total_despesa_liquida,
    ROUND(AVG(valor), 2) as valor_medio_transacao,
    MIN(valor) as menor_transacao,
    MAX(valor) as maior_transacao,
    MIN(data_despesa) as primeira_transacao,
    MAX(data_despesa) as ultima_transacao,
    COUNT(CASE WHEN status = 'pago' THEN 1 END) as transacoes_pagas,
    COUNT(CASE WHEN status = 'pendente' THEN 1 END) as transacoes_pendentes,
    COUNT(CASE WHEN status = 'atrasado' THEN 1 END) as transacoes_atrasadas,
    ROUND((COUNT(CASE WHEN status = 'pago' THEN 1 END) / COUNT(*)) * 100, 2) as percentual_pago,
    CASE 
        WHEN SUM(valor) >= 50000 THEN '🔴 Fornecedor Crítico'
        WHEN SUM(valor) >= 20000 THEN '🟠 Fornecedor Importante'
        WHEN SUM(valor) >= 10000 THEN '🟡 Fornecedor Médio'
        ELSE '🟢 Fornecedor Pequeno'
    END as classificacao_fornecedor
FROM despesas
WHERE fornecedor IS NOT NULL AND fornecedor != ''
GROUP BY fornecedor
ORDER BY total_despesa DESC;

-- =====================================================
-- ✅ VERIFICAÇÃO DAS VIEWS CRIADAS
-- =====================================================

-- Listar todas as views criadas
SHOW FULL TABLES WHERE Table_type = 'VIEW';

-- Testar cada view criada
SELECT 'Resumo Financeiro Executivo' as view_teste, COUNT(*) as registros FROM vw_resumo_financeiro_executivo
UNION ALL
SELECT 'Análise de Margem de Lucro' as view_teste, COUNT(*) as registros FROM vw_analise_margem_lucro
UNION ALL
SELECT 'Receita vs Meta' as view_teste, COUNT(*) as registros FROM vw_receita_vs_meta
UNION ALL
SELECT 'Despesas por Categoria' as view_teste, COUNT(*) as registros FROM vw_despesas_por_categoria
UNION ALL
SELECT 'Tendências Financeiras' as view_teste, COUNT(*) as registros FROM vw_tendencias_financeiras
UNION ALL
SELECT 'Análise de Clientes' as view_teste, COUNT(*) as registros FROM vw_analise_clientes
UNION ALL
SELECT 'Análise de Fornecedores' as view_teste, COUNT(*) as registros FROM vw_analise_fornecedores;

-- =====================================================
-- 🎉 VIEWS EXECUTIVAS CRIADAS COM SUCESSO!
-- =====================================================
--
-- Próximos passos:
-- 1. Executar script de análise de KPIs (04_kpi_analysis.sql)
-- 2. Configurar automação Python
-- 3. Criar dashboard executivo
-- 4. Implementar alertas automáticos
--
-- Para testar as views:
-- SELECT * FROM vw_resumo_financeiro_executivo LIMIT 5;
-- SELECT * FROM vw_analise_margem_lucro WHERE tipo = 'receita';
-- SELECT * FROM vw_receita_vs_meta WHERE ano = 2024 AND mes = 12;
-- SELECT * FROM vw_despesas_por_categoria ORDER BY total_despesas DESC;
-- SELECT * FROM vw_tendencias_financeiras WHERE ano = 2024;
-- SELECT * FROM vw_analise_clientes LIMIT 10;
-- SELECT * FROM vw_analise_fornecedores LIMIT 10;
