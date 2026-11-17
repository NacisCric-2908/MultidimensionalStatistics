"""Inspección: Global Findex 2025 (Banco Mundial), India, rondas 2011-2024.

Archivo: worldbank_findex_india/findex_india.csv (generado por descargar_worldbank.py)
Diccionario: worldbank_findex_india/GlobalFindex2025-glossary.xlsx
Los valores son proporciones (0-1) de la población adulta (15+) de India, salvo las columnas *_s
(que son proporción dentro de un subgrupo).

Variables del sintético que permite contrastar:
  Payment_Ratio  -> fin22h / fin22g = de quienes usaron tarjeta de crédito, cuántos pagaron TODO el saldo
  Mobile_App_Login (contexto) -> fin9b (revisó su saldo por celular/internet), con smartphone, uso de internet
  Contexto de penetración: fin10 (tiene tarjeta de crédito), fin22g (la usó)
OJO: en esta base agregada India solo trae las cifras de tarjeta de crédito para el total país, no por
sexo, edad o ingreso (la muestra es muy pequeña). Para eso hacen falta los microdatos (registro gratuito en
https://microdata.worldbank.org, catálogo 'Global Financial Inclusion (Global Findex) Database 2025 - India').

Uso (desde la raíz del repo): .venv/bin/python -I dataReal/scripts/inspeccionar_findex.py
"""
from pathlib import Path

import pandas as pd

D = Path(__file__).resolve().parent.parent / "worldbank_findex_india"
pd.set_option("display.width", 160, "display.float_format", "{:.3f}".format)

df = pd.read_csv(D / "findex_india.csv")
glos = pd.read_excel(D / "GlobalFindex2025-glossary.xlsx")
nombres = dict(zip(glos["Series"].str.replace(".", "_", regex=False), glos["Indicator name"]))
print("Dimensiones:", df.shape, "| rondas:", sorted(df["year"].unique()))

cols = ["fin10", "fin22g", "fin22h", "account_t_d", "borrow_any_t_d", "fin22a", "fin26b", "fin9b",
        "con9a", "internet"]
tot = df[df["group"] == "all"].set_index("year")[cols]
print("\nTotal India (proporción de adultos 15+):")
for c in cols:
    print(f"  {c:16s} {nombres.get(c, '')[:85]}")
print(tot.T.to_string())

tot["pct_paga_total_entre_usuarios"] = 100 * tot["fin22h"] / tot["fin22g"]
print("\n% de usuarios de tarjeta de crédito que pagan el saldo completo a tiempo (fin22h/fin22g):")
print(tot["pct_paga_total_entre_usuarios"].dropna().round(1).to_string())

print("\nDesagregados disponibles (2024) para préstamos formales (fin22a), sí publicados por subgrupo:")
print(df[df["year"] == 2024].set_index(["group", "group2"])[["fin22a", "account_t_d", "fin9b"]].to_string())

print("""
VEREDICTO: SE QUEDA (encuesta oficial real, pero de cobertura limitada para tarjetas).
- Da el contexto de que solo ~4.6 % de los adultos indios tienen tarjeta de crédito (2024): la población
  del sintético es una élite financiera, no "el indio promedio".
- fin22h/fin22g aproxima el comportamiento de pago total, para comparar con Payment_Ratio
  (en el sintético, la proporción de clientes con Payment_Ratio = 1).
- No da sexo, edad ni ingreso de los tarjetahabientes en la versión agregada; para eso hacen falta los microdatos.
""")
