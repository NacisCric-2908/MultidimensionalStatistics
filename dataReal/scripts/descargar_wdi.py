"""Descarga indicadores WDI del Banco Mundial para India: ingreso per cápita, distribución del ingreso,
estructura de edad y sexo de la población, empleo y tasa de cambio.

Uso (desde la raíz del repo):  .venv/bin/python -I dataReal/scripts/descargar_wdi.py
Salida: dataReal/worldbank_wdi_india/wdi_india.csv  (formato largo: indicador, nombre, anio, valor)
"""
from pathlib import Path

import pandas as pd
import requests

BASE = Path(__file__).resolve().parent.parent
API = "https://api.worldbank.org/v2/country/IND/indicator/{}"

INDICADORES = [
    "NY.GNP.PCAP.CN", "NY.GDP.PCAP.CN", "NY.ADJ.NNTY.PC.CN",           # ingreso per cápita en rupias
    "SI.DST.FRST.20", "SI.DST.02ND.20", "SI.DST.03RD.20", "SI.DST.04TH.20",
    "SI.DST.05TH.20", "SI.DST.10TH.10", "SI.DST.FRST.10", "SI.POV.GINI",  # distribución del ingreso
    "SP.POP.TOTL", "SP.POP.TOTL.FE.ZS", "SP.POP.1564.TO.ZS", "SP.POP.65UP.TO.ZS",
    "SL.TLF.CACT.FE.ZS", "SL.TLF.CACT.MA.ZS", "SL.EMP.SELF.ZS", "SL.EMP.WORK.ZS",
    "PA.NUS.FCRF", "FP.CPI.TOTL",                                         # tasa de cambio e IPC (deflactar)
] + [f"SP.POP.{g}.{s}" for g in ("1519", "2024", "2529", "3034", "3539", "4044", "4549",
                                   "5054", "5559", "6064", "6569", "70UP") for s in ("MA", "FE")]


def bajar(cod):
    for _ in range(3):
        try:
            r = requests.get(API.format(cod), params={"format": "json", "per_page": 100, "date": "2000:2025"},
                             timeout=60)
            r.raise_for_status()
            js = r.json()
            if len(js) < 2 or js[1] is None:
                return []
            return [{"indicador": cod, "nombre": d["indicator"]["value"], "anio": int(d["date"]),
                     "valor": d["value"]} for d in js[1] if d["value"] is not None]
        except requests.RequestException as e:
            print("  reintento", cod, type(e).__name__)
    print("  FALLÓ", cod)
    return []


filas = [f for cod in INDICADORES for f in bajar(cod)]
out = BASE / "worldbank_wdi_india"
out.mkdir(exist_ok=True)
pd.DataFrame(filas).sort_values(["indicador", "anio"]).to_csv(out / "wdi_india.csv", index=False)
print(len(filas), "filas ->", out / "wdi_india.csv")
