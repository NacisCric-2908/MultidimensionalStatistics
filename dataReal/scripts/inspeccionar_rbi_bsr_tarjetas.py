"""Inspección: RBI Basic Statistical Returns (BSR-1), rubro 'Personal Credit Cards'.

Archivo: rbi_credit_scb/rbi_bsr_tarjetas_credito_personales.csv (generado por filtrar_rbi_credito_tarjetas.py)
Nivel: distrito x grupo poblacional (rural/semiurbano/urbano/metro) x grupo de banco x año (2010-2023).
Unidades: no_of_accounts = número de cuentas de tarjeta; credit_limit y amount_outstanding en ₹ crore
(1 crore = 10 000 000). La unidad se comprueba abajo: con ₹ crore el cupo promedio da decenas de miles
a lakhs de rupias, que es lo plausible.

Variables del sintético que permite contrastar (promedios por cuenta):
  Credit_Limit         -> cupo promedio por cuenta = credit_limit / no_of_accounts
  Outstanding_Balance  -> saldo promedio por cuenta = amount_outstanding / no_of_accounts
  Credit_Utilization   -> utilización agregada = amount_outstanding / credit_limit
También permite ver diferencias urbano/rural, por estado y por tipo de banco.

Uso (desde la raíz del repo): .venv/bin/python -I dataReal/scripts/inspeccionar_rbi_bsr_tarjetas.py
"""
from pathlib import Path

import pandas as pd

F = Path(__file__).resolve().parent.parent / "rbi_credit_scb" / "rbi_bsr_tarjetas_credito_personales.csv"
pd.set_option("display.width", 160, "display.float_format", "{:,.2f}".format)
CRORE = 1e7

df = pd.read_csv(F)
print("Dimensiones:", df.shape, "| años:", df["year"].min(), "-", df["year"].max(),
      "| distritos:", df["district_name"].nunique())
print("Nulos:\n", df[["no_of_accounts", "credit_limit", "amount_outstanding"]].isna().sum().to_string())
print("Filas con cupo 0 o cuentas 0:", ((df["credit_limit"] == 0) | (df["no_of_accounts"] == 0)).sum())


def resumen(g):
    s = g[["no_of_accounts", "credit_limit", "amount_outstanding"]].sum()
    return pd.Series({
        "cuentas_millones": s["no_of_accounts"] / 1e6,
        "cupo_prom_INR": s["credit_limit"] * CRORE / s["no_of_accounts"],
        "saldo_prom_INR": s["amount_outstanding"] * CRORE / s["no_of_accounts"],
        "utilizacion": s["amount_outstanding"] / s["credit_limit"],
    })


print("\nNacional por año:")
print(df.groupby("year").apply(resumen, include_groups=False).to_string())
ult = df[df["year"] == df["year"].max()]
print(f"\n{df['year'].max()} por grupo poblacional:")
print(ult.groupby("population_group").apply(resumen, include_groups=False).to_string())
print(f"\n{df['year'].max()} por grupo de banco:")
print(ult.groupby("bank_group").apply(resumen, include_groups=False).to_string())
print(f"\n{df['year'].max()} top 10 estados por número de cuentas:")
print(ult.groupby("state_name").apply(resumen, include_groups=False)
      .sort_values("cuentas_millones", ascending=False).head(10).to_string())

# Distribución entre celdas (distrito x grupo) del cupo promedio: da idea de la dispersión geográfica.
c = ult[ult["no_of_accounts"] >= 100].assign(cupo=lambda x: x["credit_limit"] * CRORE / x["no_of_accounts"],
                                             util=lambda x: x["amount_outstanding"] / x["credit_limit"])
print("\nDispersión entre celdas distrito-grupo (>=100 cuentas):")
print(c[["cupo", "util"]].describe(percentiles=[.1, .25, .5, .75, .9]).to_string())

print("""
VEREDICTO: SE QUEDA (fuente oficial, real, muy granular).
- Es la única fuente pública con CUPO y SALDO reales de tarjetas, así que permite calcular la utilización real.
- Es agregada por celda distrito-banco, no por cliente: compara promedios y la dispersión geográfica,
  no la distribución individual.
- Llega hasta 2023 y los montos están en rupias nominales.
""")
