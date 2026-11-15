
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]

ARQUIVO = (
    BASE_DIR / "data" / "processed" /
    "transacoes_limpas.csv"
)

SAIDA = (
    BASE_DIR / "data" / "processed" /
    "clientes_rfm.csv"
)

print("Carregando transacoes...")

df = pd.read_csv(
    ARQUIVO,
    parse_dates=["InvoiceDate"],
    dtype={"InvoiceNo": str, "CustomerID": "int64"}
)

# Data de referencia:
# um dia depois da ultima transacao
data_referencia = (
    df["InvoiceDate"].max().normalize()
    + pd.Timedelta(days=1)
)

# Criar indicadores por cliente
rfm = df.groupby("CustomerID").agg(
    UltimaCompra=("InvoiceDate", "max"),
    Frequency=("InvoiceNo", "nunique"),
    Monetary=("TotalPrice", "sum")
)

# Recencia em dias
rfm["Recency"] = (
    data_referencia - rfm["UltimaCompra"]
).dt.days

# Reorganizar a tabela
rfm = rfm[
    ["Recency", "Frequency", "Monetary"]
].reset_index()

# Validacoes
assert rfm["CustomerID"].is_unique
assert (rfm["Recency"] >= 0).all()
assert (rfm["Frequency"] > 0).all()
assert (rfm["Monetary"] > 0).all()

# Salvar tabela RFM
rfm.to_csv(SAIDA, index=False)

print("\n--- ANALISE RFM ---")

print("\nQuantidade de clientes:")
print(len(rfm))

print("\nPrimeiros registros:")
print(rfm.head())

print("\nEstatisticas descritivas:")
print(
    rfm[["Recency", "Frequency", "Monetary"]]
    .describe()
    .round(2)
)

print("\nArquivo salvo em:", SAIDA)
