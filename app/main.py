
from pathlib import Path
import subprocess
import sys

import streamlit as st

st.set_page_config(
    page_title="Customer Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parents[1]
DADOS_DIR = BASE_DIR / "data" / "processed"

ARQUIVOS_NECESSARIOS = [
    DADOS_DIR / "transacoes_limpas.csv",
    DADOS_DIR / "clientes_segmentados.csv"
]

# Preparar os dados somente quando necessario
if not all(arquivo.exists() for arquivo in ARQUIVOS_NECESSARIOS):

    st.info("Preparando os dados da aplicacao...")

    with st.spinner("Executando pipeline de dados"):
        try:
            subprocess.run(
                [
                    sys.executable,
                    str(BASE_DIR / "src" / "preparar_projeto.py")
                ],
                cwd=BASE_DIR,
                check=True
            )

        except Exception as erro:
            st.error("Falha ao preparar os dados.")
            st.exception(erro)
            st.stop()

    st.rerun()

# Importar paginas apos verificar os dados
from views import visao_geral, segmentacao, recomendacoes

with st.sidebar:

    st.title("Customer Intelligence")
    st.caption("Data Science & Machine Learning")
    st.divider()

    pagina = st.radio(
        "Navegacao",
        [
            "Visao Geral",
            "Segmentacao",
            "Recomendacoes"
        ]
    )

    st.divider()
    st.caption("Dados historicos: 2010-2011")


if pagina == "Visao Geral":
    visao_geral.mostrar()

elif pagina == "Segmentacao":
    segmentacao.mostrar()

elif pagina == "Recomendacoes":
    recomendacoes.mostrar()
