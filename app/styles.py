
import streamlit as st


def aplicar_estilos():
    st.markdown(
        """
        <style>
        /* ========================================
           DARK ANALYTICS PRO
           CUSTOMER INTELLIGENCE
        ======================================== */

        :root {
            --bg: #0B1323;
            --sidebar: #111D31;
            --card: #19283D;
            --border: #2B3D55;
            --accent: #5EEAD4;
            --text: #F1F5F9;
            --muted: #A1B3C9;
        }

        /* ========================================
           FUNDO E LAYOUT
        ======================================== */

        .stApp {
            background-color: var(--bg);
            color: var(--text);
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1450px;
        }

        /* ========================================
           BARRA LATERAL
        ======================================== */

        [data-testid="stSidebar"] {
            background-color: var(--sidebar);
            border-right: 1px solid var(--border);
        }

        [data-testid="stSidebar"] .stRadio label {
            color: var(--text);
        }

        /* ========================================
           TITULOS
        ======================================== */

        h1, h2, h3 {
            color: var(--text) !important;
            font-family: "Segoe UI", sans-serif;
            letter-spacing: -0.5px;
        }

        h1 {
            font-weight: 750 !important;
        }

        h2, h3 {
            font-weight: 650 !important;
        }

        /* ========================================
           CARDS DOS INDICADORES
        ======================================== */

        [data-testid="stMetric"] {
            background-color: var(--card);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 22px;
            box-shadow: 0 6px 24px rgba(0, 0, 0, 0.12);
        }

        [data-testid="stMetricLabel"] {
            color: var(--muted);
        }

        [data-testid="stMetricValue"] {
            color: var(--accent);
        }

        /* ========================================
           GRAFICOS PLOTLY
        ======================================== */

        [data-testid="stPlotlyChart"] {
            background-color: var(--card);
            border: 1px solid var(--border);
            border-radius: 18px;
            overflow: hidden;
            padding: 12px;
            box-shadow: 0 6px 24px rgba(0, 0, 0, 0.15);
        }

        [data-testid="stPlotlyChart"] > div {
            border-radius: 14px;
            overflow: hidden;
        }

        /* ========================================
           CONTAINERS
        ======================================== */

        [data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 18px;
        }

        /* ========================================
           BOTOES
        ======================================== */

        .stButton > button {
            background-color: #153B40;
            color: #B6FFF0;
            border: 1px solid #276A67;
            border-radius: 12px;
            font-weight: 600;
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            background-color: #205A5B;
            color: white;
            border-color: var(--accent);
        }

        /* ========================================
           CAMPOS DE SELECAO
        ======================================== */

        [data-baseweb="select"] > div {
            background-color: var(--card);
            border: 1px solid var(--border);
            border-radius: 12px;
        }

        /* ========================================
           TABELAS
        ======================================== */

        [data-testid="stDataFrame"] {
            border: 1px solid var(--border);
            border-radius: 14px;
            overflow: hidden;
        }

        /* ========================================
           SEPARADORES
        ======================================== */

        hr {
            border-color: var(--border) !important;
            opacity: 0.8;
        }

        /* ========================================
           TEXTOS SECUNDARIOS
        ======================================== */

        [data-testid="stCaptionContainer"] {
            color: var(--muted);
        }

        /* ========================================
           CABECALHO DAS PAGINAS
        ======================================== */

        .page-eyebrow {
            color: var(--accent);
            text-transform: uppercase;
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 2px;
            margin-bottom: 7px;
        }

        /* ========================================
           IDENTIDADE VISUAL
        ======================================== */

        .brand-title {
            color: #F8FAFC;
            font-size: 1.15rem;
            font-weight: 800;
            line-height: 1.35;
        }

        .brand-accent {
            color: var(--accent);
        }

        .brand-subtitle {
            color: var(--muted);
            font-size: 0.79rem;
            margin-top: 6px;
        }

        /* ========================================
           STATUS DO SISTEMA
        ======================================== */

        .status-text {
            color: var(--accent);
            font-size: 0.82rem;
            font-weight: 600;
        }

        /* ========================================
           RESPONSIVIDADE
        ======================================== */

        @media (max-width: 768px) {

            .block-container {
                padding-top: 1.2rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }

            [data-testid="stMetric"] {
                padding: 14px;
            }

            [data-testid="stPlotlyChart"] {
                padding: 6px;
                border-radius: 14px;
            }

            h1 {
                font-size: 1.8rem !important;
            }
        }

        </style>
        """,
        unsafe_allow_html=True
    )
