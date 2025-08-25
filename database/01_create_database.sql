-- SCRIPT AVANÇADO DE CRIAÇÃO DO BANCO DE DADOS
-- Sistema de Monitoramento de KPIs Financeiros
-- Versão: 1.0
-- Data: 2024

-- OBJETIVOS:
-- 1. Criar estrutura robusta para monitoramento financeiro
-- 2. Implementar relacionamentos e constraints de integridade
-- 3. Criar índices para otimização de performance
-- 4. Implementar triggers para auditoria automática
-- 5. Preparar base para análises executivas

-- ========================================
-- CRIAÇÃO DO BANCO DE DADOS
-- ========================================

CREATE DATABASE IF NOT EXISTS kpis_financeiros_avancado
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE kpis_financeiros_avancado;

-- ========================================
-- TABELA: EMPRESAS
-- ========================================

CREATE TABLE IF NOT EXISTS empresas (
    id_empresa INT AUTO_INCREMENT PRIMARY KEY,
    nome_empresa VARCHAR(255) NOT NULL,
    cnpj VARCHAR(18) UNIQUE,
    setor VARCHAR(100),
    porte ENUM('pequena', 'media', 'grande') DEFAULT 'media',
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_nome_empresa (nome_empresa),
    INDEX idx_setor (setor),
    INDEX idx_ativo (ativo)
);

-- ========================================
-- TABELA: CATEGORIAS
-- ========================================

CREATE TABLE IF NOT EXISTS categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nome_categoria VARCHAR(255) NOT NULL,
    tipo ENUM('receita', 'despesa') NOT NULL,
    categoria_pai INT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (categoria_pai) REFERENCES categorias(id_categoria) ON DELETE SET NULL,
    INDEX idx_tipo (tipo),
    INDEX idx_ativo (ativo),
    INDEX idx_categoria_pai (categoria_pai)
);

-- ========================================
-- TABELA: RECEITAS
-- ========================================

CREATE TABLE IF NOT EXISTS receitas (
    id_receita INT AUTO_INCREMENT PRIMARY KEY,
    id_empresa INT NOT NULL,
    id_categoria INT NOT NULL,
    codigo_transacao VARCHAR(50) UNIQUE,
    descricao TEXT NOT NULL,
    valor DECIMAL(15,2) NOT NULL CHECK (valor > 0),
    valor_liquido DECIMAL(15,2) NOT NULL CHECK (valor_liquido > 0),
    data_receita DATE NOT NULL,
    data_recebimento DATE,
    status ENUM('pendente', 'recebido', 'cancelado') DEFAULT 'pendente',
    fonte_receita VARCHAR(100),
    cliente VARCHAR(255),
    forma_recebimento ENUM('dinheiro', 'pix', 'transferencia', 'boleto', 'cartao_credito', 'cartao_debito') NOT NULL,
    parcelado BOOLEAN DEFAULT FALSE,
    num_parcelas INT DEFAULT 1,
    observacoes TEXT,
    tags JSON,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_empresa) REFERENCES empresas(id_empresa) ON DELETE CASCADE,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria) ON DELETE RESTRICT,
    
    INDEX idx_empresa (id_empresa),
    INDEX idx_categoria (id_categoria),
    INDEX idx_data_receita (data_receita),
    INDEX idx_status (status),
    INDEX idx_cliente (cliente),
    INDEX idx_forma_recebimento (forma_recebimento)
);

-- ========================================
-- TABELA: DESPESAS
-- ========================================

CREATE TABLE IF NOT EXISTS despesas (
    id_despesa INT AUTO_INCREMENT PRIMARY KEY,
    id_empresa INT NOT NULL,
    id_categoria INT NOT NULL,
    codigo_transacao VARCHAR(50) UNIQUE,
    descricao TEXT NOT NULL,
    valor DECIMAL(15,2) NOT NULL CHECK (valor > 0),
    valor_liquido DECIMAL(15,2) NOT NULL CHECK (valor_liquido > 0),
    data_despesa DATE NOT NULL,
    data_pagamento DATE,
    status ENUM('pendente', 'pago', 'cancelado') DEFAULT 'pendente',
    fornecedor VARCHAR(255),
    forma_pagamento ENUM('dinheiro', 'pix', 'transferencia', 'boleto', 'cartao_credito', 'cartao_debito') NOT NULL,
    parcelado BOOLEAN DEFAULT FALSE,
    num_parcelas INT DEFAULT 1,
    observacoes TEXT,
    tags JSON,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_empresa) REFERENCES empresas(id_empresa) ON DELETE CASCADE,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria) ON DELETE RESTRICT,
    
    INDEX idx_empresa (id_empresa),
    INDEX idx_categoria (id_categoria),
    INDEX idx_data_despesa (data_despesa),
    INDEX idx_status (status),
    INDEX idx_fornecedor (fornecedor),
    INDEX idx_forma_pagamento (forma_pagamento)
);

-- ========================================
-- TABELA: METAS_MENSAIS
-- ========================================

CREATE TABLE IF NOT EXISTS metas_mensais (
    id_meta INT AUTO_INCREMENT PRIMARY KEY,
    id_empresa INT NOT NULL,
    ano INT NOT NULL CHECK (ano >= 2000 AND ano <= 2100),
    mes INT NOT NULL CHECK (mes >= 1 AND mes <= 12),
    meta_receita DECIMAL(15,2) NOT NULL CHECK (meta_receita > 0),
    meta_despesa DECIMAL(15,2) NOT NULL CHECK (meta_despesa > 0),
    meta_lucro DECIMAL(15,2),
    observacoes TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_empresa) REFERENCES empresas(id_empresa) ON DELETE CASCADE,
    UNIQUE KEY uk_empresa_ano_mes (id_empresa, ano, mes),
    
    INDEX idx_empresa (id_empresa),
    INDEX idx_ano_mes (ano, mes)
);

-- ========================================
-- TABELA: KPIS_CALCULADOS
-- ========================================

CREATE TABLE IF NOT EXISTS kpis_calculados (
    id_kpi INT AUTO_INCREMENT PRIMARY KEY,
    id_empresa INT NOT NULL,
    ano INT NOT NULL,
    mes INT NOT NULL,
    tipo_kpi VARCHAR(100) NOT NULL,
    valor_kpi DECIMAL(15,4) NOT NULL,
    unidade VARCHAR(20),
    data_calculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_empresa) REFERENCES empresas(id_empresa) ON DELETE CASCADE,
    UNIQUE KEY uk_empresa_ano_mes_tipo (id_empresa, ano, mes, tipo_kpi),
    
    INDEX idx_empresa (id_empresa),
    INDEX idx_ano_mes (ano, mes),
    INDEX idx_tipo_kpi (tipo_kpi)
);

-- ========================================
-- TABELA: LOG_TRANSACOES
-- ========================================

CREATE TABLE IF NOT EXISTS log_transacoes (
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    tabela_afetada VARCHAR(50) NOT NULL,
    id_registro INT NOT NULL,
    tipo_operacao ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    dados_anteriores JSON,
    dados_novos JSON,
    usuario VARCHAR(100),
    data_operacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_tabela_afetada (tabela_afetada),
    INDEX idx_id_registro (id_registro),
    INDEX idx_tipo_operacao (tipo_operacao),
    INDEX idx_data_operacao (data_operacao)
);

-- ========================================
-- CRIAÇÃO DE ÍNDICES AVANÇADOS
-- ========================================

-- Índices compostos para otimização de queries
CREATE INDEX idx_receitas_empresa_data ON receitas(id_empresa, data_receita);
CREATE INDEX idx_receitas_categoria_data ON receitas(id_categoria, data_receita);
CREATE INDEX idx_despesas_empresa_data ON despesas(id_empresa, data_despesa);
CREATE INDEX idx_despesas_categoria_data ON despesas(id_categoria, data_despesa);

-- Índices para análise temporal
CREATE INDEX idx_receitas_ano_mes ON receitas(YEAR(data_receita), MONTH(data_receita));
CREATE INDEX idx_despesas_ano_mes ON despesas(YEAR(data_despesa), MONTH(data_despesa));

-- Índices para análise de clientes/fornecedores
CREATE INDEX idx_receitas_cliente_valor ON receitas(cliente, valor);
CREATE INDEX idx_despesas_fornecedor_valor ON despesas(fornecedor, valor);

-- ========================================
-- CRIAÇÃO DE TRIGGERS PARA AUDITORIA
-- ========================================

DELIMITER //

-- Trigger para auditoria de receitas
CREATE TRIGGER tr_receitas_audit_insert
AFTER INSERT ON receitas
FOR EACH ROW
BEGIN
    INSERT INTO log_transacoes (tabela_afetada, id_registro, tipo_operacao, dados_novos, usuario)
    VALUES ('receitas', NEW.id_receita, 'INSERT', JSON_OBJECT(
        'id_receita', NEW.id_receita,
        'id_empresa', NEW.id_empresa,
        'valor', NEW.valor,
        'data_receita', NEW.data_receita
    ), USER());
END//

-- Trigger para auditoria de despesas
CREATE TRIGGER tr_despesas_audit_insert
AFTER INSERT ON despesas
FOR EACH ROW
BEGIN
    INSERT INTO log_transacoes (tabela_afetada, id_registro, tipo_operacao, dados_novos, usuario)
    VALUES ('despesas', NEW.id_despesa, 'INSERT', JSON_OBJECT(
        'id_despesa', NEW.id_despesa,
        'id_empresa', NEW.id_empresa,
        'valor', NEW.valor,
        'data_despesa', NEW.data_despesa
    ), USER());
END//

DELIMITER ;

-- ========================================
-- INSERÇÃO DE DADOS INICIAIS
-- ========================================

-- Inserir empresa de exemplo
INSERT INTO empresas (nome_empresa, setor, porte) VALUES
('TechCorp Solutions', 'Tecnologia', 'media');

-- Inserir categorias básicas
INSERT INTO categorias (nome_categoria, tipo) VALUES
('Vendas de Software', 'receita'),
('Consultoria', 'receita'),
('Suporte Técnico', 'receita'),
('Salários', 'despesa'),
('Infraestrutura', 'despesa'),
('Marketing', 'despesa'),
('Impostos', 'despesa');

-- ========================================
-- VERIFICAÇÃO DA ESTRUTURA
-- ========================================

-- Verificar tabelas criadas
SELECT 
    TABLE_NAME,
    TABLE_ROWS,
    DATA_LENGTH,
    INDEX_LENGTH
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA = 'kpis_financeiros_avancado'
ORDER BY TABLE_NAME;

-- Verificar relacionamentos
SELECT 
    CONSTRAINT_NAME,
    TABLE_NAME,
    COLUMN_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'kpis_financeiros_avancado'
AND REFERENCED_TABLE_NAME IS NOT NULL;

-- BANCO DE DADOS AVANÇADO CRIADO COM SUCESSO!
-- Sistema pronto para monitoramento de KPIs financeiros
