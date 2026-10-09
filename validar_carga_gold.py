import psycopg2
from config import POSTGRES_CONFIG

conexao = psycopg2.connect(**POSTGRES_CONFIG)

try:
    with conexao.cursor() as cursor:
        tabelas = [
            "gold.viagens_resumo",
            "gold.gastos_por_orgao",
            "gold.gastos_por_mes",
            "gold.destinos",
        ]

        print("CONTAGEM DE REGISTROS NO POSTGRESQL")
        for tabela in tabelas:
            cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
            quantidade = cursor.fetchone()[0]
            print(f"{tabela}: {quantidade:,}")

        cursor.execute("""
            SELECT
                SUM(valor_diarias),
                SUM(valor_passagens),
                SUM(valor_devolucao),
                SUM(valor_outros_gastos),
                SUM(gasto_total)
            FROM gold.viagens_resumo
        """)

        resultado = cursor.fetchone()

        print("\nTOTAIS FINANCEIROS")
        nomes = [
            "Valor diarias",
            "Valor passagens",
            "Valor devolucao",
            "Valor outros gastos",
            "Gasto total",
        ]

        for nome, valor in zip(nomes, resultado):
            print(f"{nome}: R$ {valor:,.2f}")

finally:
    conexao.close()
