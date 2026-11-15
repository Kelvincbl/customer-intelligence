
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# ==========================================
# 1. CAMINHOS
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[1]

PASTA_DADOS = BASE_DIR / "data" / "processed"
PASTA_RESULTADOS = BASE_DIR / "reports"
PASTA_GRAFICOS = PASTA_RESULTADOS / "figures"

PASTA_GRAFICOS.mkdir(parents=True, exist_ok=True)

# ==========================================
# 2. CARREGAR OS DADOS
# ==========================================

rfm = pd.read_csv(
    PASTA_DADOS / "clientes_rfm.csv"
)

scaled = pd.read_csv(
    PASTA_DADOS / "clientes_rfm_scaled.csv"
)

variaveis = ["Recency", "Frequency", "Monetary"]

# Garantir correspondencia entre clientes
assert rfm["CustomerID"].is_unique
assert scaled["CustomerID"].is_unique

df = rfm.merge(
    scaled,
    on="CustomerID",
    suffixes=("", "_scaled"),
    validate="one_to_one"
)

X = df[[f"{v}_scaled" for v in variaveis]]

# ==========================================
# 3. COMPARAR K=2 E K=4
# ==========================================

for k in [2, 4]:

    print(f"\n{'=' * 45}")
    print(f"AVALIACAO DO K-MEANS COM K={k}")
    print(f"{'=' * 45}")

    modelo = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    grupos = modelo.fit_predict(X)

    resultado = df[
        ["CustomerID"] + variaveis
    ].copy()

    resultado["Cluster"] = grupos

    # Quantidade de clientes por cluster
    contagem = (
        resultado["Cluster"]
        .value_counts()
        .sort_index()
    )

    print("\nCLIENTES POR CLUSTER:")
    print(contagem)

    # Perfil mediano dos clientes
    perfil = resultado.groupby("Cluster").agg(
        Clientes=("CustomerID", "count"),
        Recency_mediana=("Recency", "median"),
        Frequency_mediana=("Frequency", "median"),
        Monetary_mediana=("Monetary", "median"),
        Monetary_total=("Monetary", "sum")
    )

    perfil["Percentual_clientes"] = (
        perfil["Clientes"] / len(resultado) * 100
    )

    print("\nPERFIL DOS CLUSTERS:")
    print(perfil.round(2).to_string())

    # Silhouette na mesma amostra do experimento
    score = silhouette_score(
        X,
        grupos,
        sample_size=2000,
        random_state=42
    )

    print(f"\nSilhouette Score: {score:.4f}")

    # Salvar resultados
    resultado.to_csv(
        PASTA_RESULTADOS / f"clientes_clusters_k{k}.csv",
        index=False
    )

    perfil.to_csv(
        PASTA_RESULTADOS / f"perfil_clusters_k{k}.csv"
    )

    # ======================================
    # 4. VISUALIZACAO
    # ======================================

    fig, axes = plt.subplots(
        1, 3,
        figsize=(16, 5)
    )

    colunas = [
        "Recency_mediana",
        "Frequency_mediana",
        "Monetary_mediana"
    ]

    titulos = [
        "Recencia mediana (dias)",
        "Frequencia mediana (compras)",
        "Gasto mediano (£)"
    ]

    for ax, coluna, titulo in zip(
        axes, colunas, titulos
    ):

        sns.barplot(
            x=perfil.index.astype(str),
            y=perfil[coluna].values,
            ax=ax,
            color="steelblue"
        )

        ax.set_title(titulo)
        ax.set_xlabel("Cluster")
        ax.set_ylabel("Valor")

    plt.suptitle(
        f"Perfil dos clientes - K={k}",
        fontsize=14
    )

    plt.tight_layout()

    plt.savefig(
        PASTA_GRAFICOS / f"perfil_clusters_k{k}.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

print("\nComparacao concluida!")
