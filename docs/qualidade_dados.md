# Qualidade e Validação dos Dados

## 1. Objetivo

Este documento registra as principais verificações de qualidade realizadas no pipeline de dados de transparência, com foco na consistência dos relacionamentos entre viagens e trechos e na integridade dos indicadores analíticos.

## 2. Volume de dados

Na validação da camada Silver, foram contabilizados:

| Indicador | Resultado |
|---|---:|
| Registros de viagens | 341.860 |
| Registros de trechos | 763.349 |
| Viagens sem trecho correspondente | 51.601 |
| Trechos sem viagem correspondente | 0 |

## 3. Validação dos relacionamentos

A análise dos relacionamentos entre as bases de viagens e trechos identificou:

- 341.860 identificadores de processo distintos na base de viagens.
- 290.259 identificadores de processo distintos na base de trechos.
- Nenhum trecho sem viagem correspondente, conforme a regra de relacionamento aplicada.
- 51.601 viagens sem trecho correspondente na base analisada.

A ausência de um trecho correspondente não deve ser interpretada automaticamente como erro. Essa situação deve ser considerada na análise e na interpretação dos indicadores.

## 4. Validação da camada Gold

A camada Gold foi comparada com as bases da camada Silver para verificar a consistência dos resultados.

| Verificação | Resultado |
|---|---:|
| Registros de viagens na Silver | 341.860 |
| Registros no resumo Gold | 341.860 |
| Registros de trechos na Silver | 763.349 |
| Trechos considerados na análise de destinos | 763.349 |
| Destinos distintos na Gold | 5.924 |

Também foram conferidos os totais monetários utilizados na construção dos indicadores, incluindo diárias, passagens, devoluções e outros valores.

Os totais devem ser interpretados de acordo com as regras de cálculo e os critérios de agregação adotados em cada tabela.

## 5. Regras e cuidados analíticos

Durante a análise dos dados, foram considerados os seguintes cuidados:

- Padronização de datas e valores monetários.
- Conferência das quantidades de registros entre as camadas.
- Validação de relacionamentos entre viagens e trechos.
- Comparação dos totais de origem com os resultados analíticos.
- Atenção a registros sem correspondência e possíveis diferenças de granularidade.

## 6. Limitações conhecidas

A existência de viagens sem trecho correspondente exige cautela na interpretação de análises que dependam de informações detalhadas dos trechos.

Além disso, indicadores de custos médios, duração e utilização de meios de transporte dependem da disponibilidade, da qualidade e da granularidade dos campos de origem.

Os resultados representam os dados analisados para o período de referência do projeto e não devem ser generalizados automaticamente para outros períodos.

## 7. Conclusão

As validações realizadas permitiram verificar a correspondência das quantidades de registros e a consistência dos principais agregados da camada Gold em relação às fontes Silver.

A documentação dessas verificações contribui para a rastreabilidade, a transparência metodológica e a confiabilidade das análises apresentadas no dashboard.
