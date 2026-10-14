
import csv
import io
import psycopg2

from pathlib import Path
from config import POSTGRES_CONFIG

DATA_DIR = Path("data")
LOTE = 20000

ARQUIVOS = [
    (
        "viagem",
        "2025_Viagem.csv",
        [
            "identificador_processo_viagem", "numero_pcdp", "situacao",
            "viagem_urgente", "justificativa_urgencia",
            "codigo_orgao_superior", "nome_orgao_superior",
            "codigo_orgao_solicitante", "nome_orgao_solicitante",
            "cpf_viajante", "nome", "cargo", "funcao",
            "descricao_funcao", "data_inicio", "data_fim",
            "destinos", "motivo", "valor_diarias", "valor_passagens",
            "valor_devolucao", "valor_outros_gastos",
        ],
    ),
    (
        "trecho",
        "2025_Trecho.csv",
        [
            "identificador_processo_viagem", "numero_pcdp",
            "sequencia_trecho", "origem_data", "origem_pais",
            "origem_uf", "origem_cidade", "destino_data",
            "destino_pais", "destino_uf", "destino_cidade",
            "meio_transporte", "numero_diarias", "missao",
        ],
    ),
    (
        "pagamento",
        "2025_Pagamento.csv",
        [
            "identificador_processo_viagem", "numero_pcdp",
            "codigo_orgao_superior", "nome_orgao_superior",
            "codigo_orgao_pagador", "nome_orgao_pagador",
            "codigo_unidade_gestora_pagadora",
            "nome_unidade_gestora_pagadora", "tipo_pagamento", "valor",
        ],
    ),
    (
        "passagem",
        "2025_Passagem.csv",
        [
            "identificador_processo_viagem", "numero_pcdp",
            "meio_transporte", "pais_origem_ida", "uf_origem_ida",
            "cidade_origem_ida", "pais_destino_ida", "uf_destino_ida",
            "cidade_destino_ida", "pais_origem_volta",
            "uf_origem_volta", "cidade_origem_volta",
            "pais_destino_volta", "uf_destino_volta",
            "cidade_destino_volta", "valor_passagem", "taxa_servico",
            "data_emissao_compra", "hora_emissao_compra",
        ],
    ),
]


def carregar_arquivo(cursor, tabela, nome_arquivo, colunas):
    caminho = DATA_DIR / nome_arquivo

    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    total = 0
    comando_copy = (
        f"COPY raw.{tabela} ({', '.join(colunas)}) "
        "FROM STDIN WITH (FORMAT CSV, DELIMITER ';', "
        "QUOTE '\"', NULL '___NULL_MARKER_7f2a___')"
    )

    with caminho.open(
        "r", encoding="latin1", newline=""
    ) as arquivo:
        leitor = csv.reader(arquivo, delimiter=";")

        cabecalho = next(leitor, None)
        if cabecalho is None:
            raise ValueError(f"Arquivo vazio: {nome_arquivo}")

        while True:
            linhas = []
            for _ in range(LOTE):
                try:
                    linha = next(leitor)
                except StopIteration:
                    break

                if len(linha) != len(colunas):
                    raise ValueError(
                        f"{nome_arquivo}: linha com {len(linha)} "
                        f"campos; esperado {len(colunas)}."
                    )
                linhas.append(linha)

            if not linhas:
                break

            buffer = io.StringIO()
            escritor = csv.writer(
                buffer, delimiter=";", quotechar='"',
                lineterminator="\n"
            )
            escritor.writerows(linhas)
            buffer.seek(0)

            cursor.copy_expert(comando_copy, buffer)
            total += len(linhas)
            print(f"  {tabela}: {total:,} linhas carregadas")

    return total


def main():
    conexao = None

    try:
        conexao = psycopg2.connect(**POSTGRES_CONFIG)
        conexao.autocommit = False

        with conexao.cursor() as cursor:
            # Tudo ocorre na mesma transação.
            # Se houver erro, o rollback desfaz também o TRUNCATE.
            cursor.execute("""
                TRUNCATE TABLE
                    raw.viagem,
                    raw.trecho,
                    raw.pagamento,
                    raw.passagem;
            """)

            for tabela, arquivo, colunas in ARQUIVOS:
                print(f"\nCarregando {arquivo}...")
                total = carregar_arquivo(
                    cursor, tabela, arquivo, colunas
                )
                print(f"Concluído: {total:,} linhas em raw.{tabela}")

        conexao.commit()
        print("\nCARGA RAW CONCLUÍDA COM SUCESSO!")

    except Exception as erro:
        if conexao is not None:
            conexao.rollback()
        print("\nERRO NA CARGA RAW. A transação foi desfeita.")
        print(repr(erro))
        raise

    finally:
        if conexao is not None:
            conexao.close()


if __name__ == "__main__":
    main()
