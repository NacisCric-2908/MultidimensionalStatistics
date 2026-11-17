"""Inspección: RBI Mobile Banking Statistics (mensual, por banco, 2011-2025).

Archivo: rbi_mobile_banking/mobile-banking-statistics.csv
Espejo de India Data Portal (fuente: RBI, estadísticas de sistemas de pago):
https://ckandev.indiadataportal.com/dataset/eb565ca6-aa06-47fd-9c81-05c7ed6c538b/resource/7db4c888-ac0c-4820-9982-c4ea04307f4b/download/mobile-banking-statistics.csv

Variable del sintético que permite contrastar (como PROXY, no equivalente):
  Mobile_App_Login -> transacciones de banca móvil por cliente activo al mes.
  En el sintético, Mobile_App_Login son ingresos a la app de la tarjeta (2-71/mes, media 33). Aquí son
  transacciones de banca móvil de TODOS los clientes bancarios (incluye pagos UPI hechos desde la app del
  banco), no solo de tarjetahabientes, y un ingreso a la app no implica una transacción.

Uso (desde la raíz del repo): .venv/bin/python -I dataReal/scripts/inspeccionar_mobile_banking.py
"""
from pathlib import Path

import pandas as pd

F = Path(__file__).resolve().parent.parent / "rbi_mobile_banking" / "mobile-banking-statistics.csv"
pd.set_option("display.width", 160, "display.float_format", "{:,.1f}".format)

df = pd.read_csv(F, parse_dates=["month"])
print("Dimensiones:", df.shape, "| meses:", df["month"].min().date(), "a", df["month"].max().date(),
      "| bancos:", df["bank_name"].nunique())
print("% nulos en clientes activos:", round(100 * df["no_of_active_costumers"].isna().mean(), 1),
      "(la serie de clientes activos empieza más tarde)")
print("Duplicados (mes, banco):", df.duplicated(["month", "bank_name"]).sum(), "-> se quedan con la última fila")
df = df.drop_duplicates(["month", "bank_name"], keep="last")

m = (df.dropna(subset=["no_of_active_costumers"])
       .groupby("month")[["no_of_transactions", "no_of_active_costumers"]].sum())
m["trans_por_cliente_activo_mes"] = m["no_of_transactions"] / m["no_of_active_costumers"]
m["clientes_activos_millones"] = m["no_of_active_costumers"] / 1e6
print("\nNacional (solo bancos que reportan clientes activos):")
print(m[["clientes_activos_millones", "trans_por_cliente_activo_mes"]].iloc[::6].to_string())
print("\nÚltimos 12 meses, transacciones por cliente activo al mes:",
      round(m["trans_por_cliente_activo_mes"].iloc[-12:].mean(), 1))

# Unidad del monto inconsistente entre meses (saltos de x100): se muestra para advertir.
amt = df.groupby("month")["amt_of_transactions"].sum()
print("\nMonto total (unidad inconsistente, NO usar sin limpiar):\n", amt.iloc[-8:].to_string())

print("""
VEREDICTO: SE QUEDA COMO PROXY DÉBIL de Mobile_App_Login.
- Es real y oficial, y da un orden de magnitud: cuántas veces al mes interactúa transaccionalmente un
  usuario activo de banca móvil.
- No es lo mismo que "logins a la app de la tarjeta" y no está restringido a tarjetahabientes.
- La columna de monto cambia de unidad entre meses (saltos de x100): usar solo número de transacciones
  y clientes activos.
""")
