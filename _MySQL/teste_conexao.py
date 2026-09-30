from banco import conectar, fechar


def main():

    conexao = conectar()

    print("Banco conectado!")

    fechar(conexao)

    print("Conexão encerrada!")


if __name__ == "__main__":
    main()