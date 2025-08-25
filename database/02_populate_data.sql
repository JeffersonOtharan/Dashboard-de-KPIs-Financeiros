-- =====================================================
-- 📊 SCRIPT DE POPULAÇÃO DE DADOS EXECUTIVOS
-- Monitoramento de KPIs Financeiros - Nível Avançado
-- =====================================================
--
-- Este script insere dados realistas para demonstrar
-- análise financeira executiva com KPIs de negócio
--
-- 🎯 OBJETIVOS:
-- 1. Inserir dados de empresa realista
-- 2. Criar cenário de negócio completo
-- 3. Demonstrar análise de KPIs executivos
-- 4. Preparar dados para dashboard
-- =====================================================

USE kpis_financeiros_avancado;

-- =====================================================
-- 📊 INSERÇÃO DE DADOS EXECUTIVOS
-- =====================================================

-- Inserir dados de receitas (últimos 12 meses)
INSERT INTO receitas (id_empresa, id_categoria, codigo_transacao, descricao, valor, valor_liquido, data_receita, data_recebimento, status, cliente, forma_recebimento) VALUES
-- Janeiro 2024 - Vendas
(1, 1, 'REC-2024-001', 'Venda Software Enterprise', 50000.00, 47500.00, '2024-01-15', '2024-01-20', 'recebido', 'TechCorp Ltda', 'transferencia'),
(1, 1, 'REC-2024-002', 'Venda Licenças Mensais', 15000.00, 14250.00, '2024-01-20', '2024-01-25', 'recebido', 'StartupXYZ', 'pix'),
(1, 2, 'REC-2024-003', 'Serviço de Implementação', 25000.00, 23750.00, '2024-01-25', '2024-01-30', 'recebido', 'CorpABC', 'boleto'),

-- Fevereiro 2024 - Vendas
(1, 1, 'REC-2024-004', 'Venda Software Pro', 35000.00, 33250.00, '2024-02-10', '2024-02-15', 'recebido', 'MegaCorp', 'transferencia'),
(1, 2, 'REC-2024-005', 'Consultoria Estratégica', 40000.00, 38000.00, '2024-02-15', '2024-02-20', 'recebido', 'GlobalTech', 'boleto'),
(1, 3, 'REC-2024-006', 'Licenças Trimestrais', 20000.00, 19000.00, '2024-02-20', '2024-02-25', 'recebido', 'InnovationLab', 'pix'),

-- Março 2024 - Vendas
(1, 1, 'REC-2024-007', 'Venda Software Premium', 60000.00, 57000.00, '2024-03-05', '2024-03-10', 'recebido', 'FutureCorp', 'transferencia'),
(1, 2, 'REC-2024-008', 'Serviço de Migração', 30000.00, 28500.00, '2024-03-10', '2024-03-15', 'recebido', 'LegacyTech', 'boleto'),
(1, 4, 'REC-2024-009', 'Consultoria de Otimização', 45000.00, 42750.00, '2024-03-15', '2024-03-20', 'recebido', 'EfficiencyCorp', 'boleto'),

-- Abril 2024 - Vendas
(1, 1, 'REC-2024-010', 'Venda Software Standard', 25000.00, 23750.00, '2024-04-05', '2024-04-10', 'recebido', 'SmallBiz Inc', 'pix'),
(1, 2, 'REC-2024-011', 'Serviço de Suporte', 18000.00, 17100.00, '2024-04-10', '2024-04-15', 'recebido', 'SupportCorp', 'boleto'),
(1, 3, 'REC-2024-012', 'Licenças Anuais', 35000.00, 33250.00, '2024-04-15', '2024-04-20', 'recebido', 'AnnualTech', 'transferencia'),

-- Maio 2024 - Vendas
(1, 1, 'REC-2024-013', 'Venda Software Enterprise Plus', 75000.00, 71250.00, '2024-05-05', '2024-05-10', 'recebido', 'EnterpriseCorp', 'transferencia'),
(1, 2, 'REC-2024-014', 'Serviço de Integração', 35000.00, 33250.00, '2024-05-10', '2024-05-15', 'recebido', 'IntegrationLab', 'boleto'),
(1, 4, 'REC-2024-015', 'Consultoria de Transformação', 55000.00, 52250.00, '2024-05-15', '2024-05-20', 'recebido', 'TransformCorp', 'boleto'),

-- Junho 2024 - Vendas
(1, 1, 'REC-2024-016', 'Venda Software Cloud', 40000.00, 38000.00, '2024-06-05', '2024-06-10', 'recebido', 'CloudCorp', 'pix'),
(1, 2, 'REC-2024-017', 'Serviço de Manutenção', 22000.00, 20900.00, '2024-06-10', '2024-06-15', 'recebido', 'MaintenanceCorp', 'boleto'),
(1, 3, 'REC-2024-018', 'Licenças Semestrais', 28000.00, 26600.00, '2024-06-15', '2024-06-20', 'recebido', 'SemesterTech', 'transferencia'),

-- Julho 2024 - Vendas
(1, 1, 'REC-2024-019', 'Venda Software Mobile', 30000.00, 28500.00, '2024-07-05', '2024-07-10', 'recebido', 'MobileCorp', 'pix'),
(1, 2, 'REC-2024-020', 'Serviço de Treinamento', 25000.00, 23750.00, '2024-07-10', '2024-07-15', 'recebido', 'TrainingCorp', 'boleto'),
(1, 4, 'REC-2024-021', 'Consultoria de Segurança', 40000.00, 38000.00, '2024-07-15', '2024-07-20', 'recebido', 'SecurityCorp', 'boleto'),

-- Agosto 2024 - Vendas
(1, 1, 'REC-2024-022', 'Venda Software Analytics', 55000.00, 52250.00, '2024-08-05', '2024-08-10', 'recebido', 'AnalyticsCorp', 'transferencia'),
(1, 2, 'REC-2024-023', 'Serviço de Backup', 18000.00, 17100.00, '2024-08-10', '2024-08-15', 'recebido', 'BackupCorp', 'boleto'),
(1, 3, 'REC-2024-024', 'Licenças Trimestrais Plus', 32000.00, 30400.00, '2024-08-15', '2024-08-20', 'recebido', 'QuarterlyTech', 'pix'),

-- Setembro 2024 - Vendas
(1, 1, 'REC-2024-025', 'Venda Software AI', 80000.00, 76000.00, '2024-09-05', '2024-09-10', 'recebido', 'AICorp', 'transferencia'),
(1, 2, 'REC-2024-026', 'Serviço de Monitoramento', 28000.00, 26600.00, '2024-09-10', '2024-09-15', 'recebido', 'MonitorCorp', 'boleto'),
(1, 4, 'REC-2024-027', 'Consultoria de Inovação', 60000.00, 57000.00, '2024-09-15', '2024-09-20', 'recebido', 'InnovationCorp', 'boleto'),

-- Outubro 2024 - Vendas
(1, 1, 'REC-2024-028', 'Venda Software IoT', 45000.00, 42750.00, '2024-10-05', '2024-10-10', 'recebido', 'IoTCorp', 'pix'),
(1, 2, 'REC-2024-029', 'Serviço de Atualização', 20000.00, 19000.00, '2024-10-10', '2024-10-15', 'recebido', 'UpdateCorp', 'boleto'),
(1, 3, 'REC-2024-030', 'Licenças Anuais Premium', 45000.00, 42750.00, '2024-10-15', '2024-10-20', 'recebido', 'PremiumTech', 'transferencia'),

-- Novembro 2024 - Vendas
(1, 1, 'REC-2024-031', 'Venda Software Blockchain', 70000.00, 66500.00, '2024-11-05', '2024-11-10', 'recebido', 'BlockchainCorp', 'transferencia'),
(1, 2, 'REC-2024-032', 'Serviço de Auditoria', 35000.00, 33250.00, '2024-11-10', '2024-11-15', 'recebido', 'AuditCorp', 'boleto'),
(1, 4, 'REC-2024-033', 'Consultoria de Compliance', 50000.00, 47500.00, '2024-11-15', '2024-11-20', 'recebido', 'ComplianceCorp', 'boleto'),

-- Dezembro 2024 - Vendas
(1, 1, 'REC-2024-034', 'Venda Software ERP', 90000.00, 85500.00, '2024-12-05', '2024-12-10', 'recebido', 'ERPCorp', 'transferencia'),
(1, 2, 'REC-2024-035', 'Serviço de Configuração', 40000.00, 38000.00, '2024-12-10', '2024-12-15', 'recebido', 'ConfigCorp', 'boleto'),
(1, 3, 'REC-2024-036', 'Licenças Anuais Enterprise', 60000.00, 57000.00, '2024-12-15', '2024-12-20', 'recebido', 'EnterpriseTech', 'transferencia');

-- Inserir dados de despesas (últimos 12 meses)
INSERT INTO despesas (id_empresa, id_categoria, codigo_transacao, descricao, valor, valor_liquido, data_despesa, data_pagamento, status, fornecedor, forma_pagamento) VALUES
-- Janeiro 2024 - Despesas
(1, 5, 'DES-2024-001', 'Salários Equipe Desenvolvimento', 45000.00, 45000.00, '2024-01-05', '2024-01-05', 'pago', 'Folha de Pagamento', 'transferencia'),
(1, 6, 'DES-2024-002', 'Campanha Google Ads', 8000.00, 8000.00, '2024-01-10', '2024-01-10', 'pago', 'Google', 'cartao_credito'),
(1, 7, 'DES-2024-003', 'Servidor AWS', 3000.00, 3000.00, '2024-01-15', '2024-01-15', 'pago', 'Amazon Web Services', 'cartao_credito'),
(1, 8, 'DES-2024-004', 'Material de Escritório', 1500.00, 1500.00, '2024-01-20', '2024-01-20', 'pago', 'Papelaria Central', 'dinheiro'),

-- Fevereiro 2024 - Despesas
(1, 5, 'DES-2024-005', 'Salários Equipe Vendas', 35000.00, 35000.00, '2024-02-05', '2024-02-05', 'pago', 'Folha de Pagamento', 'transferencia'),
(1, 6, 'DES-2024-006', 'Campanha LinkedIn', 5000.00, 5000.00, '2024-02-10', '2024-02-10', 'pago', 'LinkedIn', 'cartao_credito'),
(1, 7, 'DES-2024-007', 'Licenças Software', 4000.00, 4000.00, '2024-02-15', '2024-02-15', 'pago', 'Microsoft', 'boleto'),
(1, 8, 'DES-2024-008', 'Limpeza Escritório', 1200.00, 1200.00, '2024-02-20', '2024-02-20', 'pago', 'Limpeza Pro', 'pix'),

-- Março 2024 - Despesas
(1, 5, 'DES-2024-009', 'Salários Equipe Marketing', 28000.00, 28000.00, '2024-03-05', '2024-03-05', 'pago', 'Folha de Pagamento', 'transferencia'),
(1, 6, 'DES-2024-010', 'Evento Tech Conference', 12000.00, 12000.00, '2024-03-10', '2024-03-10', 'pago', 'TechEvents', 'boleto'),
(1, 7, 'DES-2024-011', 'Internet Empresarial', 800.00, 800.00, '2024-03-15', '2024-03-15', 'pago', 'Telecom', 'boleto'),
(1, 8, 'DES-2024-012', 'Segurança Escritório', 2000.00, 2000.00, '2024-03-20', '2024-03-20', 'pago', 'SecurityPro', 'boleto'),

-- Abril 2024 - Despesas
(1, 5, 'DES-2024-013', 'Salários Equipe Suporte', 32000.00, 32000.00, '2024-04-05', '2024-04-05', 'pago', 'Folha de Pagamento', 'transferencia'),
(1, 6, 'DES-2024-014', 'Campanha Facebook Ads', 6000.00, 6000.00, '2024-04-10', '2024-04-10', 'pago', 'Meta', 'cartao_credito'),
(1, 7, 'DES-2024-015', 'Backup Cloud', 1500.00, 1500.00, '2024-04-15', '2024-04-15', 'pago', 'BackupCloud', 'cartao_credito'),
(1, 8, 'DES-2024-016', 'Manutenção Ar Condicionado', 1800.00, 1800.00, '2024-04-20', '2024-04-20', 'pago', 'ClimaTech', 'pix'),

-- Maio 2024 - Despesas
(1, 5, 'DES-2024-017', 'Salários Equipe Administrativa', 25000.00, 25000.00, '2024-05-05', '2024-05-05', 'pago', 'Folha de Pagamento', 'transferencia'),
(1, 6, 'DES-2024-018', 'Webinar Marketing', 8000.00, 8000.00, '2024-05-10', '2024-05-10', 'pago', 'WebinarPro', 'boleto'),
(1, 7, 'DES-2024-019', 'Monitoramento Sistema', 2500.00, 2500.00, '2024-05-15', '2024-05-15', 'pago', 'MonitorPro', 'cartao_credito'),
(1, 8, 'DES-2024-020', 'Alimentação Equipe', 3000.00, 3000.00, '2024-05-20', '2024-05-20', 'pago', 'Catering Pro', 'boleto'),

-- Junho 2024 - Despesas
(1, 5, 'DES-2024-021', 'Salários Equipe RH', 22000.00, 22000.00, '2024-06-05', '2024-06-05', 'pago', 'Folha de Pagamento', 'transferencia'),
(1, 6, 'DES-2024-022', 'Campanha Email Marketing', 3000.00, 3000.00, '2024-06-10', '2024-06-10', 'pago', 'MailChimp', 'cartao_credito'),
(1, 7, 'DES-2024-023', 'VPN Empresarial', 1200.00, 1200.00, '2024-06-15', '2024-06-15', 'pago', 'VPNPro', 'boleto'),
(1, 8, 'DES-2024-024', 'Transporte Equipe', 2500.00, 2500.00, '2024-06-20', '2024-06-20', 'pago', 'TransportPro', 'boleto'),

-- Julho 2024 - Despesas
(1, 5, 'DES-2024-025', 'Salários Equipe Financeira', 30000.00, 30000.00, '2024-07-05', '2024-07-05', 'pago', 'Folha de Pagamento', 'transferencia'),
(1, 6, 'DES-2024-026', 'Conferência de Vendas', 15000.00, 15000.00, '2024-07-10', '2024-07-10', 'pago', 'SalesConf', 'boleto'),
(1, 7, 'DES-2024-027', 'Antivírus Corporativo', 2000.00, 2000.00, '2024-07-15', '2024-07-15', 'pago', 'AntivirusPro', 'cartao_credito'),
(1, 8, 'DES-2024-028', 'Treinamento Equipe', 5000.00, 5000.00, '2024-07-20', '2024-07-20', 'pago', 'TrainingPro', 'boleto'),

-- Agosto 2024 - Despesas
(1, 5, 'DES-2024-029', 'Salários Equipe Legal', 28000.00, 28000.00, '2024-08-05', '2024-08-05', 'pago', 'Folha de Pagamento', 'transferencia'),
(1, 6, 'DES-2024-030', 'Campanha Influenciadores', 10000.00, 10000.00, '2024-08-10', '2024-08-10', 'pago', 'InfluencerPro', 'boleto'),
(1, 7, 'DES-2024-031', 'Backup Físico', 3000.00, 3000.00, '2024-08-15', '2024-08-15', 'pago', 'BackupFisico', 'boleto'),
(1, 8, 'DES-2024-032', 'Seguro Empresarial', 4000.00, 4000.00, '2024-08-20', '2024-08-20', 'pago', 'SeguroPro', 'boleto'),

-- Setembro 2024 - Despesas
(1, 5, 'DES-2024-033', 'Salários Equipe Operacional', 35000.00, 35000.00, '2024-09-05', '2024-09-05', 'pago', 'Folha de Pagamento', 'transferencia'),
(1, 6, 'DES-2024-034', 'Campanha Trade Marketing', 8000.00, 8000.00, '2024-09-10', '2024-09-10', 'pago', 'TradePro', 'boleto'),
(1, 7, 'DES-2024-035', 'Cloud Storage', 2500.00, 2500.00, '2024-09-15', '2024-09-15', 'pago', 'CloudStorage', 'cartao_credito'),
(1, 8, 'DES-2024-036', 'Consultoria Jurídica', 6000.00, 6000.00, '2024-09-20', '2024-09-20', 'pago', 'LegalPro', 'boleto'),

-- Outubro 2024 - Despesas
(1, 5, 'DES-2024-037', 'Salários Equipe Comercial', 40000.00, 40000.00, '2024-10-05', '2024-10-05', 'pago', 'Folha de Pagamento', 'transferencia'),
(1, 6, 'DES-2024-038', 'Campanha Outbound', 12000.00, 12000.00, '2024-10-10', '2024-10-10', 'pago', 'OutboundPro', 'boleto'),
(1, 7, 'DES-2024-039', 'Monitoramento Rede', 3000.00, 3000.00, '2024-10-15', '2024-10-15', 'pago', 'NetworkPro', 'cartao_credito'),
(1, 8, 'DES-2024-040', 'Auditoria Externa', 8000.00, 8000.00, '2024-10-20', '2024-10-20', 'pago', 'AuditoriaPro', 'boleto'),

-- Novembro 2024 - Despesas
(1, 5, 'DES-2024-041', 'Salários Equipe Técnica', 45000.00, 45000.00, '2024-11-05', '2024-11-05', 'pago', 'Folha de Pagamento', 'transferencia'),
(1, 6, 'DES-2024-042', 'Campanha Retargeting', 7000.00, 7000.00, '2024-11-10', '2024-11-10', 'pago', 'RetargetPro', 'cartao_credito'),
(1, 7, 'DES-2024-043', 'Firewall Empresarial', 4000.00, 4000.00, '2024-11-15', '2024-11-15', 'pago', 'FirewallPro', 'boleto'),
(1, 8, 'DES-2024-044', 'Consultoria Contábil', 5000.00, 5000.00, '2024-11-20', '2024-11-20', 'pago', 'ContabilPro', 'boleto'),

-- Dezembro 2024 - Despesas
(1, 5, 'DES-2024-045', 'Salários Equipe Executiva', 60000.00, 60000.00, '2024-12-05', '2024-12-05', 'pago', 'Folha de Pagamento', 'transferencia'),
(1, 6, 'DES-2024-046', 'Campanha Final de Ano', 15000.00, 15000.00, '2024-12-10', '2024-12-10', 'pago', 'FinalAnoPro', 'boleto'),
(1, 7, 'DES-2024-047', 'Backup de Fim de Ano', 5000.00, 5000.00, '2024-12-15', '2024-12-15', 'pago', 'BackupAno', 'boleto'),
(1, 8, 'DES-2024-048', 'Festa de Fim de Ano', 8000.00, 8000.00, '2024-12-20', '2024-12-20', 'pago', 'FestaPro', 'boleto');

-- Inserir metas mensais para 2024
INSERT INTO metas_mensais (id_empresa, ano, mes, id_categoria, meta_receita, meta_despesa, meta_lucro, meta_margem) VALUES
-- Metas de Receita por Categoria
(1, 2024, 1, 1, 60000.00, 0.00, 45000.00, 75.00),   -- Vendas
(1, 2024, 1, 2, 30000.00, 0.00, 22500.00, 75.00),   -- Serviços
(1, 2024, 1, 3, 20000.00, 0.00, 15000.00, 75.00),   -- Licenças
(1, 2024, 1, 4, 40000.00, 0.00, 30000.00, 75.00),   -- Consultoria

-- Metas de Despesa por Categoria
(1, 2024, 1, 5, 0.00, 45000.00, 0.00, 0.00),        -- Pessoal
(1, 2024, 1, 6, 0.00, 8000.00, 0.00, 0.00),         -- Marketing
(1, 2024, 1, 7, 0.00, 3000.00, 0.00, 0.00),         -- Infraestrutura
(1, 2024, 1, 8, 0.00, 1500.00, 0.00, 0.00),         -- Operacional

-- Continuar para todos os meses...
(1, 2024, 2, 1, 55000.00, 0.00, 41250.00, 75.00),
(1, 2024, 2, 2, 35000.00, 0.00, 26250.00, 75.00),
(1, 2024, 2, 3, 25000.00, 0.00, 18750.00, 75.00),
(1, 2024, 2, 4, 45000.00, 0.00, 33750.00, 75.00),
(1, 2024, 2, 5, 0.00, 35000.00, 0.00, 0.00),
(1, 2024, 2, 6, 0.00, 5000.00, 0.00, 0.00),
(1, 2024, 2, 7, 0.00, 4000.00, 0.00, 0.00),
(1, 2024, 2, 8, 0.00, 1200.00, 0.00, 0.00),

-- Adicionar mais meses conforme necessário...
(1, 2024, 3, 1, 70000.00, 0.00, 52500.00, 75.00),
(1, 2024, 3, 2, 40000.00, 0.00, 30000.00, 75.00),
(1, 2024, 3, 3, 30000.00, 0.00, 22500.00, 75.00),
(1, 2024, 3, 4, 50000.00, 0.00, 37500.00, 75.00),
(1, 2024, 3, 5, 0.00, 28000.00, 0.00, 0.00),
(1, 2024, 3, 6, 0.00, 12000.00, 0.00, 0.00),
(1, 2024, 3, 7, 0.00, 800.00, 0.00, 0.00),
(1, 2024, 3, 8, 0.00, 2000.00, 0.00, 0.00);

-- =====================================================
-- ✅ VERIFICAÇÃO DOS DADOS INSERIDOS
-- =====================================================

-- Resumo executivo dos dados
SELECT 
    '📊 RESUMO EXECUTIVO DOS DADOS' as titulo,
    '' as separador,
    CONCAT('Total de Receitas: R$ ', FORMAT(SUM(valor), 2)) as total_receitas,
    CONCAT('Total de Despesas: R$ ', FORMAT(SUM(valor), 2)) as total_despesas,
    CONCAT('Saldo Geral: R$ ', FORMAT(SUM(CASE WHEN tipo = 'receita' THEN valor ELSE -valor END), 2)) as saldo_geral
FROM (
    SELECT 'receita' as tipo, valor FROM receitas WHERE YEAR(data_receita) = 2024
    UNION ALL
    SELECT 'despesa' as tipo, valor FROM despesas WHERE YEAR(data_despesa) = 2024
) consolidado;

-- Análise por categoria de receita
SELECT 
    '💰 ANÁLISE POR CATEGORIA DE RECEITA' as titulo,
    '' as separador,
    c.nome_categoria,
    CONCAT('R$ ', FORMAT(SUM(r.valor), 2)) as total_receita,
    COUNT(*) as quantidade_transacoes,
    CONCAT('R$ ', FORMAT(AVG(r.valor), 2)) as valor_medio
FROM receitas r
JOIN categorias c ON r.id_categoria = c.id_categoria
WHERE c.tipo = 'receita' AND YEAR(r.data_receita) = 2024
GROUP BY c.id_categoria, c.nome_categoria
ORDER BY SUM(r.valor) DESC;

-- Análise por categoria de despesa
SELECT 
    '💸 ANÁLISE POR CATEGORIA DE DESPESA' as titulo,
    '' as separador,
    c.nome_categoria,
    CONCAT('R$ ', FORMAT(SUM(d.valor), 2)) as total_despesa,
    COUNT(*) as quantidade_transacoes,
    CONCAT('R$ ', FORMAT(AVG(d.valor), 2)) as valor_medio
FROM despesas d
JOIN categorias c ON d.id_categoria = c.id_categoria
WHERE c.tipo = 'despesa' AND YEAR(d.data_despesa) = 2024
GROUP BY c.id_categoria, c.nome_categoria
ORDER BY SUM(d.valor) DESC;

-- =====================================================
-- 🎉 DADOS EXECUTIVOS POPULADOS COM SUCESSO!
-- =====================================================
--
-- Próximos passos:
-- 1. Executar script de criação de views (03_create_views.sql)
-- 2. Executar script de análise de KPIs (04_kpi_analysis.sql)
-- 3. Configurar automação Python
-- 4. Criar dashboard executivo
--
-- Para verificar se tudo está funcionando:
-- SELECT COUNT(*) FROM receitas WHERE YEAR(data_receita) = 2024;
-- SELECT COUNT(*) FROM despesas WHERE YEAR(data_despesa) = 2024;
-- SELECT COUNT(*) FROM metas_mensais WHERE ano = 2024;
