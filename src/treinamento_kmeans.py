
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# 1. Caminhos
BASE_DIR = Path(__file__).resolve().parents[1]

ARQUIVO = (
    BASE_DIR / "data" / "processed" /
    "clientes_rfm_scaled.csv"
)

PASTA_GRAFICOS = BASE_DIR / "reports" / "figures"
PASTA_GRAFICOS.mkdir(parents=True, exist_ok=True)

PASTA_RESULTADOS = BASE_DIR / "reports"
PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)

# 2. Carregar dados padronizados
print("Carregando dados para Machine Learning...")

df = pd.read_csv(ARQUIVO)

variaveis = ["Recency", "Frequency", "Monetary"]

X = df[variaveis]

print("Clientes:", len(X))
print("Variaveis utilizadas:", variaveis)

# 3. Testar diferentes valores de K
resultados = []

for k in range(2, 11):

    print(f"\nTreinando K-Means com k={k}...")

    modelo = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    grupos = modelo.fit_predict(X)

    # Avaliacao usando amostra para reduzir o custo
    silhouette = silhouette_score(
        X,
        grupos,
        sample_size=2000,
        random_state=42
    )

    inercia = modelo.inertia_

    resultados.append({
        "K": k,
        "Inercia": inercia,
        "Silhouette": silhouette
    })

    print(f"Inercia: {inercia:.2f}")
    print(f"Silhouette: {silhouette:.4f}")

# 4. Tabela comparativa
resultados_df = pd.DataFrame(resultados)

print("\n--- COMPARACAO DOS MODELOS ---")
print(resultados_df.round(4).to_string(index=False))

# 5. Salvar metricas
resultados_df.to_csv(
    PASTA_RESULTADOS / "metricas_kmeans.csv",
    index=False
)

# 6. Metodo do cotovelo
plt.figure(figsize=(9, 5))

plt.plot(
    resultados_df["K"],
    resultados_df["Inercia"],
    marker="o"
)

plt.title("Metodo do Cotovelo - K-Means")
plt.xlabel("Numero de clusters (K)")
plt.ylabel("Inercia")
plt.xticks(resultados_df["K"])
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    PASTA_GRAFICOS / "metodo_cotovelo.png",
    dpi=300
)

plt.show()

# 7. Silhouette Score
plt.figure(figsize=(9, 5))

plt.plot(
    resultados_df["K"],
    resultados_df["Silhouette"],
    marker="o"
)

plt.title("Silhouette Score por numero de clusters")
plt.xlabel("Numero de clusters (K)")
plt.ylabel("Silhouette Score")
plt.xticks(resultados_df["K"])
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    PASTA_GRAFICOS / "silhouette_kmeans.png",
    dpi=300
)

plt.show()

print("\nAvaliacao dos modelos concluida!")
