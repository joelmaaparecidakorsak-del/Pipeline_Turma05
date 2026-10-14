
from pathlib import Path
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from config import POSTGRES_CONFIG

ARQUIVO = Path("data/2025_Passagem.csv")

MAPA_COLUNAS = {
    "Identificador do processo de viagem": "id_processo_viagem",
    "Número da Proposta (PCDP)": "pcdp",
    "Meio de transporte": "meio_transporte",
    "País - Origem ida": "pais_origem_ida",
    "UF - Origem ida": "uf_origem_ida",
    "Cidade - Origem ida": "cidade_origem_ida",
    "País - Destino ida": "pais_destino_ida",
    "UF - Destino ida": "uf_destino_ida",
    "Cidade - Destino ida": "cidade_destino_ida",
    "País - Origem volta": "pais_origem_volta",
    "UF - Origem volta": "uf_origem_volta",
    "Cidade - Origem volta": "cidade_origem_volta",
    "Pais - Destino volta": "pais_destino_volta",
    "UF - Destino volta": "uf_destino_volta",
    "Cidade - Destino volta": "cidade_destino_volta",
    "Valor da passagem": "valor_passagem",
    "Taxa de serviço": "taxa_servico",
    "Data da emissão/compra": "data_emissao_compra",
    "Hora da emissão/compra": "hora_emissao_compra",
}

COLUNAS = list(MAPA_COLUNAS.values())


def converter_valor(valor):
    if pd.isna(valor) or str(valor).strip() == "":
        return None

    valor = str(valor).strip()

    # Formato brasileiro: 1.234,56
    if "," in valor:
        valor = valor.replace(".", "").replace(",", ".")

    return float(valor)


def carregar():
    print("Lendo arquivo de passagens...")

    df = pd.read_csv(
        ARQUIVO,
        sep=";",
        encoding="latin1",
        dtype=str,
        keep_default_na=False,
    )

    df = df.rename(columns=MAPA_COLUNAS)

    # Preserva a chave como número para relacionar com silver.viagem.
    df["id_processo_viagem"] = (
        df["id_processo_viagem"].str.strip().str.lstrip("0")
    )
    df.loc[df["id_processo_viagem"] == "", "id_processo_viagem"] = "0"
    df["id_processo_viagem"] = pd.to_numeric(
        df["id_processo_viagem"], errors="raise"
    ).astype("int64")

    for coluna in ["valor_passagem", "taxa_servico"]:
        df[coluna] = df[coluna].map(converter_valor)

    df["data_emissao_compra"] = pd.to_datetime(
        df["data_emissao_compra"],
        dayfirst=True,
        errors="coerce",
    ).dt.date

    horarios = pd.to_datetime(
        df["hora_emissao_compra"],
        errors="coerce",
    )
    df["hora_emissao_compra"] = horarios.dt.time

    for coluna in COLUNAS:
        if coluna not in [
            "id_processo_viagem",
            "valor_passagem",
            "taxa_servico",
            "data_emissao_compra",
            "hora_emissao_compra",
        ]:
            df[coluna] = df[coluna].map(
                lambda x: None if str(x).strip() == "" else x
            )

    dados = [
        tuple(None if pd.isna(v) else v for v in linha)
        for linha in df[COLUNAS].itertuples(index=False, name=None)
    ]

    conexao = psycopg2.connect(**POSTGRES_CONFIG)

    try:
        with conexao.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM silver.viagem")
            total_viagem = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(*)
                FROM (
                    SELECT DISTINCT id_processo_viagem
                    FROM silver.viagem
                ) AS v
            """)
            ids_viagem = cursor.fetchone()[0]

            if total_viagem != ids_viagem:
                raise ValueError(
                    "A chave de silver.viagem não é única."
                )

            # A carga é transacional: em caso de erro, nada é confirmado.
            cursor.execute("SAVEPOINT antes_carga_passagem")
            cursor.execute("DELETE FROM silver.passagem")

            sql = """
                INSERT INTO silver.passagem (
                    id_processo_viagem, pcdp, meio_transporte,
                    pais_origem_ida, uf_origem_ida, cidade_origem_ida,
                    pais_destino_ida, uf_destino_ida, cidade_destino_ida,
                    pais_origem_volta, uf_origem_volta, cidade_origem_volta,
                    pais_destino_volta, uf_destino_volta, cidade_destino_volta,
                    valor_passagem, taxa_servico,
                    data_emissao_compra, hora_emissao_compra
                )
                VALUES %s
            """

            execute_values(cursor, sql, dados, page_size=5000)

            cursor.execute("SELECT COUNT(*) FROM silver.passagem")
            total_banco = cursor.fetchone()[0]

            if total_banco != len(df):
                raise ValueError(
                    f"Contagem divergente: CSV={len(df)}, banco={total_banco}"
                )

        conexao.commit()
        print(f"PASSAGEM carregada: {len(df):,} registros")
        print("Carga confirmada com sucesso!")

    except Exception:
        conexao.rollback()
        raise
    finally:
        conexao.close()


if __name__ == "__main__":
    carregar()
