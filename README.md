# Estadística Multidimensional — Análisis Exploratorio Integral, Inferencia Multivariante, Mahalanobis, PCA y Análisis Factorial

> **Guía Maestra del Proyecto y Manual Completo de Sustentación**  
> Este documento explica de principio a fin **absolutamente todo** lo desarrollado en [`Entrega/analisis_synthetic_credit_card.Rmd`](Entrega/analisis_synthetic_credit_card.Rmd) (los **17 módulos** que integran las sesiones **S01 a S10**, Normal Multivariante, Distancia de Mahalanobis y Componentes Principales I y II), así como los talleres aplicados de **PCA** (`TallerPca/`) y **Análisis Factorial** (`tallerAnalisisFactorial/`). Está redactado para que cualquier persona —incluso sin haber escrito el código— comprenda la lógica matemática, estadística y de negocio de cada decisión y pueda **sustentar el proyecto sin que se le escape ningún detalle**.

---

## 👥 Autores e Información del Curso

* **Oscar Manuel Contreras Gacha** — `20221020052`
* **Juan Pablo Sarmiento Ramírez** — `20221020138`
* **Steven Navarro Parrales** — `20221020048`
* **Juan Diego Grajales Castillo** — `20221020128`
* **Asignatura:** Estadística Multidimensional (`26158` · grupo `020-81` · periodo `2026-3`)
* **Dataset:** [Kaggle — Credit Card Customer Behavior Analysis & Prediction](https://www.kaggle.com/code/devraai/credit-card-customer-behavior-analysis-prediction/input) ($n = 50\,000$ clientes simulados, $p = 30$ variables, expresado en **rupias indias, INR / ₹**).
* **Cliente del Caso de Negocio:** **Gerencia de Riesgo de Crédito del banco emisor**, quien decide mensualmente qué tarjetahabientes entran al programa de seguimiento preventivo (llamada de gestor, congelamiento de aumentos de cupo o reestructuración antes de caer en mora).

---

## 📁 Arquitectura del Repositorio (Medallion Data Architecture)

```text
.
├── data/
│   ├── bronze/                                      # Datos crudos e inmutables (fuente única de verdad)
│   │   └── synthetic_credit_card_customer_behavior_dataset.csv
│   ├── silver/                                      # Datos limpios, tipados y enriquecidos (Módulo 15)
│   │   ├── credit_card_silver.csv                   # Incluye Banda_Riesgo y Caso_Raro_Mahalanobis
│   │   └── credit_card_silver.rds                   # Conserva factores y el orden ordinal de Card_Type
│   └── gold/                                        # Matriz final acondicionada para modelado (Módulo 15)
│       └── credit_card_gold_pca.csv                 # Customer_ID + 21 numéricas (log1p + scale) + 13 dummies
│
├── Entrega/
│   ├── analisis_synthetic_credit_card.Rmd           # Documento maestro reproducible (17 Módulos completos)
│   ├── analisis_synthetic_credit_card.html          # Reporte técnico tejido en HTML
│   └── Analisis_Exploratorio_Credit_Card_Presentacion.pdf
│
├── TallerPca/                                       # Talleres específicos de Componentes Principales I y II
│   ├── taller_componentes_principales_I.Rmd
│   └── taller_componentes_principales_II.Rmd
│
├── tallerAnalisisFactorial/                         # Taller de Análisis Factorial (Parte común vs. propia)
│   ├── taller_analisis_factorial.Rmd
│   ├── taller_analisis_factorial.html
│   └── explicacion_taller_analisis_factorial.md
│
├── Clase/                                           # Material de las sesiones S01 a S10, Mahalanobis y PCA
├── requirements.txt                                 # Dependencias auxiliares de Python
└── README.md                                        # Este documento (Guía maestra y de sustentación)
```

---

## 🧭 Hilo Conductor del Proyecto (La Historia en 5 Actos)

Si en la sustentación te preguntan **«¿De qué trata el trabajo y cuál es su conclusión principal?»**, esta es la respuesta ejecutiva:

1. **Acto 1 — Auditoría y Naturaleza de las Variables (Módulos 1 y 2):** Tenemos una matriz $\mathbf{X} \in \mathbb{R}^{50\,000 \times 30}$ 100 % completa (0 `NA`, 0 duplicados, sin errores de captura ni valores centinela). Aunque R guarda 4 columnas como `character` y 26 como `numeric`, estadísticamente son **3 nominales** (`Customer_ID`, `Gender`, `Occupation`), **1 ordinal** (`Card_Type`: Basic < Silver < Gold < Platinum < Signature) y **26 cuantitativas** (15 monetarias continuas, 2 ratios acotados en $[0, 1]$ y 9 conteos/puntajes discretos de escala de razón).
2. **Acto 2 — Forma Univariada, Asimetría y Escalas (Módulos 3, 4, 5 y 6):** Las variables de dinero y gasto presentan una fortísima **asimetría positiva (cola derecha)** o **inflación en cero** (ej. 70,3 % de clientes nunca pide avances en efectivo). Por eso, la regla de Tukey marca entre **8 % y 19,1 %** de datos como "atípicos" en ellas: **no son errores de captura**, sino el reflejo natural de una distribución sesgada evaluada con una regla pensada para campanas simétricas. Además, las desviaciones estándar difieren por un factor de **$6{,}83 \times 10^6$ veces** entre `Annual_Income` ($\sigma \approx 1{,}41 \times 10^6$ ₹) y `Credit_Utilization` ($\sigma = 0{,}206$), lo que hace obligatorio estandarizar ($Z$-scores).
3. **Acto 3 — El Hallazgo Central de Negocio: Capacidad vs. Riesgo (Módulos 7 y 8):** El volumen de dinero (`Annual_Income`, `Credit_Limit`, `Monthly_Spending`, `Statement_Balance`) está fuertemente colineal entre sí ($r > 0{,}93$), pero tiene **correlación prácticamente nula con el puntaje crediticio (`Credit_Score`, $r \approx 0{,}03$)**. En cambio, el riesgo crediticio está gobernado por dos variables de **conducta de pago**: `Payment_Ratio` ($r = +0{,}767$) y `Credit_Utilization` ($r = -0{,}599$). Lo mismo ocurre con las categóricas: `Occupation` explica el **63,7 %** de la varianza del ingreso ($\eta^2 = 0{,}637$) pero el **0,00 %** del puntaje ($\eta^2 = 0{,}0001$).
4. **Acto 4 — Geometría Multivariante, Paradoja de Simpson y Mahalanobis (Módulos 9 al 14):**
   * **Mirar una variable a la vez engaña:** Existen "puntos imposibles" (normales en cada eje según Tukey, pero imposibles en el plano conjunto); la correlación entre transacciones mensuales y ticket promedio es positiva en toda la cartera ($r = +0{,}136$) pero **negativa dentro de cada tipo de tarjeta** ($r$ entre $-0{,}21$ y $-0{,}61$, **Paradoja de Simpson** causada por `Card_Type` como variable confusora); y `Payment_Amount` tiene $r \approx 0$ con `Credit_Score`, pero **no son independientes** porque al condicionar por terciles cambia la dispersión y la cola izquierda de riesgo.
   * **Redundancia estructural y Mahalanobis:** La matriz de 26 variables numéricas tiene determinante casi nulo ($\det(\mathbf{R}_{26}) = 8{,}65 \times 10^{-30}$, $\lambda_{\min} = 6{,}56 \times 10^{-15}$) porque `Monthly_Spending` es la suma exacta de las 7 categorías de gasto y hay pares duplicados/derivados. Al retirar **5 variables redundantes/derivadas**, quedan **21 variables activas** con matriz invertible ($\lambda_{\min} = 0{,}018$). Sobre estas 21 variables (con $\log(x+1)$ en las 16 asimétricas), la distancia de Mahalanobis ($d_M^2 > \chi^2_{21;\,0{,}99}$) detecta **1 641 casos raros (3,28 %)**, de los cuales el **64,3 % (1 055 clientes) no tiene ninguna variable extrema univariada ($|Z| > 3$)**. Son clientes de "perfil disparejo" (ingreso alto pero una categoría de gasto en cero) y tienen mayor riesgo (mediana de score 595 vs. 643 del resto), por lo que **no se borran: se marcan y conservan**.
5. **Acto 5 — Preparación Medallion, PCA y Análisis Factorial para la Gerencia (Módulos 15, 16, 17 y Talleres):**
   * Con las 21 variables activas ($\log(x+1)$ + `scale()`), la **Componente 1 (C1 = Tamaño del cliente)** guarda el **50,1 %** de la información y la **Componente 2 (C2 = Riesgo)** guarda el **5,3 %** (juntas, **55,4 %**; 3 componentes tienen $\lambda > 1$ y se requieren 8 para superar el 80 %).
   * **El costo de decidir con un solo número:** Si la Gerencia usa solo C1 para seleccionar al 20 % de clientes a intervenir buscando al 20 % con peor `Credit_Score` (10 046 clientes), solo acierta en **1 832 clientes (18,2 %)** —peor que lanzar una moneda— y se le escapan **8 214 (81,8 %)**. Usando C2 acierta en **6 580 (65,5 %)**.
   * **El mapa de seguimiento (C1 vs. C2):** Con dos cortes operativos ($C_2 > 1\,\text{DE}$ para alto riesgo y la mediana de $C_1$ para tamaño), la cartera se divide en **Zona A** (4 226 clientes, 8,5 %: alto riesgo + alta exposición, prioridad de llamada de gestor), **Zona B** (3 969 clientes, 7,9 %: alto riesgo + baja exposición, seguimiento automatizado) y **Zona C** (41 805 clientes, 83,6 %: sin seguimiento).
   * **Análisis Factorial:** Confirma mediante máxima verosimilitud (`fa()`, KMO = 0,71) que existe una única habilidad latente común (**capacidad económica**, que explica 99,1 % del cupo y 97,5 % del ingreso), mientras que el `Credit_Score` es **100 % parte propia** (KMO = 0,02, comunalidad = 0,0 %).

---

## 🔬 Desglose Exhaustivo Módulo por Módulo (`Entrega/analisis_synthetic_credit_card.Rmd`)

A continuación se detalla qué hace exactamente cada uno de los **17 módulos**, qué código y fórmulas utiliza, qué resultados numéricos arroja y cómo defender cada punto en una sustentación.

---

### Módulo 1: Inspección Previa e Importación Reproducible (S01 & S02)

1. **Inspección en crudo (`readLines`):**
   * Antes de importar, se leen las primeras 4 líneas en texto plano (`readLines(ruta_credit, n = 4)`).
   * **Diagnóstico:** Separador de campos coma (`,`), separador decimal punto (`.`), primera línea con encabezados. Se importa con `read.csv(..., header = TRUE, sep = ",", dec = ".", stringsAsFactors = FALSE)`.
2. **Dimensiones de la matriz $\mathbf{X} \in \mathbb{R}^{n \times p}$:**
   * $n = 50\,000$ filas (clientes) y $p = 30$ columnas (variables), para un total de $1\,500\,000$ celdas.
3. **Clasificación estadística formal (Taxonomía de Everitt & Hothorn vs. tipos de R):**
   * R reporta `26` variables numéricas (`int`/`num`) y `4` de texto (`character`). Sin embargo, el tipo de almacenamiento en R no define la escala estadística; el criterio real es si las diferencias entre valores tienen magnitud constante (aritmética interpretable) o si son etiquetas/niveles. Analizando la cardinalidad (`length(unique(x))`):
     * **Cualitativas Nominales (3):**
       * `Customer_ID` (50 000 valores únicos): identificador puro sin magnitud ni orden; se excluye de todo cálculo estadístico.
       * `Gender` (2 niveles: `F`, `M`): sin jerarquía.
       * `Occupation` (6 niveles: `Business Owner`, `Government Employee`, `Private Employee`, `Retired`, `Self-Employed`, `Student`): categorías ocupacionales sin orden natural.
     * **Cualitativa Ordinal (1) — *Corrección clave de sustentación*:**
       * `Card_Type` (5 niveles): aunque viene como `character`, tiene una jerarquía estricta de producto bancario: `Basic` (8 485) < `Silver` (11 945) < `Gold` (15 068) < `Platinum` (11 967) < `Signature` (2 535, 5,1 %). Es **ordinal** porque existe orden, pero la distancia entre niveles no es necesariamente constante.
     * **Cuantitativas (26):**
       * *Continuas monetarias (15):* `Annual_Income`, `Credit_Limit`, `Monthly_Spending`, `Avg_Transaction_Value`, las 7 categorías de gasto (`Online_Shopping_Spending`, `Grocery_Spending`, `Fuel_Spending`, `Dining_Spending`, `Travel_Spending`, `Entertainment_Spending`, `Utility_Bill_Spending`), `Outstanding_Balance`, `Statement_Balance`, `Payment_Amount`, `Cash_Advance_Amount`.
       * *Continuas de razón / proporciones (2):* `Payment_Ratio` y `Credit_Utilization`, acotadas en $[0, 1]$ pero con métrica constante (0,90 es exactamente el doble de 0,45).
       * *Discretas de conteo y puntuación (9):* `Age` (52 valores, 18–69 años), `Card_Age_Months` (239 valores, 1–240 meses), `Monthly_Transactions` (165 valores, 15–179), `EMI_Count` (7 valores, 0–6 cuotas), `International_Transactions` (15 valores, 0–14), `Reward_Points_Earned`, `Reward_Points_Redeemed`, `Mobile_App_Login` (70 valores, 2–71), `Credit_Score` (426 valores, 367–792). **Defensa en sustentación:** Aunque `EMI_Count` solo tome valores de 0 a 6, es cuantitativa discreta de razón (igual que "número de hijos"): el 0 es ausencia absoluta de compras a cuotas y 4 cuotas es el doble de 2.
4. **Diccionario de negocio (`que_es` y `por_que`):**
   * Se construyen dos vectores nombrados en R que documentan para las 26 variables numéricas qué miden en el banco y la razón económica de la forma de su distribución.

---

### Módulo 2: Auditoría y Diagnóstico de Calidad de la Matriz (S02)

1. **Diagnóstico dual de datos faltantes (Celdas vs. Filas):**
   * En estadística multivariante, un `NA` en una celda anula el vector completo $\mathbf{x}_i \in \mathbb{R}^p$. Por eso se verifica tanto `sum(is.na(credit))` (**0 celdas vacías de 1 500 000**, 0,00 %) como `sum(complete.cases(credit))` (**50 000 filas completas**, 100,00 %). No se requiere amputación por casos completos, ni análisis por pares, ni imputación.
2. **Duplicados:**
   * `sum(duplicated(credit))` = **0** filas repetidas; `sum(duplicated(credit$Customer_ID))` = **0** IDs repetidos.
3. **Auditoría de rangos y reglas de negocio (`summary`):**
   * Ninguna variable monetaria o de conteo presenta valores negativos ni códigos centinela (`-99`, `999`).
   * **Verificación explícita de 3 reglas de dominio:**
     * `Age`: $[18,\; 69]$ años (solo mayores de edad).
     * `Payment_Ratio`: $[0{,}10,\; 1{,}00]$ (nadie paga menos del 10 % ni más del 100 % de lo facturado).
     * `Credit_Utilization`: $[0{,}10,\; 0{,}95]$ (el banco frena el uso al 95 % del cupo).
4. **Tablas y gráficos de frecuencias relativas categóricas (`useNA = "always"`):**
   * Sin niveles fantasma por espacios o mayúsculas, y `<NA> = 0` en todas:
     * `Gender`: `M` = **50,9 %**, `F` = **49,1 %** (casi 50/50).
     * `Card_Type` (en orden ordinal): `Basic` = **17,0 %**, `Silver` = **23,9 %**, `Gold` = **30,1 %** (moda), `Platinum` = **23,9 %**, `Signature` = **5,1 %**.
     * `Occupation`: `Private Employee` domina con **39,9 %**, seguido de `Government Employee` (**15,0 %**), `Self-Employed` (**14,9 %**), `Business Owner` (**10,2 %**), `Retired` (**10,0 %**) y `Student` (**10,0 %**).

---

### Módulo 3: Análisis Univariado y la Decisión Gráfica del Histograma (S01 & S03)

1. **Variable de referencia (`Credit_Score`):**
   * **Media:** `630,7` | **Mediana:** `642` | **Desviación estándar:** `71,5` | **Mínimo:** `367` | **Máximo:** `792`.
   * Que la media sea `11,3` puntos menor que la mediana anticipa analíticamente una **asimetría negativa** ($-0{,}58$, cola izquierda de clientes riesgosos).
2. **Regla de Sturges para el número de intervalos ($k$):**
   $$k = 1 + \log_2(n) = 1 + \log_2(50\,000) = 16{,}61 \;\longrightarrow\; k = 17 \text{ intervalos}$$
   * **Punto clave de sustentación:** $k = 17$ depende únicamente de $n = 50\,000$, por lo que es el mismo número de clases para las 26 variables numéricas; lo que cambia en cada variable es el ancho de clase $h = (\max - \min)/k$.
3. **Experimento de sensibilidad (`breaks = 5`, `17`, `60`) en las 26 variables:**
   * Se grafica cada una de las 26 variables numéricas en su propio bloque con tres paneles:
     * `breaks = 5` (**sobre-suavizado / underfitting**): barras demasiado anchas que ocultan la asimetría o aplastan toda la cartera en la primera barra.
     * `breaks = 17` (**balanceado / Sturges**): revela la estructura real (colas derechas en dinero, escalonamiento por múltiplos de mil en `Credit_Limit`, barras separadas en conteos discretos como `EMI_Count`, inflación en cero en `Cash_Advance_Amount` con 70,3 % en cero e `International_Transactions` con 59,3 % en cero).
     * `breaks = 60` (**ruidoso / overfitting**): fragmenta las colas en barras de 1 o 2 clientes y crea huecos artificiales en variables discretas.

---

### Módulo 4: Estimación por Densidad de Kernel — KDE (S04)

1. **Por qué pasar del histograma al Kernel:**
   * El histograma sufre del problema del origen arbitrario de la primera caja. El estimador de densidad de kernel reemplaza las barras por una suma de campanas gaussianas centradas en cada dato $x_i$:
     $$\hat{f}_h(x) = \frac{1}{n\,h}\sum_{i=1}^{n} K\!\left(\frac{x - x_i}{h}\right), \qquad K(u) = \frac{1}{\sqrt{2\pi}}e^{-u^2/2}$$
   * **Verificación en código (`kernel_a_mano`):** Se programa manualmente la fórmula en R para 5 valores de `Credit_Score` (`500, 580, 630, 680, 750`) y se comprueba que coincide hasta el quinto decimal con `density()`, además de integrar área igual a `1,0001`.
2. **Selección objetiva de $h$ con la Regla de Silverman (`bw.nrd0`):**
   $$h_{\text{Silverman}} = 0{,}9 \, \min\!\left(s,\; \frac{RIC}{1{,}34}\right) n^{-1/5}$$
   * Usa el mínimo entre $s$ y $RIC/1{,}34$ para evitar que los valores extremos inflen $s$ y sobre-suavicen la curva.
3. **Demostración del compromiso sesgo-varianza ($h/3$, $h$ y $3h$):**
   * **En `Monthly_Transactions` ($h = 3{,}05$):** Con $3h$ aparece **1 solo pico** (sobre-suavizado); con $h/3$ aparecen **15 picos** (ruido muestral); con $h$ de Silverman aparecen **2 picos principales (en 55 y 80 transacciones)** que coinciden con las medianas reales de los tipos de tarjeta (`Basic` = 55, `Silver` = 65, `Gold` = 80, `Platinum` = 100, `Signature` = 120). Es decir, los picos de $h$ revelan una **mezcla de subpoblaciones reales**.
   * **En `Age` ($h = 1{,}27$ años):** Con $h/3 = 0{,}42$ años aparecen **50 picos** para 52 edades enteras distintas, porque un ancho menor que la resolución de medida ($1$ año) detecta la rejilla de discretización.
4. **Limitación crítica del KDE documentada en las 26 variables:**
   * En variables infladas en cero (`Cash_Advance_Amount` 70,3 % ceros, `International_Transactions` 59,3 % ceros, `Reward_Points_Redeemed` 39,9 % ceros) y conteos cortos (`EMI_Count`, 0 a 6), `density()` dibuja una montaña continua alrededor de cero (e incluso asigna densidad a valores negativos inexistentes) porque no puede representar masas puntuales discretas.

---

### Módulo 5: Caja y Bigotes (Boxplots) y Detección Univariada de Atípicos (S03)

1. **Los 5 números de Tukey (`fivenum`) y las cercas ($Q_1 - 1{,}5\cdot RIC$, $Q_3 + 1{,}5\cdot RIC$):**
   * Caso de estudio en `Monthly_Spending`: Mínimo = `2 387 ₹`, $Q_1 = 26\,646\text{ ₹}$, Mediana = `50 022 ₹`, $Q_3 = 83\,032\text{ ₹}$, Máximo = `691 688 ₹`, $RIC = 56\,386\text{ ₹}$.
   * Límite inferior: $-57\,933\text{ ₹}$ (imposible para un gasto); límite superior: $167\,611\text{ ₹}$. Marca **4 213 clientes (8,43 %)** como atípicos superiores.
2. **Aplicación individual a las 26 variables y separación en dos regímenes:**
   * **Grupo 1 — Variables asimétricas o infladas en cero (8 % a 19,1 % de "atípicos"):**
     * `Cash_Advance_Amount` (**19,10 %**, porque $Q_1 = 0$ comprime el $RIC$), `Reward_Points_Redeemed` (**11,42 %**), `Reward_Points_Earned` (**9,86 %**), `International_Transactions` (**9,54 %**), `Statement_Balance` (**9,18 %**), `Outstanding_Balance` (**9,14 %**), `Payment_Amount` (**9,07 %**), `Travel_Spending` (**8,63 %**), `Avg_Transaction_Value` (**8,57 %**), `Entertainment_Spending` (**8,55 %**), `Monthly_Spending` (**8,43 %**), `Dining_Spending` (**8,40 %**), `Credit_Limit` (**8,35 %**), `Fuel_Spending` (**8,35 %**), `Utility_Bill_Spending` (**8,11 %**), `Online_Shopping_Spending` (**8,09 %**), `Annual_Income` (**8,07 %**), `Grocery_Spending` (**8,06 %**).
   * **Grupo 2 — Variables simétricas o acotadas por construcción (0 % a 2,6 % de atípicos):**
     * `Card_Age_Months` (**2,57 %**), `Credit_Score` (**0,79 %**, 394 clientes en la cola inferior por debajo de 441 puntos), `Age` (**0,56 %**, > 69,5 años), `Payment_Ratio` (**0,17 %**, 87 clientes en cola inferior), y **exactamente 0,00 %** en `Monthly_Transactions`, `Credit_Utilization`, `EMI_Count` y `Mobile_App_Login`.
3. **Lección de sustentación:** Un alto porcentaje de atípicos de Tukey en variables monetarias **diagnostica asimetría positiva, no errores de datos**, porque la constante $1{,}5\cdot RIC$ fue calibrada para campanas gaussianas (donde deja fuera al 0,7 %).

---

### Módulo 6: Comparación Multivariada Estandarizada mediante Boxplots (S03)

1. **Cuantificación del choque de escalas:**
   * Mayor desviación estándar: `Annual_Income` ($s = 1\,407\,257\text{ ₹}$).
   * Menor desviación estándar: `Credit_Utilization` ($s = 0{,}206$).
   * **Razón de disparidad:** $1\,407\,257 / 0{,}206 = \mathbf{6\,829\,570}$ **veces**.
   * En el boxplot conjunto sin estandarizar, 24 de las 26 variables quedan aplastadas como líneas planas en cero.
2. **Estandarización ($Z$-scores) y ranking de colas extremas ($Z_{\max}$):**
   $$z_{ij} = \frac{x_{ij} - \bar{x}_j}{s_j} \implies \bar{z}_j = 0,\; s_{z_j} = 1$$
   * La estandarización iguala centro y dispersión sin alterar la asimetría de cada variable.
   * **Top de colas derechas más extremas ($Z_{\max}$):** `Travel_Spending` (**19,40 $\sigma$**), `Entertainment_Spending` (**18,45 $\sigma$**), `Cash_Advance_Amount` (**17,84 $\sigma$**), `Dining_Spending` (**17,33 $\sigma$**), `Fuel_Spending` (**16,66 $\sigma$**), `Online_Shopping_Spending` (**15,82 $\sigma$**). En el extremo opuesto, `Credit_Score` ($2{,}26\,\sigma$), `Payment_Ratio` ($0{,}97\,\sigma$) y `Credit_Utilization` ($2{,}32\,\sigma$) son compactas.

---

### Módulo 7: Análisis Bivariado, Correlación, Anscombe y el "Punto Imposible" (S01, S03 & S04)

1. **Selección objetiva de pares (evitando elegir al azar entre $\binom{26}{2} = 325$ pares):**
   * **Criterio 1 (Numérica vs. Numérica — $|r|$ de Pearson):**
     * Pares más altos globales: `Outstanding_Balance – Statement_Balance` ($r = 0{,}997$, redundancia contable), `Monthly_Spending – Reward_Points_Earned` ($r = 0{,}980$, función directa del gasto), y **`Annual_Income – Credit_Limit` ($r = 0{,}974$)**, que es el **par de negocio genuino más fuerte** (lo que gana el cliente vs. el cupo que le aprueba el banco).
     * Pares más fuertes con la variable objetivo `Credit_Score`: **`Payment_Ratio` ($r = +0{,}767$)** y **`Credit_Utilization` ($r = -0{,}599$)**. Todas las variables de dinero tienen $|r| \approx 0{,}03$ con el score.
   * **Criterio 2 (Numérica vs. Categórica — $\eta^2 = \text{SC}_{\text{entre}} / \text{SC}_{\text{total}}$ de ANOVA):**
     * `Annual_Income ~ Card_Type`: $\eta^2 = 0{,}6582$ (65,8 %).
     * `Credit_Limit ~ Card_Type`: $\eta^2 = 0{,}6467$ (64,7 %).
     * **`Annual_Income ~ Occupation`**: $\eta^2 = 0{,}6367$ (**63,7 %**; de `251 605 ₹` promedio en `Student` a `4 369 221 ₹` en `Business Owner`, razón 17 a 1).
     * Contrastes nulos: `Credit_Score ~ Card_Type` ($\eta^2 = 0{,}0015$, 0,15 %), `Credit_Score ~ Occupation` ($\eta^2 = 0{,}0001$, 0,01 %), `Annual_Income ~ Gender` ($\eta^2 = 0{,}0000$) y `Credit_Score ~ Gender` ($\eta^2 = 0{,}0000$).
2. **De la covarianza $s_{jk}$ a la correlación $r_{jk}$:**
   * Se demuestra en código que dividir `Annual_Income` entre 1 000 reduce la covarianza mil veces (de $9{,}39 \times 10^{11}$ a $9{,}39 \times 10^8$), mientras que $r = s_{jk}/(s_j s_k) = 0{,}9737$ permanece invariante a cambios de escala (y acotado en $[-1, 1]$ por la desigualdad de Cauchy-Schwarz).
3. **Lección de Anscombe en la cartera (`Annual_Income` vs. `Credit_Limit`):**
   * Aunque $r = 0{,}974$ (Spearman $= 0{,}958$, y sin el 1 % más rico $r = 0{,}965$), al colorear el diagrama de dispersión por `Card_Type` se descubre que **no hay una sola recta, sino cinco abanicos lineales distintos**: la mediana de la razón $\text{Cupo}/\text{Ingreso}$ es **0,30** en `Basic`, **0,40** en `Silver`, **0,50** en `Gold`, **0,60** en `Platinum` y **0,75** en `Signature`. El banco asigna el cupo multiplicando el ingreso por un factor que depende del escalafón de la tarjeta.
4. **Demostración analítica y gráfica de dos "Puntos Imposibles" (S03):**
   * Un registro puede estar **dentro de las cercas de Tukey univariadas en cada variable** y, aun así, ser un atípico multivariado extremo por violar la estructura de covarianza:
     * **Caso 1 (`Payment_Ratio = 0,95`, `Credit_Score = 460`):** Límites de Tukey de `Payment_Ratio` $= [0{,}105,\; 1{,}465]$ (`TRUE`); límites de `Credit_Score` $= [441,\; 825]$ (`TRUE`). Pero en la nube conjunta ($r = 0{,}767$), quien paga el 95 % de su deuda supera los 650 puntos; tener 460 cae en el vacío absoluto del cuadrante inferior derecho.
     * **Caso 2 (`Annual_Income = 3 000 000 ₹`, `Credit_Limit = 200 ₹`):** Límites de Tukey de `Annual_Income` $= [-851\,089,\; 3\,172\,539]$ (`TRUE`); límites de `Credit_Limit` $= [-776\,000,\; 1\,712\,000]$ (`TRUE`). Pero con $r = 0{,}974$, ganar 3 millones y tener 200 rupias de cupo viola por completo la relación conjunta.
5. **Las 6 geometrías bivariadas de la cartera:**
   1. *Lineal fuerte directa:* `Annual_Income` vs. `Credit_Limit` ($r = 0{,}974$).
   2. *Lineal inversa:* `Credit_Utilization` vs. `Credit_Score` ($r = -0{,}599$).
   3. *Bloque rectangular (independencia lineal):* `Annual_Income` vs. `Credit_Score` ($r = 0{,}032$).
   4. *Efecto cuña / techo físico:* `Credit_Limit` vs. `Outstanding_Balance` ($r = 0{,}697$, ningún cliente supera el techo diagonal del 95 % de su cupo).
   5. *Efecto embudo / frontera superior:* `Monthly_Spending` vs. `Payment_Ratio`.
   6. *Escalón ordinal:* `Credit_Limit` según los 5 niveles ordenados de `Card_Type`.

---

### Módulo 8: Estructura Multivariada Conjunta (S01, S03 & S05)

1. **Matriz de correlaciones $\mathbf{R}_{26 \times 26}$ y Mapa de Calor con Clustering Jerárquico (`corrplot(..., order = "hclust")`):**
   * Reordena automáticamente las 26 variables agrupando bloques colineales:
     * **Colinealidades extremas ($r > 0{,}95$):** `Outstanding_Balance – Statement_Balance` ($r = 0{,}997$), `Monthly_Spending – Reward_Points_Earned` ($r = 0{,}980$), `Annual_Income – Credit_Limit` ($r = 0{,}974$), `Credit_Limit – Reward_Points_Earned` ($r = 0{,}958$), `Annual_Income – Monthly_Spending` ($r = 0{,}945$).
     * **Bloque de riesgo aislado del tamaño:** `Credit_Score` solo se asocia con `Payment_Ratio` ($+0{,}767$) y `Credit_Utilization` ($-0{,}599$).
2. **Verificación algebraica de las 3 propiedades de $\mathbf{R}$:**
   * Diagonal exactamente unitaria (`diag(R) == 1`: `TRUE`).
   * Simetría perfecta (`isSymmetric(R)`: `TRUE`).
   * Semidefinida positiva ($\lambda_k \ge 0$: `TRUE`, con $\lambda_{\max} = 11{,}8554$ y $\lambda_{\min} = 0{,}0000$). Ese $\lambda_{\min} \approx 0$ es la prueba espectral de que existen combinaciones lineales exactas o casi exactas dentro de las 26 variables.
3. **Coordenadas Paralelas (`MASS::parcoord`, muestra $n = 5\,000$, 12 variables):**
   * Coloreando a los clientes según su banda de `Credit_Score` (**Rojo** < 580, **Gris** 580–669, **Verde** $\ge 670$), se observa que en las variables de dinero las tres bandas se mezclan en el centro, pero al llegar a `Payment_Ratio`, `Credit_Utilization` y `Credit_Score` los haces rojo y verde se separan de forma opuesta.
4. **Matriz de dispersión `pairs()` enriquecida (3 paneles):**
   * Diagonal con histogramas (`panel.hist`), triángulo inferior con nubes de dispersión y triángulo superior con coeficientes de correlación escalados tipográficamente por $|r|$ (`panel.cor`).

---

### Módulo 9: Vector de Medias, Centroide y el Límite de la Distancia Euclidiana (S06)

1. **Definición matricial del centroide y propiedad de minimización cuadrática:**
   $$\bar{\mathbf{x}} = \frac{1}{n}\mathbf{X}'\mathbf{1}_n$$
   * Se verifica en código sobre `Annual_Income` (`1 479 318 ₹`) y `Credit_Limit` (`709 677 ₹`) que `colMeans(X)` y `(1/n) * t(X) %*% rep(1, n)` son idénticos, y que desplazar $\bar{\mathbf{x}}$ en $\pm 1\,\%$ de la desviación estándar incrementa estrictamente la suma de cuadrados $\sum_{i=1}^n \|\mathbf{x}_i - \mathbf{a}\|^2$.
2. **¿Un centro o varios? La ilusión del centroide global:**
   * Al calcular el centroide por nivel de `Card_Type`, se demuestra que el cupo medio global (`709 677 ₹`) **no representa a ningún grupo**:
     * `Basic`: `109 863 ₹` | `Silver`: `279 396 ₹` | `Gold`: `564 980 ₹` | `Platinum`: `1 228 841 ₹` | `Signature`: `2 930 701 ₹`.
   * En cambio, en `Credit_Score` los 5 centros grupales (`627,5` a `637,5`) están pegados a la media global (`630,7`).
3. **Fragilidad de la media frente a errores sistemáticos (Punto de ruptura = 0):**
   * **Escenario A (1 sola fila multiplicada por 100):** en $n = 50\,000$, la media apenas sube un `0,19 %` (`+2 769 ₹`).
   * **Escenario B (bug sistemático de unidades $\times 1\,000$ en el 0,5 % de la base = 250 filas):** la media explota un **+495 %** (pasa de `1 479 318 ₹` a `8 807 624 ₹`), mientras que la **mediana marginal** casi no se mueve (pasa de `1 127 630 ₹` a `1 131 856 ₹`) y la media recortada al 10 % sube solo a `1 229 737 ₹`.
4. **Por qué la distancia euclidiana falla (Experimento de los clientes A y B):**
   * Desde el centroide $(\overline{\text{Ingreso}}, \overline{\text{Cupo}})$, se crean dos clientes a exactamente $+0{,}5\,\sigma$ en cada eje:
     * **Cliente A** ($+0{,}5\,\sigma_{\text{Ing}},\; +0{,}5\,\sigma_{\text{Cupo}}$): va a favor de la correlación ($r = 0{,}974$).
     * **Cliente B** ($+0{,}5\,\sigma_{\text{Ing}},\; -0{,}5\,\sigma_{\text{Cupo}}$): va en contra de la correlación.
   * **Resultado:** Ambos tienen exactamente la misma **distancia euclidiana** (`752 802 ₹`), pero la **distancia de Mahalanobis** es **$d_M(A) = 0{,}51$** (cliente completamente normal) frente a **$d_M(B) = 3{,}10$** (**6,1 veces más lejos**, un cliente anómalo que gana mucho y tiene poco cupo).

---

### Módulo 10: Dispersión y Dependencia — La Matriz de Covarianzas $\mathbf{S}$ (S07)

1. **Forma matricial y Corrección de Bessel:**
   $$\mathbf{S} = \frac{1}{n - 1}\mathbf{X}_c'\mathbf{X}_c, \qquad \mathbf{X}_c = \mathbf{X} - \mathbf{1}_n\bar{\mathbf{x}}'$$
2. **Las 3 propiedades de $\mathbf{S}$ y su conexión con PCA:**
   * Diagonal = varianzas ($s_{jj} = s_j^2$); simétrica ($s_{jk} = s_{kj}$); y **semidefinida positiva** ($\mathbf{a}'\mathbf{S}\mathbf{a} \ge 0$).
   * **Demostración en código:** Para $\mathbf{a} = (1, -1, 0, 0)'$ ("ingreso menos cupo"), se comprueba que `var(X %*% a)` es idéntico a `t(a) %*% S %*% a`. Como ninguna varianza puede ser negativa, $\mathbf{a}'\mathbf{S}\mathbf{a} \ge 0$ siempre; y buscar el vector unitario $\mathbf{a}$ que maximiza $\mathbf{a}'\mathbf{S}\mathbf{a}$ es exactamente el **Análisis de Componentes Principales**.
3. **El problema de las unidades en $\mathbf{S}$ y el paso algebraico a $\mathbf{R}$:**
   * En la submatriz de 4 variables (`Annual_Income`, `Credit_Limit`, `Statement_Balance`, `Credit_Score`), `Annual_Income` acapara el **74,2 %** de la traza de $\mathbf{S}$ y `Credit_Score` el **0,0000002 %** solo por estar en rupias al cuadrado. Por ello se trabaja con la matriz estandarizada:
     $$\mathbf{R} = \mathbf{D}^{-1/2}\mathbf{S}\mathbf{D}^{-1/2} = \operatorname{cov}(\mathbf{Z}), \qquad \mathbf{D} = \operatorname{diag}(s_1^2, \dots, s_p^2)$$
4. **Traza (varianza total) vs. Determinante (varianza generalizada) y Singularidad:**
   * Con las 26 variables numéricas: $\operatorname{tr}(\mathbf{R}_{26}) = 26$, pero $\det(\mathbf{R}_{26}) = 8{,}65 \times 10^{-30} \approx 0$ y $\lambda_{\min} = 6{,}56 \times 10^{-15} \approx 0$.
   * **Causa exacta demostrada en código:** `Monthly_Spending` es la suma exacta de las 7 categorías de gasto (`max(abs(Monthly_Spending - rowSums(cat_gasto)))` $= 0{,}04$ ₹ por redondeo de centavos). La nube de 26 dimensiones es plana en al menos una dirección.
5. **Auditoría de invertibilidad (`revisar()`) y descarte de 5 variables derivadas/redundantes:**
   * Se retiran:
     1. `Monthly_Spending` (suma exacta de las 7 categorías de gasto).
     2. `Payment_Ratio` (cociente derivado `Payment_Amount / Statement_Balance`).
     3. `Credit_Utilization` (cociente derivado `Outstanding_Balance / Credit_Limit`).
     4. `Reward_Points_Earned` ($r = 0{,}980$ con `Monthly_Spending`).
     5. `Outstanding_Balance` ($r = 0{,}997$ con `Statement_Balance`).
   * **Resultado con las 21 variables activas restantes:** relación $n/p = 2\,381$ (muy superior al mínimo de 10), 0 % faltantes, $|r|_{\max} = 0{,}97$, $\lambda_{\min}(\mathbf{R}_{21}) = 0{,}018 > 0$ y número de condición $\kappa = 547 < 1\,000$ (**matriz bien condicionada e invertible**).

---

### Módulo 11: Variable Aleatoria Multivariante — Distribución Conjunta y Marginales (S08 & S09)

1. **Caso discreto (`Card_Type` $\times$ `Banda_Riesgo`):**
   * La distribución conjunta $p_{jk} = P(\text{Card\_Type} = j, \text{Riesgo} = k)$ suma 1 sobre las 20 celdas (la celda más frecuente es `Gold · Riesgo Medio` con **13,3 %**).
   * Sumando por filas y columnas se obtienen las **marginales** (ej. riesgo Alto 24,5 %, Medio 42,6 %, Bajo 28,9 %, Muy bajo 4,0 %). Todo histograma o tabla univariada de los módulos previos era una marginal empírica.
2. **Las marginales NO reconstruyen la conjunta:**
   * Comparando la tabla real $p_{jk}$ contra el producto de marginales $p_{j\cdot}p_{\cdot k}$:
     * En `Card_Type` $\times$ `Riesgo`, el desvío máximo es de solo **0,79 puntos porcentuales** (casi independientes).
     * En `Occupation` $\times$ `Card_Type`, el desvío alcanza **9,4 puntos porcentuales** y existen celdas estructuralmente vacías: **ningún `Student` tiene tarjeta distinta de `Basic`, y ningún `Business Owner` tiene tarjeta `Basic`**. Esa estructura se pierde irremediablemente si solo se miran las marginales por separado.
3. **Experimento de barajado (`sample`) en el caso continuo (`Credit_Utilization` vs. `Credit_Score`):**
   * Al permutar al azar el vector `Credit_Score`, su media (`630,7`), desviación (`71,5`) y mediana (`642`) quedan **exactamente idénticas** (misma marginal), pero la correlación con `Credit_Utilization` cae de **$r = -0{,}599$ a $r = -0{,}005$**, y el porcentaje de clientes concordantes (del mismo lado de la media en ambas variables) pasa del **29,0 %** real al **49,8 %** del azar.
   * **Dónde queda $\mathbf{S}$:** Al barajar, la diagonal de $\mathbf{S}$ no se mueve; solo colapsa a cero la covarianza fuera de la diagonal.
4. **Adelanto de la Paradoja de Simpson:**
   * En toda la cartera junta (marginalizando sobre `Card_Type`), la correlación entre `Monthly_Transactions` y `Avg_Transaction_Value` es **positiva ($r = +0{,}136$)**. Dentro de cada tipo de tarjeta es **negativa en las cinco** (`Basic`: $-0{,}209$, `Silver`: $-0{,}354$, `Gold`: $-0{,}411$, `Platinum`: $-0{,}357$, `Signature`: $-0{,}611$).

---

### Módulo 12: Distribución Condicional e Independencia (S10)

1. **Asimetría de las probabilidades condicionales ($P(Y \mid X) \neq P(X \mid Y)$):**
   * En la tabla `Occupation` $\times$ `Card_Type`:
     $$P(\text{Basic} \mid \text{Student}) = \mathbf{100\,\%}, \qquad P(\text{Student} \mid \text{Basic}) = \mathbf{38{,}2\,\%}$$
   * Confundir ambas llevaría al área comercial a creer que filtrando tarjetas `Basic` solo encontrará estudiantes, equivocándose en **62 de cada 100 clientes**.
2. **Las 3 definiciones equivalentes de independencia y $V$ de Cramér:**
   * $f(x,y) = f_X(x)f_Y(y) \iff f(y\mid x) = f_Y(y) \iff f(x\mid y) = f_X(x)$.
   * En `Card_Type` vs. `Riesgo`, la prueba $\chi^2$ da $p = 3{,}7 \times 10^{-34}$ por el tamaño muestral $n = 50\,000$, pero la **$V$ de Cramér es $0{,}034$** (independencia práctica: todas las filas condicionales calcan la marginal). En `Occupation` vs. `Card_Type`, **$V = 0{,}465$** (dependencia fuerte).
3. **Condicionamiento continuo por rebanadas (terciles) y la Normal Condicional:**
   * **Caso 1 (`Credit_Score` dado tercil de `Credit_Utilization`):** El centro cae de `678,8` (uso bajo) a `633,5` (medio) y `579,8` (alto) —casi **99 puntos de caída**—, mientras la desviación estándar (`57,6` a `59,6`) y la asimetría permanecen casi constantes. Además, las rebanadas finas confirman la fórmula teórica de la normal bivariada:
     $$E[Y \mid X = x] = \mu_Y + \rho\frac{\sigma_Y}{\sigma_X}(x - \mu_X), \qquad \operatorname{SD}(Y \mid X = x) = \sigma_Y\sqrt{1 - \rho^2} = 57{,}2 < 71{,}5$$
   * **Caso 2 — La trampa de $r \approx 0$ (`Credit_Score` dado tercil de `Payment_Amount`):** La correlación lineal es casi cero ($r = +0{,}049$) y la media condicional apenas cambia (`622,8` a `634,6`). Pero **no son independientes**: la desviación estándar condicional cae de **`79,9`** en el tercil de pago bajo a **`63,5`** en el tercil de pago alto, y el percentil 10 sube de **`510`** a **`551`**. Quienes pagan montos bajos concentran la cola de peor riesgo.
4. **Resolución de la Paradoja de Simpson:**
   * `Card_Type` es una **variable confusora**: al subir de `Basic` a `Signature`, aumentan simultáneamente el promedio de transacciones (de `55,0` a `119,7`) y el ticket medio (de `389 ₹` a `2 532 ₹`, correlación entre centros $= +0{,}96$). Al mezclar las tarjetas, la pendiente positiva entre los 5 centros domina sobre la pendiente negativa real dentro de cada tarjeta ($r$ promedio dentro $= -0{,}39$).
5. **Ley de la Varianza Total verificada exactamente:**
   $$\operatorname{Var}(Y) = E[\operatorname{Var}(Y \mid X)] + \operatorname{Var}(E[Y \mid X])$$
   * Para `Credit_Score` (`Var = 5 113,1`): varianza dentro de terciles de uso $= 3\,476{,}2$ + varianza entre centros $= 1\,636{,}9$ ($= 5\,113{,}1$ exacto; el **32,0 %** de la varianza total del puntaje la explica solo el tercil de uso del cupo).
6. **Condicional en $p$ dimensiones y por qué $\boldsymbol\Sigma_{22}$ debe ser invertible:**
   $$\mathbf{X}_1 \mid \mathbf{X}_2 = \mathbf{x}_2 \sim \mathcal{N}\!\left(\boldsymbol\mu_1 + \boldsymbol\Sigma_{12}\boldsymbol\Sigma_{22}^{-1}(\mathbf{x}_2 - \boldsymbol\mu_2),\; \boldsymbol\Sigma_{11} - \boldsymbol\Sigma_{12}\boldsymbol\Sigma_{22}^{-1}\boldsymbol\Sigma_{21}\right)$$
   * Sabiendo que un cliente tiene `Credit_Utilization = 0,80` y `Payment_Ratio = 0,40`, el puntaje esperado cae de `631` ($\text{DE} = 71{,}5$) a **`485` ($\text{DE} = 26{,}6$)** —la varianza condicional se reduce al **13,8 %** de la marginal—, y los 46 clientes reales con ese perfil tienen media `482`.
   * Si se intenta condicionar simultáneamente en el gasto total y sus 7 categorías, `solve()` falla porque $\boldsymbol\Sigma_{22}$ es singular ($\kappa \approx 10^{11}$).

---

### Módulo 13: Normal Multivariante, Distancia de Mahalanobis y Gráfico Q-Q

1. **Elipse de concentración del 95 % vs. bandas univariadas ($\pm 2\,\text{DE}$):**
   * En el plano `Credit_Utilization` vs. `Credit_Score`:
     * **1 088 clientes** caen **fuera de la elipse del 95 %** a pesar de tener ambas variables dentro de $\pm 2\,\text{DE}$ (clientes con poco uso del cupo pero puntaje bajo, contrarios a la correlación).
     * **1 814 clientes** tienen alguna variable fuera de $\pm 2\,\text{DE}$ pero caen **dentro de la elipse** porque son extremos coherentes con la correlación.
2. **Fórmula de Mahalanobis y comparación contra la distancia Euclidiana en $p = 21$ dimensiones:**
   $$d_M^2(\mathbf{x}_i) = (\mathbf{x}_i - \bar{\mathbf{x}})'\mathbf{S}^{-1}(\mathbf{x}_i - \bar{\mathbf{x}})$$
   * Sobre las 21 variables activas (con $\log(x+1)$ en las 16 asimétricas), de los **500 clientes más lejanos (top 1 %)** según distancia euclidiana estandarizada y según Mahalanobis, **solo coinciden 159**. La euclidiana marca a clientes "grandes pero coherentes" (mediana de ingreso en el percentil 98), mientras que Mahalanobis detecta combinaciones incoherentes.
3. **Corte $\chi^2_{21}$ y Gráfico Q-Q (Variables crudas vs. transformadas con $\log(x+1)$):**
   * En las variables crudas, el Q-Q plot se curva desde el principio (mediana observada `14,0` vs. teórica `20,3`, y en el percentil 99,9 % alcanza `333,7` vs. `46,8`), dejando **8,80 %** de clientes por encima del corte $\chi^2_{21;\,0{,}975} = 35{,}5$ (y **8,33 %** por encima del corte del 99 % $= 38{,}9$).
   * Al aplicar $\log(x+1)$ a las 16 variables con $|\text{asimetría}| > 1$, el cuerpo del Q-Q plot se alinea sobre la recta de 45° (mediana observada `19,9` vs. `20,3` teórica) y el exceso por encima del corte del 99 % baja a **3,28 % (1 641 clientes)**.
4. **Radiografía de los 1 641 "casos raros" y decisión de negocio:**
   * De los 1 641 casos raros por Mahalanobis, **1 055 (el 64,3 %) no tienen ninguna variable con $|Z| > 3$**: son completamente invisibles para filtros univariados.
   * **¿Quiénes son?:** Son clientes de **perfil disparejo** (tienen ingresos y consumos altos en casi todo, pero **una categoría de gasto en cero**, quedando a $-4\,\sigma$ o $-5\,\sigma$ en escala logarítmica en esa categoría), con peor puntaje mediano (`595` vs. `643` del resto) y menor ratio de pago (`0,66` vs. `0,85`).
   * **¿Se borran? No:** Quitarlos cambia la matriz de correlaciones $\mathbf{R}$ en máximo `0,006` y la media del score en `0,9` puntos. Como no distorsionan las estimaciones y representan un segmento real de mayor riesgo, **se conservan y se etiquetan con la columna `Caso_Raro_Mahalanobis`** en la capa `silver`.

---

### Módulo 14: Pruebas de Hipótesis Formales

1. **Normalidad Univariada (Lilliefors en $n = 50\,000$ y Shapiro-Wilk en submuestra $n = 5\,000$):**
   * Se evalúan `Credit_Score`, `Age`, `Annual_Income` y `Payment_Ratio`.
   * **Resultado:** Las 4 rechazan $H_0$ con $p < 2{,}2 \times 10^{-16}$ (incluso `Credit_Score`, que tiene $W = 0{,}9694$).
   * **Defensa clave en sustentación:** En muestras masivas ($n = 50\,000$), el error estándar tiende a cero con $1/\sqrt{n}$ y cualquier desviación mínima de la campana gaussiana ideal produce $p \approx 0$. Además, `shapiro.test()` en R tiene un límite estricto de $5\,000$ observaciones. Por eso la decisión práctica se apoya en la magnitud de la asimetría y en el Q-Q plot, no en el $p$-valor aislado.
2. **Normalidad Multivariante de Mardia ($b_{1,p}$ de asimetría y $b_{2,p}$ de curtosis, $p = 21$, $m = 1\,500$):**
   $$b_{1,p} = \frac{1}{n^2}\sum_{i=1}^n\sum_{j=1}^n g_{ij}^3, \qquad b_{2,p} = \frac{1}{n}\sum_{i=1}^n g_{ii}^2, \qquad g_{ij} = (\mathbf{x}_i - \bar{\mathbf{x}})'\mathbf{S}^{-1}(\mathbf{x}_j - \bar{\mathbf{x}})$$
   * Se ejecuta sobre $m = 1\,500$ clientes porque la matriz $\mathbf{G}$ de $50\,000 \times 50\,000$ tendría $2\,500$ millones de celdas.
   * **Sin transformar:** Estadístico de asimetría $= 196\,244$ (vs. $\text{gl} = 2\,024$ de la $\chi^2$) y $Z_{\text{curtosis}} = 434{,}9$ ($p < 2{,}2 \times 10^{-16}$).
   * **Con $\log(x+1)$:** El estadístico de asimetría se reduce más de 25 veces (a `7 535`) y la curtosis baja más de 12 veces (a `35,6`), confirmando la mejora del Q-Q plot, aunque sigue rechazando $H_0$ por las variables infladas en cero.
3. **Significancia de Correlaciones (`cor.test`, $H_0: \rho = 0$):**
   * `Annual_Income – Credit_Limit`: $r = 0{,}974$, $t = 959{,}5$, $\text{gl} = 49\,998$, $p < 2{,}2 \times 10^{-16}$.
   * `Payment_Ratio – Credit_Score`: $r = 0{,}767$, $t = 267{,}2$, $\text{gl} = 49\,998$, $p < 2{,}2 \times 10^{-16}$.
   * `Credit_Utilization – Credit_Score`: $r = -0{,}599$, $t = -167{,}3$, $\text{gl} = 49\,998$, $p < 2{,}2 \times 10^{-16}$.

---

### Módulo 15: Preparación de Datos para PCA y Clustering (Arquitectura Medallion)

1. **Regla reproducible de transformación sobre las 26 variables numéricas:**
   * **5 excluidas por colinealidad/derivación:** `Monthly_Spending`, `Payment_Ratio`, `Credit_Utilization`, `Reward_Points_Earned`, `Outstanding_Balance`. (Nota: `Payment_Ratio`, `Credit_Utilization` y `Monthly_Spending` se reservan como **variables suplementarias/ilustrativas** para interpretar los ejes sin contaminar la construcción de la matriz).
   * **16 transformadas con $\log(x + 1)$ + `scale()`** (todas las retenidas con $|\text{asimetría}| > 1$): `Annual_Income`, `Credit_Limit`, `Card_Age_Months`, `Avg_Transaction_Value`, las 7 categorías de gasto, `Statement_Balance`, `Payment_Amount`, `Cash_Advance_Amount`, `International_Transactions` y `Reward_Points_Redeemed`.
   * **5 estandarizadas únicamente con `scale()`** ($|\text{asimetría}| \le 1$): `Age` ($0{,}69$), `Monthly_Transactions` ($0{,}54$), `EMI_Count` ($0{,}67$), `Mobile_App_Login` ($0{,}33$) y `Credit_Score` ($-0{,}58$).
2. **Codificación *One-Hot* de las categóricas y "la trampa de las *dummies*":**
   * `Gender` (2), `Occupation` (6) y `Card_Type` (5) se convierten en **13 columnas binarias 0/1** (`model.matrix(~ f - 1)`).
   * **Demostración matemática clave:** Como cada bloque de *dummies* suma exactamente 1 en todas las filas, la matriz completa de $k$ *dummies* es singular ($\det(\mathbf{R}_{\text{card}}) = 0$, $\lambda_{\min} = 0$).
   * **Dos reglas de oro:**
     1. Para métodos que invierten $\mathbf{S}$ (regresión, Mahalanobis): usar **$k - 1$ columnas** (categoría de referencia).
     2. Para PCA y clustering: si se incluyen las $k$ columnas estandarizadas, deben **ponderarse dividiendo por $\sqrt{k}$** para que la variable categórica completa pese lo mismo que 1 variable numérica y no secuestre las componentes.
3. **Exportación reproducible:**
   * `data/silver/credit_card_silver.csv` y `.rds` (tabla limpia, factores tipados, banda de riesgo y bandera `Caso_Raro_Mahalanobis`).
   * `data/gold/credit_card_gold_pca.csv` (`Customer_ID` + 21 variables numéricas transformadas y estandarizadas con media 0 y varianza 1 + 13 *dummies*).

---

### Módulo 16: Componentes Principales I — ¿Un Número o Varios?

1. **El efecto de estandarizar antes de correr `prcomp()`:**
   * **Sin estandarizar (sobre $\mathbf{S}$ en rupias):** La CP1 "guarda" el **91,8 %** de la varianza total, pero `Annual_Income` tiene un peso de **0,884**: no es un resumen multivariado, es simplemente el ingreso en rupias disfrazado de componente.
   * **Estandarizado con $\log(x+1)$ (sobre $\mathbf{R}$, 21 variables):** La CP1 guarda el **50,1 %** (`10,519 / 21`), ninguna variable acapara el vector de pesos por su escala, la CP2 guarda el **5,3 %** (`1,112 / 21`) y la CP3 el **4,8 %** (`1,002 / 21`).
   * **Criterios de retención:** Solo **3 componentes** tienen valor propio $\lambda > 1$ (criterio de Kaiser), y se necesitan **8 componentes** para superar el 80 % de la varianza acumulada.
2. **Lectura sustantiva de los pesos (con signos fijados para interpretación directa):**
   * **C1 = Tamaño del cliente (50,1 %):** Carga de forma pareja ($\approx +0{,}23$ a $+0{,}30$) en `Credit_Limit`, `Annual_Income`, `Statement_Balance`, `Payment_Amount`, las 7 categorías de gasto, `Avg_Transaction_Value`, `Monthly_Transactions` y `Mobile_App_Login`. Su correlación con la variable suplementaria `Monthly_Spending` es **$+0{,}87$**, y con `Credit_Score` es prácticamente cero (**$-0{,}012$**).
   * **C2 = Riesgo crediticio (5,3 %):** Dominada por `Credit_Score` (peso **$-0{,}72$**), acompañada en dirección de riesgo por `Cash_Advance_Amount` ($+0{,}48$) y en dirección de estabilidad por `Card_Age_Months` ($-0{,}48$). Las variables suplementarias que no entraron al PCA lo confirman: C2 se correlaciona **$-0{,}55$** con `Payment_Ratio` y **$+0{,}45$** con `Credit_Utilization`.
   * **C3 = Edad / Demografía (4,8 %):** Dominada casi exclusivamente por `Age` (peso **$+0{,}88$**).
3. **El costo para la Gerencia de decidir con un solo número:**
   * Si el objetivo es detectar al **20 % de clientes con peor `Credit_Score` (10 046 clientes)** seleccionando al 20 % más alto de un solo índice:
     * Ordenando por **C1 (el mejor resumen de un número)**: solo detecta **1 832 clientes (18,2 %)** y **se le escapan 8 214 (81,8 %)** —rinde igual que elegir clientes al azar—.
     * Ordenando por **C2 (riesgo)**: detecta **6 580 clientes (65,5 %)**.
   * **Conclusión:** La Gerencia necesita obligatoriamente **dos números**: C1 (exposición/tamaño) y C2 (riesgo).

---

### Módulo 17: Componentes Principales II — El Mapa de la Cartera y el Biplot

1. **El Biplot (Clientes y Variables en el plano C1–C2, que guarda el 55,4 %):**
   * Las coordenadas de las flechas $\big(w_{j1}\sqrt{\lambda_1},\; w_{j2}\sqrt{\lambda_2}\big)$ son exactamente las correlaciones de cada variable con C1 y C2.
   * **Ángulos entre vectores:**
     * `Annual_Income` vs. `Credit_Limit`: **$1{,}1^\circ$** (colineales sobre el eje horizontal C1).
     * `Annual_Income` vs. `Credit_Score`: **$89{,}5^\circ$** (prácticamente **ortogonales / perpendiculares**: el tamaño y el riesgo son dimensiones independientes).
     * `Credit_Score` vs. `Cash_Advance_Amount`: **$136{,}5^\circ$** (sentidos opuestos sobre el eje vertical C2).
2. **¿Se separan los grupos conocidos (`Card_Type` y `Occupation`) en el mapa?:**
   * Medido en desviaciones estándar dentro de grupo:
     * **En C1 (Tamaño):** `Card_Type` **sí separa** la cartera en lóbulos escalonados (`Basic`: $-2{,}90$, `Silver`: $-1{,}40$, `Gold`: $+0{,}09$, `Platinum`: $+1{,}85$, `Signature`: $+3{,}82$). `Occupation` también desplaza los centros en C1 (`Student`: $-2{,}77$ hasta `Business Owner`: $+2{,}77$).
     * **En C2 (Riesgo):** Los 5 tipos de tarjeta tienen sus centros entre $-0{,}10$ y $+0{,}07$ DE, y las 6 ocupaciones entre $-0{,}02$ y $+0{,}01$ DE. **Las nubes se solapan al 100 % en el eje vertical**. Ni el tipo de tarjeta ni la ocupación sirven para filtrar riesgo.
3. **El Mapa de Seguimiento Operativo (Dos cortes, tres zonas):**
   * Usando $C_2 > 1\,\text{DE}$ como umbral de riesgo alto y la mediana de $C_1$ para separar exposición:
     * **Zona A (Riesgo alto + Cliente grande):** **4 226 clientes (8,5 %)**, puntaje medio `532`, cupo mediano `831 000 ₹`. **Prioridad #1:** seguimiento intensivo con llamada de gestor.
     * **Zona B (Riesgo alto + Cliente pequeño):** **3 969 clientes (7,9 %)**, puntaje medio `537`, cupo mediano `174 000 ₹`. **Prioridad #2:** seguimiento preventivo automatizado de bajo costo (SMS/app).
     * **Zona C (Sin seguimiento):** **41 805 clientes (83,6 %)**, puntaje medio `650`, cupo mediano `407 000 ₹`.
   * Con solo el **16,4 %** de la cartera intervenida (Zonas A + B = 8 195 clientes), la Gerencia captura al **57,8 % (5 811)** del 20 % con peor puntaje de todo el banco.
4. **Experimento Con y Sin *One-Hot* de `Card_Type` en el PCA:**
   * **Sin *one-hot* (21 columnas):** C1 guarda `50,1 %`, C2 guarda `5,3 %`.
   * **Con *one-hot* sin ponderar (26 columnas):** Las 5 *dummies* (que suman varianza 5) secuestran la segunda componente: la correlación de la nueva C2 con la C2 original de riesgo **cae a `0,11`**.
   * **Con *one-hot* ponderado por $1/\sqrt{5}$:** El mapa no se altera en absoluto ($\text{cor}(C_1, C_1^{\text{orig}}) = 0{,}9999$ y $\text{cor}(C_2, C_2^{\text{orig}}) = 0{,}9995$), y se verifica que las *dummies* de tarjeta se proyectan enteras sobre C1 y tienen correlación `0,00` con C2.

---

## 🧩 Talleres Aplicados del Curso (`TallerPca/` y `tallerAnalisisFactorial/`)

Además del documento maestro de `Entrega/`, el repositorio incluye los talleres prácticos diseñados bajo el formato ejecutivo para la Gerencia (👀 *Qué vemos*, 💼 *Qué significa para el cliente*, ✅ *Qué decide el cliente*) sobre las **9 variables clave de la ficha** (`Annual_Income`, `Credit_Limit`, `Statement_Balance`, `Payment_Amount`, `EMI_Count`, `Monthly_Transactions`, `Avg_Transaction_Value`, `International_Transactions` y `Credit_Score`, aplicando `log1p` a las 6 con $|\text{asimetría}| > 1$):

### 1. Talleres de Componentes Principales I y II (`TallerPca/`)
* Resumen el caso de negocio enfocado en las 9 variables de la ficha rápida de la Gerencia, mostrando la pérdida de clientes riesgosos al usar un solo índice (CP1 = 64,3 % en las 9 variables) y la construcción del biplot y las zonas de intervención.

### 2. Taller de Análisis Factorial (`tallerAnalisisFactorial/taller_analisis_factorial.Rmd`)
Responde a la pregunta de los analistas del banco: *«¿Existe una sola habilidad o capacidad económica detrás de las variables de la ficha, y el puntaje crediticio hace parte de ella?»*
1. **Índice KMO (`psych::KMO`):** El KMO global es **0,71 (aceptable)**; las 8 variables de dinero y uso están entre `0,65` y `0,92`, pero `Puntaje crediticio` tiene **KMO = 0,02 (inaceptable)** porque no comparte varianza común con el resto.
2. **Modelo de 1 factor por máxima verosimilitud (`fa(R, nfactors = 1, fm = "ml")`):**
   * La habilidad común (**Capacidad económica**) explica el **61,9 %** de las diferencias totales (menos que el **64,3 %** de la CP1 del PCA sobre las mismas 9 variables, porque el PCA absorbe parte propia y el análisis factorial solo retiene varianza compartida).
   * **Parte común ($\ell_i^2$) vs. Parte propia ($u_i^2 = 1 - \ell_i^2$):** `Cupo` es **99,1 % común** ($\ell = 0{,}996$), `Ingreso anual` es **97,5 % común** ($\ell = 0{,}987$), `Saldo facturado` **89,6 %**, `Monto pagado` **78,5 %**, y las variables de uso entre **42,7 % y 59,7 %**.
   * **Variable 100 % propia:** El **`Puntaje crediticio` tiene 100,0 % de parte propia** ($\ell = 0{,}018$, comunalidad $= 0{,}0\,\%$). Esto demuestra que no está mal medido, sino que mide una dimensión independiente (conducta de pago).
3. **¿Alcanza una sola habilidad? ($r_{ij}$ vs. $\ell_i \ell_j$):** En **31 de los 36 pares**, $|r_{ij} - \ell_i\ell_j| < 0{,}05$. El mayor residuo ocurre en `Compras al mes – Valor por compra` ($r = 0{,}201$ vs. $\ell_i\ell_j = 0{,}522$, diferencia de $-0{,}321$, reflejo de la paradoja de Simpson entre frecuencia y ticket) y en los cruces de `Saldo` ($-0{,}169$) y `Pago` ($+0{,}108$) con el `Puntaje`.
4. **Modelo de 2 factores (`rotate = "oblimin"`):** El segundo factor carga **0,998 en `Puntaje crediticio`** y menos de 0,17 en todas las demás. Por tanto, **no es una habilidad común con sentido, sino una sola variable vestida de factor**. Al retirar el puntaje y ajustar 2 factores sobre las 8 variables restantes, emerge un segundo factor de *frecuencia vs. ticket* (`Compras al mes` $+0{,}90$ vs. `Valor por compra` $-0{,}37$) correlacionado oblicuamente en **$0{,}43$** con la capacidad económica.
5. **Explicación detallada del taller:** Disponible en [`tallerAnalisisFactorial/explicacion_taller_analisis_factorial.md`](tallerAnalisisFactorial/explicacion_taller_analisis_factorial.md).

---

## 🎤 Banco de Preguntas Clave para la Sustentación Oral

1. **¿Por qué reclasificaron `Card_Type` como ordinal y dejaron `EMI_Count` como cuantitativa si `EMI_Count` solo tiene 7 valores (0 a 6)?**
   * Porque la clasificación estadística (Everitt & Hothorn) no depende de cuántos valores únicos tenga la columna ni de si es `character` o `int`, sino de si existe **magnitud constante y cero absoluto**. `Card_Type` ordena jerárquicamente los productos (`Basic < Silver < Gold < Platinum < Signature`), pero el salto entre niveles no es constante (es ordinal). En cambio, `EMI_Count` cuenta compras a cuotas vigentes: 0 es ausencia total de cuotas y 4 cuotas es exactamente el doble de 2 (es cuantitativa discreta de razón).
2. **Si las variables de gasto tienen entre 8 % y 19 % de datos fuera de los bigotes de Tukey, ¿por qué no los borraron como errores?**
   * Porque los límites de Tukey ($Q_1 - 1{,}5\cdot RIC$, $Q_3 + 1{,}5\cdot RIC$) están calibrados para distribuciones simétricas. En variables con fuerte asimetría positiva o masa puntual en cero (como `Cash_Advance_Amount`, donde el 70,3 % es cero y $Q_1 = 0$), el $RIC$ se comprime y el bigote superior corta la cola derecha legítima de la población. Además, el Módulo 2 demostró que no hay valores negativos ni centinelas.
3. **¿Cómo demuestran que un filtro variable por variable no sirve para detectar anomalías multivariadas?**
   * De tres maneras: (1) Con los dos **Puntos Imposibles** del Módulo 7 (ej. `Payment_Ratio = 0,95` y `Credit_Score = 460`, ambos dentro de las cercas de Tukey univariadas pero en una región vacía del plano conjunto); (2) Con los clientes A y B del Módulo 9, que están a idéntica distancia euclidiana del centroide (`752 802 ₹`), pero B va contra la correlación y tiene distancia de Mahalanobis 6,1 veces mayor (`3,10` vs. `0,51`); y (3) En el Módulo 13, donde el **64,3 % (1 055 de 1 641)** de los casos raros detectados por Mahalanobis ($\chi^2_{21;\,0{,}99}$) no tiene **ninguna** variable con $|Z| > 3$.
4. **¿Por qué fue obligatorio quitar 5 variables numéricas antes de calcular Mahalanobis y el PCA?**
   * Porque con las 26 variables numéricas la matriz de correlaciones/covarianzas es prácticamente singular ($\det(\mathbf{R}_{26}) = 8{,}65 \times 10^{-30}$, $\lambda_{\min} = 6{,}56 \times 10^{-15}$): `Monthly_Spending` es la suma exacta de las 7 categorías de gasto, `Payment_Ratio` y `Credit_Utilization` son cocientes derivados de otras columnas, `Outstanding_Balance` duplica a `Statement_Balance` ($r = 0{,}997$) y `Reward_Points_Earned` duplica al gasto ($r = 0{,}980$). Al retirarlas, las 21 variables activas forman una matriz invertible ($\lambda_{\min} = 0{,}018$, $\kappa = 547 < 1\,000$).
5. **¿Qué es la Paradoja de Simpson en esta cartera y cómo se resolvió?**
   * Al correlacionar `Monthly_Transactions` con `Avg_Transaction_Value` en los 50 000 clientes juntos (marginalizando sobre el tipo de tarjeta), la correlación es **positiva ($r = +0{,}136$)**, dando a entender que quien compra más veces hace compras más caras. Pero al **condicionar por `Card_Type`** (Módulo 12), la correlación es **negativa dentro de cada una de las 5 tarjetas** (de $-0{,}21$ a $-0{,}61$): a igual tarjeta, quien hace más transacciones las hace de menor monto. El signo se invertía porque `Card_Type` es una variable confusora que empuja ambos promedios hacia arriba simultáneamente.
6. **¿Correlación cero implica independencia en esta cartera?**
   * **No.** En el Módulo 12 mostramos dos contraejemplos: (1) Entre `Card_Type` y `Banda_Riesgo` la prueba $\chi^2$ da $p \approx 0$ por $n = 50\,000$, pero $V$ de Cramér es `0,034` (independencia práctica); y (2) Entre `Payment_Amount` y `Credit_Score` la correlación de Pearson es casi cero ($r = +0{,}049$), pero al rebanar por terciles de pago la desviación estándar del puntaje cae de `79,9` a `63,5` y el percentil 10 sube de `510` a `551` (dependencia en la dispersión y en la cola de riesgo).
7. **¿Por qué todas las pruebas de normalidad (Lilliefors, Shapiro-Wilk y Mardia) dieron $p < 2{,}2 \times 10^{-16}$?**
   * En las pruebas univariadas con $n = 50\,000$ (o $n = 5\,000$ en Shapiro-Wilk), la potencia estadística es tan alta que detecta desviaciones triviales respecto a la campana perfecta. En la prueba multivariante de Mardia ($m = 1\,500, p = 21$), el rechazo sí refleja asimetría y curtosis reales causadas por las colas derechas y las variables infladas en cero; no obstante, al aplicar $\log(x+1)$ el estadístico de asimetría de Mardia baja de `196 244` a `7 535` y el cuerpo del Q-Q plot contra $\chi^2_{21}$ se alinea con la diagonal.
8. **¿Qué diferencia hay entre el resumen del PCA (Módulos 16–17) y el factor común del Análisis Factorial (`tallerAnalisisFactorial/`)?**
   * El PCA busca combinaciones lineales que maximicen la **varianza total** (mezclando parte común y parte propia), mientras que el Análisis Factorial modela únicamente la **varianza compartida (comunalidad)** y separa la **parte propia (unicidad)**. Por eso en las 9 variables del taller la CP1 retiene el **64,3 %** y el factor común el **61,9 %**, y el análisis factorial demuestra que `Credit_Score` es **100 % parte propia** (0 % común con la capacidad económica).

---

## 🚀 Cómo Reproducir el Proyecto Completo

### Requisitos en R
Abrir R o RStudio en la raíz del repositorio e instalar los paquetes utilizados en el informe maestro y los talleres:

```r
paquetes <- c("corrplot", "MASS", "nortest", "psych", "GPArotation", "ggplot2", "ggrepel", "knitr", "rmarkdown")
install.packages(setdiff(paquetes, rownames(installed.packages())), repos = "https://cloud.r-project.org")
```

### Renderizar los documentos R Markdown

```r
# 1. Reporte maestro completo (17 Módulos + exportación de capas Silver y Gold)
rmarkdown::render("Entrega/analisis_synthetic_credit_card.Rmd")

# 2. Talleres de Componentes Principales I y II
rmarkdown::render("TallerPca/taller_componentes_principales_I.Rmd")
rmarkdown::render("TallerPca/taller_componentes_principales_II.Rmd")

# 3. Taller de Análisis Factorial
rmarkdown::render("tallerAnalisisFactorial/taller_analisis_factorial.Rmd")
```
