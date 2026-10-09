import csv
import io
from pathlib import Path

import psycopg2
from config import POSTGRES_CONFIG

PASTA_GOLD = Path("gold")
LOTE = 20000


def carregar_csv(cursor, arquivo, tabela, indices_csv, colunas_sql):
    caminho = PASTA_GOLD / arquivo

    if not caminho.is_file():
        raise FileNotFoundError(f"Arquivo nao encontrado: {caminho}")

    total = 0

    with caminho.open("r", encoding="utf-8-sig", newline="") as origem:
        leitor = csv.reader(origem, delimiter=";")
        cabecalho = next(leitor, None)

        if cabecalho is None:
            raise ValueError(f"Arquivo vazio: {arquivo}")

        if max(indices_csv) >= len(cabecalho):
            raise ValueError(
                f"{arquivo}: esperadas pelo menos "
                f"{max(indices_csv) + 1} colunas, encontradas {len(cabecalho)}"
            )

        while True:
            linhas = []

            for _ in range(LOTE):
                linha = next(leitor, None)

                if linha is None:
                    break

                if len(linha) != len(cabecalho):
                    raise ValueError(
                        f"{arquivo}: linha com {len(linha)} colunas; "
                        f"cabecalho com {len(cabecalho)}"
                    )

                linhas.append([linha[i] for i in indices_csv])

            if not linhas:
                break

            buffer = io.StringIO()
            escritor = csv.writer(
                buffer,
                delimiter="\t",
                lineterminator="\n"
            )
            escritor.writerows(linhas)
            buffer.seek(0)

            comando = (
                f"COPY {tabela} ({', '.join(colunas_sql)}) "
                "FROM STDIN WITH "
                "(FORMAT CSV, DELIMITER E'\\t', NULL '')"
            )

            cursor.copy_expert(comando, buffer)
            total += len(linhas)
            print(f"{arquivo}: {total:,} registros carregados")

    return total


def main():
    tabelas = [
        (
            "viagens_resumo.csv",
            "gold.viagens_resumo",
            [i for i in range(25) if i != 4],
            [
                "id_processo_viagem",
                "pcdp",
                "situacao",
                "viagem_urgente",
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
                "quantidade_de_trechos",
                "possui_trecho",
                "gasto_total",
            ],
        ),
        (
            "gastos_por_orgao.csv",
            "gold.gastos_por_orgao",
            list(range(11)),
            [
                "nome_orgao_superior",
                "quantidade_viagens",
                "viagens_com_trecho",
                "quantidade_de_trechos",
                "valor_diarias",
                "valor_passagens",
                "valor_devolucao",
                "valor_outros_gastos",
                "gasto_total",
                "viagens_sem_trecho",
                "percentual_sem_trecho",
            ],
        ),
        (
            "gastos_por_mes.csv",
            "gold.gastos_por_mes",
            [0, 1, 3, 4, 5, 6, 7, 8],
            [
                "ano_mes",
                "quantidade_viagens",
                "quantidade_de_trechos",
                "valor_diarias",
                "valor_passagens",
                "valor_devolucao",
                "valor_outros_gastos",
                "gasto_total",
            ],
        ),
        (
            "destinos.csv",
            "gold.destinos",
            list(range(5)),
            [
                "destino_pais",
                "destino_uf",
                "destino_cidade",
                "quantidade_de_trechos",
                "quantidade_viagens",
            ],
        ),
    ]

    conexao = None

    try:
        conexao = psycopg2.connect(**POSTGRES_CONFIG)

        with conexao:
            with conexao.cursor() as cursor:
                for arquivo, tabela, indices, colunas in tabelas:
                    print(f"\nCarregando {tabela}...")
                    cursor.execute(f"TRUNCATE TABLE {tabela}")

                    quantidade = carregar_csv(
                        cursor,
                        arquivo,
                        tabela,
                        indices,
                        colunas,
                    )

                    print(f"Concluido: {quantidade:,} registros em {tabela}")

        print("\nCARGA GOLD CONCLUIDA COM SUCESSO!")

    except Exception as erro:
        print(f"\nERRO DURANTE A CARGA: {erro}")
        raise

    finally:
        if conexao is not None:
            conexao.close()


if __name__ == "__main__":
    main()
