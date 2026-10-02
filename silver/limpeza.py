
import pandas as pd
from pathlib import Path


# CONFIGURAÇÕES

DATA_DIR = Path("data")
SILVER_DIR = Path("silver")


# LEITURA DOS CSVs

def carregar_csv(nome):

    caminho = DATA_DIR / nome

    return pd.read_csv(
        caminho,
        sep=";",
        encoding="latin1"
    )

# LIMPEZA DE NOMES DAS COLUNAS E TEXTOS

def corrigir_colunas(df):

    # Remove espaços
    df.columns = df.columns.str.strip()

    # Corrige problemas comuns de codificação
    mapa_colunas = {
        "PerÃodo - Data de inÃcio": "Período - Data de início",
        "PerÃodo - Data de fim": "Período - Data de fim",
        "Valor diÃ¡rias": "Valor diárias",
        "Valor passagens": "Valor passagens",
        "Valor devoluÃ§Ã£o": "Valor devolução",
        "Valor outros gastos": "Valor outros gastos",
        "NÃºmero DiÃ¡rias": "Número Diárias",
    }

    df = df.rename(columns=mapa_colunas)

    return df


def limpar_textos(df):

    df = corrigir_colunas(df)

    colunas_texto = df.select_dtypes(include=["object", "string"]).columns

    for coluna in colunas_texto:

        df[coluna] = (
            df[coluna]
            .astype("string")
            .str.strip()
        )

    return df

# LIMPEZA DA TABELA VIAGEM

def limpar_viagem(df):

    df = limpar_textos(df)


    # DATAS

    df["Período - Data de início"] = pd.to_datetime(
        df["Período - Data de início"],
        dayfirst=True,
        errors="coerce"
    )

    df["Período - Data de fim"] = pd.to_datetime(
        df["Período - Data de fim"],
        dayfirst=True,
        errors="coerce"
    )

    # VALORES MONETÁRIOS

    colunas_valor = [
        "Valor diárias",
        "Valor passagens",
        "Valor devolução",
        "Valor outros gastos"
    ]

    for coluna in colunas_valor:

        df[coluna] = (
            df[coluna]
            .astype("string")
            .str.strip()
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
        )

        df[coluna] = pd.to_numeric(
            df[coluna],
            errors="coerce"
        )

    return df

# LIMPEZA DA TABELA TRECHO

def limpar_trecho(df):

    df = limpar_textos(df)

    # DATAS

    df["Origem - Data"] = pd.to_datetime(
        df["Origem - Data"],
        dayfirst=True,
        errors="coerce"
    )

    df["Destino - Data"] = pd.to_datetime(
        df["Destino - Data"],
        dayfirst=True,
        errors="coerce"
    )

    # NÚMERO DE DIÁRIAS

    df["Número Diárias"] = pd.to_numeric(
        df["Número Diárias"],
        errors="coerce"
    )

    return df

# VALIDAÇÃO

def validar_dataframe(df, nome):

    print(f"\nValidação: {nome}")

    print(f"Quantidade de registros: {len(df):,}")
    print(f"Quantidade de colunas: {len(df.columns)}")

    print("\nTipos de dados:")

    print(df.dtypes)

    print("\nValores nulos:")

    print(df.isna().sum())

# PRINCIPAL

def main():

    SILVER_DIR.mkdir(exist_ok=True)

    # VIAGEM

    print("=" * 60)
    print("PROCESSANDO VIAGEM")
    print("=" * 60)

    print("\nCarregando Viagem...")

    viagem = carregar_csv("2025_Viagem.csv")

    print(f"Registros originais: {len(viagem):,}")
    print(f"Colunas originais: {len(viagem.columns)}")

    viagem = limpar_viagem(viagem)

    validar_dataframe(
        viagem,
        "VIAGEM"
    )

    caminho_viagem = SILVER_DIR / "viagem.csv"

    viagem.to_csv(
        caminho_viagem,
        sep=";",
        index=False,
        encoding="utf-8-sig"
    )

    print(f"\nArquivo criado: {caminho_viagem}")


    # TRECHO

    print("\n")
    print("=" * 60)
    print("PROCESSANDO TRECHO")
    print("=" * 60)

    print("\nCarregando Trecho...")

    trecho = carregar_csv("2025_Trecho.csv")

    print(f"Registros originais: {len(trecho):,}")
    print(f"Colunas originais: {len(trecho.columns)}")

    trecho = limpar_trecho(trecho)

    validar_dataframe(
        trecho,
        "TRECHO"
    )

    caminho_trecho = SILVER_DIR / "trecho.csv"

    trecho.to_csv(
        caminho_trecho,
        sep=";",
        index=False,
        encoding="utf-8-sig"
    )

    print(f"\nArquivo criado: {caminho_trecho}")

    # FINAL

    print("\n")
    print("=" * 60)
    print("LIMPEZA CONCLUÍDA")
    print("=" * 60)


# EXECUÇÃO

if __name__ == "__main__":
    main()
