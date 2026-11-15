
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Caminhos
BASE_DIR = Path(__file__).resolve().parents[1]

ARQUIVO = BASE_DIR / "data" / "processed" / "clientes_rfm.csv"

PASTA_GRAFICOS = BASE_DIR / "reports" / "figures"
PASTA_GRAFICOS.mkdir(parents=True, exist_ok=True)

# Carregar dados
rfm = pd.read_csv(ARQUIVO)

variaveis = ["Recency", "Frequency", "Monetary"]

sns.set_theme(style="whitegrid")

# Distribuicoes originais
fig, axes = plt.subplots(1, 3, figsize=(17, 5))

for ax, coluna in zip(axes, variaveis):
    sns.histplot(
        data=rfm,
        x=coluna,
        bins=40,
        ax=ax
    )

    ax.set_title(f"Distribuicao de {coluna}")
    ax.set_xlabel(coluna)
    ax.set_ylabel("Numero de clientes")

plt.tight_layout()

plt.savefig(
    PASTA_GRAFICOS / "distribuicoes_rfm.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# Boxplots
fig, axes = plt.subplots(1, 3, figsize=(17, 5))

for ax, coluna in zip(axes, variaveis):
    sns.boxplot(
        data=rfm,
        y=coluna,
        ax=ax
    )

    ax.set_title(f"Boxplot de {coluna}")

plt.tight_layout()

plt.savefig(
    PASTA_GRAFICOS / "boxplots_rfm.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# Assimetria
print("\n--- ASSIMETRIA DOS INDICADORES ---")
print(rfm[variaveis].skew().round(3))

# Estatisticas adicionais
print("\n--- PERCENTIS ---")
print(
    rfm[variaveis]
    .quantile([0.90, 0.95, 0.99])
    .round(2)
)
