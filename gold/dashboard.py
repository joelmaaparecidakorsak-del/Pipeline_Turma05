import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# Adiciona a pasta principal do projeto ao caminho de importação
PASTA_PROJETO = Path(__file__).resolve().parent.parent
if str(PASTA_PROJETO) not in sys.path:
    sys.path.insert(0, str(PASTA_PROJETO))

from banco import conectar


st.set_page_config(
    page_title="Dashboard de Transparência",
    page_icon="📊",
    layout="wide",
)


def moeda(valor):
    valor = float(valor or 0)
    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def inteiro(valor):
    return f"{int(valor or 0):,}".replace(",", ".")


def consultar(sql):
    """Executa uma consulta e devolve os resultados em um DataFrame."""
    conexao = conectar()
    try:
        with conexao.cursor() as cursor:
            cursor.execute(sql)
            colunas = [item[0] for item in cursor.description]
            registros = cursor.fetchall()
        return pd.DataFrame(registros, columns=colunas)
    finally:
        conexao.close()


def formatar_coluna_moeda(df, colunas):
    """Formata colunas monetárias para exibição, sem alterar os dados originais."""
    resultado = df.copy()
    for coluna in colunas:
        if coluna in resultado.columns:
            resultado[coluna] = resultado[coluna].apply(moeda)
    return resultado


st.title("📊 Dashboard de Transparência")
st.subheader("Análise de gastos com viagens em 2025")
st.caption("Fonte: camadas Gold e Silver — PostgreSQL | janeiro a junho de 2025")

try:
    # =================================================
    # CONSULTAS: todas ficam juntas no início do arquivo
    # =================================================

    indicadores = consultar("""
        SELECT
            COUNT(*) AS total_viagens,
            COALESCE(SUM(gasto_total), 0) AS gastos_totais,
            COUNT(DISTINCT nome_orgao_superior) AS total_orgaos,
            COUNT(*) FILTER (WHERE possui_trecho = FALSE) AS viagens_sem_trecho
        FROM gold.viagens_resumo
    """)

    mensal = consultar("""
        SELECT
            ano_mes,
            quantidade_viagens,
            quantidade_de_trechos,
            valor_diarias,
            valor_passagens,
            valor_devolucao,
            valor_outros_gastos,
            gasto_total
        FROM gold.gastos_por_mes
        ORDER BY ano_mes
    """)

    # Pergunta 1: cinco órgãos superiores com maior custo total
    orgaos_top5 = consultar("""
        SELECT nome_orgao_superior, quantidade_viagens, gasto_total
        FROM gold.gastos_por_orgao
        WHERE nome_orgao_superior IS NOT NULL
        ORDER BY gasto_total DESC
        LIMIT 5
    """)

    # Pergunta 2: três destinos com maior custo médio por viagem
    destinos_media = consultar("""
        SELECT
            destinos,
            COUNT(*) AS quantidade_viagens,
            SUM(gasto_total) AS gasto_total,
            AVG(gasto_total) AS custo_medio
        FROM gold.viagens_resumo
        WHERE destinos IS NOT NULL
          AND TRIM(destinos) <> ''
        GROUP BY destinos
        HAVING COUNT(*) >= 2
        ORDER BY AVG(gasto_total) DESC
        LIMIT 3
    """)

    # Pergunta 3: viagem de maior duração
    viagem_mais_longa = consultar("""
        SELECT
            id_processo_viagem,
            pcdp,
            nome_orgao_superior,
            destinos,
            data_inicio,
            data_fim,
            (data_fim::date - data_inicio::date) AS duracao_dias,
            gasto_total
        FROM gold.viagens_resumo
        WHERE data_inicio IS NOT NULL
          AND data_fim IS NOT NULL
          AND data_fim::date >= data_inicio::date
        ORDER BY (data_fim::date - data_inicio::date) DESC
        LIMIT 1
    """)

    # Pergunta 4: tipo de pagamento com maior valor médio
    pagamentos_tipo = consultar("""
        SELECT
            tipo_pagamento,
            COUNT(*) AS quantidade_pagamentos,
            SUM(valor) AS valor_total,
            AVG(valor) AS valor_medio
        FROM silver.pagamento
        WHERE tipo_pagamento IS NOT NULL
        GROUP BY tipo_pagamento
        ORDER BY AVG(valor) DESC
    """)

    # Pergunta 5: meios de transporte mais usados
    transportes = consultar("""
        SELECT
            meio_transporte,
            COUNT(*) AS quantidade_trechos
        FROM silver.trecho
        WHERE meio_transporte IS NOT NULL
          AND TRIM(meio_transporte) <> ''
        GROUP BY meio_transporte
        ORDER BY quantidade_trechos DESC
        LIMIT 10
    """)

    # Pergunta 6: UFs com mais trechos
    destinos_uf = consultar("""
        SELECT
            destino_uf,
            SUM(quantidade_de_trechos) AS total_trechos,
            SUM(quantidade_viagens) AS soma_viagens
        FROM gold.destinos
        WHERE destino_uf IS NOT NULL
          AND TRIM(destino_uf) <> ''
        GROUP BY destino_uf
        ORDER BY total_trechos DESC
        LIMIT 10
    """)

    # Pergunta 7: órgãos pagadores com maior valor total
    orgaos_pagadores = consultar("""
        SELECT
            nome_orgao_pagador,
            COUNT(*) AS quantidade_pagamentos,
            SUM(valor) AS valor_total,
            AVG(valor) AS valor_medio
        FROM silver.pagamento
        WHERE nome_orgao_pagador IS NOT NULL
          AND TRIM(nome_orgao_pagador) <> ''
        GROUP BY nome_orgao_pagador
        ORDER BY SUM(valor) DESC
        LIMIT 10
    """)

    # =================================================
    # PAINEL GERAL
    # =================================================

    st.success("Conexão com PostgreSQL realizada com sucesso!")
    st.header("Indicadores gerais")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de viagens", inteiro(indicadores.loc[0, "total_viagens"]))
    col2.metric("Gastos totais", moeda(indicadores.loc[0, "gastos_totais"]))
    col3.metric("Órgãos analisados", inteiro(indicadores.loc[0, "total_orgaos"]))

    st.metric(
        "Viagens sem trecho associado",
        inteiro(indicadores.loc[0, "viagens_sem_trecho"]),
    )
    st.divider()

    # =================================================
    # EVOLUÇÃO MENSAL — seção geral, sem número de pergunta
    # =================================================

    st.header("Evolução dos gastos mensais")
    if not mensal.empty:
        mensal_grafico = mensal.copy()
        mensal_grafico["ano_mes"] = mensal_grafico["ano_mes"].astype(str)
        mensal_grafico["gasto_total"] = pd.to_numeric(
            mensal_grafico["gasto_total"], errors="coerce"
        )
        st.bar_chart(
            mensal_grafico,
            x="ano_mes",
            y="gasto_total",
            x_label="Mês",
            y_label="Gastos (R$)",
        )

        tabela_mensal = formatar_coluna_moeda(
            mensal,
            ["gasto_total", "valor_diarias", "valor_passagens",
             "valor_devolucao", "valor_outros_gastos"],
        ).rename(columns={
            "ano_mes": "Mês",
            "quantidade_viagens": "Quantidade de viagens",
            "quantidade_de_trechos": "Quantidade de trechos",
            "valor_diarias": "Diárias",
            "valor_passagens": "Passagens",
            "valor_devolucao": "Devoluções",
            "valor_outros_gastos": "Outros gastos",
            "gasto_total": "Gasto total",
        })
        st.dataframe(tabela_mensal, use_container_width=True, hide_index=True)
    else:
        st.warning("Não foram encontrados dados mensais.")
    st.divider()

    # =================================================
    # PERGUNTA 1
    # =================================================

    st.header("1. Os 5 órgãos com maior custo total")
    if not orgaos_top5.empty:
        grafico_orgaos = orgaos_top5.copy()
        grafico_orgaos["gasto_total"] = pd.to_numeric(
            grafico_orgaos["gasto_total"], errors="coerce"
        )
        st.bar_chart(
            grafico_orgaos.set_index("nome_orgao_superior")["gasto_total"],
            horizontal=True,
            x_label="Gasto total (R$)",
            y_label="Órgão",
        )
        tabela_orgaos = orgaos_top5.rename(columns={
            "nome_orgao_superior": "Órgão",
            "quantidade_viagens": "Quantidade de viagens",
            "gasto_total": "Gasto total",
        }).copy()
        tabela_orgaos["Quantidade de viagens"] = (
            tabela_orgaos["Quantidade de viagens"].apply(inteiro)
        )
        tabela_orgaos["Gasto total"] = tabela_orgaos["Gasto total"].apply(moeda)
        st.dataframe(tabela_orgaos, use_container_width=True, hide_index=True)
    else:
        st.warning("Não foram encontrados dados de gastos por órgão.")
    st.divider()

    # =================================================
    # PERGUNTA 2
    # =================================================

    st.header("2. Os 3 destinos com maior custo médio por viagem")
    if not destinos_media.empty:
        grafico_destinos = destinos_media.copy()
        grafico_destinos["custo_medio"] = pd.to_numeric(
            grafico_destinos["custo_medio"], errors="coerce"
        )
        st.bar_chart(
            grafico_destinos.set_index("destinos")["custo_medio"],
            horizontal=True,
            x_label="Custo médio por viagem (R$)",
            y_label="Destino ou combinação de destinos",
        )
        destinos_exibir = destinos_media.rename(columns={
            "destinos": "Destino ou combinação de destinos",
            "quantidade_viagens": "Quantidade de viagens",
            "custo_medio": "Custo médio por viagem",
            "gasto_total": "Gasto total",
        }).copy()
        destinos_exibir["Custo médio por viagem"] = (
            destinos_exibir["Custo médio por viagem"].apply(moeda)
        )
        destinos_exibir["Gasto total"] = destinos_exibir["Gasto total"].apply(moeda)
        destinos_exibir["Quantidade de viagens"] = (
            destinos_exibir["Quantidade de viagens"].apply(inteiro)
        )
        st.dataframe(destinos_exibir, use_container_width=True, hide_index=True)
        st.caption(
            "A análise agrupa pelo campo de destinos registrado na viagem. "
            "Uma combinação pode conter várias localidades."
        )
    else:
        st.warning("Não há destinos suficientes para calcular o custo médio.")
    st.divider()

    # =================================================
    # PERGUNTA 3
    # =================================================

    st.header("3. A viagem de maior duração e seu custo total")
    if not viagem_mais_longa.empty:
        viagem_exibir = viagem_mais_longa.rename(columns={
            "id_processo_viagem": "Processo da viagem",
            "pcdp": "PCDP",
            "nome_orgao_superior": "Órgão",
            "destinos": "Destino(s)",
            "data_inicio": "Data de início",
            "data_fim": "Data de fim",
            "duracao_dias": "Duração (dias)",
            "gasto_total": "Custo total",
        }).copy()

        st.metric(
            "Duração da viagem (dias)",
            inteiro(viagem_mais_longa.iloc[0]["duracao_dias"]),
        )
        grafico_duracao = viagem_mais_longa.copy()
        grafico_duracao["duracao_dias"] = pd.to_numeric(
            grafico_duracao["duracao_dias"], errors="coerce"
        )
        st.bar_chart(
            grafico_duracao.set_index("pcdp")["duracao_dias"],
            horizontal=True,
            x_label="Duração (dias)",
            y_label="PCDP da viagem",
        )
        viagem_exibir["Custo total"] = viagem_exibir["Custo total"].apply(moeda)
        st.dataframe(viagem_exibir, use_container_width=True, hide_index=True)
    else:
        st.warning("Não foi encontrada uma viagem com datas válidas.")
    st.divider()

    # =================================================
    # PERGUNTA 4
    # =================================================

    st.header("4. Qual tipo de pagamento tem o maior valor médio?")
    if not pagamentos_tipo.empty:
        grafico_pagamentos = pagamentos_tipo.copy()
        grafico_pagamentos["valor_medio"] = pd.to_numeric(
            grafico_pagamentos["valor_medio"], errors="coerce"
        )
        st.bar_chart(
            grafico_pagamentos.set_index("tipo_pagamento")["valor_medio"],
            horizontal=True,
            x_label="Valor médio por pagamento (R$)",
            y_label="Tipo de pagamento",
        )
        tabela_pagamentos = formatar_coluna_moeda(
            pagamentos_tipo, ["valor_total", "valor_medio"]
        ).rename(columns={
            "tipo_pagamento": "Tipo de pagamento",
            "quantidade_pagamentos": "Quantidade de pagamentos",
            "valor_total": "Valor total",
            "valor_medio": "Valor médio por pagamento",
        }).copy()
        tabela_pagamentos["Quantidade de pagamentos"] = (
            tabela_pagamentos["Quantidade de pagamentos"].apply(inteiro)
        )
        st.dataframe(tabela_pagamentos, use_container_width=True, hide_index=True)
        lider_pagamento = pagamentos_tipo.iloc[0]
        st.success(
            f"Maior valor médio: {lider_pagamento['tipo_pagamento']} — "
            f"{moeda(lider_pagamento['valor_medio'])}"
        )
    else:
        st.warning("Não foram encontrados dados de pagamentos.")
    st.divider()

    # =================================================
    # PERGUNTA 5
    # =================================================

    st.header("5. Qual o meio de transporte mais usado nos trechos?")
    if not transportes.empty:
        grafico_transportes = transportes.copy()
        grafico_transportes["quantidade_trechos"] = pd.to_numeric(
            grafico_transportes["quantidade_trechos"], errors="coerce"
        )
        st.bar_chart(
            grafico_transportes.set_index("meio_transporte")["quantidade_trechos"],
            horizontal=True,
            x_label="Quantidade de trechos",
            y_label="Meio de transporte",
        )
        tabela_transportes = transportes.rename(columns={
            "meio_transporte": "Meio de transporte",
            "quantidade_trechos": "Quantidade de trechos",
        })
        st.dataframe(tabela_transportes, use_container_width=True, hide_index=True)
        st.success(
            f"Meio mais utilizado: {transportes.iloc[0]['meio_transporte']} — "
            f"{inteiro(transportes.iloc[0]['quantidade_trechos'])} trechos"
        )
    else:
        st.warning("Não foram encontrados dados de transporte.")
    st.divider()

    # =================================================
    # PERGUNTA 6
    # =================================================

    st.header("6. Qual UF de destino aparece em mais trechos?")
    if not destinos_uf.empty:
        uf_top = destinos_uf.iloc[0]
        col1, col2 = st.columns(2)
        col1.metric("UF com mais trechos", str(uf_top["destino_uf"]))
        col2.metric("Quantidade de trechos", inteiro(uf_top["total_trechos"]))

        st.bar_chart(
            destinos_uf,
            x="destino_uf",
            y="total_trechos",
            x_label="UF",
            y_label="Quantidade de trechos",
        )
        tabela_uf = destinos_uf.rename(columns={
            "destino_uf": "UF",
            "total_trechos": "Quantidade de trechos",
            "soma_viagens": "Soma de viagens por destino",
        }).copy()
        tabela_uf["Quantidade de trechos"] = (
            tabela_uf["Quantidade de trechos"].apply(inteiro)
        )
        tabela_uf["Soma de viagens por destino"] = (
            tabela_uf["Soma de viagens por destino"].apply(inteiro)
        )
        st.dataframe(tabela_uf, use_container_width=True, hide_index=True)
        st.caption(
            "A soma de viagens por destino pode contar a mesma viagem em mais de "
            "uma localidade. A frequência de trechos é a medida principal."
        )
    else:
        st.warning("Não há UFs preenchidas na tabela Gold de destinos.")
    st.divider()

    # =================================================
    # PERGUNTA 7
    # =================================================

    st.header("7. Qual órgão pagou o maior valor total?")
    if not orgaos_pagadores.empty:
        grafico_orgao_pagador = orgaos_pagadores.copy()
        grafico_orgao_pagador["valor_total"] = pd.to_numeric(
            grafico_orgao_pagador["valor_total"], errors="coerce"
        )
        st.bar_chart(
            grafico_orgao_pagador.set_index("nome_orgao_pagador")["valor_total"],
            horizontal=True,
            x_label="Valor total pago (R$)",
            y_label="Órgão pagador",
        )
        tabela_orgao_pagador = formatar_coluna_moeda(
            orgaos_pagadores, ["valor_total", "valor_medio"]
        ).rename(columns={
            "nome_orgao_pagador": "Órgão pagador",
            "quantidade_pagamentos": "Quantidade de pagamentos",
            "valor_total": "Valor total pago",
            "valor_medio": "Valor médio por pagamento",
        }).copy()
        tabela_orgao_pagador["Quantidade de pagamentos"] = (
            tabela_orgao_pagador["Quantidade de pagamentos"].apply(inteiro)
        )
        st.dataframe(
            tabela_orgao_pagador,
            use_container_width=True,
            hide_index=True,
        )
        lider_orgao = orgaos_pagadores.iloc[0]
        st.success(
            f"Maior total pago: {lider_orgao['nome_orgao_pagador']} — "
            f"{moeda(lider_orgao['valor_total'])}"
        )
        st.caption(
            "O ranking soma os pagamentos registrados por órgão pagador. "
            "A categoria Sigiloso é mantida como consta na fonte."
        )
    else:
        st.warning("Não foram encontrados dados por órgão pagador.")

    st.divider()
    st.caption(
        "Fonte: PostgreSQL — camadas Gold e Silver. "
        "Valores apresentados conforme os registros disponíveis no banco."
    )

except Exception as erro:
    st.error("Não foi possível carregar os dados do dashboard.")
    st.exception(erro)
    st.info(
        "Verifique se o PostgreSQL está ativo e se as tabelas necessárias "
        "estão disponíveis no banco transparencia."
    )
