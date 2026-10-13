
import streamlit as st
import pandas as pd
import psycopg2
from config import POSTGRES_CONFIG

st.set_page_config(
    page_title="Dashboard de Transparência",
    page_icon="📊",
    layout="wide"
)


def consultar_sql(sql):
    conexao = psycopg2.connect(**POSTGRES_CONFIG)
    try:
        return pd.read_sql_query(sql, conexao)
    finally:
        conexao.close()


def formatar_reais(valor):
    valor = float(valor or 0)
    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def formatar_quantidade(valor):
    return f"{int(valor):,}".replace(",", ".")


st.title("📊 Dashboard de Transparência")
st.caption("Viagens e gastos públicos — janeiro a junho de 2025")

try:
    # =====================================================
    # 1. INDICADORES GERAIS
    # =====================================================
    indicadores = consultar_sql("""
        SELECT
            COUNT(*) AS total_viagens,
            COALESCE(SUM(gasto_total), 0) AS gastos_totais,
            COUNT(DISTINCT nome_orgao_superior) AS total_orgaos,
            COALESCE(SUM(quantidade_de_trechos), 0) AS total_trechos
        FROM gold.viagens_resumo;
    """)

    dados = indicadores.iloc[0]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total de viagens",
        formatar_quantidade(dados["total_viagens"])
    )
    col2.metric(
        "Gastos totais",
        formatar_reais(dados["gastos_totais"])
    )
    col3.metric(
        "Órgãos superiores",
        formatar_quantidade(dados["total_orgaos"])
    )
    col4.metric(
        "Total de trechos",
        formatar_quantidade(dados["total_trechos"])
    )

    st.divider()

    # =====================================================
    # 2. EVOLUÇÃO MENSAL DOS GASTOS
    # =====================================================
    st.subheader("📅 Evolução mensal dos gastos")

    mensal = consultar_sql("""
        SELECT ano_mes, gasto_total
        FROM gold.gastos_por_mes
        ORDER BY ano_mes;
    """)

    st.bar_chart(
        mensal,
        x="ano_mes",
        y="gasto_total",
        x_label="Mês",
        y_label="Gastos (R$)"
    )
    

    # =====================================================
    # 3. CINCO ÓRGÃOS COM MAIOR CUSTO TOTAL
    # =====================================================
    st.divider()
    st.subheader("🏛️ 1. Os 5 órgãos com maior custo total")

    orgaos = consultar_sql("""
        SELECT
            nome_orgao_superior AS orgao,
            quantidade_viagens AS quantidade_viagens,
            gasto_total
        FROM gold.gastos_por_orgao
        ORDER BY gasto_total DESC NULLS LAST
        LIMIT 5;
    """)

    orgaos_exibicao = orgaos.copy()
    orgaos_exibicao["quantidade_viagens"] = (
        orgaos_exibicao["quantidade_viagens"]
        .map(formatar_quantidade)
    )
    orgaos_exibicao["gasto_total"] = (
        orgaos_exibicao["gasto_total"].map(formatar_reais)
    )
    orgaos_exibicao.columns = [
        "Órgão superior",
        "Quantidade de viagens",
        "Custo total"
    ]
    st.write("Tabela: os 5 órgãos com maior custo total")
    st.write(orgaos_exibicao)
    st.dataframe(orgaos_exibicao, hide_index=True, width="stretch")

    # Mantém o gráfico dos 10 órgãos com maiores gastos
    st.subheader("Comparativo dos 10 órgãos com maiores gastos")

    orgaos_grafico = consultar_sql("""
        SELECT
            nome_orgao_superior,
            gasto_total
        FROM gold.gastos_por_orgao
        ORDER BY gasto_total DESC NULLS LAST
        LIMIT 10;
    """)

    st.bar_chart(
        orgaos_grafico,
        x="nome_orgao_superior",
        y="gasto_total",
        x_label="Órgão",
        y_label="Gastos (R$)"
    )

    # =====================================================
    # 4. TRÊS DESTINOS COM MAIOR CUSTO MÉDIO POR VIAGEM
    # =====================================================
    st.divider()
    st.subheader("🌎 2. Os 3 destinos com maior custo médio por viagem")

    destinos_custo = consultar_sql("""
        WITH viagens_destino AS (
            SELECT DISTINCT
                t.destino_cidade,
                t.destino_uf,
                t.id_processo_viagem,
                v.gasto_total
            FROM silver.trecho t
            INNER JOIN gold.viagens_resumo v
                ON t.id_processo_viagem = v.id_processo_viagem
            WHERE t.destino_cidade IS NOT NULL
              AND v.gasto_total IS NOT NULL
        )
        SELECT
            destino_cidade,
            destino_uf,
            COUNT(*) AS quantidade_viagens,
            AVG(gasto_total) AS custo_medio
        FROM viagens_destino
        GROUP BY destino_cidade, destino_uf
        ORDER BY custo_medio DESC NULLS LAST
        LIMIT 3;
    """)

    destinos_exibicao = destinos_custo.copy()
    destinos_exibicao["quantidade_viagens"] = (
        destinos_exibicao["quantidade_viagens"]
        .map(formatar_quantidade)
    )
    destinos_exibicao["custo_medio"] = (
        destinos_exibicao["custo_medio"].map(formatar_reais)
    )
    destinos_exibicao.columns = [
        "Cidade",
        "UF",
        "Quantidade de viagens",
        "Custo médio por viagem"
    ]

    st.dataframe(destinos_exibicao, hide_index=True, width="stretch")

    destinos_grafico = destinos_custo.copy()

    destinos_grafico["destino"] = (
        destinos_grafico["destino_cidade"].fillna("Não informado").astype(str)
        + " - "
        + destinos_grafico["destino_uf"].fillna("UF não informada").astype(str)
    )

    st.bar_chart(
        destinos_grafico,
        x="destino",
        y="custo_medio",
        x_label="Destino",
        y_label="Custo médio por viagem (R$)"
    )

    st.caption(
        "O custo médio considera o gasto total das viagens que passaram "
        "por cada destino. Uma viagem pode visitar mais de um destino; "
        "por isso, esse valor não representa necessariamente o gasto "
        "exclusivo naquele destino."
    )

    # =====================================================
    # 5. VIAGEM DE MAIOR DURAÇÃO E CUSTO TOTAL
    # =====================================================
    st.divider()
    st.subheader("🗓️ 3. Viagem de maior duração e seu custo total")

    viagens_longas = consultar_sql("""
        SELECT
            id_processo_viagem,
            pcdp,
            nome_orgao_superior,
            data_inicio::date AS data_inicio,
            data_fim::date AS data_fim,
            (data_fim::date - data_inicio::date) AS duracao_dias,
            gasto_total,
            CASE
                WHEN data_inicio::date < DATE '2025-01-01'
                  OR data_fim::date > DATE '2025-06-30'
                THEN 'Sim'
                ELSE 'Não'
            END AS fora_periodo
        FROM gold.viagens_resumo
        WHERE data_inicio IS NOT NULL
          AND data_fim IS NOT NULL
          AND data_fim::date >= data_inicio::date
        ORDER BY duracao_dias DESC, gasto_total DESC NULLS LAST
        LIMIT 10;
    """)

    if not viagens_longas.empty:
        maior_viagem = viagens_longas.iloc[0]

        st.metric(
            "Maior duração encontrada",
            f"{int(maior_viagem['duracao_dias'])} dias"
        )

        c1, c2, c3 = st.columns(3)
        c1.write("**Processo da viagem**")
        c1.write(str(maior_viagem["id_processo_viagem"]))

        c2.write("**Data de início**")
        c2.write(str(maior_viagem["data_inicio"]))

        c3.write("**Data de término**")
        c3.write(str(maior_viagem["data_fim"]))

        st.write(
            "**Órgão:**",
            str(maior_viagem["nome_orgao_superior"])
        )
        st.write(
            "**Custo total:**",
            formatar_reais(maior_viagem["gasto_total"])
        )

        if maior_viagem["fora_periodo"] == "Sim":
            st.warning(
                "A viagem mais longa possui datas fora do recorte "
                "de janeiro a junho de 2025. É importante validar "
                "esse registro antes de tirar conclusões."
            )

        longas_exibicao = viagens_longas.copy()
        longas_exibicao["gasto_total"] = (
            longas_exibicao["gasto_total"].map(formatar_reais)
        )
        longas_exibicao.columns = [
            "Processo",
            "PCDP",
            "Órgão",
            "Início",
            "Término",
            "Duração (dias)",
            "Custo total",
            "Fora do período?"
        ]

        st.write("**As 10 viagens de maior duração**")
        st.dataframe(
            longas_exibicao,
            hide_index=True,
            width="stretch"
        )
        
        st.subheader("Comparativo das 10 viagens mais longas")

        st.bar_chart(
            viagens_longas,
            x="id_processo_viagem",
            y="duracao_dias",
            x_label="Processo da viagem",
            y_label="Duração (dias)"
        )

    else:
        st.info("Não foram encontradas viagens com datas válidas.")

    
    # =====================================================
    # 6. TIPO DE PAGAMENTO COM MAIOR VALOR MÉDIO
    # =====================================================
    st.divider()
    st.subheader("💰 4. Qual tipo de pagamento tem o maior valor médio?")

    pagamentos = consultar_sql("""
        SELECT
            tipo_pagamento,
            COUNT(*) AS quantidade_registros,
            COALESCE(SUM(valor), 0) AS valor_total,
            AVG(valor) AS valor_medio
        FROM silver.pagamento
        GROUP BY tipo_pagamento
        ORDER BY valor_medio DESC NULLS LAST;
    """)

    if not pagamentos.empty:
        maior_pagamento = pagamentos.iloc[0]

        c1, c2 = st.columns(2)

        c1.metric(
            "Tipo com maior valor médio",
            str(maior_pagamento["tipo_pagamento"])
        )

        c2.metric(
            "Valor médio por registro",
            formatar_reais(maior_pagamento["valor_medio"])
        )

        pagamentos_exibicao = pagamentos.copy()

        pagamentos_exibicao["quantidade_registros"] = (
            pagamentos_exibicao["quantidade_registros"]
            .map(formatar_quantidade)
        )

        pagamentos_exibicao["valor_total"] = (
            pagamentos_exibicao["valor_total"]
            .map(formatar_reais)
        )

        pagamentos_exibicao["valor_medio"] = (
            pagamentos_exibicao["valor_medio"]
            .map(formatar_reais)
        )

        pagamentos_exibicao.columns = [
            "Tipo de pagamento",
            "Quantidade de registros",
            "Valor total",
            "Valor médio"
        ]

        st.dataframe(
            pagamentos_exibicao,
            hide_index=True,
            width="stretch"
        )

        st.bar_chart(
            pagamentos,
            x="tipo_pagamento",
            y="valor_medio",
            x_label="Tipo de pagamento",
            y_label="Valor médio (R$)"
        )
    else:
        st.info("A tabela silver.pagamento não possui registros.")


    # =====================================================
    # 7. DEZ DESTINOS COM MAIS TRECHOS
    # =====================================================
    st.divider()
    
    # =====================================================
    # 8. MEIO DE TRANSPORTE MAIS UTILIZADO
    # =====================================================
    st.divider()
    st.subheader("🚘 5. Qual o meio de transporte mais usado nos trechos?")

    transportes = consultar_sql("""
        SELECT
            COALESCE(
                NULLIF(TRIM(meio_transporte), ''),
                'Não informado'
            ) AS meio_transporte,
            COUNT(*) AS quantidade_trechos
        FROM silver.trecho
        GROUP BY 1
        ORDER BY quantidade_trechos DESC;
    """)

    if not transportes.empty:
        maior_transporte = transportes.iloc[0]

        st.metric(
            "Meio de transporte mais utilizado",
            str(maior_transporte["meio_transporte"]),
            f"{formatar_quantidade(maior_transporte['quantidade_trechos'])} trechos"
        )

        transportes_exibicao = transportes.copy()
        transportes_exibicao["quantidade_trechos"] = (
            transportes_exibicao["quantidade_trechos"]
            .map(formatar_quantidade)
        )
        transportes_exibicao.columns = [
            "Meio de transporte",
            "Quantidade de trechos"
        ]

        st.dataframe(
            transportes_exibicao,
            hide_index=True,
            width="stretch"
        )

        st.bar_chart(
            transportes,
            x="meio_transporte",
            y="quantidade_trechos",
            x_label="Meio de transporte",
            y_label="Quantidade de trechos"
        )

    # =====================================================
    # 9. UF DE DESTINO COM MAIS TRECHOS
    # =====================================================
    st.divider()
    st.subheader("🗺️ 6. Qual UF de destino aparece em mais trechos?")

    ufs_destino = consultar_sql("""
        SELECT
            COALESCE(
                NULLIF(TRIM(destino_uf), ''),
                'Não informado'
            ) AS uf_destino,
            COUNT(*) AS quantidade_trechos
        FROM silver.trecho
        GROUP BY 1
        ORDER BY quantidade_trechos DESC;
    """)

    if not ufs_destino.empty:
        maior_uf = ufs_destino.iloc[0]

        st.metric(
            "UF de destino com mais trechos",
            str(maior_uf["uf_destino"]),
            f"{formatar_quantidade(maior_uf['quantidade_trechos'])} trechos"
        )

        ufs_exibicao = ufs_destino.copy()
        ufs_exibicao["quantidade_trechos"] = (
            ufs_exibicao["quantidade_trechos"]
            .map(formatar_quantidade)
        )
        ufs_exibicao.columns = [
            "UF de destino",
            "Quantidade de trechos"
        ]

        st.dataframe(
            ufs_exibicao,
            hide_index=True,
            width="stretch"
        )

        st.bar_chart(
            ufs_destino.head(10),
            x="uf_destino",
            y="quantidade_trechos",
            x_label="UF de destino",
            y_label="Quantidade de trechos"
        )

    # =====================================================
    # 10. ÓRGÃO PAGADOR COM MAIOR VALOR TOTAL
    # =====================================================
    st.divider()
    st.subheader("🏢 7. Qual órgão pagou mais no total?")

    orgaos_pagadores = consultar_sql("""
        SELECT
            COALESCE(
                NULLIF(TRIM(nome_orgao_pagador), ''),
                'Não informado'
            ) AS orgao_pagador,
            COUNT(*) AS quantidade_registros,
            COALESCE(SUM(valor), 0) AS valor_total
        FROM silver.pagamento
        GROUP BY 1
        ORDER BY valor_total DESC NULLS LAST
        LIMIT 10;
    """)

    if not orgaos_pagadores.empty:
        maior_orgao_pagador = orgaos_pagadores.iloc[0]

        c1, c2 = st.columns(2)

        c1.metric(
            "Órgão pagador com maior total",
            str(maior_orgao_pagador["orgao_pagador"])
        )

        c2.metric(
            "Valor total pago",
            formatar_reais(maior_orgao_pagador["valor_total"])
        )

        pagadores_exibicao = orgaos_pagadores.copy()

        pagadores_exibicao["quantidade_registros"] = (
            pagadores_exibicao["quantidade_registros"]
            .map(formatar_quantidade)
        )

        pagadores_exibicao["valor_total"] = (
            pagadores_exibicao["valor_total"]
            .map(formatar_reais)
        )

        pagadores_exibicao.columns = [
            "Órgão pagador",
            "Quantidade de registros",
            "Valor total"
        ]

        st.dataframe(
            pagadores_exibicao,
            hide_index=True,
            width="stretch"
        )

        st.bar_chart(
            orgaos_pagadores,
            x="orgao_pagador",
            y="valor_total",
            x_label="Órgão pagador",
            y_label="Valor total (R$)"
        )

    st.subheader("📍 Os 10 destinos com mais trechos")

    destinos = consultar_sql("""
        SELECT
            CONCAT_WS(' - ', destino_cidade, destino_uf) AS destino,
            quantidade_de_trechos
        FROM gold.destinos
        ORDER BY quantidade_de_trechos DESC
        LIMIT 10;
    """)
    
    destinos_exibicao = destinos.copy()

    destinos_exibicao["quantidade_de_trechos"] = (
        destinos_exibicao["quantidade_de_trechos"]
        .map(formatar_quantidade)
    )

    destinos_exibicao.columns = [
        "Destino",
        "Quantidade de trechos"
    ]

    st.dataframe(
        destinos_exibicao,
        hide_index=True,
        width="stretch"
    )


    st.bar_chart(
        destinos,
        x="destino",
        y="quantidade_de_trechos",
        x_label="Destino",
        y_label="Quantidade de trechos"
    )

    st.divider()
    st.caption(
        "Fonte: camada Gold e tabela silver.pagamento do PostgreSQL. "
        "Os gráficos e tabelas consultam os dados diretamente no banco."
    )

except Exception as erro:
    st.error("Não foi possível carregar os dados do PostgreSQL.")
    st.code(str(erro))
    st.info(
        "Confira a conexão no arquivo config.py e se as tabelas "
        "gold e silver.pagamento estão disponíveis no banco transparencia."
    )

