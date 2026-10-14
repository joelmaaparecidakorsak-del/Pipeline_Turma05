# Pipeline de Dados de Transparência Pública

## Visão geral

Projeto de engenharia e análise de dados desenvolvido para transformar dados públicos de viagens e gastos governamentais em informações estruturadas, validadas e úteis para análise.

O pipeline organiza os dados em camadas Raw, Silver e Gold, utiliza PostgreSQL para armazenamento e disponibiliza indicadores por meio de um dashboard interativo desenvolvido com Streamlit.

**Objetivo:** demonstrar, na prática, a construção de um pipeline de dados, a aplicação de regras de qualidade, a modelagem analítica e a disponibilização de informações para apoiar a tomada de decisão.

## Problema de negócio

Dados públicos podem apresentar grande volume, diferentes estruturas e dificuldades de interpretação. O projeto busca facilitar a análise das viagens governamentais e dos respectivos gastos, permitindo investigar custos, órgãos responsáveis, destinos e características das viagens.

## Arquitetura do projeto

O pipeline está organizado em três camadas:

- **Raw:** preservação dos dados de origem para rastreabilidade e auditoria.
- **Silver:** limpeza, padronização, tratamento de tipos de dados e validações de relacionamentos entre viagens e trechos.
- **Gold:** construção de tabelas analíticas e indicadores agregados para consultas e visualizações.

O PostgreSQL armazena as tabelas estruturadas, e o Streamlit apresenta os resultados em um dashboard interativo.

## Tecnologias utilizadas

- Python — processamento e transformação de dados.
- Pandas — manipulação, limpeza e análise de dados.
- PostgreSQL — armazenamento e consultas SQL.
- SQL — criação de tabelas e análise de indicadores.
- Streamlit — desenvolvimento do dashboard.
- Git e GitHub — versionamento e organização do código.

## Principais entregas

- Pipeline organizado em camadas de dados.
- Tratamento e validação de dados de viagens e trechos.
- Construção da camada Gold com indicadores analíticos.
- Carga das tabelas Gold no PostgreSQL.
- Dashboard interativo para exploração dos indicadores.
- Documentação dos processos e das validações realizadas.

## Perguntas de negócio

O projeto foi desenvolvido para responder às seguintes questões:

1. Quais são os cinco órgãos com maior custo total?
2. Quais são os três destinos com maior custo médio por viagem?
3. Qual foi a viagem de maior duração e qual foi seu custo total?
4. Qual tipo de pagamento apresenta o maior valor médio?
5. Qual meio de transporte é mais utilizado nos trechos?
6. Qual unidade federativa de destino concentra o maior número de trechos?
7. Qual órgão apresenta o maior gasto total?

## Resultados e validações

Na validação da camada Silver, foram identificados:

- 341.860 registros de viagens.
- 763.349 registros de trechos.
- 51.601 viagens sem trecho correspondente na base analisada.
- Nenhum trecho sem viagem correspondente, segundo as regras de relacionamento aplicadas.

Na camada Gold, o resumo preservou os 341.860 registros de viagens, e a agregação de destinos contemplou os 763.349 trechos.

Esses resultados documentam a cobertura das bases e ajudam a avaliar a consistência dos dados antes de sua utilização analítica.

## Dashboard

O dashboard foi desenvolvido com Streamlit e conectado ao PostgreSQL. Ele apresenta indicadores gerais, evolução mensal dos gastos, órgãos com maiores despesas, destinos mais frequentes e análises relacionadas às perguntas de negócio.

**Período de referência:** janeiro a junho de 2025.

> Adicione aqui uma captura de tela do dashboard para facilitar a visualização do resultado final.

## Estrutura do projeto

A organização principal inclui:

- `silver/` — scripts de tratamento e validação.
- `gold/` — construção de indicadores, validação e arquivos analíticos.
- `sql/` — scripts SQL para criação das tabelas.
- `docs/` — documentação e relatórios de validação.
- `dashboard.py` — aplicação do dashboard na raiz do projeto.
- `carregar_silver_postgres.py` — carga da camada Silver no PostgreSQL.
- `carregar_gold_postgres.py` — carga da camada Gold no PostgreSQL.

Consulte a estrutura atual do repositório para confirmar os caminhos e arquivos antes da publicação.

## Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/joelmaaparecidakorsak-del/Pipeline_Turma05.git
cd Pipeline_Turma05
```

### 2. Criar e ativar o ambiente virtual

No Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate.bat
```

### 3. Instalar as dependências

Após disponibilizar o arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Configurar o PostgreSQL

Crie e configure o banco de dados conforme os scripts SQL do projeto. Defina as credenciais por meio das configurações locais e do arquivo `.env`, conforme a implementação existente.

**Importante:** nunca publique senhas, credenciais ou arquivos `.env` no GitHub.

### 5. Executar o dashboard

Na estrutura atual, execute:

```bash
python -m streamlit run gold/dashboard.py
```

O Streamlit informará o endereço local para acessar a aplicação.

As tabelas necessárias devem estar previamente carregadas no PostgreSQL.

## Qualidade dos dados

A validação inclui conferência da quantidade de registros, análise de relacionamentos entre viagens e trechos e comparação dos indicadores da camada Gold com as respectivas fontes da camada Silver.

Os resultados detalhados estão documentados nos arquivos de validação do projeto.

## Aprendizados e competências demonstradas

Este projeto reúne competências práticas de engenharia e análise de dados:

- Construção de um pipeline de transformação de dados.
- Tratamento de grandes arquivos CSV.
- Implementação de regras de qualidade e rastreabilidade.
- Modelagem e armazenamento analítico em PostgreSQL.
- Consultas SQL para responder a perguntas de negócio.
- Desenvolvimento de dashboard interativo.
- Versionamento de código com Git e GitHub.

## Próximas melhorias

- Automatizar a execução do pipeline.
- Criar testes automatizados de qualidade de dados.
- Ampliar os indicadores e filtros do dashboard.
- Documentar as métricas e suas regras de cálculo.
- Avaliar a publicação do dashboard em um ambiente acessível externamente.

## Autoria

Projeto desenvolvido como iniciativa prática de engenharia e análise de dados, com foco na transformação de dados públicos em informações úteis para transparência e tomada de decisão.
