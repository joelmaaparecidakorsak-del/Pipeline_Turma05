# Documentação da Camada Gold — Pipeline de Transparência

## 1. Objetivo

A camada Gold transforma os dados tratados na camada Silver em tabelas analíticas preparadas para consultas, indicadores, visualizações e dashboards.

O objetivo é facilitar a análise das viagens, dos gastos públicos, dos órgãos responsáveis e dos destinos registrados.

## 2. Fontes de dados

Foram utilizados os seguintes arquivos da camada Silver:

* `silver/viagem.csv`
* `silver/trecho.csv`

Os arquivos foram lidos com separador `;` e codificação UTF-8 com BOM (`utf-8-sig`).

A camada Silver foi preservada, sem alterações durante a construção da Gold.

## 3. Tabelas produzidas

### 3.1. `viagens_resumo.csv`

Contém os registros de viagem acrescidos de indicadores calculados:

* quantidade de trechos;
* indicador de existência de trecho;
* gasto total por viagem.

O gasto total é calculado pela soma de diárias, passagens, devoluções e outros gastos.

### 3.2. `gastos_por_orgao.csv`

Agrega indicadores por nome do órgão superior:

* quantidade de viagens;
* viagens com trecho;
* quantidade de trechos;
* valores de diárias, passagens, devoluções e outros gastos;
* gasto total;
* viagens sem trecho;
* percentual de viagens sem trecho.

### 3.3. `gastos_por_mes.csv`

Agrega indicadores por mês da data de início da viagem, incluindo quantidade de viagens, quantidade de trechos e valores financeiros.

O conjunto analisado contém registros de janeiro a junho de 2025.

### 3.4. `destinos.csv`

Agrega os trechos por país, UF e cidade de destino, com a quantidade de trechos e a quantidade de identificadores de processo distintos.

## 4. Resultados das validações

| Indicador                          | Resultado |
| ---------------------------------- | --------: |
| Registros de VIAGEM na Silver      |   341.860 |
| Registros de viagens na Gold       |   341.860 |
| Registros de TRECHO na Silver      |   763.349 |
| Total de trechos associado na Gold |   763.349 |
| Viagens sem trecho associado       |    51.601 |
| Órgãos agregados                   |        35 |
| Períodos mensais                   |         6 |
| Combinações de destino             |     5.924 |

## 5. Validação financeira

Os totais dos quatro componentes financeiros foram comparados entre Silver e Gold.

| Componente    |             Total |
| ------------- | ----------------: |
| Diárias       | R$ 834.399.579,40 |
| Passagens     | R$ 355.012.672,10 |
| Devoluções    |   R$ 6.307.679,36 |
| Outros gastos |   R$ 5.040.158,99 |

A diferença encontrada entre Silver e Gold foi de R$ 0,00 para cada componente.

A validação do cálculo do gasto total por viagem apresentou diferença máxima de R$ 0,00 em relação à soma dos quatro componentes na Gold.

## 6. Tratamento de viagens sem trecho

Foram preservadas 51.601 viagens sem trecho associado pelo identificador do processo.

Esses registros não foram eliminados da tabela de resumo. A ausência de trecho é representada por quantidade zero e pelo indicador de existência de trecho.

A ausência de trecho registrado não prova, por si só, que a viagem não ocorreu. Ela representa uma condição dos dados que deve ser investigada ou interpretada com cautela.

## 7. Arquivos de código

* `gold/construir_gold.py`: constrói as tabelas analíticas.
* `gold/validar_gold.py`: executa verificações básicas de quantidade de registros, trechos e valores financeiros.

## 8. Limitações e próximos passos

As validações realizadas confirmam as quantidades de registros, os totais de trechos e os valores financeiros comparados.

Ainda devem ser verificadas a qualidade das datas, a consistência dos agrupamentos e a integridade das tabelas agregadas por órgão, mês e destino.

Próximas etapas do projeto:

1. ampliar as validações das tabelas agregadas;
2. preparar a carga da Gold no PostgreSQL;
3. consultar os indicadores por SQL;
4. desenvolver gráficos e dashboards.
