
from pathlib import Path

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[2]
DADOS_DIR = BASE_DIR / "data" / "processed"


@st.cache_data
def carregar_clientes():
    arquivo = DADOS_DIR / "clientes_segmentados.csv"

    return pd.read_csv(
        arquivo,
        dtype={"CustomerID": "int64"}
    )


@st.cache_data
def carregar_transacoes():
    arquivo = DADOS_DIR / "transacoes_limpas.csv"

    return pd.read_csv(
        arquivo,
        dtype={
            "CustomerID": "int64",
            "StockCode": str,
            "InvoiceNo": str
        },
        parse_dates=["InvoiceDate"]
    )
