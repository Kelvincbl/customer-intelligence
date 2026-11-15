
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
arquivo = BASE_DIR / "data" / "raw" / "Online Retail.xlsx"

print("Carregando dados...")
df = pd.read_excel(arquivo)

print("\n--- DIAGNOSTICO DOS DADOS ---")

print("\n1. Dimensoes da base:")
print(df.shape)

print("\n2. Registros duplicados:")
print(df.duplicated().sum())

print("\n3. Transacoes sem identificacao de cliente:")
print(df["CustomerID"].isna().sum())

print("\n4. Produtos sem descricao:")
print(df["Description"].isna().sum())

print("\n5. Quantidades negativas ou iguais a zero:")
print((df["Quantity"] <= 0).sum())

print("\n6. Precos negativos ou iguais a zero:")
print((df["UnitPrice"] <= 0).sum())

print("\n7. Linhas com notas de cancelamento:")
cancelamentos = df["InvoiceNo"].astype(str).str.startswith("C")
print(cancelamentos.sum())

print("\n8. Quantidade de clientes identificados:")
print(df["CustomerID"].nunique())

print("\n9. Periodo das transacoes:")
print("Inicio:", df["InvoiceDate"].min())
print("Fim:", df["InvoiceDate"].max())

print("\n10. Quantidade de paises:")
print(df["Country"].nunique())
