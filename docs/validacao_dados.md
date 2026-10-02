# Validação dos Dados — Pipeline de Transparência

## 1. Objetivo

Registrar as validações realizadas durante a construção das camadas Raw e Silver do pipeline de dados de viagens e trechos.

Os dados analisados correspondem ao ano de 2025 e foram utilizados para preservar os dados originais, realizar limpeza e preparar informações para análises posteriores.

---

# 2. Tabela VIAGEM

Arquivo:

`2025_Viagem.csv`

Após a limpeza:

* Registros: **341.860**
* Colunas: **22**

## Tipos de dados

* Identificador do processo: `int64`
* Número da Proposta (PCDP): `string`
* Campos textuais: `string`
* Datas de início e fim: `datetime64`
* Valores financeiros: `Float64`

## Valores nulos identificados

| Campo                         |   Nulos |
| ----------------------------- | ------: |
| Justificativa Urgência Viagem |     128 |
| CPF viajante                  |   2.566 |
| Cargo                         | 127.931 |
| Motivo                        |       1 |

Os valores nulos foram preservados. Não foram criados valores artificiais para substituir informações ausentes.

---

# 3. Tabela TRECHO

Arquivo:

`2025_Trecho.csv`

Após a limpeza:

* Registros: **763.349**
* Colunas: **14**

## Tipos de dados

* Identificador do processo: `int64`
* Número da Proposta (PCDP): `string`
* Sequência Trecho: `int64`
* Datas de origem e destino: `datetime64`
* Número de diárias: `Float64`
* Campos textuais: `string`

## Valores nulos identificados

| Campo          |   Nulos |
| -------------- | ------: |
| Origem - UF    |  14.770 |
| Destino - UF   |  14.742 |
| Número Diárias | 763.349 |

O campo `Número Diárias` apresentou 100% de valores nulos.

Os valores não foram substituídos por zero, pois ausência de informação não deve ser interpretada automaticamente como zero.

---

# 4. Relacionamento VIAGEM x TRECHO

Foram utilizadas duas possíveis chaves para validar o relacionamento:

* `Identificador do processo de viagem`
* `Número da Proposta (PCDP)`

## Resultado pelo identificador do processo

* Processos na VIAGEM: **341.860**
* Processos únicos no TRECHO: **290.259**
* Trechos sem processo correspondente: **0**
* Viagens sem nenhum trecho: **51.601**

Resultado:

**Nenhum trecho órfão foi identificado.**

Todas as linhas do TRECHO possuem um processo correspondente na tabela VIAGEM.

---

# 5. Viagens sem TRECHO

Foram identificadas:

**51.601 viagens sem registro correspondente na tabela TRECHO.**

Essas viagens foram mantidas nos dados e não foram excluídas.

## Situação

| Situação      | Quantidade |
| ------------- | ---------: |
| Realizada     |     51.248 |
| Não realizada |        353 |

## Viagem urgente

Todas as 51.601 viagens apresentaram:

`Viagem Urgente = NÃO`

## Período

As viagens sem trecho possuem data inicial entre:

**01/01/2025 e 30/06/2025**

## Órgão superior

A maior concentração foi:

**Ministério da Justiça e Segurança Pública: 50.857 viagens**

Isso representa aproximadamente **98,6%** das viagens sem trecho.

---

# 6. Valores financeiros das viagens sem TRECHO

As 51.601 viagens sem trecho possuem valores financeiros preenchidos.

| Categoria           |             Total |
| ------------------- | ----------------: |
| Valor diárias       | R$ 164.574.739,03 |
| Valor passagens     |  R$ 35.732.919,19 |
| Valor devolução     |   R$ 1.168.315,89 |
| Valor outros gastos |     R$ 219.331,10 |

**Total:** R$ 201.695.305,21

Esses registros não devem ser excluídos de análises financeiras apenas por não possuírem correspondência no arquivo TRECHO.

---

# 7. Análise temporal

Os registros de TRECHO apresentam datas de origem entre:

**01/01/2025 e 05/04/2026**

A maior concentração ocorre entre janeiro e junho de 2025.

| Mês     | Trechos |
| ------- | ------: |
| 2025-01 |  48.487 |
| 2025-02 |  97.239 |
| 2025-03 | 132.269 |
| 2025-04 | 137.890 |
| 2025-05 | 164.865 |
| 2025-06 | 151.434 |
| 2025-07 |  15.438 |
| 2025-08 |   3.645 |
| 2025-09 |   2.946 |
| 2025-10 |   2.943 |
| 2025-11 |   2.110 |
| 2025-12 |   4.039 |

A tabela VIAGEM analisada possui registros de janeiro a junho de 2025.

---

# 8. Quantidade de trechos por viagem

Foram identificados:

* Processos com TRECHO: **290.259**
* Média de trechos por viagem com trecho: **2,63**
* Menor quantidade de trechos: **1**
* Maior quantidade de trechos: **68**

Distribuição inicial:

| Quantidade de trechos | Viagens |
| --------------------: | ------: |
|                     1 |   6.764 |
|                     2 | 214.468 |
|                     3 |  24.532 |
|                     4 |  23.734 |
|                     5 |   8.512 |
|                     6 |   4.728 |
|                     7 |   1.714 |
|                     8 |   1.971 |
|                     9 |     537 |
|                    10 |     515 |

---

# 9. Validação pela chave PCDP

As 51.601 viagens sem TRECHO pelo identificador do processo também foram verificadas utilizando:

`Número da Proposta (PCDP)`

Resultado:

* Viagens sem TRECHO pelo identificador: **51.601**
* Encontradas pelo PCDP: **0**
* Não encontradas pelo PCDP: **51.601**

Portanto, não foi identificada evidência de que a ausência de TRECHO seja causada simplesmente pela utilização de uma chave de relacionamento incorreta.

---

# 10. PCDP no TRECHO

O campo `Número da Proposta (PCDP)` não deve ser tratado como chave única da tabela TRECHO.

Resultados:

* PCDPs únicas no TRECHO: **53.521**
* PCDPs com mais de um trecho: **53.323**

Uma mesma proposta pode possuir vários trechos.

A combinação entre processo e sequência do trecho deve ser considerada na identificação de um trecho individual.

---

# 11. Decisões adotadas

Até o momento:

* Os dados originais não foram alterados.
* Os dados Raw são preservados para rastreabilidade.
* Os dados tratados foram armazenados na camada Silver.
* Registros com valores nulos foram preservados.
* Viagens sem TRECHO não foram excluídas.
* Não foram criados valores artificiais para substituir dados ausentes.
* Nenhum trecho sem processo correspondente foi identificado.
* A relação VIAGEM x TRECHO foi validada por duas chaves.
* As limitações e diferenças de cobertura foram documentadas.

---

# 12. Próxima etapa

A próxima etapa do projeto é construir a camada **Gold**, utilizando os dados validados da Silver.

Possíveis indicadores:

* quantidade total de viagens;
* viagens realizadas;
* viagens não realizadas;
* gastos totais;
* gastos com diárias;
* gastos com passagens;
* devoluções;
* outros gastos;
* viagens por órgão;
* viagens por período;
* destinos;
* quantidade de trechos;
* viagens sem trecho.

As métricas deverão preservar a distinção entre ausência de informação e valor igual a zero.
