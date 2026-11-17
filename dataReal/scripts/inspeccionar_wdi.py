"""Inspección: World Development Indicators (Banco Mundial) para India.

Archivo: worldbank_wdi_india/wdi_india.csv (generado por descargar_wdi.py; formato largo)

Variables del sintético que permite contextualizar (población general, NO tarjetahabientes):
  Annual_Income -> INB per cápita en rupias y participación del ingreso por quintil/decil
  Age, Gender   -> pirámide de población adulta por grupo quinquenal y sexo
  Para deflactar o convertir montos: IPC (FP.CPI.TOTL) y tasa de cambio INR/USD (PA.NUS.FCRF)

Uso (desde la raíz del repo): .venv/bin/python -I dataReal/scripts/inspeccionar_wdi.py
"""
from pathlib import Path

import pandas as pd

F = Path(__file__).resolve().parent.parent / "worldbank_wdi_india" / "wdi_india.csv"
pd.set_option("display.width", 160, "display.float_format", "{:,.2f}".format)

df = pd.read_csv(F)
print("Filas:", len(df), "| indicadores:", df["indicador"].nunique(), "| años:", df["anio"].min(), "-", df["anio"].max())
ancho = df.pivot_table(index="anio", columns="indicador", values="valor")

print("\nÚltimo valor disponible de cada indicador:")
ult = df.sort_values("anio").groupby("indicador").last()
print(ult[["nombre", "anio", "valor"]].to_string())

if "NY.GNP.PCAP.CN" in ancho:
    inb = ancho["NY.GNP.PCAP.CN"].dropna()
    print(f"\nINB per cápita {inb.index[-1]}: ₹{inb.iloc[-1]:,.0f} al año. La media de Annual_Income del sintético "
          f"(₹1 479 318) equivale a {1479318 / inb.iloc[-1]:.1f} veces ese valor.")

pob = df[df["indicador"].str.match(r"SP\.POP\.\d{2}(\d{2}|UP)\.(MA|FE)$")]
if not pob.empty:
    a = pob["anio"].max()
    p = pob[pob["anio"] == a].copy()
    p["grupo"] = p["indicador"].str.extract(r"SP\.POP\.(\w+)\.")[0]
    p["sexo"] = p["indicador"].str[-2:]
    tabla = p.pivot_table(index="grupo", columns="sexo", values="valor", aggfunc="sum")
    print(f"\nPirámide {a} (población, valores tal como vienen; algunos indicadores son % del sexo):")
    print(tabla.to_string())

print("""
VEREDICTO: SE QUEDA COMO CONTEXTO.
- Muestra cuánto se aleja el ingreso del sintético del indio promedio, y sirve para deflactar y convertir.
- No describe tarjetahabientes. Con Findex (4.6 % de los adultos tiene tarjeta) se ve que la población
  de la tarjeta es la cola alta de la distribución.
""")
