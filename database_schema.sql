-- Esquema de Banco de Dados para Dados CNPJ
-- Baseado na estrutura padrão dos dados abertos da Receita Federal

-- Configurações iniciais
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- =====================================================
-- TABELA: empresas
-- Armazena dados principais das empresas
-- =====================================================
CREATE TABLE empresas (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    cnpj VARCHAR(14) NOT NULL UNIQUE,
    razao_social VARCHAR(255),
    nome_fantasia VARCHAR(255),
    data_abertura DATE,
    porte_empresa VARCHAR(2),
    natureza_juridica VARCHAR(4),
    capital_social DECIMAL(15,2),
    ente_federativo VARCHAR(100),
    situacao_cadastral VARCHAR(2),
    data_situacao_cadastral DATE,
    motivo_situacao_cadastral VARCHAR(2),
    nome_cidade_exterior VARCHAR(100),
    pais VARCHAR(3),
    data_inicio_atividade DATE,
    cnae_fiscal VARCHAR(7),
    tipo_logradouro VARCHAR(20),
    logradouro VARCHAR(125),
    numero VARCHAR(6),
    complemento VARCHAR(100),
    bairro VARCHAR(50),
    cep VARCHAR(8),
    uf VARCHAR(2),
    municipio VARCHAR(4),
    ddd_1 VARCHAR(4),
    telefone_1 VARCHAR(8),
    ddd_2 VARCHAR(4),
    telefone_2 VARCHAR(8),
    ddd_fax VARCHAR(4),
    fax VARCHAR(8),
    email VARCHAR(115),
    situacao_especial VARCHAR(23),
    data_situacao_especial DATE,
    pais_origem VARCHAR(3),
    inscricao_municipal VARCHAR(15),
    inscricao_estadual VARCHAR(15),
    data_ultima_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_cnpj (cnpj),
    INDEX idx_razao_social (razao_social),
    INDEX idx_situacao (situacao_cadastral),
    INDEX idx_uf (uf),
    INDEX idx_municipio (municipio),
    INDEX idx_cnae_fiscal (cnae_fiscal)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABELA: estabelecimentos
-- Armazena dados dos estabelecimentos
-- =====================================================
CREATE TABLE estabelecimentos (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    cnpj VARCHAR(14) NOT NULL,
    cnpj_ordem VARCHAR(4) NOT NULL,
    cnpj_dv VARCHAR(2) NOT NULL,
    identificador_matriz_filial VARCHAR(1),
    nome_fantasia VARCHAR(255),
    situacao_cadastral VARCHAR(2),
    data_situacao_cadastral DATE,
    motivo_situacao_cadastral VARCHAR(2),
    nome_cidade_exterior VARCHAR(100),
    pais VARCHAR(3),
    data_inicio_atividade DATE,
    cnae_fiscal VARCHAR(7),
    cnae_fiscal_descricao VARCHAR(255),
    tipo_logradouro VARCHAR(20),
    logradouro VARCHAR(125),
    numero VARCHAR(6),
    complemento VARCHAR(100),
    bairro VARCHAR(50),
    cep VARCHAR(8),
    uf VARCHAR(2),
    municipio VARCHAR(4),
    ddd_1 VARCHAR(4),
    telefone_1 VARCHAR(8),
    ddd_2 VARCHAR(4),
    telefone_2 VARCHAR(8),
    ddd_fax VARCHAR(4),
    fax VARCHAR(8),
    email VARCHAR(115),
    situacao_especial VARCHAR(23),
    data_situacao_especial DATE,
    data_ultima_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_cnpj_completo (cnpj, cnpj_ordem, cnpj_dv),
    INDEX idx_cnpj (cnpj),
    INDEX idx_situacao (situacao_cadastral),
    INDEX idx_uf (uf),
    INDEX idx_municipio (municipio),
    INDEX idx_cnae_fiscal (cnae_fiscal),
    FOREIGN KEY (cnpj) REFERENCES empresas(cnpj) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABELA: socios
-- Armazena dados dos sócios
-- =====================================================
CREATE TABLE socios (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    cnpj VARCHAR(14) NOT NULL,
    identificador_socio VARCHAR(1),
    nome_socio VARCHAR(150),
    cnpj_cpf_socio VARCHAR(14),
    codigo_qualificacao_socio VARCHAR(2),
    percentual_capital_social DECIMAL(5,2),
    data_entrada_sociedade DATE,
    cpf_representante_legal VARCHAR(11),
    nome_representante_legal VARCHAR(150),
    codigo_qualificacao_representante_legal VARCHAR(2),
    faixa_etaria VARCHAR(1),
    data_ultima_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_cnpj (cnpj),
    INDEX idx_cpf_cnpj_socio (cnpj_cpf_socio),
    INDEX idx_nome_socio (nome_socio),
    FOREIGN KEY (cnpj) REFERENCES empresas(cnpj) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABELA: cnaes_secundarios
-- Armazena CNAEs secundários dos estabelecimentos
-- =====================================================
CREATE TABLE cnaes_secundarios (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    cnpj VARCHAR(14) NOT NULL,
    cnpj_ordem VARCHAR(4) NOT NULL,
    cnpj_dv VARCHAR(2) NOT NULL,
    cnae_secundario VARCHAR(7),
    cnae_secundario_descricao VARCHAR(255),
    data_ultima_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_cnpj_completo (cnpj, cnpj_ordem, cnpj_dv),
    INDEX idx_cnae_secundario (cnae_secundario),
    FOREIGN KEY (cnpj, cnpj_ordem, cnpj_dv) REFERENCES estabelecimentos(cnpj, cnpj_ordem, cnpj_dv) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABELA: qualificacoes_socios
-- Tabela de domínio para qualificações de sócios
-- =====================================================
CREATE TABLE qualificacoes_socios (
    codigo VARCHAR(2) PRIMARY KEY,
    descricao VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABELA: naturezas_juridicas
-- Tabela de domínio para naturezas jurídicas
-- =====================================================
CREATE TABLE naturezas_juridicas (
    codigo VARCHAR(4) PRIMARY KEY,
    descricao VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABELA: cnaes
-- Tabela de domínio para CNAEs
-- =====================================================
CREATE TABLE cnaes (
    codigo VARCHAR(7) PRIMARY KEY,
    descricao VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABELA: municipios
-- Tabela de domínio para municípios
-- =====================================================
CREATE TABLE municipios (
    codigo VARCHAR(4) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    uf VARCHAR(2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_uf (uf)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABELA: paises
-- Tabela de domínio para países
-- =====================================================
CREATE TABLE paises (
    codigo VARCHAR(3) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABELA: importacoes
-- Controle de importações realizadas
-- =====================================================
CREATE TABLE importacoes (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    arquivo VARCHAR(255) NOT NULL,
    data_importacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    registros_processados INT DEFAULT 0,
    registros_importados INT DEFAULT 0,
    registros_com_erro INT DEFAULT 0,
    status ENUM('em_andamento', 'concluida', 'erro') DEFAULT 'em_andamento',
    mensagem_erro TEXT,
    tempo_processamento_seconds INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_arquivo (arquivo),
    INDEX idx_data_importacao (data_importacao),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABELA: logs_importacao
-- Logs detalhados de importação
-- =====================================================
CREATE TABLE logs_importacao (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    importacao_id BIGINT,
    linha_arquivo INT,
    cnpj VARCHAR(14),
    tipo_registro VARCHAR(50),
    mensagem TEXT,
    nivel ENUM('INFO', 'WARNING', 'ERROR') DEFAULT 'INFO',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_importacao_id (importacao_id),
    INDEX idx_cnpj (cnpj),
    INDEX idx_nivel (nivel),
    FOREIGN KEY (importacao_id) REFERENCES importacoes(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- ÍNDICES ADICIONAIS PARA PERFORMANCE
-- =====================================================

-- Índices compostos para consultas comuns
CREATE INDEX idx_empresa_situacao_uf ON empresas(situacao_cadastral, uf);
CREATE INDEX idx_estabelecimento_situacao_uf ON estabelecimentos(situacao_cadastral, uf);
CREATE INDEX idx_empresa_cnae_situacao ON empresas(cnae_fiscal, situacao_cadastral);
CREATE INDEX idx_estabelecimento_cnae_situacao ON estabelecimentos(cnae_fiscal, situacao_cadastral);

-- Índices para consultas por data
CREATE INDEX idx_empresa_data_abertura ON empresas(data_abertura);
CREATE INDEX idx_estabelecimento_data_inicio ON estabelecimentos(data_inicio_atividade);
CREATE INDEX idx_socio_data_entrada ON socios(data_entrada_sociedade);

-- Índices para consultas de texto
CREATE FULLTEXT INDEX idx_empresa_razao_social ON empresas(razao_social);
CREATE FULLTEXT INDEX idx_estabelecimento_nome_fantasia ON estabelecimentos(nome_fantasia);
CREATE FULLTEXT INDEX idx_socio_nome ON socios(nome_socio);

-- =====================================================
-- VIEWS PARA CONSULTAS COMUNS
-- =====================================================

-- View para empresas ativas
CREATE VIEW vw_empresas_ativas AS
SELECT 
    e.*,
    COUNT(est.id) as total_estabelecimentos,
    COUNT(CASE WHEN est.situacao_cadastral = '02' THEN 1 END) as estabelecimentos_ativos
FROM empresas e
LEFT JOIN estabelecimentos est ON e.cnpj = est.cnpj
WHERE e.situacao_cadastral = '02'
GROUP BY e.cnpj;

-- View para estabelecimentos com dados completos
CREATE VIEW vw_estabelecimentos_completos AS
SELECT 
    est.*,
    e.razao_social,
    e.natureza_juridica,
    e.porte_empresa,
    c.descricao as cnae_descricao,
    m.nome as municipio_nome,
    m.uf as uf_nome
FROM estabelecimentos est
JOIN empresas e ON est.cnpj = e.cnpj
LEFT JOIN cnaes c ON est.cnae_fiscal = c.codigo
LEFT JOIN municipios m ON est.municipio = m.codigo;

-- View para estatísticas por UF
CREATE VIEW vw_estatisticas_uf AS
SELECT 
    e.uf,
    COUNT(DISTINCT e.cnpj) as total_empresas,
    COUNT(DISTINCT est.id) as total_estabelecimentos,
    COUNT(CASE WHEN e.situacao_cadastral = '02' THEN 1 END) as empresas_ativas,
    COUNT(CASE WHEN est.situacao_cadastral = '02' THEN 1 END) as estabelecimentos_ativos
FROM empresas e
LEFT JOIN estabelecimentos est ON e.cnpj = est.cnpj
GROUP BY e.uf;

-- =====================================================
-- PROCEDURES PARA MANUTENÇÃO
-- =====================================================

DELIMITER //

-- Procedure para limpar dados antigos
CREATE PROCEDURE sp_limpar_dados_antigos(IN dias INT)
BEGIN
    DECLARE data_limite DATE;
    SET data_limite = DATE_SUB(CURDATE(), INTERVAL dias DAY);
    
    DELETE FROM logs_importacao WHERE created_at < data_limite;
    DELETE FROM importacoes WHERE created_at < data_limite;
    
    SELECT ROW_COUNT() as registros_removidos;
END //

-- Procedure para estatísticas do banco
CREATE PROCEDURE sp_estatisticas_banco()
BEGIN
    SELECT 
        'empresas' as tabela,
        COUNT(*) as total_registros,
        COUNT(CASE WHEN situacao_cadastral = '02' THEN 1 END) as ativos
    FROM empresas
    UNION ALL
    SELECT 
        'estabelecimentos' as tabela,
        COUNT(*) as total_registros,
        COUNT(CASE WHEN situacao_cadastral = '02' THEN 1 END) as ativos
    FROM estabelecimentos
    UNION ALL
    SELECT 
        'socios' as tabela,
        COUNT(*) as total_registros,
        COUNT(*) as ativos
    FROM socios;
END //

DELIMITER ;

-- =====================================================
-- TRIGGERS PARA AUDITORIA
-- =====================================================

-- Trigger para auditoria de empresas
CREATE TABLE empresas_audit (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    cnpj VARCHAR(14) NOT NULL,
    acao ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    dados_anteriores JSON,
    dados_novos JSON,
    usuario VARCHAR(100),
    data_auditoria TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_cnpj (cnpj),
    INDEX idx_acao (acao),
    INDEX idx_data_auditoria (data_auditoria)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DELIMITER //

CREATE TRIGGER tr_empresas_audit_insert
AFTER INSERT ON empresas
FOR EACH ROW
BEGIN
    INSERT INTO empresas_audit (cnpj, acao, dados_novos)
    VALUES (NEW.cnpj, 'INSERT', JSON_OBJECT(
        'razao_social', NEW.razao_social,
        'situacao_cadastral', NEW.situacao_cadastral,
        'uf', NEW.uf
    ));
END //

CREATE TRIGGER tr_empresas_audit_update
AFTER UPDATE ON empresas
FOR EACH ROW
BEGIN
    INSERT INTO empresas_audit (cnpj, acao, dados_anteriores, dados_novos)
    VALUES (NEW.cnpj, 'UPDATE', 
        JSON_OBJECT(
            'razao_social', OLD.razao_social,
            'situacao_cadastral', OLD.situacao_cadastral,
            'uf', OLD.uf
        ),
        JSON_OBJECT(
            'razao_social', NEW.razao_social,
            'situacao_cadastral', NEW.situacao_cadastral,
            'uf', NEW.uf
        )
    );
END //

DELIMITER ;

-- =====================================================
-- CONFIGURAÇÕES FINAIS
-- =====================================================

SET FOREIGN_KEY_CHECKS = 1;

-- Comentários sobre as tabelas
ALTER TABLE empresas COMMENT = 'Dados principais das empresas do CNPJ';
ALTER TABLE estabelecimentos COMMENT = 'Estabelecimentos das empresas';
ALTER TABLE socios COMMENT = 'Sócios das empresas';
ALTER TABLE cnaes_secundarios COMMENT = 'CNAEs secundários dos estabelecimentos';
ALTER TABLE importacoes COMMENT = 'Controle de importações de arquivos';
ALTER TABLE logs_importacao COMMENT = 'Logs detalhados de importação'; 