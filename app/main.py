
from pathlib import Path
import subprocess
import sys

import streamlit as st

# ========================================
# CONFIGURACAO
# ========================================

st.set_page_config(
    page_title="Customer Intelligence Pro",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

from styles import aplicar_estilos

aplicar_estilos()

BASE_DIR = Path(__file__).resolve().parents[1]
DADOS_DIR = BASE_DIR / "data" / "processed"

ARQUIVOS_NECESSARIOS = [
    DADOS_DIR / "transacoes_limpas.csv",
    DADOS_DIR / "clientes_segmentados.csv"
]

# ========================================
# PREPARACAO DOS DADOS
# ========================================

if not all(p.exists() for p in ARQUIVOS_NECESSARIOS):

    st.info("Preparando os dados da aplicacao...")

    with st.spinner("Executando pipeline de dados"):
        try:
            subprocess.run(
                [
                    sys.executable,
                    str(
                        BASE_DIR / "src" /
                        "preparar_projeto.py"
                    )
                ],
                cwd=BASE_DIR,
                check=True
            )
        except Exception as erro:
            st.error("Falha ao preparar os dados.")
            st.exception(erro)
            st.stop()

    st.rerun()

# ========================================
# IMPORTAR PAGINAS
# ========================================

from views import (
    visao_geral,
    segmentacao,
    recomendacoes
)

# ========================================
# MENU LATERAL
# ========================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand-title">
            CUSTOMER<br>
            <span class="brand-accent">
                INTELLIGENCE
            </span>
        </div>
        <div class="brand-subtitle">
            Data Science & Machine Learning
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        '<div class="page-eyebrow">Navegacao</div>',
        unsafe_allow_html=True
    )

    pagina = st.radio(
        "Selecione uma pagina",
        [
            "Visao Geral",
            "Segmentacao",
            "Recomendacoes"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown(
        '<div class="status-text">'
        '● Sistema operacional'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption("K-Means | Recomendacao item-item")
    st.caption("Base historica: 2010-2011")

# ========================================
# PAGINAS
# ========================================

if pagina == "Visao Geral":
    visao_geral.mostrar()

elif pagina == "Segmentacao":
    segmentacao.mostrar()

elif pagina == "Recomendacoes":
    recomendacoes.mostrar()
