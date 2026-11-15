
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from services.dados import (
    carregar_clientes,
    carregar_transacoes
)
from services.recomendador import recomendar_cliente


# ==========================================
# DARK ANALYTICS PRO - PALETA
# ==========================================

BG = "#0B1323"
CARD = "#19283D"
TEXT = "#F1F5F9"
MUTED = "#A1B3C9"
GRID = "#334155"

ACCENT = "#5EEAD4"
BLUE = "#38BDF8"
PURPLE = "#A78BFA"

CORES = {
    0: ACCENT,
    1: "#F5B65C",
    2: PURPLE,
    3: BLUE
}


# ==========================================
# FORMATACAO
# ==========================================

def formatar_numero(valor, casas=2):
    texto = f"{valor:,.{casas}f}"
    return (
        texto.replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


# ==========================================
# GRAFICO DE RECOMENDACOES
# ==========================================

def criar_grafico_recomendacoes(recomendacoes):

    dados = recomendacoes.sort_values(
        "Score",
        ascending=True
    ).copy()

    dados["Rotulo"] = (
        dados["Codigo"].astype(str)
        + " | "
        + dados["Produto"].str.slice(0, 32)
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=dados["Score"],
            y=dados["Rotulo"],
            orientation="h",
            marker=dict(
                color=ACCENT,
                line=dict(width=0)
            ),
            text=dados["Score"].map(
                lambda x: f"{x:.4f}"
            ),
            textposition="outside",
            textfont=dict(
                color=TEXT,
                size=12
            ),
            customdata=dados[
                ["Codigo", "Produto"]
            ].to_numpy(),
            hovertemplate=(
                "<b>%{customdata[1]}</b>"
                "<br>Código: %{customdata[0]}"
                "<br>Score: %{x:.4f}"
                "<extra></extra>"
            )
        )
    )

    maior_score = max(
        float(dados["Score"].max()),
        0.01
    )

    fig.update_layout(
        title=dict(
            text="Ranking de produtos recomendados",
            font=dict(
                size=19,
                color=TEXT
            )
        ),
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font=dict(color=TEXT),
        height=420,
        margin=dict(
            l=20,
            r=45,
            t=70,
            b=45
        ),
        xaxis=dict(
            title="Score de recomendação",
            range=[0, maior_score * 1.23],
            showgrid=True,
            gridcolor=GRID,
            zeroline=False
        ),
        yaxis=dict(
            title=None,
            showgrid=False,
            automargin=True
        ),
        showlegend=False,
        bargap=0.38,
        barcornerradius=12
    )

    return fig


# ==========================================
# PAGINA PRINCIPAL
# ==========================================

def mostrar():

    clientes = carregar_clientes()

    # ======================================
    # 1. CABECALHO
    # ======================================

    st.markdown(
        '<p class="page-eyebrow">'
        'CUSTOMER INTELLIGENCE / AI ENGINE'
        '</p>',
        unsafe_allow_html=True
    )

    st.title("Recomendação de Produtos")

    st.caption(
        "Descubra produtos relacionados ao histórico "
        "de compras de cada cliente utilizando "
        "similaridade entre itens."
    )

    st.divider()

    # ======================================
    # 2. SELECIONAR CLIENTE
    # ======================================

    cliente_id = st.selectbox(
        "Selecione um cliente",
        options=sorted(
            clientes["CustomerID"].unique()
        ),
        format_func=lambda x: f"Cliente {x}",
        key="cliente_recomendacoes"
    )

    cliente = clientes.loc[
        clientes["CustomerID"] == cliente_id
    ].iloc[0]

    cluster = int(cliente["Cluster"])
    segmento = str(cliente["Segmento"])
    cor = CORES.get(cluster, ACCENT)

    # ======================================
    # 3. CARTAO DE PERFIL
    # ======================================

    with st.container(border=True):

        col1, col2 = st.columns([2, 1])

        with col1:
            st.caption("CLIENTE SELECIONADO")
            st.subheader(
                f"Cliente {int(cliente_id)}"
            )
            st.write(f"**Segmento:** {segmento}")

        with col2:
            st.caption("MODELO DE SEGMENTAÇÃO")
            st.markdown(
                f"**Cluster {cluster}**"
            )
            st.caption("K-Means | K=4")

    st.markdown("### Indicadores do cliente")

    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric(
            "Recência",
            f"{int(cliente['Recency'])} dias"
        )

    with m2:
        st.metric(
            "Frequência",
            f"{int(cliente['Frequency'])} compras"
        )

    with m3:
        st.metric(
            "Valor das compras",
            "£ " + formatar_numero(
                cliente["Monetary"]
            )
        )

    # ======================================
    # 4. HISTORICO DE COMPRAS
    # ======================================

    st.divider()

    st.markdown("### Histórico de compras")

    transacoes = carregar_transacoes()

    historico = transacoes.loc[
        transacoes["CustomerID"] == cliente_id
    ].copy()

    if historico.empty:

        st.warning(
            "Nenhuma transação encontrada "
            "para este cliente."
        )

    else:

        produtos_cliente = (
            historico.groupby(
                ["StockCode", "Description"],
                as_index=False
            )
            .agg(
                Quantidade=("Quantity", "sum"),
                Valor=("TotalPrice", "sum")
            )
            .sort_values(
                "Valor",
                ascending=False
            )
        )

        h1, h2 = st.columns(2)

        with h1:
            st.metric(
                "Produtos distintos no histórico",
                historico["StockCode"].nunique()
            )

        with h2:
            st.metric(
                "Notas de compra",
                historico["InvoiceNo"].nunique()
            )

        with st.expander(
            "Visualizar produtos comprados",
            expanded=True
        ):

            st.dataframe(
                produtos_cliente.rename(
                    columns={
                        "StockCode": "Código",
                        "Description": "Produto",
                        "Quantidade": "Quantidade",
                        "Valor": "Valor (£)"
                    }
                ),
                hide_index=True,
                width="stretch"
            )

    # ======================================
    # 5. RECOMENDACOES PERSONALIZADAS
    # ======================================

    st.divider()

    st.markdown("### Recomendações personalizadas")

    st.caption(
        "Os produtos são sugeridos a partir de "
        "padrões de compras de outros clientes. "
        "Itens já adquiridos são excluídos."
    )

    with st.spinner(
        "Analisando o histórico de compras..."
    ):

        recomendacoes = recomendar_cliente(
            int(cliente_id),
            top_n=5
        )

    if recomendacoes.empty:

        st.warning(
            "Não foram encontradas recomendações "
            "elegíveis para este cliente."
        )

    else:

        recomendacoes = (
            recomendacoes.sort_values(
                "Score",
                ascending=False
            )
            .reset_index(drop=True)
        )

        melhor = recomendacoes.iloc[0]

        with st.container(border=True):

            st.caption("MELHOR RECOMENDAÇÃO")

            st.subheader(
                str(melhor["Produto"])
            )

            c1, c2 = st.columns(2)

            with c1:
                st.metric(
                    "Código do produto",
                    str(melhor["Codigo"])
                )

            with c2:
                st.metric(
                    "Score",
                    f"{melhor['Score']:.4f}"
                )

        # ==================================
        # 6. RANKING VISUAL
        # ==================================

        st.markdown("### Ranking de recomendações")

        fig = criar_grafico_recomendacoes(
            recomendacoes
        )

        st.plotly_chart(
            fig,
            width="stretch",
            config={
                "displayModeBar": False
            }
        )

        # ==================================
        # 7. TABELA COMPLETA
        # ==================================

        st.markdown(
            "### Detalhamento dos produtos"
        )

        tabela = recomendacoes.copy()

        tabela.insert(
            0,
            "Posição",
            range(1, len(tabela) + 1)
        )

        st.dataframe(
            tabela,
            hide_index=True,
            width="stretch",
            column_config={
                "Score": st.column_config.NumberColumn(
                    "Score",
                    format="%.4f"
                )
            }
        )

        st.info(
            "Os scores representam pontuações "
            "relativas de similaridade, não "
            "probabilidades de compra."
        )

    # ======================================
    # 8. INFORMACOES DO MODELO
    # ======================================

    st.divider()

    with st.expander(
        "Como funciona o sistema de recomendação?"
    ):

        st.markdown(
            """
            O recomendador utiliza uma matriz
            cliente-produto para identificar padrões
            de compras compartilhados.

            **Metodologia:**

            - Representação binária das compras.
            - Similaridade de cosseno entre produtos.
            - Agregação de similaridades para cada cliente.
            - Exclusão de produtos já comprados.
            - Seleção dos cinco maiores scores.

            **Resultados da avaliação temporal:**

            - Precision@5: 8,53%.
            - Recall@5: 2,77%.
            - HitRate@5: 28,42%.
            - Cobertura do catálogo: 22,34%.

            Esses resultados foram obtidos em um
            experimento temporal com 1.752 clientes
            elegíveis, não em produção.
            """
        )

    # ======================================
    # 9. RODAPE
    # ======================================

    st.divider()

    st.caption(
        "Customer Intelligence | Dark Analytics Pro | "
        "Sistema demonstrativo com dados históricos "
        "de 2010-2011. As recomendações não "
        "representam comportamento atual."
    )
