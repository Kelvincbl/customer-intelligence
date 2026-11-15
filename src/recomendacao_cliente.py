
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.preprocessing import normalize

# 1. Carregar os dados
BASE_DIR = Path(__file__).resolve().parents[1]

arquivo = (
    BASE_DIR / "data" / "processed"
    / "transacoes_limpas.csv"
)

df = pd.read_csv(
    arquivo,
    dtype={"StockCode": str, "CustomerID": "int64"}
)

# 2. Remover registros administrativos conhecidos
excluidos = {
    "POST", "DOT", "M", "BANK CHARGES",
    "AMAZONFEE", "CRUK", "D", "S",
    "C2", "PADS"
}

df = df[
    ~df["StockCode"].isin(excluidos)
].dropna(subset=["Description"]).copy()

# 3. Criar pares unicos cliente-produto
compras = df[
    ["CustomerID", "StockCode"]
].drop_duplicates()

# Manter produtos comprados por pelo menos 5 clientes
frequencia = compras.groupby("StockCode")[
    "CustomerID"
].nunique()

validos = frequencia[frequencia >= 5].index

compras = compras[
    compras["StockCode"].isin(validos)
].copy()

# 4. Criar matriz esparsa cliente-produto
clientes = pd.Index(
    sorted(compras["CustomerID"].unique())
)

produtos = pd.Index(
    sorted(compras["StockCode"].unique())
)

linhas = clientes.get_indexer(
    compras["CustomerID"]
)

colunas = produtos.get_indexer(
    compras["StockCode"]
)

matriz = csr_matrix(
    (
        np.ones(len(compras)),
        (linhas, colunas)
    ),
    shape=(len(clientes), len(produtos))
)

# Normalizar vetores de produtos
itens_normalizados = normalize(
    matriz, axis=0, norm="l2"
).tocsr()

# Descricao mais frequente de cada produto
descricoes = (
    df.groupby("StockCode")["Description"]
    .agg(lambda x: x.mode().iloc[0])
    .to_dict()
)

# 5. Funcao personalizada
def recomendar_cliente(cliente_id, top_n=5):

    if cliente_id not in clientes:
        print("Cliente sem historico elegivel.")
        return

    idx = clientes.get_loc(cliente_id)

    # Produtos adquiridos pelo cliente
    comprados = matriz[idx].indices

    # Similaridade entre todos os itens e
    # o conjunto de itens comprados
    perfil = matriz[idx].T

    scores = (
        itens_normalizados.T
        @ (itens_normalizados @ perfil)
    ).toarray().ravel()

    # Excluir itens ja comprados
    scores[comprados] = 0

    # Selecionar apenas recomendacoes positivas
    candidatos = np.flatnonzero(scores > 0)

    melhores = candidatos[
        np.argsort(scores[candidatos])[::-1][:top_n]
    ]

    print(f"\nCLIENTE: {cliente_id}")
    print("Produtos distintos comprados:", len(comprados))

    print("\nPRODUTOS RECOMENDADOS:")

    for posicao in melhores:
        codigo = produtos[posicao]

        print(
            f"{codigo} | "
            f"{descricoes[codigo]} | "
            f"Score: {scores[posicao]:.4f}"
        )

    if len(melhores) == 0:
        print("Nenhuma recomendacao encontrada.")


# 6. Testar com um cliente existente
cliente_teste = clientes[0]

print("Clientes elegiveis:", len(clientes))
print("Produtos elegiveis:", len(produtos))

recomendar_cliente(int(cliente_teste), top_n=5)
