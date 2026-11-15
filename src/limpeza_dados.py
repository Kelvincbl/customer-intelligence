from pathlib import Path
import pandas as pd

# 1. Definir os caminhos
BASE_DIR = Path(__file__).resolve().parents[1]

ARQUIVO_ORIGINAL = (
    BASE_DIR / "data" / "raw" / "Online Retail.xlsx"
)

PASTA_PROCESSADA = BASE_DIR / "data" / "processed"
PASTA_PROCESSADA.mkdir(parents=True, exist_ok=True)

# 2. Carregar a base original
print("Carregando base original...")
df = pd.read_excel(ARQUIVO_ORIGINAL)

total_original = len(df)

# 3. Remover duplicatas exatas
df = df.drop_duplicates().copy()
print("Apos remover duplicatas:", len(df))

# 4. Manter clientes identificados
df = df.dropna(subset=["CustomerID"]).copy()
print("Apos filtrar clientes identificados:", len(df))

# 5. Identificar e separar cancelamentos
df["Cancelamento"] = (
    df["InvoiceNo"]
    .astype(str)
    .str.upper()
    .str.startswith("C")
)

cancelamentos = df[df["Cancelamento"]].copy()

print("Linhas de cancelamento:", len(cancelamentos))

# 6. Manter somente compras regulares
df = df[~df["Cancelamento"]].copy()

# 7. Filtrar quantidades e precos validos
df = df[
    (df["Quantity"] > 0) &
    (df["UnitPrice"] > 0)
].copy()

# 8. Padronizar identificadores
df["CustomerID"] = df["CustomerID"].astype("int64")

# 9. Criar valor monetario da linha
df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

# 10. Salvar dados tratados
ARQUIVO_FINAL = (
    PASTA_PROCESSADA / "transacoes_limpas.csv"
)

df.to_csv(ARQUIVO_FINAL, index=False)

# 11. Apresentar resultados
print("\n--- RESULTADO DA LIMPEZA ---")
print("Registros originais:", total_original)
print("Registros finais:", len(df))
print("Registros removidos:", total_original - len(df))
print("Clientes identificados:", df["CustomerID"].nunique())
print("Valor total de compras:", round(df["TotalPrice"].sum(), 2))
print("Arquivo salvo em:", ARQUIVO_FINAL)
