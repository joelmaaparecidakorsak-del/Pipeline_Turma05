# Arquitetura do Pipeline de Dados

## 1. Objetivo

Este documento descreve a arquitetura do pipeline desenvolvido para tratar, validar, transformar e disponibilizar dados públicos de viagens e gastos governamentais.

A solução utiliza Python para processamento, PostgreSQL para armazenamento e Streamlit para visualização dos indicadores.

## 2. Fluxo de dados

O pipeline está organizado em três camadas:

**Raw → Silver → Gold → Dashboard**

- Raw: dados de origem preservados para rastreabilidade.
- Silver: dados tratados e submetidos a verificações de qualidade.
- Gold: dados organizados para análises e indicadores de negócio.
- Dashboard: apresentação interativa dos resultados consultados no PostgreSQL.

## 3. Camada Raw

A camada Raw representa a entrada dos dados originais no projeto.

Sua finalidade é preservar a referência dos dados recebidos, permitindo rastreabilidade e comparação com as etapas posteriores do processamento.

Os arquivos de origem incluem informações relacionadas a viagens, trechos e pagamentos.

## 4. Camada Silver

A camada Silver concentra as atividades de preparação e validação dos dados.

As principais atividades incluem:

- Leitura de arquivos CSV com tratamento de separadores e codificação.
- Padronização de datas e valores monetários.
- Análise de chaves e relacionamentos entre viagens e trechos.
- Identificação de viagens sem trecho correspondente.
- Documentação das verificações de qualidade.

Na validação realizada, foram identificadas 341.860 viagens e 763.349 trechos. Foram encontradas 51.601 viagens sem trecho correspondente na base analisada.

Esse resultado foi registrado como uma característica dos dados que exige atenção nas análises, e não como evidência automática de erro.

## 5. Camada Gold

A camada Gold transforma os dados tratados em estruturas voltadas à análise de negócio.

Entre os produtos analíticos desenvolvidos estão:

- `gold.viagens_resumo`
- `gold.gastos_por_mes`
- `gold.gastos_por_orgao`
- `gold.destinos`

O resumo de viagens contém 341.860 registros, enquanto a tabela analítica de destinos contempla 5.924 destinos distintos, derivados dos 763.349 trechos.

As tabelas Gold são carregadas no PostgreSQL e utilizadas nas consultas do dashboard.

## 6. Banco de dados

O PostgreSQL armazena as tabelas estruturadas e permite executar consultas SQL para analisar gastos, órgãos, destinos e características das viagens.

Os scripts SQL e Python do projeto organizam a criação e a carga das tabelas.

As credenciais de conexão devem permanecer em configuração local, fora do controle de versão público.

## 7. Dashboard

A aplicação foi desenvolvida com Streamlit e utiliza o PostgreSQL como fonte dos indicadores.

O painel apresenta métricas gerais, gráficos de gastos e análises relacionadas às perguntas de negócio definidas no projeto.

O período de referência do painel é de janeiro a junho de 2025.

## 8. Qualidade e rastreabilidade

A validação inclui comparação das quantidades de registros entre as camadas e conferência de indicadores de gastos e trechos.

Os resultados detalhados estão registrados nos documentos de validação do projeto.

A preservação dos dados de origem e a documentação das regras permitem compreender como os indicadores foram produzidos.

## 9. Possíveis evoluções

Como melhorias futuras, o projeto poderá incorporar execução automatizada, testes de qualidade integrados ao pipeline, monitoramento de cargas e atualização programada dos indicadores.
