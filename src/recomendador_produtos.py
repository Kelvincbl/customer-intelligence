
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.preprocessing import normalize

# ======================================
# 1. CONFIGURACOES
# ======================================

BASE_DIR = Path(__file__).resolve().parents[1]

ARQUIVO = (
    BASE_DIR / "data" / "processed"
    / "transacoes_limpas.csv"
)

# Codigos administrativos conhecidos
CODIGOS_EXCLUIDOS = {
    "POST", "DOT", "M", "BANK CHARGES",
    "AMAZONFEE", "CRUK", "D", "S",
    "C2", "PADS"
}

MIN_CLIENTES = 5

# ======================================
# 2. CARREGAR TRANSACOES
# ======================================

print("Carregando transacoes...")

df = pd.read_csv(
    ARQUIVO,
    dtype={
        "StockCode": str,
        "CustomerID": "int64"
    }
)

# Remover codigos administrativos
df = df[
    ~df["StockCode"].isin(CODIGOS_EXCLUIDOS)
].copy()

# Manter somente itens identificados
df = df.dropna(
    subset=["StockCode", "Description"]
)

# Cada par cliente-produto aparece uma vez
compras = df[
    ["CustomerID", "StockCode"]
].drop_duplicates()

# ======================================
# 3. FILTRAR PRODUTOS RAROS
# ======================================

popularidade = (
    compras.groupby("StockCode")["CustomerID"]
    .nunique()
)

codigos_validos = popularidade[
    popularidade >= MIN_CLIENTES
].index

compras = compras[
    compras["StockCode"].isin(codigos_validos)
].copy()

# ======================================
# 4. MATRIZ CLIENTE-PRODUTO
# ======================================

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

print("\nMatriz cliente-produto:", matriz.shape)

# Normalizacao por produto
matriz_normalizada = normalize(
    matriz,
    axis=0,
    norm="l2"
).tocsr()

# ======================================
# 5. DESCRICOES DOS PRODUTOS
# ======================================

descricoes = (
    df.groupby("StockCode")["Description"]
    .agg(lambda x: x.mode().iloc[0])
    .to_dict()
)

# ======================================
# 6. FUNCAO DE RECOMENDACAO
# ======================================

def recomendar(codigo_produto, top_n=5):

    if codigo_produto not in produtos:
        print("Produto nao encontrado no catalogo.")
        return

    indice = produtos.get_loc(codigo_produto)

    # Similaridade de cosseno entre produtos
    similaridades = (
        matriz_normalizada.T
        @ matriz_normalizada[:, indice]
    ).toarray().ravel()

    # Nao recomendar o proprio produto
    similaridades[indice] = -1

    melhores = np.argsort(
        similaridades
    )[::-1][:top_n]

    print("\nProduto consultado:")
    print(codigo_produto, descricoes[codigo_produto])

    print("\nProdutos recomendados:")

    for posicao in melhores:

        codigo = produtos[posicao]
        score = similaridades[posicao]

        print(
            f"{codigo} | "
            f"{descricoes[codigo]} | "
            f"Similaridade: {score:.4f}"
        )


# ======================================
# 7. TESTE INICIAL
# ======================================

print("\n--- SISTEMA DE RECOMENDACAO ---")

print("Produtos disponiveis:", len(produtos))
print("Clientes considerados:", len(clientes))

recomendar("85123A", top_n=5)

print("\nTeste concluido!")
