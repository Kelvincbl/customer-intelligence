
from pathlib import Path
import sys

import joblib
import numpy as np
import pandas as pd

# Pasta principal do projeto
BASE_DIR = Path(__file__).resolve().parents[1]

# Permitir importar os modulos de app
sys.path.insert(0, str(BASE_DIR / "app"))

from services.dados import carregar_clientes
from services.recomendador import (
    recomendar_cliente,
    preparar_recomendador
)


def test_carregamento_clientes():
    df = carregar_clientes()

    assert not df.empty
    assert df["CustomerID"].is_unique

    colunas = {
        "CustomerID",
        "Recency",
        "Frequency",
        "Monetary",
        "Cluster",
        "Segmento"
    }

    assert colunas.issubset(df.columns)


def test_segmentos():
    df = carregar_clientes()

    assert df["Cluster"].nunique() == 4
    assert df["Segmento"].notna().all()


def test_indicadores_rfm():
    df = carregar_clientes()

    assert (df["Recency"] >= 0).all()
    assert (df["Frequency"] > 0).all()
    assert (df["Monetary"] > 0).all()


def test_modelo_salvo():
    caminho = (
        BASE_DIR / "models" / "pipeline_kmeans.joblib"
    )

    modelo = joblib.load(caminho)

    df = carregar_clientes()

    X = df[
        ["Recency", "Frequency", "Monetary"]
    ]

    previsoes = modelo.predict(X)

    assert len(previsoes) == len(df)
    assert np.array_equal(
        previsoes,
        df["Cluster"].to_numpy()
    )


def test_recomendacoes_nao_repetem_compras():
    (
        clientes,
        produtos,
        matriz,
        itens_norm,
        descricoes
    ) = preparar_recomendador()

    cliente_id = int(clientes[0])

    recomendacoes = recomendar_cliente(
        cliente_id,
        top_n=5
    )

    idx = clientes.get_loc(cliente_id)

    codigos_comprados = set(
        produtos[matriz[idx].indices]
    )

    codigos_recomendados = set(
        recomendacoes["Codigo"].astype(str)
    )

    assert codigos_comprados.isdisjoint(
        codigos_recomendados
    )
