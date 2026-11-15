
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]

ARQUIVO = (
    BASE_DIR / "data" / "processed"
    / "transacoes_limpas.csv"
)

df = pd.read_csv(
    ARQUIVO,
    dtype={"StockCode": str, "InvoiceNo": str}
)

print("\n--- DIAGNOSTICO DO CATALOGO ---")

print("\nProdutos distintos por codigo:")
print(df["StockCode"].nunique())

print("\nDescricoes distintas:")
print(df["Description"].nunique())

print("\nNotas de compra distintas:")
print(df["InvoiceNo"].nunique())

print("\nProdutos sem descricao:")
print(df["Description"].isna().sum())

print("\n15 codigos com maior valor de compras:")
ranking = (
    df.groupby("StockCode", as_index=False)
    .agg(
        Descricao=("Description", "first"),
        Valor=("TotalPrice", "sum"),
        Quantidade=("Quantity", "sum")
    )
    .sort_values("Valor", ascending=False)
    .head(15)
)

print(ranking.to_string(index=False))

print("\nCodigos nao numericos mais frequentes:")
especiais = df[
    ~df["StockCode"].str.fullmatch(r"\d+", na=False)
]

print(
    especiais["StockCode"]
    .value_counts()
    .head(20)
    .to_string()
)

print("\nDiagnostico concluido!")
