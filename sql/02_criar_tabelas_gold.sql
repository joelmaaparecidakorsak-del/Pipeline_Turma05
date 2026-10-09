-- ============================================================
-- PROJETO: Pipeline de Dados de Transparência
-- CAMADA: Gold
-- OBJETIVO: Criar tabelas analíticas para consultas e dashboards
-- ============================================================

CREATE SCHEMA IF NOT EXISTS gold;

-- 1. RESUMO DAS VIAGENS
CREATE TABLE IF NOT EXISTS gold.viagens_resumo (
id_processo_viagem BIGINT PRIMARY KEY,
pcdp TEXT,
situacao TEXT,
viagem_urgente TEXT,
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
valor_outros_gastos NUMERIC(15,2),
quantidade_de_trechos BIGINT,
possui_trecho BOOLEAN,
gasto_total NUMERIC(15,2)
);

-- 2. GASTOS POR ÓRGÃO
CREATE TABLE IF NOT EXISTS gold.gastos_por_orgao (
nome_orgao_superior TEXT PRIMARY KEY,
quantidade_viagens BIGINT,
viagens_com_trecho BIGINT,
quantidade_de_trechos BIGINT,
valor_diarias NUMERIC(18,2),
valor_passagens NUMERIC(18,2),
valor_devolucao NUMERIC(18,2),
valor_outros_gastos NUMERIC(18,2),
gasto_total NUMERIC(18,2),
viagens_sem_trecho BIGINT,
percentual_sem_trecho NUMERIC(7,2)
);

-- 3. GASTOS POR MÊS
CREATE TABLE IF NOT EXISTS gold.gastos_por_mes (
ano_mes TEXT PRIMARY KEY,
quantidade_viagens BIGINT,
quantidade_de_trechos BIGINT,
valor_diarias NUMERIC(18,2),
valor_passagens NUMERIC(18,2),
valor_devolucao NUMERIC(18,2),
valor_outros_gastos NUMERIC(18,2),
gasto_total NUMERIC(18,2)
);

-- 4. DESTINOS
CREATE TABLE IF NOT EXISTS gold.destinos (
destino_pais TEXT,
destino_uf TEXT,
destino_cidade TEXT,
quantidade_de_trechos BIGINT,
quantidade_viagens BIGINT
);

CREATE INDEX IF NOT EXISTS idx_gold_viagens_orgao
ON gold.viagens_resumo (nome_orgao_superior);

CREATE INDEX IF NOT EXISTS idx_gold_viagens_data_inicio
ON gold.viagens_resumo (data_inicio);

CREATE INDEX IF NOT EXISTS idx_gold_destinos_cidade
ON gold.destinos (destino_cidade);

-- Conferência das tabelas criadas no schema Gold
SELECT schemaname, tablename
FROM pg_tables
WHERE schemaname = 'gold'
ORDER BY tablename;
