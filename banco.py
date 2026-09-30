import psycopg2

from config import POSTGRES_CONFIG


def conectar():
    try:
        conexao = psycopg2.connect(**POSTGRES_CONFIG)

        print("Conexão com PostgreSQL realizada com sucesso!")

        return conexao

    except Exception as erro:
        raise RuntimeError(
            f"Erro ao conectar ao PostgreSQL: {erro}"
        )


def fechar(conexao):
    if conexao:
        conexao.close()