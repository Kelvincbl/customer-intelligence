
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from services.dados import carregar_clientes


# ==========================================
# DARK ANALYTICS PRO - CORES
# ==========================================

BG = "#0B1323"
CARD = "#19283D"
TEXT = "#F1F5F9"
MUTED = "#A1B3C9"
GRID = "#334155"

CORES = {
    0: "#5EEAD4",
    1: "#F5B65C",
    2: "#A78BFA",
    3: "#38BDF8"
}

DESCRICOES = {
    0: (
        "Clientes com compras recentes, maior "
        "frequencia e elevado valor monetario."
    ),
    1: (
        "Clientes com baixa frequencia e maior "
        "tempo desde a ultima compra."
    ),
    2: (
        "Clientes que compraram recentemente, "
        "mas apresentam baixa frequencia."
    ),
    3: (
        "Clientes com frequencia e valor monetario "
        "intermediarios em relacao aos demais grupos."
    )
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
# GRAFICO COMPARATIVO
# ==========================================

def grafico_comparacao(nome, valor, mediana, cor):

    maior = max(float(valor), float(mediana), 1)

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=[valor, mediana],
            y=["Cliente", "Mediana do segmento"],
            orientation="h",
            marker=dict(
                color=[cor, "#64748B"]
            ),
            text=[
                formatar_numero(valor),
                formatar_numero(mediana)
            ],
            textposition="auto",
            textfont=dict(
                color=TEXT,
                size=13
            ),
            hovertemplate=(
                "%{y}<br>Valor: %{x:,.2f}"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        title=dict(
            text=nome,
            font=dict(
                size=17,
                color=TEXT
            )
        ),
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font=dict(color=TEXT),
        height=220,
        margin=dict(
            l=20,
            r=35,
            t=55,
            b=25
        ),
        xaxis=dict(
            range=[0, maior * 1.20],
            showgrid=True,
            gridcolor=GRID,
            zeroline=False,
            title=None
        ),
        yaxis=dict(
            title=None,
            showgrid=False,
            autorange="reversed"
        ),
        showlegend=False,
        bargap=0.40,
        barcornerradius=10
    )

    return fig


# ==========================================
# PAGINA PRINCIPAL
# ==========================================

def mostrar():

    df = carregar_clientes()

    # ======================================
    # CABECALHO
    # ======================================

    st.markdown(
        '<p class="page-eyebrow">'
        'CUSTOMER ANALYTICS / SEGMENTACAO'
        '</p>',
        unsafe_allow_html=True
    )

    st.title("Segmentação de Clientes")

    st.caption(
        "Explore o comportamento individual "
        "dos clientes e os segmentos "
        "identificados pelo K-Means."
    )

    st.divider()

    # ======================================
    # SELECAO DO CLIENTE
    # ======================================

    cliente_id = st.selectbox(
        "Selecione o cliente",
        options=sorted(df["CustomerID"].unique()),
        format_func=lambda x: f"Cliente {x}"
    )

    cliente = df.loc[
        df["CustomerID"] == cliente_id
    ].iloc[0]

    cluster = int(cliente["Cluster"])
    segmento = str(cliente["Segmento"])

    cor = CORES.get(cluster, "#5EEAD4")

    # ======================================
    # CARTAO DO CLIENTE - SEM HTML MULTILINHA
    # ======================================

    with st.container(border=True):

        col1, col2 = st.columns([2, 1])

        with col1:
            st.caption("PERFIL DO CLIENTE")

            st.subheader(
                f"Cliente {int(cliente_id)}"
            )

            st.markdown(
                f"**Segmento:** {segmento}"
            )

        with col2:
            st.caption("CLASSIFICAÇÃO")

            st.markdown(
                f":green[**Cluster {cluster}**]"
            )

            st.caption(
                "Modelo K-Means | K=4"
            )

        st.markdown(
            f"**Descrição:** {DESCRICOES.get(cluster, '')}"
        )

    # ======================================
    # INDICADORES RFM
    # ======================================

    st.markdown("### Indicadores RFM")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Recência",
            f"{int(cliente['Recency'])} dias"
        )

    with c2:
        st.metric(
            "Frequência",
            f"{int(cliente['Frequency'])} compras"
        )

    with c3:
        st.metric(
            "Valor das compras",
            "£ " + formatar_numero(
                cliente["Monetary"]
            )
        )

    st.divider()

    # ======================================
    # MEDIANAS DO SEGMENTO
    # ======================================

    grupo = df[
        df["Cluster"] == cluster
    ]

    medianas = grupo[
        ["Recency", "Frequency", "Monetary"]
    ].median()

    st.markdown(
        "### Cliente vs. mediana do segmento"
    )

    st.caption(
        "Comparação entre os indicadores individuais "
        "e o comportamento típico dos clientes "
        "pertencentes ao mesmo grupo."
    )

    # ======================================
    # GRAFICOS COMPARATIVOS
    # ======================================

    graficos = [
        (
            "Recência (dias)",
            float(cliente["Recency"]),
            float(medianas["Recency"])
        ),
        (
            "Frequência (compras)",
            float(cliente["Frequency"]),
            float(medianas["Frequency"])
        ),
        (
            "Valor monetário (£)",
            float(cliente["Monetary"]),
            float(medianas["Monetary"])
        )
    ]

    for nome, valor, mediana in graficos:

        fig = grafico_comparacao(
            nome=nome,
            valor=valor,
            mediana=mediana,
            cor=cor
        )

        st.plotly_chart(
            fig,
            width="stretch",
            config={
                "displayModeBar": False
            }
        )

    # ======================================
    # ANALISE DE PERFIL ATIPICO
    # ======================================

    indicadores_atipicos = []

    for coluna in [
        "Recency",
        "Frequency",
        "Monetary"
    ]:

        mediana = float(medianas[coluna])
        valor = float(cliente[coluna])

        if mediana > 0:

            if valor > mediana * 3:
                indicadores_atipicos.append(coluna)

    if indicadores_atipicos:

        st.warning(
            "Este cliente apresenta valores "
            "superiores a três vezes a mediana "
            "do segmento nos indicadores: "
            + ", ".join(indicadores_atipicos)
            + ". Isso não significa necessariamente "
            "um erro do modelo."
        )

    # ======================================
    # COMPARACAO ENTRE SEGMENTOS
    # ======================================

    st.divider()

    st.markdown(
        "### Comparação entre segmentos"
    )

    resumo = (
        df.groupby(
            ["Cluster", "Segmento"]
        )
        .agg(
            Clientes=("CustomerID", "count"),
            Recencia_mediana=("Recency", "median"),
            Frequencia_mediana=(
                "Frequency", "median"
            ),
            Monetary_mediana=(
                "Monetary", "median"
            )
        )
        .reset_index()
    )

    resumo = resumo.rename(
        columns={
            "Recencia_mediana": "Recência (dias)",
            "Frequencia_mediana": "Frequência",
            "Monetary_mediana": "Gasto mediano (£)"
        }
    )

    st.dataframe(
        resumo,
        hide_index=True,
        width="stretch"
    )

    # ======================================
    # RODAPE
    # ======================================

    st.divider()

    st.caption(
        "Customer Intelligence | Dark Analytics Pro | "
        "Dados históricos de 2010-2011. "
        "Os segmentos representam agrupamentos "
        "estatísticos, não classificações "
        "comerciais definitivas."
    )
