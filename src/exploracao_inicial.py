
from pathlib import Path
import pandas as pd

# Caminho da pasta principal do projeto
BASE_DIR = Path(__file__).resolve().parents[1]

# Arquivo com os dados de clientes
arquivo = BASE_DIR / "data" / "raw" / "Online Retail.xlsx"

# Leitura dos dados
print("Carregando a base de dados...")
df = pd.read_excel(arquivo)

print("\nBase carregada com sucesso!")

print("\nDimensões (linhas, colunas):")
print(df.shape)

print("\nPrimeiros 5 registros:")
print(df.head())

print("\nColunas disponíveis:")
print(df.columns.tolist())

print("\nValores ausentes por coluna:")
print(df.isnull().sum())

print("\nQuantidade de registros duplicados:")
print(df.duplicated().sum())
