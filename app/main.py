
import streamlit as st

from views import (
    visao_geral,
    segmentacao,
    recomendacoes
)

st.set_page_config(
    page_title="Customer Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.sidebar:

    st.title("Customer Intelligence")

    st.caption(
        "Data Science & Machine Learning"
    )

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

    st.caption(
        "Dados historicos: 2010-2011"
    )

if pagina == "Visao Geral":
    visao_geral.mostrar()

elif pagina == "Segmentacao":
    segmentacao.mostrar()

elif pagina == "Recomendacoes":
    recomendacoes.mostrar()
