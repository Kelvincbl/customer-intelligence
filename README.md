# Customer Intelligence

### Segmentação de Clientes e Sistema de Recomendação de Produtos com Machine Learning

Projeto de Ciência de Dados desenvolvido em Python com o objetivo de analisar o comportamento de consumidores, identificar perfis de clientes e gerar recomendações personalizadas de produtos.

## 1. Objetivos

- Realizar análise exploratória de transações comerciais reais.
- Construir indicadores de Recência, Frequência e Valor Monetário (RFM).
- Identificar segmentos de clientes utilizando K-Means.
- Desenvolver um sistema de recomendação baseado em similaridade de compras.
- Avaliar o desempenho do recomendador utilizando dados futuros.
- Disponibilizar os resultados em uma aplicação web interativa.

## 2. Tecnologias

- Python
- Pandas e NumPy
- Scikit-learn
- SciPy
- Matplotlib e Seaborn
- Plotly
- Streamlit
- Pytest
- Git e GitHub

## 3. Base de Dados

Foi utilizada a base **Online Retail**, disponibilizada pelo UCI Machine Learning Repository.

- Registros originais: 541.909
- Período: dezembro de 2010 a dezembro de 2011
- Clientes identificados após o tratamento: 4.338
- Transações positivas mantidas: 392.692 linhas
- Valor bruto das compras positivas: £8.887.208,89

Fonte: https://archive.ics.uci.edu/dataset/352/online+retail

## 4. Preparação dos Dados

O processamento incluiu identificação de valores ausentes, remoção de duplicatas exatas e seleção de transações com clientes identificados.

Também foram separados cancelamentos e excluídas da base de segmentação transações com quantidade ou preço não positivo.

O arquivo original foi preservado, e os dados tratados foram utilizados nas etapas seguintes.

## 5. Segmentação RFM

Foram construídos três indicadores:

- **Recency:** quantidade de dias desde a última compra.
- **Frequency:** número de notas de compra distintas.
- **Monetary:** soma dos valores das compras positivas.

Aplicaram-se transformação logarítmica (`log1p`) e padronização (`StandardScaler`) antes do treinamento do K-Means.

Foram avaliadas configurações entre 2 e 10 clusters, utilizando inércia e Silhouette Score.

### Resultados

| Segmento | Clientes | Percentual |
|---|---:|---:|
| Alto valor | 699 | 16,11% |
| Inativos ou ocasionais | 1.635 | 37,69% |
| Recentes de baixa frequência | 826 | 19,04% |
| Recorrentes intermediários | 1.178 | 27,16% |

Foi selecionado K=4 por oferecer maior granularidade e perfis comercialmente interpretáveis.

O modelo apresentou Silhouette Score de 0,3322 e ARI médio de 0,9821 na avaliação de estabilidade entre inicializações.

O segmento de alto valor representou aproximadamente 64,5% do valor das compras positivas.

## 6. Sistema de Recomendação

Foi desenvolvido um recomendador baseado em similaridade de cosseno entre produtos, considerando os históricos de compras dos clientes.

O sistema identifica produtos relacionados, recomenda itens personalizados e exclui produtos já comprados pelo cliente.

### Avaliação temporal

Os dados foram divididos cronologicamente, com treinamento anterior a outubro de 2011 e teste a partir de outubro de 2011.

Foram avaliados 1.752 clientes elegíveis.

| Métrica | Recomendador | Popularidade |
|---|---:|---:|
| Precision@5 | 0,0853 | 0,0443 |
| Recall@5 | 0,0277 | 0,0104 |
| HitRate@5 | 0,2842 | 0,1838 |
| Cobertura | 0,2234 | 0,0133 |

O recomendador apresentou uma melhoria relativa de aproximadamente **92,6% em Precision@5**, comparado à estratégia de popularidade.

Os resultados são limitados ao período, catálogo e conjunto de clientes elegíveis utilizados na avaliação.

## 7. Aplicação Web

A aplicação foi desenvolvida com Streamlit e possui três áreas principais:

**Visão Geral:** indicadores e gráficos de distribuição dos clientes.

**Segmentação:** consulta individual dos indicadores RFM e comparação com o perfil típico do segmento.

**Recomendações:** histórico de compras e sugestões personalizadas de produtos.

## 8. Execução Local

Crie e ative um ambiente virtual Python.

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Para executar a aplicação, após disponibilizar os arquivos processados e o modelo treinado nas pastas correspondentes:

```bash
python -m streamlit run app/main.py
```

Para executar os testes:

```bash
python -m pytest tests/ -v
```

Os dados processados podem ser gerados a partir da base original utilizando os scripts disponíveis em `src`.

## 9. Limitações e Trabalhos Futuros

- Considerar devoluções no cálculo dos indicadores monetários.
- Investigar valores extremos e estabilidade dos segmentos em diferentes amostras.
- Avaliar recomendações em diferentes períodos temporais.
- Comparar o recomendador com outras técnicas de filtragem colaborativa.
- Automatizar o processamento de dados e a geração dos modelos.
- Implantar a aplicação em uma plataforma de hospedagem.

## 10. Considerações Finais

O projeto demonstra um fluxo de Ciência de Dados que integra preparação e análise exploratória, aprendizado não supervisionado, sistemas de recomendação, avaliação quantitativa, desenvolvimento web e testes automatizados.

Os resultados representam uma demonstração técnica baseada em dados históricos e não uma avaliação de desempenho em produção.