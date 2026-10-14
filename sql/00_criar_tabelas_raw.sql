
-- Projeto: Pipeline de Dados de Transparência
-- Camada Raw: armazenamento dos dados originais
-- Todas as colunas são VARCHAR, conforme o enunciado.

CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.viagem (
    identificador_processo_viagem VARCHAR,
    numero_pcdp VARCHAR,
    situacao VARCHAR,
    viagem_urgente VARCHAR,
    justificativa_urgencia VARCHAR,
    codigo_orgao_superior VARCHAR,
    nome_orgao_superior VARCHAR,
    codigo_orgao_solicitante VARCHAR,
    nome_orgao_solicitante VARCHAR,
    cpf_viajante VARCHAR,
    nome VARCHAR,
    cargo VARCHAR,
    funcao VARCHAR,
    descricao_funcao VARCHAR,
    data_inicio VARCHAR,
    data_fim VARCHAR,
    destinos VARCHAR,
    motivo VARCHAR,
    valor_diarias VARCHAR,
    valor_passagens VARCHAR,
    valor_devolucao VARCHAR,
    valor_outros_gastos VARCHAR
);

CREATE TABLE IF NOT EXISTS raw.trecho (
    identificador_processo_viagem VARCHAR,
    numero_pcdp VARCHAR,
    sequencia_trecho VARCHAR,
    origem_data VARCHAR,
    origem_pais VARCHAR,
    origem_uf VARCHAR,
    origem_cidade VARCHAR,
    destino_data VARCHAR,
    destino_pais VARCHAR,
    destino_uf VARCHAR,
    destino_cidade VARCHAR,
    meio_transporte VARCHAR,
    numero_diarias VARCHAR,
    missao VARCHAR
);

CREATE TABLE IF NOT EXISTS raw.pagamento (
    identificador_processo_viagem VARCHAR,
    numero_pcdp VARCHAR,
    codigo_orgao_superior VARCHAR,
    nome_orgao_superior VARCHAR,
    codigo_orgao_pagador VARCHAR,
    nome_orgao_pagador VARCHAR,
    codigo_unidade_gestora_pagadora VARCHAR,
    nome_unidade_gestora_pagadora VARCHAR,
    tipo_pagamento VARCHAR,
    valor VARCHAR
);

CREATE TABLE IF NOT EXISTS raw.passagem (
    identificador_processo_viagem VARCHAR,
    numero_pcdp VARCHAR,
    meio_transporte VARCHAR,
    pais_origem_ida VARCHAR,
    uf_origem_ida VARCHAR,
    cidade_origem_ida VARCHAR,
    pais_destino_ida VARCHAR,
    uf_destino_ida VARCHAR,
    cidade_destino_ida VARCHAR,
    pais_origem_volta VARCHAR,
    uf_origem_volta VARCHAR,
    cidade_origem_volta VARCHAR,
    pais_destino_volta VARCHAR,
    uf_destino_volta VARCHAR,
    cidade_destino_volta VARCHAR,
    valor_passagem VARCHAR,
    taxa_servico VARCHAR,
    data_emissao_compra VARCHAR,
    hora_emissao_compra VARCHAR
);
