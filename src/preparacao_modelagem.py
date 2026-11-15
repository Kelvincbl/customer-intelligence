
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parents[1]

ARQUIVO = BASE_DIR / "data" / "processed" / "clientes_rfm.csv"

PASTA_SAIDA = BASE_DIR / "data" / "processed"
PASTA_GRAFICOS = BASE_DIR / "reports" / "figures"

PASTA_SAIDA.mkdir(parents=True, exist_ok=True)
PASTA_GRAFICOS.mkdir(parents=True, exist_ok=True)

# 1. Carregar os indicadores RFM
rfm = pd.read_csv(ARQUIVO)

variaveis = ["Recency", "Frequency", "Monetary"]

X = rfm[variaveis].copy()

# 2. Transformacao logaritmica
X_log = np.log1p(X)

# 3. Padronizacao
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_log)

# 4. Criar DataFrame padronizado
rfm_scaled = pd.DataFrame(
    X_scaled,
    columns=variaveis
)

rfm_scaled.insert(
    0,
    "CustomerID",
    rfm["CustomerID"].values
)

# 5. Salvar dados preparados
saida = PASTA_SAIDA / "clientes_rfm_scaled.csv"

rfm_scaled.to_csv(saida, index=False)

# 6. Exibir estatisticas
print("\n--- ESTATISTICAS APOS LOG1P ---")
print(X_log.describe().round(3))

print("\n--- ESTATISTICAS APOS PADRONIZACAO ---")
print(
    rfm_scaled[variaveis]
    .describe()
    .round(3)
)

print("\n--- ASSIMETRIA ORIGINAL ---")
print(X.skew().round(3))

print("\n--- ASSIMETRIA APOS LOG1P ---")
print(X_log.skew().round(3))

# 7. Comparar distribuicoes
fig, axes = plt.subplots(2, 3, figsize=(16, 9))

for i, coluna in enumerate(variaveis):

    sns.histplot(
        X[coluna],
        bins=40,
        ax=axes[0, i]
    )

    axes[0, i].set_title(
        f"{coluna} - Original"
    )

    sns.histplot(
        X_log[coluna],
        bins=40,
        ax=axes[1, i]
    )

    axes[1, i].set_title(
        f"{coluna} - Log1p"
    )

plt.tight_layout()

plt.savefig(
    PASTA_GRAFICOS / "comparacao_transformacoes_rfm.png",
    dpi=300
)

plt.show()

print("\nDados preparados com sucesso!")
print("Arquivo salvo em:", saida)
