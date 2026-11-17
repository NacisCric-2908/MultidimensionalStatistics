"""Inspección: RBI Bank-wise ATM/POS/Card Statistics (mensual, por banco).

Archivos (espejo de India Data Portal de https://rbi.org.in/Scripts/ATMView.aspx):
  rbi_card_stats/bankwise_atm_pos_card_statistics_2022_onwards.csv  (2022-03 en adelante, valores en ₹ miles)
  rbi_card_stats/bankwise-atm-pos-card-statistics-20112022.csv      (2011-04 a 2022-02, valores en ₹ millones)

Variables del sintético que permite contrastar (a nivel PROMEDIO NACIONAL, no por cliente):
  Monthly_Spending        -> gasto mensual por tarjeta
  Monthly_Transactions    -> transacciones mensuales por tarjeta
  Avg_Transaction_Value   -> ticket promedio (valor / volumen)
  Online_Shopping_Spending (proporción) -> participación online en el gasto
  Cash_Advance_Amount     -> retiros en efectivo con tarjeta de crédito en ATM
  Card_Type (emisor)      -> concentración de tarjetas por banco

Uso (desde la raíz del repo): .venv/bin/python -I dataReal/scripts/inspeccionar_rbi_tarjetas.py
"""
from pathlib import Path

import pandas as pd

D = Path(__file__).resolve().parent.parent / "rbi_card_stats"
pd.set_option("display.width", 160, "display.float_format", "{:,.2f}".format)

# ---------- 2022 en adelante ----------
df = pd.read_csv(D / "bankwise_atm_pos_card_statistics_2022_onwards.csv", parse_dates=["date"])
print("=== RBI 2022+ ===")
print("Dimensiones:", df.shape, "| meses:", df["date"].min().date(), "a", df["date"].max().date(),
      "| bancos:", df["bank_name"].nunique())
print("Nulos por columna (cc_*):\n", df.filter(like="cc_").isna().sum().to_string())
# Problemas de calidad del espejo: mayo-2025 viene duplicado y '2026-01-03' es una copia mal fechada de 2026-03.
print("Filas duplicadas (fecha, banco):", df.duplicated(["date", "bank_name"]).sum(),
      "| fechas que no son día 1:", sorted(df.loc[df["date"].dt.day != 1, "date"].dt.date.unique()))
df = df[df["date"].dt.day == 1].drop_duplicates(["date", "bank_name"])
# En el espejo, las columnas de retiro en ATM tienen los nombres invertidos: '_val' trae el número de
# transacciones y '_vol' el valor (₹ miles); con el intercambio, el retiro promedio da ~₹4 000 (plausible).
df = df.rename(columns={"cc_cash_withdraw_atm_val": "cc_cash_withdraw_atm_vol",
                        "cc_cash_withdraw_atm_vol": "cc_cash_withdraw_atm_val",
                        "dc_cash_withdraw_atm_val": "dc_cash_withdraw_atm_vol",
                        "dc_cash_withdraw_atm_vol": "dc_cash_withdraw_atm_val"})

cc = df.groupby("date")[["credit_cards", "cc_pay_trns_at_pos_vol", "cc_pay_trns_at_pos_val",
                         "cc_pay_trns_online_vol", "cc_pay_trns_online_val", "cc_pay_trns_other_vol",
                         "cc_pay_trns_other_val", "cc_cash_withdraw_atm_vol", "cc_cash_withdraw_atm_val"]].sum()
vol = cc[["cc_pay_trns_at_pos_vol", "cc_pay_trns_online_vol", "cc_pay_trns_other_vol"]].sum(axis=1)
val = cc[["cc_pay_trns_at_pos_val", "cc_pay_trns_online_val", "cc_pay_trns_other_val"]].sum(axis=1) * 1000  # ₹
res = pd.DataFrame({
    "tarjetas_millones": cc["credit_cards"] / 1e6,
    "gasto_mensual_por_tarjeta_INR": val / cc["credit_cards"],
    "trans_mensuales_por_tarjeta": vol / cc["credit_cards"],
    "ticket_promedio_INR": val / vol,
    "ticket_POS_INR": cc["cc_pay_trns_at_pos_val"] * 1000 / cc["cc_pay_trns_at_pos_vol"],
    "ticket_online_INR": cc["cc_pay_trns_online_val"] * 1000 / cc["cc_pay_trns_online_vol"],
    "pct_gasto_online": 100 * cc["cc_pay_trns_online_val"] * 1000 / val,
    "avance_efectivo_por_tarjeta_INR": cc["cc_cash_withdraw_atm_val"] * 1000 / cc["credit_cards"],
    "retiro_ATM_promedio_INR": cc["cc_cash_withdraw_atm_val"] * 1000 / cc["cc_cash_withdraw_atm_vol"],
    "pct_tarjetas_con_retiro_aprox": 100 * cc["cc_cash_withdraw_atm_vol"] / cc["credit_cards"],
})
print("\nIndicadores nacionales por mes (tarjetas de crédito):")
print(res.iloc[::6].to_string())
ult = res.iloc[-12:].mean()
print("\nPromedio últimos 12 meses:\n", ult.to_string())

ultimo = df[df["date"] == df["date"].max()]
cuota = (ultimo.groupby("bank_name")["credit_cards"].sum().sort_values(ascending=False) /
         ultimo["credit_cards"].sum() * 100).head(10)
print("\nParticipación de tarjetas por emisor (último mes, %):\n", cuota.to_string())

# ---------- 2011-2022 ----------
h = pd.read_csv(D / "bankwise-atm-pos-card-statistics-20112022.csv", parse_dates=["date"])
print("\n=== RBI 2011-2022 ===")
print("Dimensiones:", h.shape, "| meses:", h["date"].min().date(), "a", h["date"].max().date())
hh = h.groupby("date")[["cc_outstanding_cards_eom", "cc_trans_pos", "cc_amt_pos", "cc_trans_atm", "cc_amt_atm"]].sum()
hres = pd.DataFrame({
    "tarjetas_millones": hh["cc_outstanding_cards_eom"] / 1e6,
    "ticket_POS_INR": hh["cc_amt_pos"] * 1e6 / hh["cc_trans_pos"],
    "gasto_POS_por_tarjeta_INR": hh["cc_amt_pos"] * 1e6 / hh["cc_outstanding_cards_eom"],
})
print(hres.iloc[::12].to_string())

print("""
VEREDICTO: SE QUEDA (fuente oficial, real, mensual, completa).
- Sirve para comparar promedios nacionales: gasto, número de transacciones y ticket por tarjeta,
  peso del canal online y retiros de efectivo.
- No trae variables del cliente (edad, ingreso, score). Es agregado por banco y no por persona.
- La serie 2011-2022 solo cuenta POS (sin online) y usa otra unidad (₹ millones), así que se usa solo para tendencia.
""")
