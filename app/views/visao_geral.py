
import streamlit as st
import plotly.express as px

from services.dados import carregar_clientes


def mostrar():

    df = carregar_clientes()

    st.title("Visao Geral")
    st.write("Indicadores e distribuicao dos clientes.")

    c1, c2, c3 = st.columns(3)

    c1.metric("Clientes", f"{len(df):,}")

    c2.metric(
        "Segmentos",
        df["Cluster"].nunique()
    )

    c3.metric(
        "Valor das compras positivas",
        f"£ {df['Monetary'].sum():,.2f}"
    )

    st.divider()

    distribuicao = (
        df.groupby("Segmento")
        .agg(
            Clientes=("CustomerID", "count"),
            Valor=("Monetary", "sum")
        )
        .reset_index()
        .sort_values("Clientes")
    )

    fig = px.bar(
        distribuicao,
        x="Clientes",
        y="Segmento",
        orientation="h",
        text="Clientes",
        color="Segmento",
        title="Clientes por segmento"
    )

    fig.update_layout(
        showlegend=False,
        height=400,
        yaxis_title="",
        xaxis_title="Numero de clientes"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Participacao no valor das compras")

    fig2 = px.pie(
        distribuicao,
        names="Segmento",
        values="Valor",
        hole=0.5
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.caption(
        "Os valores representam compras positivas "
        "na base historica de 2010-2011."
    )
