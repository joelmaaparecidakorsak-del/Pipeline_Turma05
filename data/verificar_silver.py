import os
import sys

# Adiciona a pasta principal do projeto ao caminho do Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import psycopg2
from config import POSTGRES_CONFIG


def verificar_tabelas():
    conexao = None

    try:
        conexao = psycopg2.connect(**POSTGRES_CONFIG)
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_name LIKE 'silver_%'
            ORDER BY table_name;
        """)

        tabelas = cursor.fetchall()

        print("\nTABELAS SILVER ENCONTRADAS:\n")

        if not tabelas:
            print("Nenhuma tabela Silver encontrada.")
        else:
            for tabela in tabelas:
                print(tabela[0])

        cursor.close()

    except Exception as erro:
        print(f"Erro na consulta: {erro}")

    finally:
        if conexao:
            conexao.close()


if __name__ == "__main__":
    verificar_tabelas()
    
