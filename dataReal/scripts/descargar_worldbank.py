"""Descarga la base Global Findex 2025 (Banco Mundial) y se queda solo con India.

Global Findex es una encuesta real (~3 000 adultos por país) con rondas 2011, 2014, 2017, 2021 y 2024.
Trae, para India, tenencia y uso de tarjeta de crédito, pago total del saldo, préstamos, cuentas,
pagos digitales, etc., desagregado por sexo, edad, ingreso, educación, zona y situación laboral.

La API (api.worldbank.org) estaba sin responder al momento de armar esto, así que se usa el archivo masivo:
https://www.worldbank.org/en/publication/globalfindex/download-data

Uso (desde la raíz del repo):  .venv/bin/python -I dataReal/scripts/descargar_worldbank.py [csv_ya_descargado]
Salida: dataReal/worldbank_findex_india/findex_india.csv
"""
import sys
import tempfile
from pathlib import Path

import pandas as pd
import requests

BASE = Path(__file__).resolve().parent.parent
URL = ("https://thedocs.worldbank.org/en/doc/be6615202d1f08a25855c8ac2d615122-0050012025/"
       "related/GlobalFindexDatabase2025.csv")


def main():
    if len(sys.argv) > 1:
        origen = Path(sys.argv[1])
    else:
        origen = Path(tempfile.gettempdir()) / "GlobalFindexDatabase2025.csv"
        with requests.get(URL, stream=True, timeout=300) as r:
            r.raise_for_status()
            with open(origen, "wb") as f:
                for b in r.iter_content(1 << 20):
                    f.write(b)
    df = pd.read_csv(origen, low_memory=False)
    india = df[df["codewb"] == "IND"].dropna(axis=1, how="all")
    out = BASE / "worldbank_findex_india"
    out.mkdir(exist_ok=True)
    india.to_csv(out / "findex_india.csv", index=False)
    print(f"India: {india.shape[0]} filas x {india.shape[1]} columnas -> {out / 'findex_india.csv'}")


if __name__ == "__main__":
    main()
