
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.preprocessing import normalize

BASE = Path(__file__).resolve().parents[1]
ARQUIVO = BASE / "data/processed/transacoes_limpas.csv"

DATA_CORTE = pd.Timestamp("2011-10-01")
TOP_K = 5
MIN_CLIENTES = 5

EXCLUIDOS = {
    "POST", "DOT", "M", "BANK CHARGES",
    "AMAZONFEE", "CRUK", "D", "S",
    "C2", "PADS"
}

print("Carregando transacoes...")

df = pd.read_csv(
    ARQUIVO,
    dtype={"StockCode": str, "CustomerID": "int64"},
    parse_dates=["InvoiceDate"]
)

df = df[
    ~df["StockCode"].isin(EXCLUIDOS)
].copy()

# Separacao cronologica
treino = df[df["InvoiceDate"] < DATA_CORTE]
teste = df[df["InvoiceDate"] >= DATA_CORTE]

treino = treino[
    ["CustomerID", "StockCode"]
].drop_duplicates()

teste = teste[
    ["CustomerID", "StockCode"]
].drop_duplicates()

# Catalogo aprendido apenas no treinamento
popularidade = treino.groupby("StockCode")[
    "CustomerID"
].nunique()

populares = popularidade[
    popularidade >= MIN_CLIENTES
].sort_values(ascending=False)

produtos = pd.Index(populares.index)
treino = treino[treino["StockCode"].isin(produtos)]

clientes = pd.Index(
    sorted(treino["CustomerID"].unique())
)

linhas = clientes.get_indexer(treino["CustomerID"])
colunas = produtos.get_indexer(treino["StockCode"])

matriz = csr_matrix(
    (
        np.ones(len(treino)),
        (linhas, colunas)
    ),
    shape=(len(clientes), len(produtos))
)

itens_norm = normalize(
    matriz, axis=0, norm="l2"
).tocsr()

# Compras futuras que podem ser avaliadas
historico = treino.groupby("CustomerID")[
    "StockCode"
].agg(set)

futuro = teste.groupby("CustomerID")[
    "StockCode"
].agg(set)

clientes_avaliaveis = []
verdades = {}

for cliente in clientes.intersection(futuro.index):
    comprados = historico[cliente]

    # Avaliamos somente produtos novos e
    # conhecidos no catalogo de treinamento
    novos = (futuro[cliente] & set(produtos)) - comprados

    if novos:
        clientes_avaliaveis.append(cliente)
        verdades[cliente] = novos

print("\n--- AVALIACAO TEMPORAL ---")
print("Transacoes distintas de treino:", len(treino))
print("Transacoes distintas de teste:", len(teste))
print("Clientes avaliaveis:", len(clientes_avaliaveis))
print("Produtos no catalogo:", len(produtos))

# Indices dos produtos por ordem de popularidade
ranking_popular = [
    produtos.get_loc(codigo)
    for codigo in populares.index
]

def recomendar_populares(comprados):
    return [
        produtos[i]
        for i in ranking_popular
        if produtos[i] not in comprados
    ][:TOP_K]

def recomendar_modelo(cliente, comprados):
    idx = clientes.get_loc(cliente)
    perfil = matriz[idx].T

    scores = (
        itens_norm.T @ (itens_norm @ perfil)
    ).toarray().ravel()

    indices_comprados = matriz[idx].indices
    scores[indices_comprados] = -np.inf

    # Considerar apenas candidatos com score positivo
    candidatos = np.flatnonzero(
        np.isfinite(scores) & (scores > 0)
    )

    ordem = candidatos[
        np.argsort(-scores[candidatos], kind="stable")
    ]

    return [
        produtos[i] for i in ordem[:TOP_K]
    ]

def calcular_metricas(recomendacoes, verdade):
    acertos = len(set(recomendacoes) & verdade)

    return {
        "Precision@5": acertos / TOP_K,
        "Recall@5": acertos / len(verdade),
        "HitRate@5": int(acertos > 0)
    }

resultados = []
itens_recomendados = {
    "Modelo": set(),
    "Popularidade": set()
}

for cliente in clientes_avaliaveis:
    comprados = historico[cliente]
    verdade = verdades[cliente]

    recomendacao_modelo = recomendar_modelo(
        cliente, comprados
    )

    recomendacao_popular = recomendar_populares(
        comprados
    )

    for nome, recomendacoes in [
        ("Modelo", recomendacao_modelo),
        ("Popularidade", recomendacao_popular)
    ]:
        metricas = calcular_metricas(
            recomendacoes, verdade
        )

        itens_recomendados[nome].update(
            recomendacoes
        )

        resultados.append({
            "Cliente": cliente,
            "Metodo": nome,
            **metricas
        })

resultado = pd.DataFrame(resultados)

resumo = resultado.groupby("Metodo")[
    ["Precision@5", "Recall@5", "HitRate@5"]
].mean()

resumo["Cobertura"] = [
    len(itens_recomendados[nome]) / len(produtos)
    for nome in resumo.index
]

print("\n--- RESULTADOS FINAIS ---")
print(resumo.round(4).to_string())

# Salvar os resultados
PASTA = BASE / "reports"
PASTA.mkdir(exist_ok=True)

resumo.to_csv(
    PASTA / "avaliacao_recomendador.csv"
)

print("\nAvaliacao concluida!")
