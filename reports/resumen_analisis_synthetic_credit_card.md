# Resumen Ejecutivo y Técnico del Análisis Multidimensional
**Dataset:** `data/bronze/synthetic_credit_card_customer_behavior_dataset.csv`
**Documento base:** `analysis/analisis_synthetic_credit_card.Rmd` (Semanas 1 a 3 — S01 a S03)
**Fecha de actualización:** 26 de agosto de 2026
**Nota:** todas las cifras de este resumen se recalcularon contra la versión vigente del dataset. Si se vuelve a generar el CSV, hay que rehacer este documento (o leer los valores directamente del `.Rmd`, que los calcula de forma dinámica).

---

## 1. Naturaleza y Estructura de la Matriz de Datos ($\mathbf{X} \in \mathbb{R}^{n \times p}$)

* **Dimensiones:**
  * $n = 50\,000$ observaciones (clientes).
  * $p = 30$ variables medidas.
* **Clasificación de Variables:**
  * **26 Variables Cuantitativas / Numéricas:**
    * *Escala monetaria:* `Annual_Income`, `Monthly_Spending`, `Credit_Limit`, `Outstanding_Balance`, `Statement_Balance`, `Payment_Amount`, `Avg_Transaction_Value`, `Cash_Advance_Amount` y gastos por rubro (`Grocery_Spending`, `Fuel_Spending`, `Dining_Spending`, `Travel_Spending`, `Entertainment_Spending`, `Utility_Bill_Spending`, `Online_Shopping_Spending`).
    * *Ratios e índices continuos:* `Payment_Ratio` (rango $0.10$ a $1.00$), `Credit_Utilization` (rango $0.10$ a $0.95$).
    * *Conteos y puntuaciones discretas:* `Age` ($18$ a $70$ años), `Card_Age_Months` ($1$ a $240$), `Monthly_Transactions`, `EMI_Count`, `International_Transactions`, `Reward_Points_Earned`, `Reward_Points_Redeemed`, `Mobile_App_Login`, `Credit_Score` ($367$ a $792$).
  * **4 Variables Cualitativas / Categóricas:**
    * `Customer_ID`: identificador alfanumérico único (no es variable de análisis; en la capa *silver* se mueve a nombres de fila).
    * `Gender`: género (`F`, `M`).
    * `Occupation`: ocupación (`Business Owner`, `Government Employee`, `Private Employee`, `Retired`, `Self-Employed`, `Student`).
    * `Card_Type`: nivel de producto (`Basic`, `Silver`, `Gold`, `Platinum`, `Signature`).

---

## 2. Auditoría e Integridad de los Datos (Módulos S01 - S02)

1. **Inspección previa (`readLines`):** delimitador de columnas por comas (`,`), punto como separador decimal (`.`), encabezados en primera fila. Carga reproducible con `read.csv()` declarando `sep`, `dec`, `stringsAsFactors = FALSE` y `na.strings = c("", "NA", "N/A", "NULL")`.
2. **Diagnóstico multivariante de faltantes:**
   * Celdas `NA` en la matriz: **0 celdas** ($0.00\%$).
   * Casos completos (`complete.cases`): **$50\,000$ filas** ($100.00\%$).
   * No hay pérdida de vectores $\mathbf{x}_i \in \mathbb{R}^p$.
3. **Duplicados:** $0$ filas duplicadas y $50\,000$ identificadores `Customer_ID` únicos.
4. **Revisión de anomalías (`summary`):**
   * No hay centinelas de error (`-99`, ingresos o edades negativas, ceros imposibles).
   * `999` aparece en `Reward_Points_Earned` / `Reward_Points_Redeemed`, pero es un conteo legítimo, no un código de faltante — por eso **no** se incluye en `na.strings`.
5. **Exportación (S02):** la capa *bronze* pasa las 8 verificaciones sin correcciones; se exporta una copia trabajada a `data/silver/credit_card_silver.csv` con `write.csv(..., row.names = TRUE)` y se vuelve a leer para verificar tipos.

---

## 3. Principales Hallazgos Univariados (Módulos S01, S03)

1. **Histogramas y calibración de cortes (`breaks`):**
   * Se evaluó la sensibilidad de la distribución de `Credit_Score` ante tres anchos de clase: `breaks = 5` (sobre-suavizado), `breaks = 17` (regla de Sturges) y `breaks = 60` (ruidoso).
   * La **regla de Sturges** da $k = 17$ para $n = 50\,000$ ($1 + \log_2(50\,000) \approx 16.6$). Con esos $17$ cortes el histograma capta la forma unimodal aproximadamente simétrica de `Credit_Score` sin picos artificiales.
2. **Dispersión y criterio de Tukey (boxplots) — `Monthly_Spending`:**
   * Cinco números de Tukey: Mínimo $\approx \$2\,236$; $Q_1 \approx \$26\,646$; Mediana $\approx \$50\,022$; $Q_3 \approx \$83\,032$; Máximo $\approx \$691\,688$.
   * Límites de Tukey ($Q_1 - 1.5 \cdot RIC$ a $Q_3 + 1.5 \cdot RIC$): $[\$-57\,933,\ \$167\,611]$.
   * **Atípicos univariados: $4\,213$ observaciones ($8.43\%$)**, todos por el lado superior.
   * *Interpretación (pregunta clave de S03):* no son errores de medición. `Monthly_Spending` tiene **asimetría positiva marcada** (la media es $1.48$ veces la mediana; el máximo, $\approx 13.8$ veces la mediana). Con una cola derecha larga, la regla $Q_3 + 1.5 \cdot RIC$ marca como atípica toda la parte alta aunque sean clientes plausibles. Aplicando `log()` antes de calcular los límites, los atípicos bajan de $4\,213$ a $875$: la transformación reconstruye la simetría que hace interpretable la regla.
3. **Comparación multivariada estandarizada (`scale`):**
   * Sin estandarizar, `boxplot(credit_num)` deja que `Annual_Income` y `Credit_Limit` (orden $10^6$) aplasten a los ratios en $[0, 1]$.
   * Con `boxplot(scale(credit_num))` se comparan colas y asimetría en unidades homogéneas ($Z$-scores). Las colas superiores más largas en unidades de $\sigma$ corresponden a `Avg_Transaction_Value` ($z_{\max} \approx 12.3$), `Outstanding_Balance` ($\approx 11.0$) y `Monthly_Spending` ($\approx 7.3$).

---

## 4. Principales Hallazgos Bivariados y Multivariados (Módulos S01, S03)

1. **Estructura de correlaciones lineales:**
   * **Colinealidades estructurales altas ($|r| > 0.90$):**
     * `Outstanding_Balance` y `Statement_Balance`: $r = 0.997$ (casi idénticas).
     * `Monthly_Spending` y `Reward_Points_Earned`: $r = 0.980$.
     * `Annual_Income` y `Credit_Limit`: $r = 0.974$.
     * `Credit_Limit` y `Reward_Points_Earned`: $r = 0.958$.
     * `Annual_Income` y `Monthly_Spending`: $r = 0.945$.
   * **Determinantes del score crediticio:**
     * `Payment_Ratio` con `Credit_Score`: $r = 0.767$ (relación positiva fuerte: quien paga mayor proporción de su saldo tiene mejor scoring).
     * `Credit_Utilization` con `Credit_Score`: $r = -0.599$ (relación inversa: mayor saturación del cupo, menor calificación).
   * **Par menos correlacionado:** `Avg_Transaction_Value` y `Payment_Ratio` ($|r| \approx 0.0001$).
2. **El "punto imposible" (outlier multivariante):**
   * Cliente hipotético con `Payment_Ratio = 0.95` y `Credit_Score = 460`.
   * **Univariadamente inocente:** ambos valores caen dentro de los bigotes de Tukey ($0.95 \in [0.11, 1.47]$ y $460 \in [441, 825]$).
   * **Multivariadamente imposible:** de los $17\,755$ clientes reales con `Payment_Ratio` $\geq 0.95$, **ninguno baja de $516$ puntos** de `Credit_Score` (percentil 1 en $\approx 567$). El punto hipotético queda $56$ puntos por debajo del mínimo observado en esa franja: cae en una región de densidad nula.
   * **Lección central:** la normalidad marginal **no** garantiza la normalidad conjunta.
3. **La paradoja de las proyecciones bivariadas:**
   * Con $p = 26$ variables numéricas hay $\binom{26}{2} = 325$ diagramas de dispersión posibles. Aunque se revisaran todos con `pairs()` y ninguno mostrara puntos extraños, **no se puede descartar la existencia de outliers en subespacios de dimensión $\geq 3$**. Para ello se requerirá el cálculo de distancias multivariantes (Mahalanobis $D^2$) y Componentes Principales (PCA).

---

## 5. Síntesis de Conclusiones

| Nivel de Análisis | Conclusión Principal |
|---|---|
| **Univariado** | Conviven variables aproximadamente simétricas (`Credit_Score`, `Payment_Ratio`, `Age`) con variables monetarias de **asimetría positiva fuerte**. Para las primeras, la regla de Sturges ($k = 17$) da un histograma fiel; para las segundas, la regla de Tukey marca muchos "atípicos" ($8.4\%$ de `Monthly_Spending`) porque el supuesto de simetría no se cumple — se corrige con una transformación `log()`. |
| **Bivariado** | El ratio de pago es el determinante positivo clave del puntaje crediticio ($r = 0.767$); la utilización del cupo lo deprime ($r = -0.599$). El "punto imposible" muestra que una combinación univariadamente plausible puede ser inexistente en la nube conjunta. |
| **Multivariado** | Matriz $100\%$ completa pero con redundancia alta: varios pares con $|r| > 0.95$. La dimensionalidad efectiva es bastante menor que $26$, lo que la hace idónea para reducción de dimensionalidad (PCA) en la unidad 6. |
