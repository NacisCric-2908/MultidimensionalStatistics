"""Reduce el CSV de 'Credit by Scheduled Commercial Banks' (RBI, BSR-1, ~227 MB) a las filas
de tarjetas de crédito personales ('Personal Credit Cards').

Fuente: RBI, Basic Statistical Returns (BSR-1), espejo en India Data Portal:
https://ckandev.indiadataportal.com/dataset/eb565ca6-aa06-47fd-9c81-05c7ed6c538b/resource/733d27c5-e6a7-4cbf-a03e-b7cda032b608/download/credit-by-scheduled-commercial-banks.csv

Uso (desde la raíz del repo):
  .venv/bin/python -I dataReal/scripts/filtrar_rbi_credito_tarjetas.py <csv_completo>
Salida: dataReal/rbi_credit_scb/rbi_bsr_tarjetas_credito_personales.csv
"""
import sys
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent.parent
entrada = Path(sys.argv[1]) if len(sys.argv) > 1 else BASE / "rbi_credit_scb" / "credit-by-scheduled-commercial-banks.csv"

partes = []
for trozo in pd.read_csv(entrada, chunksize=200_000):
    partes.append(trozo[trozo["occupation_sub_group"].str.contains("Credit Card", case=False, na=False)])
df = pd.concat(partes)
salida = BASE / "rbi_credit_scb" / "rbi_bsr_tarjetas_credito_personales.csv"
df.to_csv(salida, index=False)
print(f"{len(df):,} filas de tarjetas de crédito -> {salida}")
print("Años:", sorted(df["year"].unique()))
print("Subgrupos:", df["occupation_sub_group"].unique())
