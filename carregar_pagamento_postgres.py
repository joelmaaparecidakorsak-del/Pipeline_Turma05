
from pathlib import Path

import pandas as pd
import psycopg2
from config import POSTGRES_CONFIG

ARQUIVO = Path("data/2025_Pagamento.csv")
LOTE = 20000

COLUNAS_ORIGINAIS = [
    "Identificador do processo de viagem",
    "Número da Proposta (PCDP)",
    "Código do órgão superior",
    "Nome do órgão superior",
    "Codigo do órgão pagador",
    "Nome do órgao pagador",
    "Código da unidade gestora pagadora",
    "Nome da unidade gestora pagadora",
    "Tipo de pagamento",
    "Valor",
]

COLUNAS_BANCO = [
    "id_processo_viagem",
    "pcdp",
    "codigo_orgao_superior",
    "nome_orgao_superior",
    "codigo_orgao_pagador",
    "nome_orgao_pagador",
    "codigo_unidade_gestora_pagadora",
    "nome_unidade_gestora_pagadora",
    "tipo_pagamento",
    "valor",
]

SQL_INSERT = """
INSERT INTO silver.pagamento (
    id_processo_viagem,
    pcdp,
    codigo_orgao_superior,
    nome_orgao_superior,
    codigo_orgao_pagador,
    nome_orgao_pagador,
    codigo_unidade_gestora_pagadora,
    nome_unidade_gestora_pagadora,
    tipo_pagamento,
    valor
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

if not ARQUIVO.exists():
    raise FileNotFoundError(f"Arquivo não encontrado: {ARQUIVO}")

conexao = psycopg2.connect(**POSTGRES_CONFIG)

try:
    cursor = conexao.cursor()

    # Limpa somente a tabela de pagamentos antes da carga.
    cursor.execute("TRUNCATE TABLE silver.pagamento")
    conexao.commit()

    total = 0

    leitor = pd.read_csv(
        ARQUIVO,
        sep=";",
        encoding="latin1",
        dtype=str,
        chunksize=LOTE,
    )

    for lote in leitor:
        lote.columns = lote.columns.str.strip()

        faltantes = set(COLUNAS_ORIGINAIS) - set(lote.columns)
        if faltantes:
            raise ValueError(
                f"Colunas não encontradas: {sorted(faltantes)}"
            )

        lote = lote[COLUNAS_ORIGINAIS].copy()
        lote.columns = COLUNAS_BANCO

        valor = (
            lote["valor"]
            .str.strip()
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
        )
        lote["valor"] = pd.to_numeric(valor, errors="coerce")

        lote["id_processo_viagem"] = pd.to_numeric(
            lote["id_processo_viagem"],
            errors="coerce",
        )

        lote = lote.astype(object).where(pd.notna(lote), None)

        registros = list(lote.itertuples(index=False, name=None))
        cursor.executemany(SQL_INSERT, registros)
        conexao.commit()

        total += len(registros)
        print(f"Registros carregados: {total:,}".replace(",", "."))

    print(f"\nCarga concluída! Total: {total:,}".replace(",", "."))

except Exception:
    conexao.rollback()
    raise

finally:
    conexao.close()
