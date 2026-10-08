from pathlib import Path

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

from config import POSTGRES_CONFIG


DATA_DIR = Path("silver")


def carregar_viagem(conexao):
    print("Lendo silver/viagem.csv...")

    df = pd.read_csv(
        DATA_DIR / "viagem.csv",
        sep=";",
        encoding="utf-8-sig",
    )

    df = df.rename(
        columns={
            "Identificador do processo de viagem": "id_processo_viagem",
            "Número da Proposta (PCDP)": "pcdp",
            "Situação": "situacao",
            "Viagem Urgente": "viagem_urgente",
            "Justificativa Urgência Viagem": "justificativa_urgencia",
            "Código do órgão superior": "codigo_orgao_superior",
            "Nome do órgão superior": "nome_orgao_superior",
            "Código órgão solicitante": "codigo_orgao_solicitante",
            "Nome órgão solicitante": "nome_orgao_solicitante",
            "CPF viajante": "cpf_viajante",
            "Nome": "nome",
            "Cargo": "cargo",
            "Função": "funcao",
            "Descrição Função": "descricao_funcao",
            "Período - Data de início": "data_inicio",
            "Período - Data de fim": "data_fim",
            "Destinos": "destinos",
            "Motivo": "motivo",
            "Valor diárias": "valor_diarias",
            "Valor passagens": "valor_passagens",
            "Valor devolução": "valor_devolucao",
            "Valor outros gastos": "valor_outros_gastos",
        }
    )

    df["data_inicio"] = pd.to_datetime(
        df["data_inicio"], errors="coerce"
    ).dt.date

    df["data_fim"] = pd.to_datetime(
        df["data_fim"], errors="coerce"
    ).dt.date

    colunas_valores = [
        "valor_diarias",
        "valor_passagens",
        "valor_devolucao",
        "valor_outros_gastos",
    ]

    for coluna in colunas_valores:
        df[coluna] = pd.to_numeric(
            df[coluna], errors="coerce"
        )

    colunas = [
        "id_processo_viagem",
        "pcdp",
        "situacao",
        "viagem_urgente",
        "justificativa_urgencia",
        "codigo_orgao_superior",
        "nome_orgao_superior",
        "codigo_orgao_solicitante",
        "nome_orgao_solicitante",
        "cpf_viajante",
        "nome",
        "cargo",
        "funcao",
        "descricao_funcao",
        "data_inicio",
        "data_fim",
        "destinos",
        "motivo",
        "valor_diarias",
        "valor_passagens",
        "valor_devolucao",
        "valor_outros_gastos",
    ]

    dados = [
        tuple(None if pd.isna(valor) else valor for valor in linha)
        for linha in df[colunas].itertuples(index=False, name=None)
    ]

    sql = """
        INSERT INTO silver.viagem (
            id_processo_viagem,
            pcdp,
            situacao,
            viagem_urgente,
            justificativa_urgencia,
            codigo_orgao_superior,
            nome_orgao_superior,
            codigo_orgao_solicitante,
            nome_orgao_solicitante,
            cpf_viajante,
            nome,
            cargo,
            funcao,
            descricao_funcao,
            data_inicio,
            data_fim,
            destinos,
            motivo,
            valor_diarias,
            valor_passagens,
            valor_devolucao,
            valor_outros_gastos
        )
        VALUES %s
    """

    with conexao.cursor() as cursor:
        execute_values(
            cursor,
            sql,
            dados,
            page_size=5000,
        )

    conexao.commit()

    print(f"VIAGEM carregada: {len(dados):,} registros")


def carregar_trecho(conexao):
    print("Lendo silver/trecho.csv...")

    df = pd.read_csv(
        DATA_DIR / "trecho.csv",
        sep=";",
        encoding="utf-8-sig",
    )

    df = df.rename(
        columns={
            "Identificador do processo de viagem": "id_processo_viagem",
            "Número da Proposta (PCDP)": "pcdp",
            "Sequência Trecho": "sequencia_trecho",
            "Origem - Data": "origem_data",
            "Origem - País": "origem_pais",
            "Origem - UF": "origem_uf",
            "Origem - Cidade": "origem_cidade",
            "Destino - Data": "destino_data",
            "Destino - País": "destino_pais",
            "Destino - UF": "destino_uf",
            "Destino - Cidade": "destino_cidade",
            "Meio de transporte": "meio_transporte",
            "Número Diárias": "numero_diarias",
            "Missao?": "missao",
        }
    )

    df["origem_data"] = pd.to_datetime(
        df["origem_data"], errors="coerce"
    ).dt.date

    df["destino_data"] = pd.to_datetime(
        df["destino_data"], errors="coerce"
    ).dt.date

    df["numero_diarias"] = pd.to_numeric(
        df["numero_diarias"], errors="coerce"
    )

    colunas = [
        "id_processo_viagem",
        "pcdp",
        "sequencia_trecho",
        "origem_data",
        "origem_pais",
        "origem_uf",
        "origem_cidade",
        "destino_data",
        "destino_pais",
        "destino_uf",
        "destino_cidade",
        "meio_transporte",
        "numero_diarias",
        "missao",
    ]

    dados = [
        tuple(None if pd.isna(valor) else valor for valor in linha)
        for linha in df[colunas].itertuples(index=False, name=None)
    ]

    sql = """
        INSERT INTO silver.trecho (
            id_processo_viagem,
            pcdp,
            sequencia_trecho,
            origem_data,
            origem_pais,
            origem_uf,
            origem_cidade,
            destino_data,
            destino_pais,
            destino_uf,
            destino_cidade,
            meio_transporte,
            numero_diarias,
            missao
        )
        VALUES %s
    """

    with conexao.cursor() as cursor:
        execute_values(
            cursor,
            sql,
            dados,
            page_size=5000,
        )

    conexao.commit()

    print(f"TRECHO carregado: {len(dados):,} registros")


def main():
    print("Conectando ao PostgreSQL...")

    conexao = psycopg2.connect(**POSTGRES_CONFIG)

    try:
        carregar_viagem(conexao)
        carregar_trecho(conexao)

        print()
        print("Carga da camada Silver concluída com sucesso!")

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()


if __name__ == "__main__":
    main()
    