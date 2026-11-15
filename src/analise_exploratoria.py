
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parents[1]

arquivo = (
    BASE_DIR / "data" / "processed" /
    "transacoes_limpas.csv"
)

PASTA_GRAFICOS = BASE_DIR / "reports" / "figures"
PASTA_GRAFICOS.mkdir(parents=True, exist_ok=True)

print("Carregando dados tratados...")

df = pd.read_csv(
    arquivo,
    parse_dates=["InvoiceDate"]
)

sns.set_theme(style="whitegrid")

# =========================================
# GRAFICO 1 - EVOLUCAO MENSAL DAS VENDAS
# =========================================

df["Mes"] = df["InvoiceDate"].dt.to_period("M")

vendas_mensais = (
    df.groupby("Mes")["TotalPrice"]
    .sum()
)

plt.figure(figsize=(12, 5))

plt.plot(
    vendas_mensais.index.astype(str),
    vendas_mensais.values,
    marker="o"
)

plt.title("Evolucao mensal das vendas")
plt.xlabel("Mes")
plt.ylabel("Valor das compras (£)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    PASTA_GRAFICOS / "vendas_mensais.png",
    dpi=300
)

plt.show()

# =========================================
# GRAFICO 2 - PRODUTOS COM MAIOR FATURAMENTO
# =========================================

top_produtos = (
    df.groupby("Description")["TotalPrice"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12, 6))

sns.barplot(
    x=top_produtos.values,
    y=top_produtos.index
)

plt.title("10 produtos com maior faturamento")
plt.xlabel("Valor das compras (£)")
plt.ylabel("Produto")
plt.tight_layout()

plt.savefig(
    PASTA_GRAFICOS / "top_produtos.png",
    dpi=300
)

plt.show()

# =========================================
# GRAFICO 3 - PAISES COM MAIOR FATURAMENTO
# =========================================

top_paises = (
    df.groupby("Country")["TotalPrice"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12, 6))

sns.barplot(
    x=top_paises.values,
    y=top_paises.index
)

plt.title("10 paises com maior valor de compras")
plt.xlabel("Valor das compras (£)")
plt.ylabel("Pais")
plt.tight_layout()

plt.savefig(
    PASTA_GRAFICOS / "top_paises.png",
    dpi=300
)

plt.show()

print("\nAnalise exploratoria concluida!")
print("Graficos salvos em:", PASTA_GRAFICOS)
