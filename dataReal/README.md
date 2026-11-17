# dataReal — datos reales de India para contrastar el dataset sintético

Fuentes reales y verificables para comparar contra `data/bronze/synthetic_credit_card_customer_behavior_dataset.csv`.
No existe una base pública real de India **a nivel de cliente** con estas variables. Por eso casi todas las
comparaciones son contra **promedios, proporciones y distribuciones agregadas** del país o de un emisor.

Fecha de descarga: 16-nov-2026. Todos los scripts se corren desde la raíz del repo con el entorno del proyecto:

```bash
.venv/bin/python -I dataReal/scripts/<script>.py
```

(La primera vez se instalaron `pandas openpyxl xlrd pypdf requests` en `.venv`.)

---

## 1. Inventario y veredicto

| Carpeta | Fuente (institución) | Periodo | Nivel | Formato | Script de inspección | Veredicto |
|---|---|---|---|---|---|---|
| `rbi_card_stats/` | **RBI** — Bank-wise ATM/POS/Card Statistics (espejo de India Data Portal) | 2011-04 → 2026-03, mensual | Banco × mes | CSV | `inspeccionar_rbi_tarjetas.py` | ✅ **Se queda.** Es la mejor fuente para gasto, transacciones y ticket |
| `rbi_credit_scb/` | **RBI** — Basic Statistical Returns (BSR-1), rubro *Personal Credit Cards* | 2010 → 2023, anual | Distrito × grupo poblacional × tipo de banco | CSV (filtrado) | `inspeccionar_rbi_bsr_tarjetas.py` | ✅ **Se queda.** Es la única fuente con cupo y saldo reales |
| `sbi_card_investor_presentations/` | **SBI Card** (2.º emisor, ~19 % del mercado), presentaciones a inversionistas | Q4 FY25, Q4 FY26, Q1 FY27 | Emisor (cartera completa) | PDF (+ .txt extraído) | `inspeccionar_pdfs.py` | ✅ **Se queda.** Trae perfil de edad, ocupación, mezcla de saldo (transactor/revolver/EMI) y morosidad |
| `crif_highmark_reports/` | **CRIF High Mark** (buró de crédito) — *How India Lends*, *The Credit Goes to Her* | FY24 → dic-2025 | Mercado | PDF (+ .txt) | `inspeccionar_pdfs.py` | ✅ **Se queda.** Trae saldo total del mercado, cuentas activas y morosidad de tarjetas |
| `worldline_digital_payments/` | **Worldline India** — Digital Payments Report 1H 2025 | ene-2024 → jun-2025 | Mercado | PDF (+ .txt) | `inspeccionar_pdfs.py` | ✅ **Se queda** (complemento): ticket POS y online, principales categorías de comercio |
| `worldbank_findex_india/` | **Banco Mundial** — Global Findex 2025 (encuesta) | 2011, 2014, 2017, 2021, 2024 | País (y algunos subgrupos) | CSV + glosario XLSX | `inspeccionar_findex.py` | ✅ **Se queda.** Da penetración (% adultos con tarjeta) y % que paga el saldo completo |
| `rbi_mobile_banking/` | **RBI** — Mobile Banking Statistics (espejo IDP) | 2011 → 2025-12, mensual | Banco × mes | CSV | `inspeccionar_mobile_banking.py` | ⚠️ **Proxy débil** de `Mobile_App_Login` |
| `mospi_plfs_2023_24/` | **MoSPI** — PLFS: nota de prensa del informe anual 2023-24 y boletín trimestral abr-jun 2024 | 2023-24 | País | PDF (+ .txt) | `inspeccionar_pdfs.py` | ⚠️ **Contexto.** Distribución por tipo de empleo; los ingresos de la población general **no** son los de tarjetahabientes |
| `worldbank_wdi_india/` | **Banco Mundial** — World Development Indicators | 2000 → 2025 | País | CSV | `descargar_wdi.py` | ⚠️ **Contexto.** Ingreso per cápita, quintiles, pirámide de edad, tasa de cambio e IPC (para deflactar) |
| `_descartados/kaggle_credit_card_spending_india/` | Kaggle *Credit Card Spending Habits in India* | 2013-2015 | Transacción | CSV | `inspeccionar_kaggle_spending.py` | ❌ **Descartado.** Es casi con certeza simulado: montos uniformes, ~25 % por tipo de tarjeta, medianas idénticas |

Scripts de descarga o filtrado: `descargar_worldbank.py` (Findex), `descargar_wdi.py` (WDI) y
`filtrar_rbi_credito_tarjetas.py` (reduce el CSV BSR de 227 MB a las 39 444 filas de tarjetas; el original se borró).

### Problemas de calidad detectados (y corregidos en los scripts)
- **RBI card stats 2022+**: mayo-2025 viene duplicado y la fecha `2026-01-03` es una copia mal fechada de marzo-2026.
  Además, en las columnas de retiro en ATM, los nombres `_val` y `_vol` están **invertidos** en el espejo.
- **RBI card stats**: los montos van en **₹ miles** (2022+) y en **₹ millones** (2011-2022). Se comprobó con el
  ticket POS: da ₹2 936, y Worldline reporta ₹3 031 para 1H 2025.
- **RBI BSR**: los montos van en **₹ crore**. Maharashtra concentra el 42 % de las cuentas porque muchos bancos las
  registran en su sede de Mumbai, no en el domicilio del cliente.
- **RBI mobile banking**: 167 filas duplicadas y la columna de monto cambia de unidad entre meses (saltos de x100).
  Se usa solo número de transacciones y clientes activos.
- **Findex**: India no publica las cifras de tarjeta de crédito por sexo, edad ni ingreso en la base agregada.

---

## 2. Cobertura por variable del sintético

Los valores reales son los que dan los scripts y los PDF. **Verifiquen las cifras de PDF en la página indicada**,
porque el texto se extrajo automáticamente de gráficos.

| Variable sintética | Sintético | Valor real | Fuente | ¿Comparable? |
|---|---|---|---|---|
| `Age` | ≤30: 38.4 % · 31-45: 40.4 % · >45: 21.2 % | Tarjetas vigentes SBI Card (mar-26): <30: 19 % · 31-45: 55 % · >45: 26 %. Nuevas cuentas: 30 / 50 / 20 % | SBI Card abr-2026, p.15 | Sí (un emisor) |
| `Gender` | M 55.2 % · F 44.8 % | Solo hay contexto: CRIF dice que las mujeres crecen más rápido "desde una base pequeña" en tarjetas; el Findex por sexo no está publicado para India | CRIF *Credit Goes to Her* mar-2026, p.6 | Parcial. Para la cifra exacta: microdatos de Findex o CIBIL |
| `Occupation` | Empleado privado + público: 57.1 % · Independiente + empresario: 27.0 % · Jubilado + estudiante: 15.9 % | Nuevas cuentas SBI Card: asalariados 61 % · independientes 39 %. Asalariados por empleador: Gobierno/PSU 34 %, Cat A 24 %, Cat B 42 % | SBI Card Q4 FY25, p.15 | Sí (agrupando categorías) |
| `Annual_Income` | Media ₹14.8 lakh, mediana ₹11.3 lakh | Población general (no tarjetahabientes): ingreso mensual de asalariados ~₹20 700 y de independientes ~₹13 300 (PLFS 2023-24, citado en el Economic Survey 2024-25; **verificar**). Ingreso per cápita y quintiles en WDI | PLFS / WDI | Solo contexto. Sirve para mostrar que el sintético representa la parte más rica de la distribución |
| `Card_Type` | Gold 33.8 % … Signature 5 % | No hay estadística pública por variante de tarjeta. Sí hay concentración por emisor: HDFC 22 %, SBI 19 %, ICICI 16 %, Axis 14 % | RBI card stats | No directo |
| `Credit_Limit` | Media ₹7.1 lakh, mediana ₹3.96 lakh | Cupo promedio por cuenta en 2023: **₹1.34 lakh** (P10-P90 entre distritos: ₹73 k – ₹184 k) | RBI BSR | Sí (promedio) |
| `Card_Age_Months` | Media 53.6 | No encontrado | — | No |
| `Monthly_Spending` | Media ₹73 872 | **₹17 271** por tarjeta al mes (promedio de los últimos 12 meses, todas las tarjetas). SBI Card: gasto minorista ~₹1.64 lakh por tarjeta al año (~₹13.7 k al mes) | RBI card stats; SBI p.8 | Sí |
| `Monthly_Transactions` | Media 83 | **4.4** transacciones por tarjeta al mes | RBI card stats | Sí |
| `Avg_Transaction_Value` | Media ₹836 (agregado: ₹890) | **₹3 928** en total · POS ₹2 936 · online ₹4 959. Worldline 1H25: POS ₹3 031, online ₹5 330 | RBI; Worldline p.20 | Sí |
| `Online_Shopping_Spending` y demás categorías | Online 15 %, supermercado 24 %, servicios 16 %, combustible 14 %, restaurantes 12 %, entretenimiento 10 %, viajes 8 % | Canal online = **62.5 %** del gasto (RBI y SBI FY26). En POS (todas las tarjetas, Worldline): supermercado, restaurantes, ropa, hospitales, hoteles, farmacias, joyería y tiendas por departamento suman el 62 % del volumen | RBI; SBI p.9; Worldline p.28-29 | Parcial: el "online" del sintético es una categoría y el del RBI es un canal |
| `International_Transactions` | 40.7 % con al menos una | No encontrado en fuentes abiertas | — | No |
| `Outstanding_Balance` | Media ₹3.03 lakh | Saldo por cuenta: **₹28 k** (RBI BSR 2023). SBI Card: ₹25.8 k por tarjeta (mar-26). CRIF: ₹3.42 lakh crore / 109 M tarjetas ≈ ₹31 k (dic-25) | RBI BSR; SBI p.8; CRIF feb-26 p.5 | Sí |
| `Statement_Balance`, `Payment_Amount` | Medias ₹3.66 lakh / ₹2.79 lakh | No publicado directamente | — | No |
| `Payment_Ratio` | 3.4 % con PR = 1; 35.5 % con PR ≥ 0.95 | Findex 2024: **87 %** de quienes usaron tarjeta pagaron todo a tiempo. SBI Card: saldo = transactor 46 % · revolver 22 % · EMI 32 % | Findex; SBI p.8 | Sí (con matices de definición) |
| `Credit_Utilization` | Media 0.43 (agregado 0.43) | **0.21** agregado nacional (2023). Mediana entre distritos: 0.25 | RBI BSR | Sí |
| `Cash_Advance_Amount` | 29.7 % lo usa | ~**0.6 %** de las tarjetas hace un retiro en ATM al mes; retiro promedio ₹5 580 | RBI card stats | Sí (aprox.) |
| `EMI_Count` | 83.7 % con al menos 1 EMI | 32 % del saldo de SBI Card está en EMI; CRIF habla de un giro hacia productos EMI | SBI p.8; CRIF p.50 | Parcial |
| `Reward_Points_*` | — | No hay estadística pública | — | No |
| `Mobile_App_Login` | Media 33 al mes | ~**67** transacciones de banca móvil por cliente activo al mes (2025, incluye UPI; no son logins) | RBI mobile banking | Proxy débil |
| `Credit_Score` | Media 629, mediana 638 | No se pudo descargar: los PDF de TransUnion CIBIL devuelven 403. Morosidad como referencia de riesgo: PAR 31-90 de tarjetas 2.1 % (CRIF dic-25), GNPA SBI Card 2.41 % | CRIF p.51-53; SBI p.4 | Parcial |
| Contexto de penetración | 50 000 clientes | Solo el **4.6 %** de los adultos indios tiene tarjeta de crédito (2024). Hay 114-118 M de tarjetas | Findex; RBI | Clave para interpretar |

### Lectura rápida (sin hacer el análisis por ustedes)
El sintético parece un cliente **mucho más intensivo** que el tarjetahabiente real promedio de India:
- unas 4 veces más gasto mensual;
- unas 19 veces más transacciones al mes, con un ticket unas 4 veces más bajo;
- cerca de 10 veces más saldo;
- el doble de utilización;
- unas 50 veces más uso de avances en efectivo.
La edad también está más cargada hacia menores de 30 que la cartera de SBI Card.

---

## 3. Qué no se consiguió (y cómo conseguirlo a mano)
- **Distribución del CIBIL score**: transunioncibil.com bloquea las descargas automáticas (403). Bajen a mano los
  informes *Credit Market Indicator* (CMI) en https://www.transunioncibil.com/lp/cmi-report-june-2025.
- **Edad, sexo e ingreso de los tarjetahabientes a nivel individual**: están en los microdatos de Global Findex 2025
  para India (registro gratuito): https://microdata.worldbank.org (buscar "Global Findex 2025 India").
- **Ingresos del PLFS (tablas oficiales)**: el PDF del informe anual devolvía 404. Microdatos en
  https://microdata.gov.in/NADA/index.php/catalog/213 (registro gratuito).
- **Tablas del RBI directamente** (rbi.org.in / rbidocs): tienen protección anti-bots. Por eso se usó el espejo de
  India Data Portal (https://indiadataportal.com), que cita al RBI como fuente.

## 4. URLs de origen
- RBI card stats 2022+: https://ckandev.indiadataportal.com/dataset/eb565ca6-aa06-47fd-9c81-05c7ed6c538b/resource/1bb59cb1-6965-4c02-88ab-82333f101f5b/download/bankwise_atm_pos_card_statistics_2022_onwards.csv (origen: https://rbi.org.in/Scripts/ATMView.aspx)
- RBI card stats 2011-2022: https://ckandev.indiadataportal.com/dataset/eb565ca6-aa06-47fd-9c81-05c7ed6c538b/resource/7f303693-2dd0-42e7-9a70-d7a9cd917f66/download/bankwise-atm-pos-card-statistics-20112022.csv
- RBI BSR (crédito SCB): https://ckandev.indiadataportal.com/dataset/eb565ca6-aa06-47fd-9c81-05c7ed6c538b/resource/733d27c5-e6a7-4cbf-a03e-b7cda032b608/download/credit-by-scheduled-commercial-banks.csv
- RBI mobile banking: https://ckandev.indiadataportal.com/dataset/eb565ca6-aa06-47fd-9c81-05c7ed6c538b/resource/7db4c888-ac0c-4820-9982-c4ea04307f4b/download/mobile-banking-statistics.csv
- Global Findex 2025: https://www.worldbank.org/en/publication/globalfindex/download-data
- WDI: https://api.worldbank.org/v2/country/IND/indicator/...
- SBI Card: https://www.sbicard.com/en/who-we-are/business-presentations.page
- CRIF High Mark: https://www.crifhighmark.com/media/6260/how-india-lends-feb-2026.pdf (y los demás en la carpeta)
- Worldline: https://worldline.com/content/dam/worldline/local/en-in/documents/main-page11111/Worldline-India-Digital-Payment-Report-1H-2025-1.pdf
- MoSPI PLFS: https://mospi.gov.in/sites/default/files/press_release/Press_note_AR_PLFS_2023_24_22092024.pdf y https://mospi.gov.in/sites/default/files/publication_reports/Quarterly_Bulletin_PLFS_April_June_2024.pdf
