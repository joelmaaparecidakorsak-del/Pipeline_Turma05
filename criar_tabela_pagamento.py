
import psycopg2
from config import POSTGRES_CONFIG

sql = """
CREATE SCHEMA IF NOT EXISTS silver;

CREATE TABLE IF NOT EXISTS silver.pagamento (
    id_processo_viagem BIGINT,
    pcdp VARCHAR(30),
    codigo_orgao_superior VARCHAR(20),
    nome_orgao_superior TEXT,
    codigo_orgao_pagador VARCHAR(20),
    nome_orgao_pagador TEXT,
    codigo_unidade_gestora_pagadora VARCHAR(30),
    nome_unidade_gestora_pagadora TEXT,
    tipo_pagamento TEXT,
    valor NUMERIC(15, 2)
);

CREATE INDEX IF NOT EXISTS idx_pagamento_processo
ON silver.pagamento (id_processo_viagem);

CREATE INDEX IF NOT EXISTS idx_pagamento_tipo
ON silver.pagamento (tipo_pagamento);
"""

conexao = psycopg2.connect(**POSTGRES_CONFIG)

try:
    cursor = conexao.cursor()
    cursor.execute(sql)
    conexao.commit()

    print("Tabela silver.pagamento criada com sucesso!")

except Exception as erro:
    conexao.rollback()
    print("Erro ao criar a tabela:")
    print(erro)
    raise

finally:
    conexao.close()
