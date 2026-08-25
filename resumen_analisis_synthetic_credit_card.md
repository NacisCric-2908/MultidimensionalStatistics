# Resumen Ejecutivo y Técnico del Análisis Multidimensional
**Dataset:** `bronze/synthetic_credit_card_customer_behavior_dataset.csv`  
**Documento base:** `analisis_synthetic_credit_card.Rmd` (Semanas 1 a 3 — S01 a S03)  
**Fecha:** 25 de agosto de 2026  

---

## 1. Naturaleza y Estructura de la Matriz de Datos ($\mathbf{X} \in \mathbb{R}^{n \times p}$)

* **Dimensiones:**
  * $n = 50\,000$ observaciones (clientes).
  * $p = 30$ variables medidas.
* **Clasificación de Variables:**
  * **26 Variables Cuantitativas / Numéricas:**
    * *Escala monetaria:* `Annual_Income`, `Monthly_Spending`, `Credit_Limit`, `Outstanding_Balance`, `Statement_Balance`, `Payment_Amount`, `Avg_Transaction_Value`, `Cash_Advance_Amount` y gastos por rubro (`Grocery_Spending`, `Fuel_Spending`, `Dining_Spending`, `Travel_Spending`, `Entertainment_Spending`, `Utility_Bill_Spending`, `Online_Shopping_Spending`).
    * *Ratios e Índices continuos:* `Payment_Ratio` (rango $0.10$ a $1.00$), `Credit_Utilization` (rango $0.03$ a $0.98$).
    * *Conteos y Puntuaciones discretas:* `Age` ($18$ a $69$ años), `Card_Age_Months` ($1$ a $120$), `Monthly_Transactions`, `EMI_Count`, `International_Transactions`, `Reward_Points_Earned`, `Reward_Points_Redeemed`, `Mobile_App_Login`, `Credit_Score` ($367$ a $792$).
  * **4 Variables Cualitativas / Categóricas:**
    * `Customer_ID`: Identificador alfanumérico único (no es variable de análisis).
    * `Gender`: Género (`M`, `F`).
    * `Occupation`: Ocupación (`Salaried`, `Self-Employed`, `Business Owner`, `Freelancer`, `Retired`).
    * `Card_Type`: Nivel de producto (`Basic`, `Silver`, `Gold`, `Platinum`).

---

## 2. Auditoría e Integridad de los Datos (Módulos S01 - S02)

1. **Inspección Previa (`readLines`):** Delimitador de columnas por comas (`,`), punto como separador decimal (`.`), encabezados en primera fila. Carga reproducible con `read.csv()`.
2. **Diagnóstico Multivariante de Faltantes:**
   * Celdas `NA` en la matriz: **0 celdas** ($0.00\%$).
   * Casos completos (`complete.cases`): **$50\,000$ filas** ($100.00\%$).
   * No hay pérdida de vectores $\mathbf{x}_i \in \mathbb{R}^p$.
3. **Duplicados:** $0$ filas duplicadas y $50\,000$ identificadores `Customer_ID` únicos.
4. **Resumen de Anomalías (`summary`):**
   * No existen códigos de error o centinelas (como `-99`, `999` o ingresos negativos).
   * Datos sintéticos balanceados y consistentes con reglas de negocio crediticias.

---

## 3. Principales Hallazgos Univariados (Módulos S01, S03)

1. **Histogramas y Calibración de Cortes (`breaks`):**
   * Se evaluó la sensibilidad de la distribución de `Credit_Score` ante 3 anchos de clase: `breaks = 5` (sobre-suavizado), `breaks = 20` (balanceado) y `breaks = 60` (ruidoso/sobreajustado).
   * La **Regla de Sturges** ($k = 1 + \log_2(50\,000) \approx 16$) respalda una partición moderada ($k \approx 16 - 20$) que capta la forma unimodal simétrica sin picos artificiales.
2. **Dispersión y Criterio de Tukey (Boxplots):**
   * Para `Monthly_Spending`, los cinco números de Tukey son:
     * $\text{Mínimo} \approx \$1\,619$
     * $Q_1 \approx \$20\,843$
     * $\text{Mediana} \approx \$35\,139$
     * $Q_3 \approx \$54\,759$
     * $\text{Máximo} \approx \$164\,860$
   * Límites de Tukey ($Q_1 - 1.5 \cdot RIC$ a $Q_3 + 1.5 \cdot RIC$): $[\$-30\,031, \$105\,634]$.
   * Atípicos univariados: Al ser datos sintéticos de dispersión controlada, la proporción de valores marcados como atípicos es marginal ($< 0.5\%$).
3. **Comparación Multivariada Estandarizada (`scale`):**
   * Al graficar `boxplot(credit_num)` sin estandarizar, las variables en millones (`Annual_Income`, `Credit_Limit`) ocultan completamente a los ratios ($0$ a $1$).
   * La estandarización `boxplot(scale(credit_num))` permite comparar la longitud de colas y asimetría en unidades homogéneas de desviación estándar ($Z$-scores).

---

## 4. Principales Hallazgos Bivariados y Multivariados (Módulos S01, S03)

1. **Estructura de Correlaciones Lineales:**
   * **Colinealidades Estructurales Altas ($r > 0.80$):**
     * `Outstanding_Balance` y `Statement_Balance`: $r = 0.997$ (casi idénticas).
     * `Monthly_Spending` y `Reward_Points_Earned`: $r = 0.980$.
     * `Credit_Limit` y `Reward_Points_Earned`: $r = 0.958$.
     * `Monthly_Spending` y `Annual_Income`: $r = 0.945$.
     * `Statement_Balance` y `Payment_Amount`: $r = 0.936$.
   * **Determinantes del Score Crediticio:**
     * `Payment_Ratio` con `Credit_Score`: $r = 0.767$ (fuerte relación positiva: quien paga más de su saldo mensual tiene mejor scoring).
     * `Credit_Utilization` con `Credit_Score`: $r = -0.599$ (relación inversa: alta saturación del cupo disminuye la calificación).
2. **El "Punto Imposible" (Demostración de Outlier Multivariante):**
   * Se construyó un cliente hipotético con `Payment_Ratio = 0.95` y `Credit_Score = 460`.
   * **Univariadamente inocente:** Ambos valores caen perfectamente dentro de los bigotes de Tukey de sus respectivas variables ($0.95 \in [0.11, 1.47]$ y $460 \in [441, 825]$).
   * **Multivariadamente imposible:** En la nube bivariada de puntos, ningún cliente con $95\%$ de pago tiene un scoring menor a $650$. Cae en una zona de densidad cero (punto rojo destacado).
   * **Lección central:** La normalidad marginal **no** garantiza la normalidad conjunta.
3. **La Paradoja de las 55 Dimensiones Bivariadas:**
   * Aunque se revisen todas las $\binom{p}{2}$ proyecciones 2D con `pairs()` y ninguna muestre puntos extraños, **no se puede descartar la existencia de outliers en subespacios de dimensión $\geq 3$**. Para ello se requerirá el cálculo de distancias multivariantes (Mahalanobis $D^2$) y Componentes Principales (PCA).

---

## 5. Síntesis de Conclusiones

| Nivel de Análisis | Conclusión Principal |
|---|---|
| **Univariado** | Distribuciones balanceadas y bien acondicionadas; el número de intervalos en histogramas debe responder a la regla de Sturges para evitar distorsiones. |
| **Bivariado** | El ratio de pago es el determinante positivo clave del puntaje crediticio ($r = 0.767$). Existen relaciones bivariadas estrictas donde combinaciones univariadamente normales resultan imposibles en conjunto. |
| **Multivariado** | Matriz con redundancia de información y alta colinealidad ($r > 0.90$), lo cual la hace ideal para técnicas de reducción de dimensionalidad (PCA) en etapas posteriores del curso. |
