
import streamlit as st

from services.dados import carregar_clientes


def mostrar():

    df = carregar_clientes()

    st.title("Segmentacao de Clientes")
    st.write(
        "Consulte os indicadores RFM e "
        "o segmento atribuido pelo K-Means."
    )

    cliente_id = st.selectbox(
        "Selecione um cliente",
        sorted(df["CustomerID"].unique()),
        format_func=lambda x: f"Cliente {x}"
    )

    cliente = df.loc[
        df["CustomerID"] == cliente_id
    ].iloc[0]

    st.success(
        f"Segmento: {cliente['Segmento']}"
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Recencia",
        f"{int(cliente['Recency'])} dias"
    )

    c2.metric(
        "Frequencia",
        f"{int(cliente['Frequency'])} compras"
    )

    c3.metric(
        "Valor das compras",
        f"£ {cliente['Monetary']:,.2f}"
    )

    st.divider()

    st.subheader("Comparacao com o segmento")

    grupo = df[
        df["Cluster"] == cliente["Cluster"]
    ]

    tabela = {
        "Indicador": [
            "Recencia (dias)",
            "Frequencia (compras)",
            "Valor (£)"
        ],
        "Cliente": [
            cliente["Recency"],
            cliente["Frequency"],
            cliente["Monetary"]
        ],
        "Mediana do segmento": [
            grupo["Recency"].median(),
            grupo["Frequency"].median(),
            grupo["Monetary"].median()
        ]
    }

    import pandas as pd
    st.dataframe(
        pd.DataFrame(tabela),
        hide_index=True,
        use_container_width=True
    )

    st.info(
        "Os segmentos representam perfis gerais. "
        "Um cliente individual pode apresentar "
        "comportamento diferente da mediana."
    )
