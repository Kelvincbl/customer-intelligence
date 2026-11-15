
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler
from sklearn.cluster import KMeans

# =====================================
# 1. CONFIGURACOES
# =====================================

BASE_DIR = Path(__file__).resolve().parents[1]

ARQUIVO_RFM = (
    BASE_DIR / "data" / "processed" / "clientes_rfm.csv"
)

PASTA_MODELOS = BASE_DIR / "models"
PASTA_RESULTADOS = BASE_DIR / "data" / "processed"

PASTA_MODELOS.mkdir(parents=True, exist_ok=True)

variaveis = ["Recency", "Frequency", "Monetary"]

# =====================================
# 2. CARREGAR DADOS
# =====================================

rfm = pd.read_csv(ARQUIVO_RFM)

X = rfm[variaveis].copy()

assert X.notna().all().all()
assert (X >= 0).all().all()
assert rfm["CustomerID"].is_unique

print("Clientes:", len(rfm))

# =====================================
# 3. CRIAR PIPELINE COMPLETO
# =====================================

pipeline = Pipeline([
    (
        "log",
        FunctionTransformer(np.log1p)
    ),
    (
        "scaler",
        StandardScaler()
    ),
    (
        "kmeans",
        KMeans(
            n_clusters=4,
            random_state=42,
            n_init=10
        )
    )
])

# =====================================
# 4. TREINAR MODELO FINAL
# =====================================

print("\nTreinando modelo final...")

pipeline.fit(X)

# =====================================
# 5. ATRIBUIR SEGMENTOS
# =====================================

rfm["Cluster"] = pipeline.predict(X)

nomes_clusters = {
    0: "Alto valor",
    1: "Inativos ou ocasionais",
    2: "Recentes de baixa frequencia",
    3: "Recorrentes intermediarios"
}

rfm["Segmento"] = (
    rfm["Cluster"].map(nomes_clusters)
)

# =====================================
# 6. VALIDAR PERFIS
# =====================================

perfil = rfm.groupby("Cluster").agg(
    Clientes=("CustomerID", "count"),
    Recency=("Recency", "median"),
    Frequency=("Frequency", "median"),
    Monetary=("Monetary", "median")
)

print("\nPERFIL DO MODELO FINAL:")
print(perfil.round(2).to_string())

# =====================================
# 7. SALVAR MODELO
# =====================================

caminho_modelo = (
    PASTA_MODELOS / "pipeline_kmeans.joblib"
)

joblib.dump(pipeline, caminho_modelo)

# =====================================
# 8. SALVAR CLIENTES SEGMENTADOS
# =====================================

caminho_clientes = (
    PASTA_RESULTADOS / "clientes_segmentados.csv"
)

rfm.to_csv(caminho_clientes, index=False)

print("\nModelo salvo em:", caminho_modelo)
print("Clientes salvos em:", caminho_clientes)

# =====================================
# 9. TESTAR REUTILIZACAO
# =====================================

modelo_carregado = joblib.load(caminho_modelo)

previsoes = modelo_carregado.predict(X)

assert np.array_equal(
    previsoes,
    rfm["Cluster"].to_numpy()
)

print("\nModelo salvo e recarregado com sucesso!")
