
from pathlib import Path
import subprocess
import sys

from baixar_dados import baixar_base

BASE_DIR = Path(__file__).resolve().parents[1]
PASTA_SRC = BASE_DIR / "src"


def executar_preparacao():
    print("\n--- PREPARACAO DO PROJETO ---")

    # Verificar ou baixar a base original
    baixar_base()

    etapas = [
        "limpeza_dados.py",
        "analise_rfm.py",
        "modelo_final.py"
    ]

    for etapa in etapas:
        print(f"\nExecutando: {etapa}", flush=True)

        subprocess.run(
            [sys.executable, str(PASTA_SRC / etapa)],
            cwd=BASE_DIR,
            check=True
        )

    print("\nPreparacao concluida com sucesso!")


if __name__ == "__main__":
    executar_preparacao()
