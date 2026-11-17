# Especificación: búsqueda de datos reales de India para contrastar el dataset sintético

> Copia todo lo que está debajo de la línea en la IA que vaya a buscar (necesita tener búsqueda web).

---

## Rol y objetivo

Eres un asistente de investigación de datos. Tengo un dataset **sintético** de Kaggle (*Credit Card Customer Behavior Analysis & Prediction*, 50 000 tarjetahabientes simulados de **India**, montos en **rupias (INR)**, 30 columnas). Para un curso de Estadística Multidimensional debo **compararlo con datos reales de India** y decir en qué se parece y en qué no a la realidad.

Necesito que busques **fuentes de datos reales y verificables** que permitan contrastar las variables listadas abajo. Como ninguna fuente pública tiene las 30 variables a nivel de cliente, espero **varias fuentes**, cada una cubriendo un grupo de variables.

## Variables del dataset sintético y sus valores (para comparar)

| Grupo | Variable | Valores en el sintético |
|---|---|---|
| Demografía | `Age` | 18–70 años, media 36.1, mediana 34 |
| | `Gender` | M 55.2 %, F 44.8 % |
| | `Occupation` | Empleado privado 41.9 %, Empleado público 15.2 %, Independiente 14.9 %, Empresario 12.1 %, Jubilado 8.1 %, Estudiante 7.8 % |
| Ingreso | `Annual_Income` | ₹1.0 lakh – ₹80 lakh; media ₹14.8 lakh, mediana ₹11.3 lakh |
| Tarjeta | `Card_Type` | Gold 33.8 %, Silver 24.1 %, Basic 20.5 %, Platinum 16.6 %, Signature 5.0 % |
| | `Credit_Limit` | ₹16 000 – ₹65.9 lakh; media ₹7.1 lakh, mediana ₹3.96 lakh |
| | `Card_Age_Months` | 1–240 meses, media 53.6 |
| Gasto | `Monthly_Spending` | media ₹73 872/mes, mediana ₹50 022 |
| | `Monthly_Transactions` | 15–179, media 83 |
| | `Avg_Transaction_Value` | media ₹836 por transacción |
| | Gasto por categoría (mensual, medias) | Supermercado ₹17 794, Servicios públicos ₹11 746, Compras online ₹11 238, Combustible ₹10 213, Restaurantes ₹9 090, Entretenimiento ₹7 648, Viajes ₹6 142 |
| | `International_Transactions` | 0–14/mes; 40.7 % de clientes con al menos una |
| Deuda y pago | `Outstanding_Balance` | media ₹3.03 lakh, mediana ₹1.45 lakh |
| | `Statement_Balance`, `Payment_Amount` | medias ₹3.66 lakh y ₹2.79 lakh |
| | `Payment_Ratio` | 0.10–1.00, media 0.76, mediana 0.84 |
| | `Credit_Utilization` | 0.10–0.95, media 0.43, mediana 0.40 |
| | `Cash_Advance_Amount` | 29.7 % de clientes usa avances; media ₹23 057 |
| | `EMI_Count` | 0–6 cuotas EMI activas, media 2.45 |
| Fidelización / canal | `Reward_Points_Earned` / `Redeemed` | medias 3 891 / 872 |
| | `Mobile_App_Login` | 2–71 ingresos/mes, media 33 |
| Riesgo | `Credit_Score` | 367–792, media 629, mediana 638 (escala tipo CIBIL 300–900) |

## Qué buscar (prioridades)

1. **Indicadores agregados de tarjetas de crédito en India** (los más importantes): número de tarjetas activas, gasto total y gasto por tarjeta al mes, número de transacciones por tarjeta, valor promedio por transacción (*average ticket size*), saldos pendientes (*credit card outstanding*), tasa de morosidad (NPA/GNPA) de tarjetas, participación por canal (POS vs. e-commerce). Fuentes típicas: **RBI** (Reserve Bank of India: *Bank-wise ATM/POS/Card Statistics*, *Payment System Indicators*, *Handbook of Statistics on Indian Economy*, *Sectoral Deployment of Bank Credit*, *Financial Stability Report*), **NPCI**, **TransUnion CIBIL / Experian / CRIF High Mark** (informes de crédito de consumo).
2. **Perfil del tarjetahabiente**: distribución por edad, género, ocupación e ingreso de quienes tienen tarjeta de crédito. Fuentes posibles: **RBI**, **CIBIL** (*Credit Market Indicator*, informes sobre mujeres prestatarias / jóvenes), **NSO/MoSPI** (PLFS para ingreso y ocupación; NSS/AIDIS para deuda de hogares), **World Bank Global Findex** (tenencia de tarjeta de crédito en India por sexo, edad e ingreso), **CMIE Consumer Pyramids** (si es accesible).
3. **Distribución del puntaje de crédito** en India (CIBIL 300–900): proporción de personas por rango de score, score promedio.
4. **Composición del gasto con tarjeta por categoría** (supermercado, combustible, viajes, restaurantes, online, servicios): informes de bancos (HDFC, SBI Card, ICICI, Axis), de redes (Visa, Mastercard, RuPay), o consultoras (Worldline India Digital Payments Report, PwC, RedSeer).
5. **Utilización de cupo, pago mínimo vs. total, avances en efectivo y EMI**: informes de CIBIL/Experian, informes anuales de **SBI Card** (empresa listada que publica gasto por tarjeta, saldo por tarjeta, mezcla de gasto).
6. **Datasets a nivel de individuo** (bonus, si existen): microdatos públicos reales de India con alguna de estas variables (p. ej. encuestas de hogares con tenencia de tarjeta, ingreso y edad). **Excluye** cualquier dataset sintético o simulado, y datasets de otros países (p. ej. el de Taiwán de UCI) salvo que lo marques explícitamente como "no India, solo referencia".

## Requisitos de cada fuente

- Que sea **real** (no simulada) y de **India**; si es sintética o de otro país, descártala o márcala claramente.
- Preferir datos de **2019 en adelante** (idealmente 2022–2025) y de fuentes oficiales o institucionales.
- **URL directa** al archivo o a la página de descarga (no solo al sitio principal), y que la URL exista: no inventes enlaces ni cifras. Si no puedes verificar un dato, escribe "no verificado".
- Indica el **formato** (CSV, XLSX, PDF, API) y si es de libre acceso o requiere registro/pago.
- Indica la **unidad**: rupias, lakh, crore, USD; nominal o real; mensual o anual; por tarjeta, por cliente o total país.

## Formato de la respuesta

1. **Tabla de fuentes**, una fila por fuente:
   `Fuente | Institución | Año(s) | URL | Formato y acceso | Nivel (agregado / individuo) | Variables del sintético que cubre | Cifras clave encontradas`
2. **Tabla de cobertura**, una fila por variable del sintético:
   `Variable | Valor en el sintético | Valor real encontrado (con fuente y año) | ¿Comparable? (sí / parcialmente / no) | Comentario`
   Ejemplo: `Avg_Transaction_Value | ₹836 | ticket promedio con tarjeta de crédito según RBI ₹X (año) | sí | ...`
3. **Variables sin dato real**: lista de las que no encontraste con fuente confiable y por qué (p. ej. `Mobile_App_Login`, `Reward_Points`).
4. **Advertencias de comparabilidad**: diferencias de unidad, año, población (todos los adultos vs. solo tarjetahabientes), agregados vs. individuos, y cualquier sesgo que impida una comparación directa.
