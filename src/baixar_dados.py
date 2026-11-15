
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile
import io

BASE_DIR = Path(__file__).resolve().parents[1]

PASTA_DADOS = BASE_DIR / "data" / "raw"
PASTA_DADOS.mkdir(parents=True, exist_ok=True)

DESTINO = PASTA_DADOS / "Online Retail.xlsx"

URL = (
    "https://archive.ics.uci.edu/static/public/"
    "352/online+retail.zip"
)


def baixar_base():
    if DESTINO.exists() and DESTINO.stat().st_size > 0:
        print("Base original ja existe.")
        return DESTINO

    print("Baixando base oficial da UCI...")

    with urlopen(URL, timeout=120) as resposta:
        conteudo = resposta.read()

    with ZipFile(io.BytesIO(conteudo)) as zip_ref:
        arquivos = [
            nome for nome in zip_ref.namelist()
            if nome.lower().endswith(".xlsx")
        ]

        if not arquivos:
            raise FileNotFoundError(
                "Arquivo Excel nao encontrado no ZIP."
            )

        with zip_ref.open(arquivos[0]) as origem:
            with DESTINO.open("wb") as destino:
                import shutil
                shutil.copyfileobj(origem, destino)

    print("Download concluido!")
    print("Arquivo:", DESTINO)

    return DESTINO


if __name__ == "__main__":
    baixar_base()
