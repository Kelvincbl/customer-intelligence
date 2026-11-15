
from pathlib import Path
from itertools import combinations

import pandas as pd
import numpy as np

from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

BASE_DIR = Path(__file__).resolve().parents[1]

ARQUIVO = (
    BASE_DIR / "data" / "processed" /
    "clientes_rfm_scaled.csv"
)

# Carregar os dados preparados
df = pd.read_csv(ARQUIVO)

variaveis = ["Recency", "Frequency", "Monetary"]
X = df[variaveis]

# Vamos comparar 10 inicializacoes para cada K
sementes = range(10)

for k in [2, 4]:

    resultados = []
    inercias = []

    print(f"\n--- ESTABILIDADE PARA K={k} ---")

    for seed in sementes:

        modelo = KMeans(
            n_clusters=k,
            random_state=seed,
            n_init=10
        )

        labels = modelo.fit_predict(X)

        resultados.append(labels)
        inercias.append(modelo.inertia_)

    # Comparar todos os pares de inicializacoes
    scores_ari = []

    for i, j in combinations(range(len(resultados)), 2):

        ari = adjusted_rand_score(
            resultados[i],
            resultados[j]
        )

        scores_ari.append(ari)

    print(f"ARI medio: {np.mean(scores_ari):.4f}")
    print(f"ARI minimo: {np.min(scores_ari):.4f}")
    print(f"ARI maximo: {np.max(scores_ari):.4f}")

    print(f"Inercia media: {np.mean(inercias):.2f}")
    print(f"Desvio da inercia: {np.std(inercias):.2f}")

print("\nValidacao concluida!")
