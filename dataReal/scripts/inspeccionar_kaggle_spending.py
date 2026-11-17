"""Inspección: 'Credit Card Spending Habits in India' (Kaggle, thedevastator), ~26 000 transacciones de 2013-2015.

Archivo: _descartados/kaggle_credit_card_spending_india/credit_card_india.csv
Copia descargada de: https://github.com/gu12934/LHL_Final_Capstone_Project (data/credit_card_india.csv)
Original: https://www.kaggle.com/datasets/thedevastator/analyzing-credit-card-spending-habits-in-india

Es el único conjunto a nivel de transacción con Card_Type (Gold/Silver/Platinum/Signature),
Gender y categoría de gasto. Pero en Kaggle no se documenta de dónde salen los datos, así que el
script revisa si se comporta como datos reales o como datos generados.

Uso (desde la raíz del repo): .venv/bin/python -I dataReal/scripts/inspeccionar_kaggle_spending.py
"""
from pathlib import Path

import pandas as pd

F = Path(__file__).resolve().parent.parent / "_descartados" / "kaggle_credit_card_spending_india" / "credit_card_india.csv"
pd.set_option("display.width", 160, "display.float_format", "{:,.1f}".format)

df = pd.read_csv(F)
df["Date"] = pd.to_datetime(df["Date"], format="%d-%b-%y")
print("Dimensiones:", df.shape, "| fechas:", df["Date"].min().date(), "a", df["Date"].max().date())
print("Nulos:", df.isna().sum().sum(), "| duplicados:", df.drop(columns="index").duplicated().sum())
print("Ciudades:", df["City"].nunique())

for col in ["Card Type", "Gender", "Exp Type"]:
    print(f"\n{col} (%):\n", (df[col].value_counts(normalize=True) * 100).to_string())

print("\nMonto por transacción (₹):\n", df["Amount"].describe(percentiles=[.01, .25, .5, .75, .99]).to_string())
print("\nMonto mediano por tipo de tarjeta:\n", df.groupby("Card Type")["Amount"].median().to_string())
print("\nMonto mediano por categoría:\n", df.groupby("Exp Type")["Amount"].median().to_string())

# Señales de datos generados: distribución casi uniforme de categorías y montos sin relación con la categoría.
uni = df["Amount"].between(df["Amount"].quantile(.05), df["Amount"].quantile(.95))
print("\nHistograma de montos en 10 tramos iguales (5%-95%):")
print(pd.cut(df.loc[uni, "Amount"], 10).value_counts(sort=False).to_string())
tab = pd.crosstab(df["Card Type"], df["Exp Type"], normalize="index") * 100
print("\nMezcla de categorías por tipo de tarjeta (% fila):\n", tab.to_string())
print("\nTop 10 ciudades (% de transacciones):\n",
      (df["City"].value_counts(normalize=True).head(10) * 100).to_string())

print("""
VEREDICTO: DESCARTAR (casi con certeza es simulado, no real).
Evidencia que muestra la salida de arriba:
- Los montos son UNIFORMES: los 10 tramos iguales tienen casi la misma frecuencia (~2 300 cada uno).
  Un gasto real es muy asimétrico, con muchas compras pequeñas y pocas grandes.
- La mediana es ~₹153 000 por transacción, unas 40 veces el ticket real del RBI (~₹3 900), y es igual
  en todas las tarjetas y categorías. En la realidad, Signature y Platinum gastan más que Silver.
- Los 4 tipos de tarjeta salen ~25 % cada uno, y las 4 ciudades principales tienen exactamente 13.4 %.
- La mezcla de categorías es idéntica para todos los tipos de tarjeta.
Usarlo como "realidad" sería comparar un sintético contra otro sintético.
""")
