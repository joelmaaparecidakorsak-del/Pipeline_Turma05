import psycopg2

try:
    conexao = psycopg2.connect(
        host="localhost",
        port=5432,
        user="postgres",
        password=123456,
        dbname="transparencia"
    )

    print("CONEXÃO COM POSTGRESQL OK!")

    conexao.close()

except Exception as erro:
    print("ERRO:")
    print(repr(erro))
    