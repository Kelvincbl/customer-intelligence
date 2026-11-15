
import numpy as np
import pandas as pd
import streamlit as st

from scipy.sparse import csr_matrix
from sklearn.preprocessing import normalize

from services.dados import carregar_transacoes


EXCLUIDOS = {
    "POST", "DOT", "M", "BANK CHARGES",
    "AMAZONFEE", "CRUK", "D", "S",
    "C2", "PADS"
}


@st.cache_resource
def preparar_recomendador():

    df = carregar_transacoes()

    df = df[
        ~df["StockCode"].isin(EXCLUIDOS)
    ].dropna(
        subset=["StockCode", "Description"]
    ).copy()

    compras = df[
        ["CustomerID", "StockCode"]
    ].drop_duplicates()

    frequencia = compras.groupby(
        "StockCode"
    )["CustomerID"].nunique()

    validos = frequencia[
        frequencia >= 5
    ].index

    compras = compras[
        compras["StockCode"].isin(validos)
    ].copy()

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

    itens_norm = normalize(
        matriz,
        axis=0,
        norm="l2"
    ).tocsr()

    descricoes = (
        df.groupby("StockCode")["Description"]
        .agg(lambda x: x.mode().iloc[0])
        .to_dict()
    )

    return (
        clientes,
        produtos,
        matriz,
        itens_norm,
        descricoes
    )


def recomendar_cliente(cliente_id, top_n=5):

    (
        clientes,
        produtos,
        matriz,
        itens_norm,
        descricoes
    ) = preparar_recomendador()

    if cliente_id not in clientes:
        return pd.DataFrame(
            columns=["Codigo", "Produto", "Score"]
        )

    idx = clientes.get_loc(cliente_id)

    perfil = matriz[idx].T

    scores = (
        itens_norm.T @ (itens_norm @ perfil)
    ).toarray().ravel()

    # Excluir produtos ja comprados
    comprados = matriz[idx].indices
    scores[comprados] = -np.inf

    candidatos = np.flatnonzero(
        np.isfinite(scores) & (scores > 0)
    )

    melhores = candidatos[
        np.argsort(
            -scores[candidatos],
            kind="stable"
        )[:top_n]
    ]

    recomendacoes = [
        {
            "Codigo": str(produtos[i]),
            "Produto": descricoes[produtos[i]],
            "Score": round(float(scores[i]), 4)
        }
        for i in melhores
    ]

    return pd.DataFrame(
        recomendacoes,
        columns=["Codigo", "Produto", "Score"]
    )
