
import streamlit as st
import plotly.graph_objects as go

from services.dados import carregar_clientes


# ==========================================
# DARK ANALYTICS PRO - PALETA
# ==========================================

BG = "#0B1323"
CARD = "#19283D"
TEXT = "#F1F5F9"
MUTED = "#A1B3C9"
GRID = "#334155"

CORES = {
    "Alto valor": "#5EEAD4",
    "Inativos ou ocasionais": "#F5B65C",
    "Recentes de baixa frequencia": "#A78BFA",
    "Recorrentes intermediarios": "#38BDF8"
}


def mostrar():

    # ======================================
    # 1. CARREGAR DADOS
    # ======================================

    df = carregar_clientes()

    st.markdown(
        '<div class="page-eyebrow">'
        'ANALYTICS / OVERVIEW'
        '</div>',
        unsafe_allow_html=True
    )

    st.title("Visão Geral")

    st.caption(
        "Monitoramento dos segmentos e "
        "comportamento de compra dos clientes."
    )

    st.divider()

    # ======================================
    # 2. INDICADORES PRINCIPAIS
    # ======================================

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Clientes analisados",
            f"{len(df):,}".replace(",", ".")
        )

    with c2:
        st.metric(
            "Segmentos identificados",
            df["Cluster"].nunique()
        )

    with c3:
        st.metric(
            "Valor das compras positivas",
            f"£ {df['Monetary'].sum():,.2f}"
        )

    st.markdown("## Inteligência de Clientes")

    # ======================================
    # 3. PREPARAR DISTRIBUICAO
    # ======================================

    distribuicao = (
        df.groupby("Segmento")
        .agg(
            Clientes=("CustomerID", "count"),
            Valor=("Monetary", "sum")
        )
        .reset_index()
        .sort_values("Clientes", ascending=True)
    )

    cores_segmentos = [
        CORES.get(segmento, "#5EEAD4")
        for segmento in distribuicao["Segmento"]
    ]

    # ======================================
    # 4. GRAFICO DE BARRAS ARREDONDADAS
    # ======================================

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=distribuicao["Clientes"],
            y=distribuicao["Segmento"],
            orientation="h",
            marker=dict(
                color=cores_segmentos,
                line=dict(width=0)
            ),
            text=distribuicao["Clientes"],
            textposition="inside",
            insidetextanchor="end",
            textfont=dict(
                color=BG,
                size=13
            ),
            hovertemplate=(
                "<b>%{y}</b>"
                "<br>Clientes: %{x:,}"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        title=dict(
            text="Distribuição dos clientes",
            font=dict(
                size=20,
                color=TEXT
            )
        ),
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font=dict(color=TEXT),
        height=420,
        margin=dict(
            l=20,
            r=30,
            t=70,
            b=45
        ),
        xaxis=dict(
            title="Número de clientes",
            showgrid=True,
            gridcolor=GRID,
            zeroline=False
        ),
        yaxis=dict(
            title=None,
            showgrid=False,
            autorange="reversed"
        ),
        showlegend=False,
        bargap=0.35,

        # Arredondamento das barras
        barcornerradius=12
    )

    st.plotly_chart(
        fig,
        width="stretch",
        config={"displayModeBar": False}
    )

    # ======================================
    # 5. GRAFICO DE PARTICIPACAO
    # ======================================

    st.markdown(
        "## Participação no valor das compras"
    )

    fig2 = go.Figure()

    fig2.add_trace(
        go.Pie(
            labels=distribuicao["Segmento"],
            values=distribuicao["Valor"],
            hole=0.65,
            marker=dict(
                colors=cores_segmentos,
                line=dict(
                    color=CARD,
                    width=3
                )
            ),
            textinfo="percent",
            textfont=dict(size=14),
            hovertemplate=(
                "<b>%{label}</b>"
                "<br>Participação: %{percent}"
                "<br>Valor: £%{value:,.2f}"
                "<extra></extra>"
            )
        )
    )

    fig2.update_layout(
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font=dict(color=TEXT),
        height=470,
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=80
        ),
        legend=dict(
            orientation="h",
            y=-0.15,
            x=0.5,
            xanchor="center",
            font=dict(size=12)
        ),
        annotations=[
            dict(
                text=(
                    "<b>£8,89M</b>"
                    "<br>"
                    "<span style='font-size:12px'>"
                    "Compras positivas"
                    "</span>"
                ),
                x=0.5,
                y=0.5,
                font=dict(
                    size=22,
                    color="#5EEAD4"
                ),
                showarrow=False
            )
        ]
    )

    st.plotly_chart(
        fig2,
        width="stretch",
        config={"displayModeBar": False}
    )

    # ======================================
    # 6. RESUMO DOS SEGMENTOS
    # ======================================

    st.markdown("## Resumo dos segmentos")

    resumo = distribuicao.copy()

    resumo["Participação (%)"] = (
        resumo["Clientes"] / len(df) * 100
    ).round(2)

    resumo["Valor (£)"] = resumo["Valor"].round(2)

    st.dataframe(
        resumo[
            [
                "Segmento",
                "Clientes",
                "Participação (%)",
                "Valor (£)"
            ]
        ],
        hide_index=True,
        width="stretch"
    )

    # ======================================
    # 7. RODAPE
    # ======================================

    st.divider()

    st.caption(
        "Customer Intelligence | "
        "Dark Analytics Pro | "
        "Dados históricos de 2010-2011. "
        "Valores referentes a compras positivas."
    )
