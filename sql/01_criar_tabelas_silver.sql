-- ============================================================
-- PROJETO: Pipeline de Dados de Transparência
-- CAMADA: Silver
-- OBJETIVO: Criar tabelas tratadas no PostgreSQL
-- ============================================================


-- ============================================================
-- 1. CRIAR SCHEMA SILVER
-- ============================================================

CREATE SCHEMA IF NOT EXISTS silver;


-- ============================================================
-- 2. TABELA VIAGEM
-- ============================================================

CREATE TABLE IF NOT EXISTS silver.viagem (

    id_processo_viagem BIGINT PRIMARY KEY,

    pcdp TEXT,

    situacao TEXT,

    viagem_urgente TEXT,

    justificativa_urgencia TEXT,

    codigo_orgao_superior BIGINT,

    nome_orgao_superior TEXT,

    codigo_orgao_solicitante BIGINT,

    nome_orgao_solicitante TEXT,

    cpf_viajante TEXT,

    nome TEXT,

    cargo TEXT,

    funcao TEXT,

    descricao_funcao TEXT,

    data_inicio DATE,

    data_fim DATE,

    destinos TEXT,

    motivo TEXT,

    valor_diarias NUMERIC(15,2),

    valor_passagens NUMERIC(15,2),

    valor_devolucao NUMERIC(15,2),

    valor_outros_gastos NUMERIC(15,2)

);


-- ============================================================
-- 3. TABELA TRECHO
-- ============================================================

CREATE TABLE IF NOT EXISTS silver.trecho (

    id_processo_viagem BIGINT,

    pcdp TEXT,

    sequencia_trecho INTEGER,

    origem_data DATE,

    origem_pais TEXT,

    origem_uf TEXT,

    origem_cidade TEXT,

    destino_data DATE,

    destino_pais TEXT,

    destino_uf TEXT,

    destino_cidade TEXT,

    meio_transporte TEXT,

    numero_diarias NUMERIC(10,2),

    missao TEXT

);


-- ============================================================
-- 4. ÍNDICES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_trecho_id_processo
ON silver.trecho (id_processo_viagem);

CREATE INDEX IF NOT EXISTS idx_trecho_pcdp
ON silver.trecho (pcdp);

CREATE INDEX IF NOT EXISTS idx_viagem_pcdp
ON silver.viagem (pcdp);


-- ============================================================
-- FIM
-- ============================================================
SELECT schemaname, tablename
FROM pg_tables
WHERE schemaname = 'silver'
ORDER BY tablename;