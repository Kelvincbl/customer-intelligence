
import streamlit as st

from services.dados import (
    carregar_clientes,
    carregar_transacoes
)

from services.recomendador import recomendar_cliente


def mostrar():

    st.title("Recomendacao de Produtos")

    clientes = carregar_clientes()

    cliente_id = st.selectbox(
        "Selecione um cliente",
        sorted(clientes["CustomerID"].unique()),
        format_func=lambda x: f"Cliente {x}"
    )

    cliente = clientes.loc[
        clientes["CustomerID"] == cliente_id
    ].iloc[0]

    st.write(
        f"Segmento RFM: **{cliente['Segmento']}**"
    )

    st.divider()

    st.subheader("Historico do cliente")

    transacoes = carregar_transacoes()

    historico = transacoes[
        transacoes["CustomerID"] == cliente_id
    ]

    produtos_cliente = (
        historico.groupby(
            ["StockCode", "Description"],
            as_index=False
        )
        .agg(
            Quantidade=("Quantity", "sum"),
            Valor=("TotalPrice", "sum")
        )
        .sort_values("Valor", ascending=False)
    )

    st.dataframe(
        produtos_cliente,
        hide_index=True,
        use_container_width=True
    )

    st.divider()

    st.subheader("Top 5 produtos recomendados")

    with st.spinner("Calculando recomendacoes..."):
        recomendacoes = recomendar_cliente(
            int(cliente_id),
            top_n=5
        )

    if recomendacoes.empty:
        st.warning(
            "Nenhuma recomendacao elegivel "
            "para este cliente."
        )
    else:
        st.dataframe(
            recomendacoes,
            hide_index=True,
            use_container_width=True
        )

    st.caption(
        "Pontuacoes representam similaridade, "
        "nao probabilidades de compra. "
        "Recomendacoes baseadas no historico "
        "completo de 2010-2011."
    )
