-- =====================================================
-- 📊 SCRIPT DE ANÁLISE DE KPIs EXECUTIVOS
-- Monitoramento de KPIs Financeiros - Nível Avançado
-- =====================================================
--
-- Este script contém as principais consultas para análise
-- de KPIs financeiros executivos usando as views criadas
--
-- 🎯 OBJETIVOS:
-- 1. Calcular Margem de Lucro
-- 2. Analisar Receita vs Meta
-- 3. Analisar Despesas por Categoria
-- 4. Calcular Lucro Líquido
-- 5. Analisar Evolução de Receitas
-- 6. Comparar Meta x Realizado
-- =====================================================

USE kpis_financeiros_avancado;

-- =====================================================
-- 🎯 KPI 1: MARGEM DE LUCRO
-- =====================================================
-- Propósito: Análise de rentabilidade por período
-- Boa prática: KPI principal para diretoria

SELECT 
    '📊 KPI 1: MARGEM DE LUCRO' as titulo,
    '' as separador,
    mes_ano,
    CONCAT('R$ ', FORMAT(total_receitas, 2)) as receitas,
    CONCAT('R$ ', FORMAT(total_despesas, 2)) as despesas,
    CONCAT('R$ ', FORMAT(lucro_bruto, 2)) as lucro_bruto,
    CONCAT(FORMAT(margem_lucro_percentual, 1), '%') as margem_lucro,
    CONCAT('R$ ', FORMAT(lucro_liquido, 2)) as lucro_liquido,
    CONCAT(FORMAT(margem_liquida_percentual, 1), '%') as margem_liquida,
    status_financeiro,
    classificacao_margem
FROM vw_resumo_financeiro_executivo
WHERE ano = 2024
ORDER BY ano DESC, mes DESC;

-- =====================================================
-- 🎯 KPI 2: RECEITA VS META
-- =====================================================
-- Propósito: Performance de vendas vs metas
-- Boa prática: Controle de orçamento

SELECT 
    '🎯 KPI 2: RECEITA VS META' as titulo,
    '' as separador,
    mes_ano,
    nome_categoria,
    CONCAT('R$ ', FORMAT(meta_receita, 2)) as meta_receita,
    CONCAT('R$ ', FORMAT(receita_realizada, 2)) as receita_realizada,
    CONCAT(FORMAT(percentual_atingimento_receita, 1), '%') as atingimento_receita,
    CONCAT('R$ ', FORMAT(meta_despesa, 2)) as meta_despesa,
    CONCAT('R$ ', FORMAT(despesa_realizada, 2)) as despesa_realizada,
    CONCAT(FORMAT(percentual_controle_despesa, 1), '%') as controle_despesa,
    CONCAT('R$ ', FORMAT(meta_lucro, 2)) as meta_lucro,
    CONCAT('R$ ', FORMAT(lucro_realizado, 2)) as lucro_realizado,
    CONCAT(FORMAT(percentual_atingimento_lucro, 1), '%') as atingimento_lucro,
    status_meta
FROM vw_receita_vs_meta
WHERE ano = 2024 AND mes = 12
ORDER BY tipo, nome_categoria;

-- =====================================================
-- 🎯 KPI 3: DESPESAS POR CATEGORIA
-- =====================================================
-- Propósito: Análise detalhada de custos
-- Boa prática: Controle de gastos por área

SELECT 
    '💸 KPI 3: DESPESAS POR CATEGORIA' as titulo,
    '' as separador,
    nome_categoria,
    CONCAT('R$ ', FORMAT(total_despesas, 2)) as total_despesas,
    CONCAT('R$ ', FORMAT(total_despesas_liquido, 2)) as total_despesas_liquido,
    quantidade_despesas,
    CONCAT('R$ ', FORMAT(valor_medio_despesa, 2)) as valor_medio,
    CONCAT('R$ ', FORMAT(menor_despesa, 2)) as menor_despesa,
    CONCAT('R$ ', FORMAT(maior_despesa, 2)) as maior_despesa,
    CONCAT(FORMAT(percentual_total, 1), '%') as percentual_total,
    CONCAT(FORMAT(percentual_pago, 1), '%') as percentual_pago,
    classificacao_custo
FROM vw_despesas_por_categoria
ORDER BY total_despesas DESC;

-- =====================================================
-- 🎯 KPI 4: LUCRO LÍQUIDO
-- =====================================================
-- Propósito: Resultado final da empresa
-- Boa prática: KPI executivo principal

SELECT 
    '💰 KPI 4: LUCRO LÍQUIDO' as titulo,
    '' as separador,
    mes_ano,
    CONCAT('R$ ', FORMAT(total_receitas_liquido, 2)) as receitas_liquidas,
    CONCAT('R$ ', FORMAT(total_despesas_liquido, 2)) as despesas_liquidas,
    CONCAT('R$ ', FORMAT(lucro_liquido, 2)) as lucro_liquido,
    CONCAT(FORMAT(margem_liquida_percentual, 1), '%') as margem_liquida,
    CASE 
        WHEN lucro_liquido > 0 THEN '🟢 Lucrativo'
        WHEN lucro_liquido < 0 THEN '🔴 Prejuízo'
        ELSE '⚪ Neutro'
    END as status_lucro,
    CASE 
        WHEN margem_liquida_percentual >= 25 THEN '🟢 Excelente'
        WHEN margem_liquida_percentual >= 15 THEN '🟡 Bom'
        WHEN margem_liquida_percentual >= 5 THEN '🟠 Regular'
        ELSE '🔴 Crítico'
    END as classificacao_lucro
FROM vw_resumo_financeiro_executivo
WHERE ano = 2024
ORDER BY ano DESC, mes DESC;

-- =====================================================
-- 🎯 KPI 5: EVOLUÇÃO DE RECEITAS
-- =====================================================
-- Propósito: Análise de tendências de vendas
-- Boa prática: Análise temporal de performance

SELECT 
    '📈 KPI 5: EVOLUÇÃO DE RECEITAS' as titulo,
    '' as separador,
    mes_ano,
    CONCAT('R$ ', FORMAT(total_receitas, 2)) as receitas,
    CONCAT('R$ ', FORMAT(receita_mes_anterior, 2)) as receita_mes_anterior,
    CONCAT(FORMAT(variacao_receita_percentual, 1), '%') as variacao_receita,
    CONCAT('R$ ', FORMAT(total_despesas, 2)) as despesas,
    CONCAT('R$ ', FORMAT(despesa_mes_anterior, 2)) as despesa_mes_anterior,
    CONCAT(FORMAT(variacao_despesa_percentual, 1), '%') as variacao_despesa,
    CONCAT('R$ ', FORMAT(lucro_bruto, 2)) as lucro_bruto,
    CONCAT('R$ ', FORMAT(lucro_mes_anterior, 2)) as lucro_mes_anterior,
    CONCAT(FORMAT(variacao_lucro_percentual, 1), '%') as variacao_lucro,
    tendencia_receita,
    tendencia_despesa,
    tendencia_lucro
FROM vw_tendencias_financeiras
WHERE ano = 2024
ORDER BY ano, mes;

-- =====================================================
-- 🎯 KPI 6: COMPARAÇÃO META X REALIZADO
-- =====================================================
-- Propósito: Dashboard de controle de orçamento
-- Boa prática: Análise de performance das metas

SELECT 
    '🎯 KPI 6: COMPARAÇÃO META X REALIZADO' as titulo,
    '' as separador,
    mes_ano,
    nome_categoria,
    tipo,
    CONCAT('R$ ', FORMAT(meta_receita, 2)) as meta_receita,
    CONCAT('R$ ', FORMAT(receita_realizada, 2)) as receita_realizada,
    CONCAT(FORMAT(percentual_atingimento_receita, 1), '%') as atingimento_receita,
    CONCAT('R$ ', FORMAT(meta_despesa, 2)) as meta_despesa,
    CONCAT('R$ ', FORMAT(despesa_realizada, 2)) as despesa_realizada,
    CONCAT(FORMAT(percentual_controle_despesa, 1), '%') as controle_despesa,
    status_meta
FROM vw_receita_vs_meta
WHERE ano = 2024
ORDER BY mes DESC, tipo, nome_categoria;

-- =====================================================
-- 🎯 KPI 7: ANÁLISE DE MARGEM POR CATEGORIA
-- =====================================================
-- Propósito: Rentabilidade por linha de negócio
-- Boa prática: Análise de portfólio

SELECT 
    '📊 KPI 7: ANÁLISE DE MARGEM POR CATEGORIA' as titulo,
    '' as separador,
    nome_categoria,
    tipo_analise,
    CONCAT('R$ ', FORMAT(total_receitas, 2)) as total_receitas,
    CONCAT('R$ ', FORMAT(total_despesas, 2)) as total_despesas,
    CONCAT('R$ ', FORMAT(lucro_bruto, 2)) as lucro_bruto,
    CONCAT(FORMAT(margem_lucro_percentual, 1), '%') as margem_lucro,
    CONCAT('R$ ', FORMAT(lucro_liquido, 2)) as lucro_liquido,
    CONCAT(FORMAT(margem_liquida_percentual, 1), '%') as margem_liquida,
    quantidade_receitas,
    quantidade_despesas
FROM vw_analise_margem_lucro
ORDER BY margem_lucro_percentual DESC;

-- =====================================================
-- 🎯 KPI 8: ANÁLISE DE CLIENTES
-- =====================================================
-- Propósito: Performance por cliente
-- Boa prática: Análise de portfólio de clientes

SELECT 
    '👥 KPI 8: ANÁLISE DE CLIENTES' as titulo,
    '' as separador,
    cliente,
    quantidade_transacoes,
    CONCAT('R$ ', FORMAT(total_receita, 2)) as total_receita,
    CONCAT('R$ ', FORMAT(valor_medio_transacao, 2)) as valor_medio,
    CONCAT('R$ ', FORMAT(menor_transacao, 2)) as menor_transacao,
    CONCAT('R$ ', FORMAT(maior_transacao, 2)) as maior_transacao,
    CONCAT(FORMAT(percentual_recebido, 1), '%') as percentual_recebido,
    classificacao_cliente
FROM vw_analise_clientes
ORDER BY total_receita DESC
LIMIT 15;

-- =====================================================
-- 🎯 KPI 9: ANÁLISE DE FORNECEDORES
-- =====================================================
-- Propósito: Controle de custos por fornecedor
-- Boa prática: Gestão de fornecedores

SELECT 
    '🏢 KPI 9: ANÁLISE DE FORNECEDORES' as titulo,
    '' as separador,
    fornecedor,
    quantidade_transacoes,
    CONCAT('R$ ', FORMAT(total_despesa, 2)) as total_despesa,
    CONCAT('R$ ', FORMAT(valor_medio_transacao, 2)) as valor_medio,
    CONCAT(FORMAT(percentual_pago, 1), '%') as percentual_pago,
    classificacao_fornecedor
FROM vw_analise_fornecedores
ORDER BY total_despesa DESC
LIMIT 15;

-- =====================================================
-- 🎯 KPI 10: RESUMO EXECUTIVO CONSOLIDADO
-- =====================================================
-- Propósito: Visão macro para diretoria
-- Boa prática: Dashboard executivo consolidado

WITH resumo_executivo AS (
    SELECT 
        COUNT(DISTINCT CASE WHEN status_financeiro = 'Positivo' THEN mes END) as meses_lucrativos,
        COUNT(DISTINCT mes) as total_meses,
        AVG(CASE WHEN status_financeiro = 'Positivo' THEN margem_lucro_percentual END) as margem_media_lucrativa,
        AVG(margem_lucro_percentual) as margem_media_geral,
        SUM(total_receitas) as receita_total_ano,
        SUM(total_despesas) as despesa_total_ano,
        SUM(lucro_bruto) as lucro_total_ano,
        SUM(lucro_liquido) as lucro_liquido_total_ano,
        MAX(margem_lucro_percentual) as melhor_margem,
        MIN(margem_lucro_percentual) as pior_margem
    FROM vw_resumo_financeiro_executivo
    WHERE ano = 2024
)
SELECT 
    '🎯 KPI 10: RESUMO EXECUTIVO CONSOLIDADO - 2024' as titulo,
    '' as separador,
    CONCAT(meses_lucrativos, ' de ', total_meses, ' meses com lucro') as performance_mensal,
    CONCAT(FORMAT((meses_lucrativos / total_meses) * 100, 1), '% dos meses com lucro') as taxa_sucesso,
    CONCAT('R$ ', FORMAT(receita_total_ano, 2), ' em receitas totais') as receita_anual,
    CONCAT('R$ ', FORMAT(despesa_total_ano, 2), ' em despesas totais') as despesa_anual,
    CONCAT('R$ ', FORMAT(lucro_total_ano, 2), ' de lucro bruto total') as lucro_bruto_anual,
    CONCAT('R$ ', FORMAT(lucro_liquido_total_ano, 2), ' de lucro líquido total') as lucro_liquido_anual,
    CONCAT(FORMAT(margem_media_geral, 1), '% de margem média mensal') as margem_media,
    CONCAT(FORMAT(melhor_margem, 1), '% melhor margem mensal') as melhor_margem,
    CONCAT(FORMAT(pior_margem, 1), '% pior margem mensal') as pior_margem,
    CASE 
        WHEN (meses_lucrativos / total_meses) >= 0.8 THEN '🟢 Excelente Performance'
        WHEN (meses_lucrativos / total_meses) >= 0.6 THEN '🟡 Boa Performance'
        WHEN (meses_lucrativos / total_meses) >= 0.4 THEN '🟠 Performance Regular'
        ELSE '🔴 Performance Crítica'
    END as classificacao_geral
FROM resumo_executivo;

-- =====================================================
-- 🎯 KPI 11: ANÁLISE DE SAZONALIDADE
-- =====================================================
-- Propósito: Identificar padrões temporais
-- Boa prática: Planejamento estratégico

SELECT 
    '📅 KPI 11: ANÁLISE DE SAZONALIDADE - 2024' as titulo,
    '' as separador,
    CASE 
        WHEN mes IN (12, 1, 2) THEN 'Verão'
        WHEN mes IN (3, 4, 5) THEN 'Outono'
        WHEN mes IN (6, 7, 8) THEN 'Inverno'
        ELSE 'Primavera'
    END as estacao,
    COUNT(*) as meses_analisados,
    CONCAT('R$ ', FORMAT(AVG(total_receitas), 2)) as receita_media,
    CONCAT('R$ ', FORMAT(AVG(total_despesas), 2)) as despesa_media,
    CONCAT('R$ ', FORMAT(AVG(lucro_bruto), 2)) as lucro_medio,
    CONCAT(FORMAT(AVG(margem_lucro_percentual), 1), '%') as margem_media,
    CONCAT('R$ ', FORMAT(AVG(lucro_liquido), 2)) as lucro_liquido_medio,
    CONCAT(FORMAT(AVG(margem_liquida_percentual), 1), '%') as margem_liquida_media
FROM vw_resumo_financeiro_executivo
WHERE ano = 2024
GROUP BY 
    CASE 
        WHEN mes IN (12, 1, 2) THEN 'Verão'
        WHEN mes IN (3, 4, 5) THEN 'Outono'
        WHEN mes IN (6, 7, 8) THEN 'Inverno'
        ELSE 'Primavera'
    END
ORDER BY 
    CASE estacao
        WHEN 'Verão' THEN 1
        WHEN 'Outono' THEN 2
        WHEN 'Inverno' THEN 3
        WHEN 'Primavera' THEN 4
    END;

-- =====================================================
-- 🎯 KPI 12: ANÁLISE DE FORMAS DE PAGAMENTO
-- =====================================================
-- Propósito: Comportamento de pagamento
-- Boa prática: Análise de fluxo de caixa

SELECT 
    '💳 KPI 12: ANÁLISE DE FORMAS DE PAGAMENTO' as titulo,
    '' as separador,
    forma_pagamento,
    COUNT(*) as quantidade_transacoes,
    CONCAT('R$ ', FORMAT(SUM(valor), 2)) as valor_total,
    CONCAT('R$ ', FORMAT(AVG(valor), 2)) as valor_medio,
    ROUND((SUM(valor) / (SELECT SUM(valor) FROM despesas WHERE YEAR(data_despesa) = 2024)) * 100, 2) as percentual_total,
    MIN(valor) as valor_minimo,
    MAX(valor) as valor_maximo
FROM despesas
WHERE YEAR(data_despesa) = 2024
GROUP BY forma_pagamento
ORDER BY valor_total DESC;

-- =====================================================
-- ✅ VERIFICAÇÃO DOS KPIs
-- =====================================================

-- Comando para verificar se todas as views estão funcionando
SELECT 'Verificação das Views' as teste, COUNT(*) as total FROM vw_resumo_financeiro_executivo
UNION ALL
SELECT 'Verificação das Views' as teste, COUNT(*) as total FROM vw_analise_margem_lucro
UNION ALL
SELECT 'Verificação das Views' as teste, COUNT(*) as total FROM vw_receita_vs_meta
UNION ALL
SELECT 'Verificação das Views' as teste, COUNT(*) as total FROM vw_despesas_por_categoria
UNION ALL
SELECT 'Verificação das Views' as teste, COUNT(*) as total FROM vw_tendencias_financeiras
UNION ALL
SELECT 'Verificação das Views' as teste, COUNT(*) as total FROM vw_analise_clientes
UNION ALL
SELECT 'Verificação das Views' as teste, COUNT(*) as total FROM vw_analise_fornecedores;

-- =====================================================
-- 🎉 ANÁLISE DE KPIs EXECUTIVOS CONCLUÍDA!
-- =====================================================
--
-- 📊 KPIs ANALISADOS:
-- 1. ✅ Margem de Lucro - Rentabilidade por período
-- 2. ✅ Receita vs Meta - Performance de vendas
-- 3. ✅ Despesas por Categoria - Controle de custos
-- 4. ✅ Lucro Líquido - Resultado final
-- 5. ✅ Evolução de Receitas - Tendências temporais
-- 6. ✅ Comparação Meta x Realizado - Controle de orçamento
-- 7. ✅ Análise de Margem por Categoria - Rentabilidade por linha
-- 8. ✅ Análise de Clientes - Performance por cliente
-- 9. ✅ Análise de Fornecedores - Controle de custos
-- 10. ✅ Resumo Executivo Consolidado - Visão macro
-- 11. ✅ Análise de Sazonalidade - Padrões temporais
-- 12. ✅ Análise de Formas de Pagamento - Fluxo de caixa
--
-- 🚀 PRÓXIMOS PASSOS:
-- 1. Configurar automação Python para atualização
-- 2. Criar dashboard executivo com Streamlit
-- 3. Implementar alertas automáticos
-- 4. Criar relatórios periódicos
--
-- 💡 DICAS DE USO:
-- - Execute cada KPI individualmente para análise detalhada
-- - Use as views para criar dashboards personalizados
-- - Monitore os KPIs regularmente para tomada de decisão
-- - Compare períodos para identificar tendências
-- - Use os dados para planejamento estratégico
