
CREATE TABLE IF NOT EXISTS silver.passagem (
    id_processo_viagem BIGINT NOT NULL,
    pcdp TEXT,
    meio_transporte TEXT,
    pais_origem_ida TEXT,
    uf_origem_ida TEXT,
    cidade_origem_ida TEXT,
    pais_destino_ida TEXT,
    uf_destino_ida TEXT,
    cidade_destino_ida TEXT,
    pais_origem_volta TEXT,
    uf_origem_volta TEXT,
    cidade_origem_volta TEXT,
    pais_destino_volta TEXT,
    uf_destino_volta TEXT,
    cidade_destino_volta TEXT,
    valor_passagem NUMERIC(15,2),
    taxa_servico NUMERIC(15,2),
    data_emissao_compra DATE,
    hora_emissao_compra TIME,

    CONSTRAINT passagem_viagem_fk
        FOREIGN KEY (id_processo_viagem)
        REFERENCES silver.viagem (id_processo_viagem),

    CONSTRAINT passagem_valor_check
        CHECK (valor_passagem IS NULL OR valor_passagem >= 0),

    CONSTRAINT passagem_taxa_check
        CHECK (taxa_servico IS NULL OR taxa_servico >= 0)
);
