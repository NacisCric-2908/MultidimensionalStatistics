# Todo el trabajo sobre `synthetic_credit_card_customer_behavior_dataset.csv`

> **Documento integral de sustentación.** Reúne y explica *todo* lo que se ha hecho con la base de 50 000 tarjetahabientes simulados: el informe maestro (`Entrega/analisis_synthetic_credit_card.Rmd` / `.html`, 18 módulos y conclusiones), los talleres de Componentes Principales I y II, el taller de Análisis Factorial, el taller del 31 de octubre (PCA + factorial), el taller del 7 de noviembre (T² de Hotelling) y la presentación ejecutiva en PDF.
>
> En cada sección se explica: **qué es el concepto**, **cómo lo aplicamos**, **qué resultados obtuvimos**, **qué decisiones tomamos y por qué**, y **qué significa para el negocio**. Todas las cifras provienen de las salidas renderizadas (HTML) de cada documento, incluidas las tablas paginadas. Cuando una cifra no aparece en ninguna salida se indica como *no reportado*; cuando una cifra es un cálculo aritmético hecho a partir de las cifras reportadas, se indica como *derivado*.

---

## Información general

| Elemento | Detalle |
|---|---|
| **Asignatura** | Estadística Multidimensional (26158 · grupo 020-81 · periodo 2026-3) |
| **Autores** | Oscar Manuel Contreras Gacha (20221020052) · Juan Pablo Sarmiento Ramírez (20221020138) · Steven Navarro Parrales (20221020048) · Juan Diego Grajales Castillo (20221020128) |
| **Dataset** | Kaggle — *Credit Card Customer Behavior Analysis & Prediction*. $n = 50\,000$ clientes simulados, $p = 30$ columnas, montos en **rupias indias (INR, ₹)** |
| **Cliente del caso de negocio** | **Gerencia de Riesgo de Crédito** del banco emisor: decide cada mes qué tarjetahabientes entran al programa de **seguimiento preventivo** (llamada de gestor, congelar aumentos de cupo, reestructuración antes de la mora) |
| **Lenguaje** | R / R Markdown (reportes tejidos a HTML) |

### Dónde vive cada pieza del trabajo

```text
data/
├── bronze/synthetic_credit_card_customer_behavior_dataset.csv   # Crudo e inmutable (50 000 × 30)
├── silver/credit_card_silver.csv | .rds                         # Limpio + Banda_Riesgo + Caso_Raro_Mahalanobis (50 000 × 32)
└── gold/credit_card_gold_pca.csv                                # Customer_ID + 21 numéricas (log1p + scale) + 13 dummies (50 000 × 35)
Entrega/
├── analisis_synthetic_credit_card.Rmd / .html                   # Informe maestro: Módulos 1–18 + conclusiones
└── Analisis_Exploratorio_Credit_Card_Presentacion.pdf           # Presentación ejecutiva (38 diapositivas)
TallerPca/
├── TALLER_Componentes_Principales_I.md                          # Enunciado del taller PCA I
├── taller_componentes_principales_I.Rmd / .html                 # «¿Un número o varios?»
├── taller_componentes_principales_II.Rmd / .html                # «El mapa de su negocio» (versión previa)
└── taller_componentes_principales_II_final.Rmd                  # Versión final de PCA II
tallerAnalisisFactorial/
├── taller_analisis_factorial.Rmd / .html                        # «Lo que las variables comparten»
└── explicacion_taller_analisis_factorial.md                     # Guía explicativa del taller
taller31octubre/TALLER_31oct.Rmd / .html                         # Resumen y dimensiones (PCA + factorial)
TALLER_7nov_CreditoIndia.Rmd / .html                             # ¿Son distintos estos grupos? (Hotelling)
```

### Hilo conductor (la historia en una página)

1. **Conocer la matriz** (Módulos 1–2): qué hay en la base, de qué tipo es cada variable, si hay faltantes, duplicados o valores imposibles.
2. **Mirar cada variable sola** (Módulos 3–6): histogramas, densidades de kernel, boxplots, atípicos de Tukey, estandarización.
3. **Mirar las variables de a dos y todas juntas** (Módulos 7–8): correlación, η², el «punto imposible», matriz de correlaciones, coordenadas paralelas.
4. **Teoría multivariante aplicada** (Módulos 9–12): vector de medias, covarianzas, distribuciones conjuntas, marginales y condicionales, independencia, Simpson.
5. **Normalidad y casos raros** (Módulos 13–14): Mahalanobis, χ², Q-Q, Mardia y pruebas de hipótesis.
6. **Preparar los datos** (Módulo 15): transformaciones, selección de variables, one-hot, exportación silver/gold.
7. **Resumir y explicar** (Módulos 16–18 y talleres): componentes principales, mapa de la cartera, análisis factorial.
8. **Comparar grupos** (taller del 7 de noviembre): T² de Hotelling de una y dos muestras.
9. **Comunicar** (presentación PDF).

---

## Índice

- **Parte I — Informe maestro**
  - Contexto y objetivos del análisis
  - Módulo 1: Inspección previa e importación reproducible
  - Módulo 2: Auditoría y diagnóstico de calidad
  - Módulo 3: Análisis univariado e histogramas
  - Módulo 4: Densidad de kernel
  - Módulo 5: Boxplots y atípicos univariados
  - Módulo 6: Comparación multivariada estandarizada
  - Módulo 7: Análisis bivariado, correlación y el «punto imposible»
  - Módulo 8: Estructura multivariada conjunta
  - Módulo 9: Vector de medias, centroide y distancia euclidiana
  - Módulo 10: Matriz de covarianzas
  - Módulo 11: Distribución conjunta y marginales
  - Módulo 12: Distribución condicional e independencia
  - Módulo 13: Normal multivariante, Mahalanobis y Q-Q
  - Módulo 14: Pruebas de hipótesis
  - Módulo 15: Preparación de datos para PCA y clustering
  - Módulo 16: Componentes Principales I
  - Módulo 17: Componentes Principales II
  - Módulo 18: Análisis Factorial
  - Conclusiones generales del informe
- **Parte II — Talleres de Componentes Principales y Análisis Factorial**
- **Parte III — Taller del 31 de octubre, taller del 7 de noviembre y presentación**
- **Anexo A — Glosario de conceptos**
- **Anexo B — Inconsistencias y puntos a revisar**

---

# Parte I — Informe maestro (`Entrega/analisis_synthetic_credit_card.Rmd`)


## Contexto y objetivos del análisis

### Ficha técnica del informe

El informe principal es el documento reproducible `Entrega/analisis_synthetic_credit_card.Rmd`, tejido a HTML (`Entrega/analisis_synthetic_credit_card.html`). Su encabezado YAML declara:

| Campo | Valor |
|---|---|
| Título | *Estadística Multidimensional — Análisis Exploratorio Integral* |
| Subtítulo | *Dataset Sintético: Comportamiento Crediticio y Riesgo Financiero (S01 a S10, Mahalanobis, Componentes Principales y Análisis Factorial)* |
| Autores | Oscar Manuel Contreras Gacha (`20221020052`), Juan Pablo Sarmiento Ramírez (`20221020138`), Steven Navarro Parrales (`20221020048`), Juan Diego Grajales Castillo (`20221020128`) |
| Fecha | Dinámica: `format(Sys.Date(), '%d/%m/%Y')`. En el HTML renderizado aparece **02/11/2026** |
| Salidas | `html_document` (tabla de contenido hasta nivel 3, secciones numeradas, `df_print: paged`, tema `readable`, resaltado `tango`) y `pdf_document` (TOC nivel 3) |
| Naturaleza de los datos | Dataset sintético sobre comportamiento crediticio, capacidad financiera y riesgo |
| Fuente | Kaggle, *Credit Card Customer Behavior Analysis & Prediction* (`https://www.kaggle.com/code/devraai/credit-card-customer-behavior-analysis-prediction/input`) |

Según el README, la asignatura es Estadística Multidimensional (código `26158`, grupo `020-81`, periodo `2026-3`). El **cliente del caso de negocio** es la **Gerencia de Riesgo de Crédito del banco emisor**: cada mes decide qué tarjetahabientes entran al programa de seguimiento preventivo, que puede consistir en una llamada del gestor, el congelamiento de aumentos de cupo o una reestructuración antes de que el cliente caiga en mora.

> **Detalle de la opción `df_print: paged`:** con esta opción, las tablas que R imprime como `data.frame` se muestran en el HTML como tablas paginadas interactivas, guardadas como JSON dentro del HTML. Por eso dos tablas de esta parte (el diccionario de variables del Módulo 1 y la comparación "fórmula a mano vs. `density()`" del Módulo 4) no aparecen en la versión de texto plano del informe. Sus valores se recuperaron directamente del JSON del HTML y se reproducen más abajo.

#### Chunk de configuración global (`setup`)

Este bloque no forma parte del análisis. Es la configuración global de `knitr`, el motor que "teje" el documento, es decir, que ejecuta el código R y pega sus resultados junto al texto:

```r
knitr::opts_chunk$set(
  echo = TRUE, comment = "#>", fig.width = 9, fig.height = 6,
  fig.align = "center", warning = FALSE, message = FALSE
)
```

- `echo = TRUE` deja el código visible junto a cada resultado, para que el análisis sea **reproducible y verificable**.
- `comment = "#>"` marca con `#>` las líneas de salida de R.
- `fig.width = 9` y `fig.height = 6` (en pulgadas), junto con `fig.align = "center"`, dan a todos los gráficos un tamaño consistente. Algunos chunks lo cambian localmente, por ejemplo `fig.width=11, fig.height=4` en las comparaciones de tres anchos de banda del Módulo 4.
- `warning = FALSE` y `message = FALSE` silencian avisos rutinarios de R, como los de carga de paquetes, para que no ensucien la lectura.
- El informe aclara que **ningún resultado numérico se ve afectado por estas opciones**. Solo cambia la presentación.

### Objetivo general

El documento desarrolla la exploración multidimensional de `bronze/synthetic_credit_card_customer_behavior_dataset.csv`. Son **50.000 clientes simulados** de una tarjeta de crédito, con **30 variables** que describen su perfil demográfico, su capacidad financiera, su comportamiento de gasto y su historial de pago.

El informe recorre, en orden, los métodos y herramientas conceptuales de las sesiones **S01 a S10** de la asignatura, de la sesión de **normal multivariante y distancia de Mahalanobis** y de las **dos sesiones de componentes principales**. Están organizados en **diecisiete módulos encadenados**: cada módulo cierra con sus propias conclusiones y retoma de forma explícita lo que dejó listo el anterior.

| Módulo | Sesión(es) | Contenido declarado |
|---|---|---|
| 1 | S01 & S02 | Importación reproducible y clasificación de las $p$ variables según su verdadera escala de medición, no solo según su tipo de almacenamiento en R |
| 2 | S02 | Auditoría de calidad de la matriz: faltantes, duplicados, rangos y frecuencias |
| 3 | S01 & S03 | Análisis univariado y decisión del número de clases de un histograma |
| 4 | S04 | Densidad de kernel como alternativa al histograma y efecto del ancho de banda $h$ |
| 5 | S03 | Cajas y bigotes, cinco números de Tukey y detección univariada de atípicos |
| 6 | S03 | Por qué hay que estandarizar para comparar variables en escalas distintas |
| 7 | S03 & S04 | Análisis bivariado con una selección **justificada** de los pares que merecen ese análisis, covarianza y correlación, y el "punto imposible" |
| 8 | S05 | Estructura conjunta de las $p$ variables: matriz de correlación, mapa de calor, coordenadas paralelas y matriz de dispersión |
| 9 | S06 | Vector de medias y centroide, y por qué la distancia euclidiana no basta para medir qué tan lejos está un cliente del centro |
| 10 | S07 | Matriz de covarianzas $\mathbf{S}$, su relación exacta con $\mathbf{R}$, varianza total y generalizada, y verificación de que $\mathbf{S}$ es invertible |
| 11 | S08 & S09 | Variable aleatoria multivariante: distribución conjunta y marginales, y lo que se pierde al marginalizar |
| 12 | S10 | Distribución condicional e independencia, paradoja de Simpson en la cartera y ley de la varianza total |
| 13 | Normal multivariante | Distancia de Mahalanobis, gráfico Q-Q contra la $\chi^2$ y qué hacer con cada caso raro |
| 14 | — | Pruebas de hipótesis formales: normalidad univariada y multivariante, y significancia de las correlaciones usadas en los Módulos 7 y 8 |
| 15 | — | Preparación para PCA y *clustering*: transformación de cada variable, selección, codificación *one-hot* de las categóricas y exportación de las tablas limpias |
| 16 | PCA I | Cuánta información guarda cada componente, qué mide y qué se pierde al resumir la cartera en un solo número |
| 17 | PCA II | Mapa de los clientes, biplot, si los grupos conocidos se separan y efecto de incluir el tipo de tarjeta con *one-hot* |

Esta sección cubre los Módulos 1 a 4. Los siguientes se documentan en otras partes.

### Contexto económico del análisis sobre el dataset

El análisis se ubica en el **contexto económico de la India** y usa la **rupia india (INR, ₹)** como unidad monetaria. Los datos describen el comportamiento de clientes de tarjetas de crédito: ingresos, límites de crédito, gastos mensuales, saldos pendientes y pagos realizados. **Todos los valores monetarios del informe están en rupias indias**, lo que permite leer el comportamiento financiero de los clientes dentro del sistema económico indio.

**Por qué importa para el negocio:** las magnitudes no se pueden comparar en bruto con cifras en pesos o dólares. Por ejemplo, un ingreso anual mediano de 1.127.630 ₹ (Módulo 2) solo se juzga como "alto" o "bajo" dentro de la escala india. Para la Gerencia de Riesgo esto significa que los umbrales de alerta (de cupo, de saldo o de avance en efectivo) deben fijarse en la escala de la cartera y no copiarse de otros mercados.

---

## Módulo 1: Inspección previa e importación reproducible (S02)

**Objetivo:** cargar la matriz de datos de forma explícita y verificable, y clasificar cada variable según su **verdadera escala de medición** (taxonomía de Everitt & Hothorn), no según el tipo con que R la guarda.

### 1.1 Mirar antes de leer (`readLines`)

**Qué es.** `readLines(archivo, n = k)` lee las primeras `k` líneas de un archivo como texto plano, sin interpretarlo. Es una buena práctica de reproducibilidad: antes de cargar un archivo en memoria se revisa en crudo para confirmar **cuál es el delimitador de columnas**, **cuál es el separador decimal** y **si hay encabezado**. Si se asumen mal, `read.csv` puede "funcionar" y aun así producir columnas pegadas, números leídos como texto o la primera fila de datos usada como nombres.

**Cómo lo aplicamos.**

```r
ruta_credit <- "../data/bronze/synthetic_credit_card_customer_behavior_dataset.csv"
lineas_muestra <- readLines(ruta_credit, n = 4)
```

La ruta es **relativa** al directorio `Entrega/` y apunta a la capa *bronze*, la de datos crudos e inmutables de la arquitectura Medallion del repositorio.

**Resultado (las 4 primeras líneas en crudo):**

```text
[1] "Customer_ID,Age,Gender,Annual_Income,Occupation,Card_Type,Credit_Limit,Card_Age_Months,Monthly_Spending,Monthly_Transactions,Avg_Transaction_Value,Online_Shopping_Spending,Grocery_Spending,Fuel_Spending,Dining_Spending,Travel_Spending,Entertainment_Spending,Utility_Bill_Spending,Outstanding_Balance,Statement_Balance,Payment_Amount,Payment_Ratio,Credit_Utilization,Cash_Advance_Amount,EMI_Count,International_Transactions,Reward_Points_Earned,Reward_Points_Redeemed,Mobile_App_Login,Credit_Score"
[2] "CC100000,33,M,787406,Self-Employed,Silver,220000.0,20,36733.49,83,427.21,1317.13,9400.14,4339.48,10476.83,3092.29,2275.83,5831.79,149956.45,178851.64,82271.75,0.46,0.7,14839.84,2,0,1081,210,23,492"
[3] "CC100001,58,M,598084,Retired,Basic,112000.0,101,30212.78,72,399.89,3892.84,6134.61,3442.74,3869.99,2020.56,2639.89,8212.15,84159.21,110031.93,104530.33,0.95,0.76,0.0,2,0,606,163,22,607"
[4] "CC100002,40,F,1710737,Private Employee,Platinum,928000.0,12,115895.71,142,837.85,13547.09,40293.0,11946.73,6272.35,1440.7,8502.96,33892.88,342440.99,424486.51,148570.28,0.35,0.38,73713.82,2,3,6857,0,48,549"
```

**Diagnóstico preliminar del informe:**

- **Separador de columnas:** coma (`,`).
- **Separador decimal:** punto (`.`). Se ve en valores como `36733.49`.
- **Encabezado:** presente en la primera fila, con nombres descriptivos.
- **Estrategia de lectura:** `read.csv()` con `header = TRUE`, `sep = ","`, `dec = "."` y `stringsAsFactors = FALSE`.

**Observaciones adicionales de la salida cruda:**

- `Credit_Limit` aparece con formato `220000.0`: cupos redondos escritos como decimales. Esto anticipa que el cupo solo toma valores redondeados a miles (Módulo 3).
- `Cash_Advance_Amount` vale `0.0` en el segundo cliente, la primera pista de la inflación en cero que se documenta más adelante.
- `Reward_Points_Redeemed` vale `0` en el tercer cliente.

### 1.2 Importación explícita

**Qué es.** Importar de forma *explícita* significa declarar todos los parámetros de lectura en lugar de confiar en los valores por defecto. Así el resultado es el mismo en cualquier máquina o configuración regional (*locale*). En algunas configuraciones en español, por ejemplo, el separador decimal por defecto es la coma.

```r
credit <- read.csv(
  file = ruta_credit, header = TRUE, sep = ",", dec = ".",
  stringsAsFactors = FALSE
)
```

**Decisión: `stringsAsFactors = FALSE`.** Las columnas de texto quedan como `character` y no como `factor`. Así R no les impone niveles en orden alfabético. Esto pesa en el caso de `Card_Type`: su orden real (Basic < Silver < Gold < Platinum < Signature) no es el alfabético, y se impone a mano más adelante (gráficos del Módulo 2).

### 1.3 Dimensiones de la matriz de datos ($\mathbf{X} \in \mathbb{R}^{n \times p}$)

**Qué es.** En estadística multivariante los datos se representan como una matriz $\mathbf{X}$ de $n$ filas (observaciones o individuos) por $p$ columnas (variables). Cada fila $\mathbf{x}_i \in \mathbb{R}^p$ es el vector que describe a un cliente.

**Cómo lo aplicamos:** `dim_matriz <- dim(credit)`.

**Resultado:** `[1] 50000 30`, es decir:

- $n = 50000$ observaciones (clientes simulados, filas).
- $p = 30$ variables medidas (columnas).

### 1.4 Estructura y clasificación de variables (S01 & Everitt & Hothorn)

#### Conceptos

- **Tipo de almacenamiento frente a escala de medición.** R guarda cada columna como `character`, `integer` o `numeric`. Ese tipo **no basta** para clasificar una variable en la taxonomía de Everitt & Hothorn:
  - Una variable guardada como texto puede ser **ordinal** y no nominal (es el caso de `Card_Type`).
  - Una variable guardada como entero puede ser **genuinamente cuantitativa** aunque tome pocos valores (es el caso de `EMI_Count`).
- **El criterio real** es si la media, la varianza o un coeficiente de regresión calculados sobre la variable son interpretables, y si sus valores reflejan una **magnitud constante**:
  - Si se cumple, la variable es **cuantitativa**.
  - Si sus valores son solo etiquetas o niveles sin una distancia métrica consistente entre ellos, es **cualitativa**: **nominal** si no hay orden y **ordinal** si lo hay.
- **Cardinalidad.** Es el número de valores únicos distintos que toma una variable. Se calcula con `length(unique(x))`. Sirve como **evidencia** para la clasificación, pero no la decide sola: tener pocos niveles no hace categórica a una variable (un conteo puede tener rango corto y seguir siendo cuantitativo). La cardinalidad es la **señal** que se usó para revisar de cerca los casos límite, como `Card_Type`.

#### Cómo lo aplicamos

```r
str(credit)
n_numericas  <- sum(sapply(credit, is.numeric))
n_categoricas <- sum(sapply(credit, is.character))
c(Numericas_R = n_numericas, Categoricas_R = n_categoricas)

n_niveles <- sapply(credit, function(x) length(unique(x)))   # cardinalidad
sort(n_niveles)
table(credit$Card_Type)
```

#### Resultados

**Salida de `str(credit)`:** `'data.frame': 50000 obs. of 30 variables`.

| Variable | Tipo en R | Primeros valores |
|---|---|---|
| `Customer_ID` | chr | "CC100000" "CC100001" "CC100002" "CC100003" … |
| `Age` | int | 33 58 40 42 19 19 18 51 35 38 … |
| `Gender` | chr | "M" "M" "F" "M" … |
| `Annual_Income` | int | 787406 598084 1710737 712664 1504662 … |
| `Occupation` | chr | "Self-Employed" "Retired" "Private Employee" "Private Employee" … |
| `Card_Type` | chr | "Silver" "Basic" "Platinum" "Silver" … |
| `Credit_Limit` | num | 220000 112000 928000 211000 572000 … |
| `Card_Age_Months` | int | 20 101 12 54 44 59 38 44 74 81 … |
| `Monthly_Spending` | num | 36733 30213 115896 21804 91039 … |
| `Monthly_Transactions` | int | 83 72 142 64 67 66 49 66 46 70 … |
| `Avg_Transaction_Value` | num | 427 400 838 357 1367 … |
| `Online_Shopping_Spending` | num | 1317 3893 13547 7583 19794 … |
| `Grocery_Spending` | num | 9400 6135 40293 5597 9898 … |
| `Fuel_Spending` | num | 4339 3443 11947 1207 13912 … |
| `Dining_Spending` | num | 10477 3870 6272 1929 13865 … |
| `Travel_Spending` | num | 3092 2021 1441 878 2876 … |
| `Entertainment_Spending` | num | 2276 2640 8503 535 2445 … |
| `Utility_Bill_Spending` | num | 5832 8212 33893 4075 28248 … |
| `Outstanding_Balance` | num | 149956 84159 342441 33925 85498 … |
| `Statement_Balance` | num | 178852 110032 424487 49983 153558 … |
| `Payment_Amount` | num | 82272 104530 148570 47484 50674 … |
| `Payment_Ratio` | num | 0.46 0.95 0.35 0.95 0.33 0.43 0.95 0.61 0.3 0.96 … |
| `Credit_Utilization` | num | 0.7 0.76 0.38 0.16 0.15 0.52 0.65 0.5 0.54 0.11 … |
| `Cash_Advance_Amount` | num | 14840 0 73714 0 0 … |
| `EMI_Count` | int | 2 2 2 3 5 3 1 3 0 0 … |
| `International_Transactions` | int | 0 0 3 1 0 0 4 0 0 0 … |
| `Reward_Points_Earned` | int | 1081 606 6857 660 3673 3587 2114 492 549 624 … |
| `Reward_Points_Redeemed` | int | 210 163 0 369 1322 0 695 177 372 0 … |
| `Mobile_App_Login` | int | 23 22 48 13 37 54 19 10 28 29 … |
| `Credit_Score` | int | 492 607 549 740 570 544 648 556 504 765 … |

**Conteo por tipo de almacenamiento:** `Numericas_R = 26`, `Categoricas_R = 4`.

**Cardinalidad de las 30 variables (`sort(n_niveles)`, de menor a mayor):**

| Variable | Valores únicos | Variable | Valores únicos |
|---|---:|---|---:|
| `Gender` | 2 | `Reward_Points_Earned` | 11.681 |
| `Card_Type` | 5 | `Cash_Advance_Amount` | 14.826 |
| `Occupation` | 6 | `Avg_Transaction_Value` | 40.475 |
| `EMI_Count` | 7 | `Travel_Spending` | 48.587 |
| `International_Transactions` | 15 | `Entertainment_Spending` | 48.937 |
| `Age` | 53 | `Dining_Spending` | 49.133 |
| `Mobile_App_Login` | 70 | `Fuel_Spending` | 49.264 |
| `Credit_Utilization` | 86 | `Online_Shopping_Spending` | 49.287 |
| `Payment_Ratio` | 91 | `Utility_Bill_Spending` | 49.359 |
| `Monthly_Transactions` | 165 | `Annual_Income` | 49.485 |
| `Card_Age_Months` | 227 | `Grocery_Spending` | 49.588 |
| `Credit_Score` | 402 | `Monthly_Spending` | 49.900 |
| `Credit_Limit` | 4.318 | `Outstanding_Balance` | 49.970 |
| `Reward_Points_Redeemed` | 5.517 | `Payment_Amount` | 49.971 |
| | | `Statement_Balance` | 49.980 |
| | | `Customer_ID` | 50.000 |

`Cash_Advance_Amount` tiene solo 14.826 valores únicos, muchos menos que las demás variables monetarias, porque el 70,3 % de sus valores son exactamente cero (Módulo 3). `Credit_Limit` tiene 4.318 porque solo toma valores redondeados a miles. Las dos cifras anticipan las formas "anómalas" que se analizan después.

**Tabla `table(credit$Card_Type)`:**

| Basic | Gold | Platinum | Signature | Silver |
|---:|---:|---:|---:|---:|
| 10.261 | 16.895 | 8.284 | 2.504 | 12.056 |

R ordena la tabla alfabéticamente, no según la jerarquía real.

#### Clasificación resultante (taxonomía estadística)

R reporta **4 columnas de texto** (`character`) y **26 numéricas** (`int`/`num`). Esa proporción **no cambia** tras la revisión. Lo que cambia es cómo se clasifica cada grupo dentro de la taxonomía:

1. **Cualitativas nominales (sin orden entre sus niveles):**
   - `Customer_ID`: 50.000 valores únicos, uno por fila. Es un identificador puro, sin distancia ni orden, y **se excluye de cualquier cálculo numérico** (medias, correlaciones, distancias).
   - `Gender`: solo 2 niveles (M/F), sin jerarquía.
   - `Occupation`: 6 niveles (Retired, Student, Business Owner, Government Employee, Private Employee, Self-Employed). Son categorías laborales sin orden natural.
2. **Cualitativa ordinal (con orden, pero sin distancia constante entre niveles).** El informe la marca como **corrección respecto a una clasificación anterior**:
   - `Card_Type` tiene 5 niveles que forman una jerarquía real de categoría de tarjeta: **Basic < Silver < Gold < Platinum < Signature**. Va de **10.261 clientes en Basic** a apenas **2.504 en Signature (5,0 % de la cartera)**. Hay orden, pero no una distancia numérica garantizada entre un nivel y el siguiente: el salto de Basic a Silver no es necesariamente igual al de Gold a Platinum. Por eso la clasificación correcta es **ordinal**, y no nominal como figuraba antes.
3. **Cuantitativas (26).** Todas pasan la prueba de **magnitud constante y aritmética interpretable**, incluidas las de rango corto que a primera vista podrían parecer categóricas:
   - **Continuas de escala monetaria y gastos (15):** `Annual_Income`, `Monthly_Spending`, `Avg_Transaction_Value`, `Online_Shopping_Spending`, `Grocery_Spending`, `Fuel_Spending`, `Dining_Spending`, `Travel_Spending`, `Entertainment_Spending`, `Utility_Bill_Spending`, `Cash_Advance_Amount`, `Outstanding_Balance`, `Statement_Balance`, `Payment_Amount` y `Credit_Limit`.
     - El informe dice que cada una tiene "entre **40.475 y 50.000** valores únicos". El mínimo se calcula en el código solo sobre `Avg_Transaction_Value`, `Annual_Income` y `Monthly_Spending`, y en realidad `Cash_Advance_Amount` (14.826) y `Credit_Limit` (4.318) tienen menos. Además, ninguna monetaria llega a 50.000: el máximo del grupo es `Statement_Balance` con 49.980, y 50.000 es la cardinalidad de `Customer_ID`.
     - Son montos en los que duplicar la cifra duplica el gasto real, así que **la media y la desviación estándar son directamente interpretables**.
   - **Continuas: ratios e índices (2):** `Payment_Ratio` y `Credit_Utilization`. Están acotadas en $[0,1]$ por construcción, pero con distancia constante: pagar 0,90 del saldo es exactamente el doble de pagar 0,45.
   - **Discretas: conteos y puntuaciones (9):**
     - `Age`: 53 valores únicos. El texto dice "de 18 a 69 años", pero `summary()` y `range()` del Módulo 2 dan un **máximo real de 70**.
     - `Card_Age_Months`: 227 valores únicos.
     - `Monthly_Transactions`: 165 valores únicos.
     - `EMI_Count`: 7 valores, de 0 a 6 cuotas.
     - `International_Transactions`: 15 valores únicos.
     - `Reward_Points_Earned`: 11.681 valores únicos.
     - `Reward_Points_Redeemed`: 5.517 valores únicos.
     - `Mobile_App_Login`: 70 valores únicos.
     - `Credit_Score`: 402 valores únicos.

     Todas son conteos o puntajes de **escala de razón**: la edad tiene cero absoluto, y la diferencia entre 20 y 30 años es la misma magnitud que entre 50 y 60.

     La relación de la edad con el riesgo crediticio puede ser **no lineal**: los perfiles jóvenes y los de edad avanzada pueden ser más riesgosos que los de edad media. El informe aclara que eso es un argumento para **transformarla al modelar** (con *bins* o *splines*), **no para reclasificarla como categórica**.

     El mismo razonamiento vale para `EMI_Count`, `International_Transactions` y `Mobile_App_Login`. Tienen rango corto porque cuentan lo que ocurre en un mes o en la vida de la tarjeta, pero su media (por ejemplo, cuotas vigentes promedio por cliente) sigue siendo una cifra con sentido real. Es lo mismo que pasa con "número de hijos", una variable cuantitativa clásica pese a su rango corto.

**Decisión y por qué.** No se convierte ninguna variable numérica en factor. El único ajuste conceptual es tratar `Card_Type` como **ordinal**. Esto define qué técnicas son válidas en el resto del informe:

- Las medias, correlaciones y distancias se calculan solo sobre las 26 cuantitativas.
- `Customer_ID` nunca entra a un cálculo.
- `Card_Type` se grafica en su orden natural y, en el Módulo 15, se codifica con *one-hot*.

**Significado para el negocio.** Para la Gerencia de Riesgo, `Card_Type` no es una "etiqueta de marketing" sino un **escalón de producto con jerarquía**. Esa jerarquía se refleja después en el número de transacciones (Módulo 4) y en los cupos. Tratar `EMI_Count` o `Age` como cuantitativas permite hablar de "cuotas vigentes promedio" o de "edad media del segmento" en los reportes de cartera.

### 1.5 Diccionario de variables

**Qué es y por qué se construye aquí.** Antes de auditar la matriz (Módulo 2) o de graficar una sola variable (Módulo 3) hay que saber **qué mide cada variable en el lenguaje del negocio**. Sin eso, no se puede juzgar si un valor "atípico" o una cola larga son razonables o un error de captura. El diccionario se construye una sola vez y se usa en todo el informe.

**Cómo se implementó.** Es un chunk con `echo = FALSE`, de modo que el código no se muestra en el HTML, y define dos vectores con nombre:

- `que_es`: qué mide cada una de las 26 variables numéricas.
- `por_que`: por qué su distribución tiene la forma que tiene. Este vector alimenta conceptualmente los Módulos 3, 4 y 5.

Después se imprime `diccionario <- data.frame(Variable = names(que_es), Descripcion = unname(que_es))`. Es una tabla paginada (`df_print: paged`) y su contenido en el HTML coincide con el vector `que_es`. Solo esa columna se imprime; la columna `por_que` se toma del código fuente, porque el vector se define pero no se imprime:

| Variable | Qué mide (`que_es`) | Por qué su distribución tiene esa forma (`por_que`) |
|---|---|---|
| `Age` | La edad del titular en años | Forma casi simétrica con una leve inclinación hacia la derecha: la cartera se concentra entre los 27 y los 44 años y se adelgaza hacia los 70, porque hay pocos titulares mayores y ninguno menor de 18. |
| `Annual_Income` | El ingreso anual declarado por el cliente | La cola larga a la derecha es lo esperable en cualquier variable de ingreso: la mayoría gana alrededor de la mediana y unos pocos ganan varias veces más, lo que empuja la media muy por encima de la mediana. |
| `Credit_Limit` | El cupo total aprobado en la tarjeta | El cupo se asigna en función del ingreso, así que hereda la misma cola derecha. Además solo toma valores redondeados (múltiplos de mil), por eso el histograma se ve escalonado y no continuo. |
| `Card_Age_Months` | La antigüedad de la tarjeta en meses | Hay más tarjetas nuevas que antiguas: la masa se acumula en los primeros años y decae hacia los 240 meses. Es el perfil de una cartera que sigue creciendo y captando clientes. |
| `Monthly_Spending` | El gasto mensual total, que es la suma de las siete categorías de consumo | Al sumar siete categorías que ya vienen sesgadas a la derecha, acumula todas esas colas: la mayoría gasta cerca de la mediana y un grupo pequeño gasta un orden de magnitud más. |
| `Monthly_Transactions` | El número de compras realizadas en el mes | Conteo acotado por lo que una persona alcanza a hacer en un mes (entre 15 y 179 compras), por eso la forma es prácticamente simétrica y sin colas largas. |
| `Avg_Transaction_Value` | El ticket promedio: gasto mensual dividido entre el número de transacciones | Es un cociente cuyo numerador tiene cola derecha y cuyo denominador está acotado, así que el resultado queda fuertemente sesgado: dominan los tickets pequeños del día a día y unos pocos compradores de tickets altos estiran la cola. |
| `Online_Shopping_Spending` | El gasto mensual en compras por internet | Como todo gasto por categoría, la mayoría gasta poco y unos pocos gastan mucho: pico pegado al origen y cola larga a la derecha. |
| `Grocery_Spending` | El gasto mensual en supermercado | Tiene la mediana más alta de todas las categorías: el mercado es un gasto recurrente que casi todos hacen, por eso el pico está más desplazado del origen que en las demás, aunque conserva la cola derecha. |
| `Fuel_Spending` | El gasto mensual en combustible | Depende de si el cliente tiene vehículo y de cuánto se desplaza: conviven un grupo grande de gasto bajo y una minoría de gasto alto que alarga la cola. |
| `Dining_Spending` | El gasto mensual en restaurantes | Comer fuera es discrecional: la mayoría lo hace con moderación y una minoría concentra montos muy altos, de ahí el sesgo pronunciado a la derecha. |
| `Travel_Spending` | El gasto mensual en viajes | Es el gasto más esporádico (la mediana más baja de las categorías): la mayoría viaja poco o nada en el mes, y los pocos que viajan gastan montos grandes. Produce la cola más larga del grupo. |
| `Entertainment_Spending` | El gasto mensual en entretenimiento | Gasto discrecional y ocasional: se concentra en montos bajos, con una cola derecha marcada que corresponde a quienes consumen ocio de forma intensiva. |
| `Utility_Bill_Spending` | El gasto mensual en servicios públicos pagados con la tarjeta | Domiciliar los servicios públicos en la tarjeta es frecuente pero de monto acotado: la masa está en valores bajos y la cola derecha viene de hogares con facturas altas. |
| `Outstanding_Balance` | El saldo que el cliente aún debe | La deuda pendiente sigue la lógica del gasto y del cupo: casi todos deben montos moderados y unos pocos arrastran saldos muy grandes, lo que estira la cola derecha. |
| `Statement_Balance` | El saldo facturado en el último corte del extracto | Es prácticamente la misma magnitud que el saldo pendiente, medida en el corte de facturación, por eso su forma es casi idéntica. |
| `Payment_Amount` | El monto que el cliente pagó en el mes | El pago es proporcional a lo facturado y reproduce la forma sesgada del saldo: pagos moderados en la mayoría y pagos muy grandes en la minoría con saldos altos. |
| `Payment_Ratio` | La proporción del saldo facturado que el cliente efectivamente pagó | Es la única variable con cola a la izquierda: está acotada en 1 (nadie paga más del 100 %) y la mayoría paga casi todo su saldo, así que la masa se apila contra el techo y los pagadores parciales forman la cola inferior. |
| `Credit_Utilization` | La proporción del cupo que el cliente tiene usada | Proporción acotada entre 0 y 1 por construcción, y las políticas de cupo evitan que los clientes lleguen al tope: forma compacta, sin colas y sin ningún dato fuera de los bigotes. |
| `Cash_Advance_Amount` | El monto retirado como avance en efectivo | Más de la mitad de los clientes nunca hace avances: hay un bloque enorme en cero y una cola larga formada por la minoría que sí los usa. Es una variable **inflada en cero**, no una distribución continua clásica. |
| `EMI_Count` | El número de compras diferidas a cuotas vigentes | Solo toma siete valores enteros (0 a 6 cuotas vigentes), por eso el histograma son barras separadas y no una curva: conteo discreto de rango muy corto. |
| `International_Transactions` | El número de compras hechas en el exterior | La mayoría no compra en el exterior: el valor típico es cero, y las pocas decenas de compras internacionales aparecen como cola derecha discreta. |
| `Reward_Points_Earned` | Los puntos de recompensa acumulados, que el banco calcula a partir del gasto | Los puntos son función del gasto, así que la gráfica es esencialmente la del gasto mensual reescalada: mismo pico bajo y misma cola derecha. |
| `Reward_Points_Redeemed` | Los puntos que el cliente ya redimió | Muchos acumulan puntos pero no los redimen: hay una acumulación en cero y una cola derecha de quienes sí los usan, normalmente en redenciones grandes y puntuales. |
| `Mobile_App_Login` | El número de ingresos a la aplicación móvil en el mes | Conteo acotado de sesiones al mes (entre 2 y 71) que refleja un hábito de consulta bastante uniforme: forma casi simétrica y sin atípicos. |
| `Credit_Score` | El puntaje crediticio asignado al cliente | Puntaje acotado por diseño en un rango estrecho, con la mayoría en la zona media-alta. La cola corta a la izquierda corresponde a la minoría de perfiles de alto riesgo. |

**Cómo se usa.** La columna `Descripcion` responde "¿qué es esta variable?" cada vez que aparezca una cola larga, un grupo de atípicos o una correlación alta. Antes de calificar algo de "raro" hay que poder decir qué mide. Los Módulos 3, 4 y 5 remiten a este diccionario en la primera línea de cada variable. Aun así, **cada histograma, boxplot y curva de densidad tiene su propio código y su propia interpretación**, escrita para esa variable y **no generada automáticamente**.

**Significado para el negocio.** El diccionario traduce cada columna a una pregunta de gestión:

- **Capacidad:** ingreso y cupo.
- **Hábito de consumo:** las siete categorías de gasto.
- **Endeudamiento:** saldo pendiente, saldo facturado y utilización.
- **Disciplina de pago:** monto y razón de pago.
- **Señales de estrés:** avances en efectivo y cuotas EMI.
- **Riesgo resumido:** puntaje crediticio.

Esa agrupación es la que la Gerencia necesita para interpretar cualquier hallazgo posterior.

### 1.6 Conclusión del Módulo 1

1. La matriz importada tiene $n = 50000$ filas y $p = 30$ columnas, verificadas con el protocolo de las cuatro funciones (`dim`, `str`, `summary`, `head`) antes de continuar.
2. Solo 4 de las $p$ variables son cualitativas por naturaleza: `Customer_ID`, `Gender` y `Occupation` son nominales, y `Card_Type` es ordinal. Las 26 restantes pasan la prueba de magnitud constante y quedan cuantitativas, incluidas las de rango corto como `Age` o `EMI_Count`.
3. El diccionario de variables es la base textual de todo el informe. Sin él, ningún módulo posterior podría explicar *por qué* una distribución tiene la forma que tiene; solo podría describirla.

---

## Módulo 2: Auditoría y diagnóstico de calidad de la matriz (S02)

**Objetivo.** Con la matriz importada y clasificada, el siguiente paso de S02 no es analizar todavía sino **auditar**. Una tabla puede cargar sin ningún error y aun así estar rota: columnas mal tipadas, códigos de faltante disfrazados de número o filas repetidas. Esos defectos **contaminan en silencio** cualquier estadístico posterior. Este módulo responde, en orden, las cuatro preguntas pendientes de la lista de chequeo de importación:

1. ¿Cuántos datos faltan y dónde?
2. ¿Hay duplicados?
3. ¿Son creíbles los rangos de cada variable?
4. ¿Las categorías declaradas son las que de verdad aparecen en los datos?

### 2.1 Diagnóstico multivariante de datos faltantes

**Qué es.** Un dato faltante (`NA` en R) es una celda sin valor. En análisis multivariante su costo es mayor que en el univariado: al descartar una fila incompleta en un análisis conjunto **se pierde el vector completo** $\mathbf{x}_i \in \mathbb{R}^p$, no solo el valor de una variable. Por eso se cuenta dos veces:

- **Celdas vacías**, con `is.na()`.
- **Filas que sobreviven completas**, con `complete.cases()`, que devuelve `TRUE` para las filas sin ningún `NA`.

La sesión S02, con el dataset `airquality`, mostró que los dos porcentajes pueden ser muy distintos: un **4,8 %** de celdas vacías se traducía en un **27,5 %** de filas perdidas, porque los `NA` estaban repartidos en filas diferentes.

**Cómo lo aplicamos.**

```r
total_celdas <- prod(dim(credit))
celdas_na <- sum(is.na(credit))
pct_celdas_na <- (celdas_na / total_celdas) * 100
filas_completas <- sum(complete.cases(credit))
pct_filas_completas <- (filas_completas / nrow(credit)) * 100
faltantes_por_col <- colSums(is.na(credit))
faltantes_por_col[faltantes_por_col > 0]
```

**Resultados.**

| Métrica | Valor |
|---|---|
| Celdas totales ($n \times p$) | 1.500.000 |
| Celdas vacías | 0 (0,00 %) |
| Filas completas | 50.000 de 50.000 (100,00 %) |
| Columnas con algún `NA` | Ninguna. La salida es `named numeric(0)`, un vector vacío |

**Decisión.** A diferencia de `airquality`, aquí **ambos porcentajes son cero**. No hace falta elegir entre las tres estrategias de S02 frente a faltantes:

- **Casos completos:** eliminar filas incompletas.
- **Análisis por pares:** usar, en cada cálculo, las observaciones disponibles para ese par.
- **Imputación:** rellenar los faltantes con valores estimados.

La matriz $\mathbf{X}$ está **100 % completa** y la decisión queda cerrada antes de empezar a analizar.

**Negocio.** Todo indicador de cartera que se calcule usa a los 50.000 clientes. No hay sesgo de selección por registros incompletos.

### 2.2 Verificación de duplicados e identificadores

**Qué es.** Un archivo puede estar completo y seguir corrupto si trae la misma observación repetida, o si el identificador que debería ser único no lo es. Se verifican dos cosas por separado:

- `duplicated(credit)` marca las filas **exactamente iguales** en todas sus columnas a una fila anterior.
- `duplicated(credit$Customer_ID)` marca los **identificadores repetidos**.

```r
n_duplicados_filas <- sum(duplicated(credit))
n_duplicados_id    <- sum(duplicated(credit$Customer_ID))
```

**Resultado.** **0 filas exactamente duplicadas** y **0 identificadores repetidos** sobre 50.000 registros.

**Decisión.** No hay que eliminar filas ni corregir ningún `Customer_ID`: cada cliente es único y aparece una sola vez. Esto coincide con la cardinalidad de `Customer_ID` (50.000) del Módulo 1.

**Negocio.** No hay clientes contados dos veces, ni en los conteos de la cartera ni en la exposición total.

### 2.3 Resumen univariado global y revisión de rangos (`summary`)

**Qué es.** `summary()` es el tercer punto de la lista de chequeo de importación, y el más fácil de pasar por alto. Aquí **no busca formas ni distribuciones** (eso es el Módulo 3). Busca **valores imposibles**:

- un mínimo negativo en una variable de gasto;
- una edad de $-99$ usada como código de faltante (un **valor centinela**, es decir, un número arbitrario que el sistema de origen usa para decir "sin dato");
- una utilización de crédito mayor que 1.

Para cada variable numérica `summary()` da el mínimo, el primer cuartil, la mediana, la media, el tercer cuartil y el máximo. Para las columnas de texto, la versión de R usada reporta `Length`, `N.unique`, `N.blank`, `Min.nchar` y `Max.nchar`.

**Cómo lo aplicamos:** `summary(credit)` sobre las 30 columnas, seguido de una verificación manual de los rangos que definen reglas de negocio.

**Resultado de `summary()`, columnas de texto:**

| Variable | Length | N.unique | N.blank | Min.nchar | Max.nchar |
|---|---:|---:|---:|---:|---:|
| `Customer_ID` | 50000 | 50000 | 0 | 8 | 8 |
| `Gender` | 50000 | 2 | 0 | 1 | 1 |
| `Occupation` | 50000 | 6 | 0 | 7 | 19 |
| `Card_Type` | 50000 | 5 | 0 | 4 | 9 |

**Resultado de `summary()`, 26 columnas numéricas** (montos en ₹, tal como los imprime R):

| Variable | Mín. | 1.er cuartil | Mediana | Media | 3.er cuartil | Máx. |
|---|---:|---:|---:|---:|---:|---:|
| `Age` | 18,00 | 27,00 | 34,00 | 36,08 | 44,00 | 70,00 |
| `Annual_Income` | 100.050 | 657.774 | 1.127.630 | 1.479.318 | 1.663.624 | 7.995.831 |
| `Credit_Limit` | 16.000 | 157.000 | 396.000 | 709.677 | 779.000 | 6.591.000 |
| `Card_Age_Months` | 1,00 | 31,00 | 48,00 | 53,63 | 70,00 | 240,00 |
| `Monthly_Spending` | 2.236 | 26.646 | 50.022 | 73.872 | 83.030 | 691.688 |
| `Monthly_Transactions` | 15,00 | 49,00 | 76,00 | 83,04 | 108,00 | 179,00 |
| `Avg_Transaction_Value` | 57,76 | 448,38 | 617,16 | 835,99 | 901,25 | 10.463,06 |
| `Online_Shopping_Spending` | 13,85 | 2.800,70 | 6.163,21 | 11.238,28 | 12.820,20 | 258.176,00 |
| `Grocery_Spending` | 83,81 | 5.176,97 | 10.651,41 | 17.794,28 | 20.419,57 | 352.971,49 |
| `Fuel_Spending` | 10,95 | 2.432,16 | 5.466,36 | 10.212,73 | 11.560,76 | 235.635,14 |
| `Dining_Spending` | 5,77 | 2.089,51 | 4.847,46 | 9.090,10 | 10.381,72 | 227.439,65 |
| `Travel_Spending` | 0,26 | 1.077,05 | 2.883,43 | 6.141,73 | 6.862,71 | 213.127,41 |
| `Entertainment_Spending` | 1,37 | 1.570,09 | 3.829,70 | 7.648,22 | 8.612,79 | 216.730,17 |
| `Utility_Bill_Spending` | 19,75 | 2.978,53 | 6.574,18 | 11.746,45 | 13.509,58 | 300.191,63 |
| `Outstanding_Balance` | 1.600 | 55.641 | 145.306 | 303.420 | 319.978 | 5.789.683 |
| `Statement_Balance` | 4.161 | 82.472 | 192.358 | 366.172 | 387.432 | 6.102.803 |
| `Payment_Amount` | 887,6 | 55.193,2 | 136.639,8 | 279.373,9 | 299.100,5 | 5.980.747,0 |
| `Payment_Ratio` | 0,1000 | 0,6200 | 0,8400 | 0,7634 | 0,9600 | 1,0000 |
| `Credit_Utilization` | 0,1000 | 0,2700 | 0,4000 | 0,4262 | 0,5600 | 0,9500 |
| `Cash_Advance_Amount` | 0 | 0 | 0 | 23.057 | 8.692 | 1.212.849 |
| `EMI_Count` | 0,000 | 1,000 | 2,000 | 2,447 | 4,000 | 6,000 |
| `International_Transactions` | 0,00 | 0,00 | 0,00 | 1,53 | 2,00 | 14,00 |
| `Reward_Points_Earned` | 44 | 720 | 1.833 | 3.891 | 3.767 | 56.341 |
| `Reward_Points_Redeemed` | 0 | 0 | 135 | 872 | 731 | 44.818 |
| `Mobile_App_Login` | 2,00 | 20,00 | 31,00 | 33,16 | 44,00 | 71,00 |
| `Credit_Score` | 367 | 585 | 638 | 629 | 681 | 792 |

**Rangos de reglas de negocio**, verificados a mano con `range()` y `rbind()`:

| Variable | Mínimo | Máximo |
|---|---:|---:|
| `Age` | 18,0 | 70,00 |
| `Payment_Ratio` | 0,1 | 1,00 |
| `Credit_Utilization` | 0,1 | 0,95 |

**Lectura del informe.**

- Ninguna de las 26 columnas numéricas tiene un mínimo negativo ni un valor centinela típico (`-99`, `999`).
- Los mínimos de las variables de gasto y saldo son 0 o valores positivos razonables.
- Los tres rangos de negocio se verifican explícitamente porque no basta con "no tener error": tienen que tener sentido en el dominio.
  - **Edad de 18 a 70 años:** cartera de adultos, sin menores de edad ni casos por encima de una expectativa de vida razonable para el producto.
  - **`Payment_Ratio` de 0,1 a 1:** nadie paga menos del 10 % ni más del 100 % de su saldo, coherente con que es una proporción.
  - **`Credit_Utilization` de 0,1 a 0,95:** nadie usa menos del 10 % ni supera el 95 % de su cupo, señal de que el banco no deja llegar a los clientes al límite exacto.
- Los tres rangos son plausibles: **la auditoría no encuentra evidencia de errores de captura**.

**Observaciones que ya se leen en la tabla y que retoman los módulos siguientes:**

- En casi todas las variables monetarias la media supera con holgura a la mediana. Es la primera evidencia numérica de asimetría positiva.
  - `Annual_Income`: 1.479.318 frente a 1.127.630.
  - `Outstanding_Balance`: 303.420 frente a 145.306.
- `Cash_Advance_Amount` tiene en 0 el mínimo, el primer cuartil y la mediana, y aun así una media de 23.057 ₹. Es la marca de la inflación en cero.
- `International_Transactions` tiene mediana 0 y `Reward_Points_Redeemed` tiene primer cuartil 0.
- `Payment_Ratio` es la única variable numérica con la media (0,7634) por debajo de la mediana (0,84) por un margen amplio.
- `Credit_Score` también tiene la media (629) por debajo de la mediana (638).

**Negocio.** No hay datos "basura" que distorsionen indicadores como el saldo promedio o la utilización promedio. Que `Credit_Utilization` nunca pase de 0,95 es en sí mismo un dato de política: el banco limita la utilización máxima.

### 2.4 Tablas de frecuencia para variables categóricas

**Qué es.** `summary()` no detecta niveles repetidos por diferencias de mayúsculas, espacios o tildes dentro de una misma categoría. Es el caso del cereal "s P" visto en S02: el mismo nivel escrito de dos formas aparece como dos categorías. Solo lo detecta una tabla de frecuencias, variable por variable. Con `useNA = "always"`, `table()` añade siempre una columna `<NA>`, aunque esté en cero, lo que hace explícita la ausencia de faltantes.

```r
table(credit$Gender, useNA = "always")
table(credit$Card_Type, useNA = "always")
table(credit$Occupation, useNA = "always")
```

**Resultados.**

`Gender`:

| F | M | `<NA>` |
|---:|---:|---:|
| 22.392 | 27.608 | 0 |

`Card_Type` (orden alfabético de `table()`):

| Basic | Gold | Platinum | Signature | Silver | `<NA>` |
|---:|---:|---:|---:|---:|---:|
| 10.261 | 16.895 | 8.284 | 2.504 | 12.056 | 0 |

`Occupation`:

| Business Owner | Government Employee | Private Employee | Retired | Self-Employed | Student | `<NA>` |
|---:|---:|---:|---:|---:|---:|---:|
| 6.038 | 7.595 | 20.960 | 4.047 | 7.440 | 3.920 | 0 |

**Lectura.** `Gender` tiene exactamente 2 niveles (`F`/`M`), `Card_Type` exactamente 5 (`Basic`, `Silver`, `Gold`, `Platinum`, `Signature`) y `Occupation` exactamente 6. En los tres casos no hay ningún nivel "fantasma" por error tipográfico o espacio en blanco, y la columna `<NA>` está en cero.

**Decisión.** Las tres categóricas llegan limpias a los módulos siguientes **sin necesidad de `trimws()`** (que quita espacios al inicio y al final) **ni de `tolower()`** (que pasa el texto a minúsculas).

### 2.5 Distribución gráfica de las variables categóricas

**Qué es y por qué.** Una tabla de conteos dice si los niveles están limpios, pero no deja ver de un vistazo qué tan repartida está la cartera. Por eso se grafican las tres variables como **frecuencia relativa**: el porcentaje, calculado con `prop.table()`, en vez del conteo bruto. Así son comparables entre sí aunque tengan distinto número de niveles.

Decisiones gráficas:

- `Card_Type` se dibuja en su **orden natural de jerarquía** (Basic → Signature), ya establecido como ordinal en el Módulo 1, y no en el orden alfabético que da `table()`. El orden se impone con el vector `orden_tipo <- c("Basic","Silver","Gold","Platinum","Signature")`. El color es un degradado `colorRampPalette(c("grey80", "#1E7F63"))(5)` que también comunica el orden.
- `Occupation` se ordena de mayor a menor con `sort(..., decreasing = TRUE)`, con etiquetas verticales (`las = 2`).
- En los tres gráficos, `text(bp, pct, labels = paste0(pct, "%"), pos = 3)` escribe el porcentaje encima de cada barra, y `ylim = c(0, max(pct) * 1.2)` deja espacio para esas etiquetas.

#### `Gender`

`barplot` en color `steelblue`, titulado *Distribución de Gender*.

**Resultado:** **55,2 % M** frente a **44,8 % F**, una diferencia de solo **10,4 puntos porcentuales**. El informe lo relaciona con el Módulo 7: `Gender` explica menos del 0,01 % de la varianza de cualquier variable de negocio, y esta distribución casi pareja es parte de la razón.

#### `Card_Type`

*Distribución de Card_Type (orden ordinal)*.

| Basic | Silver | Gold | Platinum | Signature |
|---:|---:|---:|---:|---:|
| 20,5 % | 24,1 % | **33,8 %** | 16,6 % | **5 %** |

Gold (33,8 %) y Signature (5 %) se citan en el texto del informe. Los porcentajes de Basic, Silver y Platinum se obtienen de los conteos de la tabla (10.261, 12.056 y 8.284 sobre 50.000) con el mismo redondeo a un decimal que usa el código.

**Lectura.** La cartera se concentra en los niveles intermedios. `Gold` es el más frecuente y la frecuencia decae hacia los extremos. `Signature`, el nivel más alto, es el más raro: apenas 1 de cada 20 clientes. El informe señala que esa escasez es, en parte, la razón de que los grupos de `Card_Type` en el Módulo 9 muestren medias tan dispares en `Credit_Limit`: el nivel más alto se sostiene en pocas observaciones.

#### `Occupation`

*Distribución de Occupation*, barras naranja (`darkorange`) ordenadas de mayor a menor.

| Private Employee | Government Employee | Self-Employed | Business Owner | Retired | Student |
|---:|---:|---:|---:|---:|---:|
| **41,9 %** | **15,2 %** | 14,9 % | **12,1 %** | **8,1 %** | **7,8 %** |

Los valores en negrita están citados en el texto del informe. El de Self-Employed se obtiene de su conteo (7.440 / 50.000).

**Lectura.** `Private Employee` domina la cartera, con casi tres veces el peso del siguiente nivel (`Government Employee`). `Student` y `Retired` son las categorías más pequeñas. Según el informe, son justamente los extremos de ingreso que el Módulo 7 identifica en el boxplot por ocupación: `Student` tiene la media más baja y `Business Owner` la más alta, y este último tampoco es mayoritario (12,1 %).

**Negocio.**

- Las conclusiones sobre Signature y sobre Students o Retirees se apoyan en grupos pequeños (entre 2.504 y 4.047 clientes). Cualquier política dirigida a esos segmentos debe considerar que sus estimaciones son menos estables.
- El grueso de la exposición está en empleados privados y en tarjetas Gold y Silver.

### 2.6 Conclusión del Módulo 2

1. La matriz está **100 % completa**: 0 celdas vacías de 1.500.000. Ninguna de las tres estrategias frente a faltantes (casos completos, por pares, imputación) es necesaria.
2. No hay filas ni identificadores duplicados: cada una de las 50.000 observaciones es un cliente distinto.
3. `summary()` y las tablas de frecuencia no encuentran valores centinela, rangos imposibles ni niveles categóricos mal escritos. La matriz $\mathbf{X}$ queda **auditada y lista** para el análisis univariado del Módulo 3.

---

## Módulo 3: Análisis univariado y la decisión gráfica del histograma (S01 & S03)

**Objetivo.** Con la matriz auditada empieza el análisis propiamente dicho, una variable a la vez. Es el nivel más simple de la taxonomía de S01: univariado, antes de bivariado y multivariado.

Se elige `Credit_Score` como **variable de referencia** de todo el módulo porque es **la variable de riesgo**: el resto del informe (Módulos 7, 8 y 9) termina relacionándolo todo con ella, así que conviene entender primero su forma a solas.

### 3.1 Estadísticos descriptivos univariados

**Conceptos.**

- **Media** $\bar x = \frac{1}{n}\sum_{i=1}^n x_i$: centro de gravedad de los datos. Es sensible a valores extremos.
- **Desviación estándar** $s = \sqrt{\frac{1}{n-1}\sum_{i=1}^n (x_i-\bar x)^2}$: dispersión típica alrededor de la media, en las unidades de la variable.
- **Mediana:** valor que deja la mitad de los datos a cada lado. Es robusta frente a extremos.
- **Mínimo y máximo:** los extremos del rango observado.
- **Comparar media y mediana** es la primera prueba numérica de simetría:
  - si la media está por debajo de la mediana, la cola que "arrastra" está a la izquierda;
  - si está por encima, la cola está a la derecha.

**Cómo lo aplicamos.**

```r
score <- credit$Credit_Score
c(Media = mean(score), Desv_Std = sd(score), Mediana = median(score),
  Min = min(score), Max = max(score))
```

**Resultado.**

| Media | Desv. estándar | Mediana | Mín. | Máx. |
|---:|---:|---:|---:|---:|
| 628,98458 | 68,44425 | 638 | 367 | 792 |

**Lectura.**

- La media (**629**) queda **por debajo** de la mediana (**638**), una diferencia de **9 puntos**. Antes de graficar nada, es la primera señal numérica de que la distribución no es perfectamente simétrica y tiene una **cola a la izquierda**: los perfiles de alto riesgo arrastran la media hacia abajo.
- La desviación estándar de **68,4 puntos**, sobre un rango de **367 a 792**, indica que la cartera está razonablemente concentrada: la mayoría de los puntajes cae dentro de una o dos desviaciones de la media y no se dispersa por todo el rango posible.

**Negocio.** El cliente "típico" tiene un puntaje alrededor de 630-640. El grupo de interés para el seguimiento preventivo es la **cola izquierda**: una minoría con puntajes bajos que tira de la media hacia abajo.

### 3.2 Regla de Sturges

**Qué es.** Un histograma necesita un número de intervalos o clases, $k$, y hace falta un criterio que no dependa de "probar hasta que se vea bien". La regla de Sturges propone $k$ como función **únicamente de $n$** (el tamaño de muestra), bajo el supuesto de datos aproximadamente normales:

$$k = 1 + \log_2(n) = 1 + 3.322 \cdot \log_{10}(n)$$

**Intuición.** $k$ crece con $n$, pero **logarítmicamente** y no en proporción: duplicar la muestra no debería duplicar el número de barras. Cada barra necesita suficientes observaciones para que su altura sea informativa y no solo ruido de muestreo. Duplicar $n$ añade apenas **una** barra, porque $\log_2(2n) = \log_2 n + 1$.

**Cómo lo aplicamos.**

```r
n_obs <- length(score)
k_sturges <- nclass.Sturges(score)   # implementación de R (redondea hacia arriba)
k_teorico <- 1 + log2(n_obs)
```

**Resultado:** `n = 50000`, `k_Sturges = 17`, `k_Formula = 16.61`.

**Evaluación y decisión.**

- Para $n = 50.000$ la fórmula da $k = 16{,}61$, y `nclass.Sturges()` lo lleva a **$k = 17$ intervalos**.
- Es el valor del panel "Balanceado" de la comparación de histogramas. No es una coincidencia: es la **justificación formal** de por qué se declara ese panel y no el de `breaks = 5` ni el de `breaks = 60`.
- **$k$ no depende de la variable.** Es la misma para las 26 variables numéricas porque solo usa $n$, que es común a todas. Lo que sí cambia de una variable a otra es el **ancho de cada barra**, $h = \text{rango}/k$, que se expresa en las unidades de cada variable.

> **Nota de orden en el documento:** el texto de esta sección dice "la comparación anterior" y "¿por qué 17 y no cualquier otro número entre 5 y 60?", y se refiere al ancho de barra "ya explícito en la sección anterior". En el Rmd final, sin embargo, la regla de Sturges (sección 4.2 del HTML) aparece **antes** que la comparación de histogramas (4.3) y que los histogramas por variable (4.4). Es un vestigio de una reordenación del texto. El contenido no cambia.

**Detalle técnico.** En `hist()`, el argumento `breaks = 17` es una **sugerencia**. R ajusta los cortes a números "bonitos" con `pretty()`, así que el número real de barras puede diferir un poco de 17. Esto se ve con claridad en `EMI_Count` (abajo).

### 3.3 El histograma y el efecto del número de cortes (`breaks`) (S03, Sesión 4)

**Qué es.** El histograma es una **estimación no paramétrica de la función de densidad** subyacente: no supone ninguna forma (normal u otra) para los datos. Cuenta cuántas observaciones caen en cada intervalo de ancho $h$ y dibuja esa cuenta como una barra. El número de intervalos (`breaks`) **no es un detalle estético**: es una decisión que cambia lo que el gráfico *dice* sobre los mismos datos.

- **Pocos cortes** producen **sobre-suavizado**, equivalente al *underfitting*: se esconde la estructura.
- **Demasiados cortes** producen un **histograma ruidoso**, equivalente al *overfitting*: se dibuja el ruido de muestreo como si fuera estructura.

**Cómo lo aplicamos.** Se grafica `Credit_Score` tres veces lado a lado (`par(mfrow = c(1, 3))`):

- `breaks = 5`, en `lightblue`, titulado "Sobre-suavizado";
- `breaks = 17`, en `lightgreen`, titulado "Balanceado, Sturges";
- `breaks = 60`, en `salmon`, titulado "Ruidoso".

Al final se restaura el panel con `par(mfrow = c(1, 1))`.

**Lectura del gráfico.**

- **`breaks = 5`:** las barras son tan anchas (cerca de **85 puntos** cada una) que la distribución parece casi uniforme, y se pierde por completo la asimetría a la izquierda que ya anunciaban la media y la mediana.
- **`breaks = 60`:** cada barra cubre apenas **7 puntos**, y 50.000 clientes ya no alcanzan para llenarlas de forma pareja. Aparecen **dientes y huecos** que son ruido de muestreo, no estructura real.
- **`breaks = 17` (Sturges):** se ve la forma real sin aplanarla ni fragmentarla. Es **unimodal**, está **centrada cerca de 640** y tiene la **cola izquierda** que la relación media-mediana ya había anticipado.
- La mayor parte de los clientes tiene un **puntaje crediticio entre 500 y 700 puntos**.

**Negocio.** Si un analista mostrara a la Gerencia el panel de `breaks = 5`, concluiría que los puntajes se reparten de forma uniforme y no vería a la minoría de alto riesgo. El panel de `breaks = 60` invitaría a "ver" segmentos que no existen. La regla de Sturges protege la decisión de ambos errores.

### 3.4 Histogramas de todas las variables numéricas

**Cómo lo aplicamos.** La comparación de tres anchos (`breaks = 5`, `17` y `60`) se repite sobre **cada una de las 26 variables numéricas**, con los mismos colores y la misma disposición 1×3. Cada variable tiene **su propio bloque de código, sin un `for` que las recorra en silencio**, y una interpretación específica de lo que esa variable muestra.

#### Tabla resumen

Asimetría según el texto del informe; centro y extremos según `summary()`.

| # | Variable | Mediana | Media | Máx. | Asimetría reportada | Forma clave (histograma con k = 17) |
|---|---|---:|---:|---:|---:|---|
| 1 | `Age` | 34 | 36,1 | 70 | 0,69 | Pico entre 27 y 44 años, leve cola derecha |
| 2 | `Annual_Income` | 1.127.630 | 1.479.318 | 7.995.831 | 2,55 | Cola derecha de altos ingresos |
| 3 | `Credit_Limit` | 396.000 | 709.677 | 6.591.000 | 3,01 | Escalonado (valores redondeados a miles) |
| 4 | `Card_Age_Months` | 48 | 53,63 | 240 | 1,14\* | Más tarjetas nuevas que antiguas |
| 5 | `Monthly_Spending` | 50.022 | 73.872 | 691.688 | 3,00 | Masa entre 26.646 y 83.032; cola larga |
| 6 | `Monthly_Transactions` | 76 | 83,0 | 179 | 0,54 | Casi simétrica y acotada |
| 7 | `Avg_Transaction_Value` | 617 | 836 | 10.463 | 3,90 | Máximo a más de 12 desviaciones estándar |
| 8 | `Online_Shopping_Spending` | 6.163 | 11.240 | 258.200 | 4,56\* | Mayor brecha relativa media/mediana |
| 9 | `Grocery_Spending` | 10.650 | 17.794 | 352.971 | 4,01 | Pico más alejado del origen |
| 10 | `Fuel_Spending` | 5.466 | 10.213 | 235.600 | 4,69 | Grupo bajo y minoría alta |
| 11 | `Dining_Spending` | 4.847 | 9.090 | 227.400 | 4,64\* | Calco de Online |
| 12 | `Travel_Spending` | 2.883 | 6.142 | 213.100 | 5,71 | Masa aplastada contra el origen |
| 13 | `Entertainment_Spending` | 3.830 | 7.648 | 216.730 | 5,01 | Pico pegado al origen |
| 14 | `Utility_Bill_Spending` | 6.574 | 11.746 | 300.192 | 4,35 | Cola más corta de las categorías |
| 15 | `Outstanding_Balance` | 145.300 | 303.400 | 5.790.000 | 4,02\* | Máximo ≈ 19 veces la media |
| 16 | `Statement_Balance` | 192.400 | 366.172 | 6.103.000 | 3,80\* | Idéntica a Outstanding |
| 17 | `Payment_Amount` | 136.600 | 279.400 | 5.980.747 | 4,20\* | Forma sesgada del saldo |
| 18 | `Payment_Ratio` | 0,84 | 0,7634 | 1,00 | −1,04 | Masa apilada contra el techo |
| 19 | `Credit_Utilization` | 0,40 | 0,4262 | 0,95 | 0,53 | Compacta, sin cola |
| 20 | `Cash_Advance_Amount` | 0 | 23.057 | 1.212.849 | 6,78 | 70,3 % en cero |
| 21 | `EMI_Count` | 2 | 2,447 | 6 | 0,17\* | 7 barras separadas |
| 22 | `International_Transactions` | 0 | 1,53 | 14 | 2,11 | 59,3 % en cero |
| 23 | `Reward_Points_Earned` | 1.833 | 3.891 | 56.341 | 3,50 | Igual a `Monthly_Spending` reescalada |
| 24 | `Reward_Points_Redeemed` | 135 | 872 | 44.818 | 6,55 | 39,9 % en cero |
| 25 | `Mobile_App_Login` | 31 | 33,16 | 71 | 0,33 | Casi simétrica, sin huecos |
| 26 | `Credit_Score` | 638 | 629 | 792 | −0,58 | Cola izquierda |

**Qué es la asimetría (*skewness*).** Es una medida de la falta de simetría, $g_1 = \frac{\frac1n\sum (x_i-\bar x)^3}{s^3}$.

- $g_1 > 0$: cola larga a la derecha.
- $g_1 < 0$: cola larga a la izquierda.
- $g_1 \approx 0$: forma simétrica.

En los Módulos 3 y 4 las asimetrías solo se citan en el texto: el chunk que las calcula no está en esos módulos. Los valores marcados con \* no aparecen en el texto de estos módulos. Se tomaron de la tabla paginada del Módulo 15 (columna `Skew`), que recoge la asimetría de las 26 variables y coincide con todas las demás cifras citadas aquí.

#### `Age`

**Qué mide:** la edad del titular en años.

**Lectura del gráfico.**

- **`breaks = 5`:** cada barra cubre **10,4 años** y la cartera parece casi uniforme entre 20 y 60.
- **`breaks = 17`:** aparece un **pico claro entre 27 y 44 años**, coherente con una **media de 36,1** y una **asimetría leve (0,69)** hacia los titulares mayores.
- **`breaks = 60`:** cada barra cubre poco más de **0,9 años** y empiezan a verse dientes aislados. Son ruido de muestreo, no estructura demográfica real.

**Negocio:** la cartera es de adultos jóvenes y de mediana edad. El segmento mayor de 60 años es pequeño.

#### `Annual_Income`

**Qué mide:** el ingreso anual declarado.

**Lectura del gráfico.** La asimetría de **2,55** es de las más altas del dataset, y se nota en los tres paneles.

- **`breaks = 5`:** casi toda la masa cae en la primera barra (de **100.050 ₹ a 1.679.166 ₹**) y el resto del eje queda vacío.
- **`breaks = 17`:** se distingue la **mediana (1.127.630 ₹)** muy por debajo de la **media (1.479.318 ₹)**, la firma clásica de una cola de altos ingresos.
- **`breaks = 60`:** la cola se disuelve en barras de una sola observación, imposibles de interpretar.

La gran mayoría tiene ingresos bajos a moderados, y una parte tiene ingresos bastante elevados respecto a la mediana.

**Negocio:** la media no representa al cliente típico. Para fijar políticas (por ejemplo, cupo por nivel de ingreso) conviene usar la mediana o percentiles.

#### `Credit_Limit`

**Qué mide:** el cupo aprobado.

**Lectura del gráfico.**

- Hereda la cola derecha de `Annual_Income`, de la que depende casi linealmente ($r = 0{,}974$, Módulo 7).
- El informe la describe como "la variable con **mayor asimetría de todo el dataset (3,01)**". Esa afirmación no es coherente con otras asimetrías reportadas más altas, como 6,78 en `Cash_Advance_Amount` o 5,71 en `Travel_Spending`.
- **`breaks = 17`:** el histograma ya se ve **escalonado** en vez de continuo, porque el cupo solo toma valores **redondeados a miles**. Ningún ajuste de `breaks` puede suavizar ese patrón, porque no es ruido de muestreo sino **la resolución real con la que el banco define los cupos**.

**Negocio:** los cupos son un instrumento de política discreto, en escalones de 1.000 ₹, ligado al ingreso.

#### `Card_Age_Months`

**Qué mide:** la antigüedad de la tarjeta en meses.

**Lectura del gráfico.**

- **`breaks = 17`:** se ve con claridad que la **mediana (48 meses)** está muy por debajo del **máximo (240 meses)**. Hay más tarjetas nuevas que antiguas, el perfil de una **cartera que sigue creciendo**.
- **`breaks = 60`:** cada barra cubre **4 meses**, un nivel de detalle que no aporta nada de negocio (nadie gestiona antigüedad de tarjeta con precisión mensual). Es solo ruido.

**Negocio:** una cartera joven tiene menos historia de pago observada por cliente, lo que es relevante para evaluar riesgo.

#### `Monthly_Spending`

**Qué mide:** el gasto mensual total, suma de las siete categorías de gasto.

**Lectura del gráfico.**

- Acumula la cola derecha de las siete categorías a la vez: **asimetría 3,00**, más alta que la de cualquier categoría individual según el texto. Las categorías individuales (de 4,01 a 5,71 según la tabla `Skew` del Módulo 15) son, sin embargo, mayores. El informe no resuelve esta tensión.
- **`breaks = 5`:** esa acumulación es invisible.
- **`breaks = 17`:** se ve una masa concentrada **entre 26.646 ₹ y 83.032 ₹** (el rango intercuartílico) y una **cola larga hasta 691.688 ₹**. `summary()` da 83.030 como tercer cuartil.
- Es la variable que el Módulo 5 usa como **caso de estudio de atípicos**, y este histograma es la contraparte visual de esos números.

La mayoría tiene un gasto mensual moderado a bajo, y una parte tiene gastos mensuales muy elevados.

#### `Monthly_Transactions`

**Qué mide:** el número de compras en el mes.

**Lectura del gráfico.**

- Es de las variables **más simétricas** del dataset: asimetría **0,54**, con media 83,0 y mediana 76 muy cercanas.
- A diferencia de las variables de dinero, **`breaks = 60` no fragmenta tanto la forma**, porque el rango (**15 a 179**) es angosto y la variable ya es acotada y regular: el número de compras que una persona alcanza a hacer en un mes tiene un techo práctico.

#### `Avg_Transaction_Value`

**Qué mide:** el gasto mensual dividido entre el número de transacciones, es decir, el ticket promedio.

**Lectura del gráfico.**

- Hereda la asimetría del numerador: **3,90**.
- **`breaks = 17`:** la mayoría de los tickets cae **entre 448 ₹ y 901 ₹** (el rango intercuartílico).
- El **máximo (10.460 ₹)** está a **más de 12 desviaciones estándar** de la media.
- Un cociente entre una variable sesgada y una acotada produce aquí **la cola más extrema de todas las variables de transacción individual**.

#### `Online_Shopping_Spending`

**Qué mide:** el gasto en compras por internet.

**Lectura del gráfico.**

- **Mediana de 6.163 ₹**, que el informe describe como "menos de un tercio de su media (11.240 ₹)". El cociente real es de alrededor de 0,55, así que "un tercio" no se ajusta a las cifras.
- Según el informe, es la **brecha media/mediana más amplia, en términos relativos, de las siete categorías de gasto**.
- **`breaks = 5`:** la brecha ni se nota.
- **`breaks = 17`:** el **pico pegado al origen** y la **cola larga hasta 258.200 ₹** quedan claramente separados.

#### `Grocery_Spending`

**Qué mide:** el gasto en supermercado.

**Lectura del gráfico.**

- Tiene la **mediana más alta de las siete categorías (10.650 ₹)**, porque el mercado es un gasto recurrente que casi todos hacen.
- **`breaks = 17`:** el pico queda visiblemente **más alejado del origen** que en `Travel_Spending` o `Entertainment_Spending`, aunque conserva la cola derecha (**asimetría 4,01**).

**Negocio:** es el gasto "de necesidad" más estable. Una caída brusca en esta categoría para un cliente podría ser una señal de estrés financiero (esto es una lectura interpretativa, no un análisis del informe).

#### `Fuel_Spending`

**Qué mide:** el gasto en combustible.

**Lectura del gráfico.**

- Depende de si el cliente tiene vehículo: conviven un grupo grande de gasto bajo y una minoría de gasto alto (**asimetría 4,69**; **mediana 5.466 ₹** frente a un **máximo de 235.600 ₹**).
- **`breaks = 60`:** esa minoría se dispersa en barras de 1 o 2 observaciones. Visualmente parece "más información", pero es exactamente **el ruido de muestreo que la regla de Sturges busca evitar**.

#### `Dining_Spending`

**Qué mide:** el gasto en restaurantes.

**Lectura del gráfico.**

- Es un gasto discrecional: la **mediana (4.847 ₹)** es menos de la mitad de la **media (9.090 ₹)**.
- **`breaks = 17`:** se distingue el grueso de clientes que gastan de forma moderada frente a la minoría que concentra montos muy altos (**hasta 227.400 ₹**).
- En escala es **casi un calco de `Online_Shopping_Spending`**. Es otra señal de que varias categorías de gasto discrecional comparten el **mismo mecanismo generador**, algo propio de un dataset sintético.

#### `Travel_Spending`

**Qué mide:** el gasto en viajes.

**Lectura del gráfico.**

- Tiene la **asimetría más alta de las siete categorías de gasto (5,71)**.
- Según el Módulo 6, es la variable con el **$Z$-máximo más extremo de todo el dataset (19,4 σ)**.
- **`breaks = 17`:** casi toda la masa se aplasta contra el origen (**mediana 2.883 ₹**), y la cola visible hacia **213.100 ₹** es literalmente un puñado de clientes.

La mayoría no viaja o viaja poco, y quienes viajan gastan un orden de magnitud más.

#### `Entertainment_Spending`

**Qué mide:** el gasto en entretenimiento.

**Lectura del gráfico.**

- Es un gasto discrecional y ocasional, con **asimetría 5,01**, la segunda más alta después de `Travel_Spending` entre las categorías.
- **`breaks = 17`:** el pico queda pegado al origen (**mediana 3.830 ₹**), con una cola derecha marcada de quienes consumen ocio de forma intensiva.
- **`breaks = 60`:** la cola se vuelve un rastro de barras casi vacías, sin información adicional real.

#### `Utility_Bill_Spending`

**Qué mide:** el gasto en servicios públicos pagados con la tarjeta.

**Lectura del gráfico.**

- Domiciliar servicios públicos es una práctica frecuente pero de monto acotado.
- **`breaks = 17`:** la masa vive en valores bajos (**mediana 6.574 ₹**).
- La cola derecha es **más corta que la de `Travel_Spending` o `Fuel_Spending`** (**asimetría 4,35**). El informe la llama "la más baja de las siete categorías", aunque `Grocery_Spending` tiene 4,01 según el mismo informe.
- Esa cola corresponde a hogares con facturas altas, no a un grupo tan extremo como en las demás categorías.

#### `Outstanding_Balance`

**Qué mide:** el saldo que el cliente aún debe.

**Lectura del gráfico.**

- Sigue la lógica del gasto y del cupo.
- **`breaks = 17`:** la **mediana (145.300 ₹)** queda muy por debajo de la **media (303.400 ₹)**, y el **máximo (5.790.000 ₹)** es **casi 19 veces la media**.
- Comparte casi toda su información con `Statement_Balance` ($r = 0{,}997$, Módulo 8): el histograma de una es, en la práctica, el de la otra reescalado.

**Negocio:** unos pocos clientes concentran saldos muy grandes. La exposición de la cartera está concentrada en la cola.

#### `Statement_Balance`

**Qué mide:** el saldo del último corte de facturación.

**Lectura del gráfico.**

- Su forma es **prácticamente idéntica** a la de `Outstanding_Balance` en los tres paneles: misma cola derecha y misma sensibilidad a `breaks = 60`.
- Es coherente con ser casi la **misma magnitud económica medida en dos momentos distintos** del ciclo de facturación (**mediana 192.400 ₹, máximo 6.103.000 ₹**).

#### `Payment_Amount`

**Qué mide:** el monto pagado en el mes.

**Lectura del gráfico.**

- Es proporcional a lo facturado y reproduce la misma forma sesgada del saldo (**mediana 136.600 ₹, media 279.400 ₹**).
- **`breaks = 17`:** se distinguen bien los pagos moderados de la mayoría frente a los pagos muy grandes de la minoría con saldos altos, sin el ruido que `breaks = 60` introduce en la cola.

#### `Payment_Ratio`

**Qué mide:** la proporción del saldo facturado que efectivamente se pagó.

**Lectura del gráfico.**

- Es la **única variable de las 26 con asimetría negativa (−1,04)**. Más abajo, `Credit_Score` también se reporta con asimetría negativa (−0,58), así que en rigor son dos.
- Está acotada en 1 (nadie paga más del 100 %), y la mayoría paga casi todo su saldo (**mediana 0,84**). La masa se apila contra el techo.
- **`breaks = 17`:** la acumulación cerca de 1 se ve de inmediato.
- **`breaks = 60`:** el efecto es menos dañino que en las variables de dinero, porque el rango es corto (**0,10 a 1,00**) y el ancho de barra sigue siendo razonable.

**Negocio:** los **pagadores parciales** forman la cola izquierda. Son el grupo natural de vigilancia para la Gerencia, y el informe muestra después que `Payment_Ratio` es una de las variables más asociadas al puntaje.

#### `Credit_Utilization`

**Qué mide:** la proporción del cupo usada.

**Lectura del gráfico.**

- Está acotada entre 0 y 1 por construcción, con **asimetría de apenas 0,53**, de las más simétricas.
- Las políticas de cupo evitan llegar al tope: el **máximo real es 0,95**, no 1.
- En los tres paneles la forma es **compacta y estable**: ni `breaks = 5` la aplana de forma engañosa ni `breaks = 60` la fragmenta, porque **no hay una cola larga que fragmentar**.

#### `Cash_Advance_Amount`

**Qué mide:** el monto retirado como avance en efectivo.

**Lectura del gráfico.**

- El **70,3 %** de los clientes **nunca hace avances**, así que en los tres paneles la primera barra domina por completo el gráfico.
- No es una variable continua clásica sino una **masa puntual en cero más una cola larga** (**asimetría 6,78**, "la segunda más alta del dataset" según el texto; en la sección de `Reward_Points_Redeemed` el mismo informe la presenta como la más alta).

**Decisión:** ningún valor de `breaks` resuelve este problema. Hace falta **tratar el cero como su propia categoría** y no como el extremo de un histograma continuo.

**Negocio:** el avance en efectivo es una conducta minoritaria (29,7 % de los clientes). Para la Gerencia, *usar o no usar* avances es en sí una señal binaria, separada de *cuánto* se retira.

#### `EMI_Count`

**Qué mide:** el número de compras diferidas a cuotas (EMI, *Equated Monthly Installments*) vigentes.

**Lectura del gráfico.**

- Solo toma **siete valores enteros (0 a 6)**.
- Con `breaks = 17` o `breaks = 60`, R ya no tiene 17 o 60 intervalos que llenar: dibuja **como mucho 7 barras separadas por huecos**, porque no hay datos entre un entero y el siguiente.
- Es el ejemplo más claro del dataset de que el histograma "correcto" para un conteo discreto de rango corto no depende de escoger bien `breaks`, sino de **reconocer que la variable ya viene en barras**.

#### `International_Transactions`

**Qué mide:** el número de compras hechas en el exterior.

**Lectura del gráfico.**

- El **59,3 %** de los clientes no compra en el exterior (**mediana 0**), y el resto se reparte en apenas **14 valores enteros posibles** (15 valores únicos contando el cero).
- Se parece a `EMI_Count`, pero con una **cola derecha más larga (asimetría 2,11)**, porque unos pocos clientes acumulan varias compras internacionales.
- **`breaks = 60`:** aparecen más huecos que barras.

#### `Reward_Points_Earned`

**Qué mide:** los puntos acumulados, calculados a partir del gasto.

**Lectura del gráfico.**

- En los tres paneles es esencialmente la gráfica de `Monthly_Spending` reescalada: mismo pico bajo (**mediana 1.833**) y misma cola derecha (**asimetría 3,50**).
- **`breaks = 17`:** se distingue bien esa forma común.
- El parecido visual con `Monthly_Spending` es la contraparte gráfica de su **correlación de 0,980** (Módulo 8).

**Negocio:** los puntos son una variable redundante con el gasto. No aportan información nueva sobre riesgo.

#### `Reward_Points_Redeemed`

**Qué mide:** los puntos ya redimidos.

**Lectura del gráfico.**

- El **39,9 %** de los clientes nunca redime puntos (**mediana 135**, muy cerca de cero).
- Tiene **la segunda asimetría más alta del dataset (6,55)**, superada solo por `Cash_Advance_Amount`.
- **`breaks = 17`:** se ve la misma estructura de **masa en cero más cola larga** que las otras variables de uso opcional.
- **`breaks = 60`:** la cola (**hasta 44.820 puntos**) se disuelve en barras vacías.

#### `Mobile_App_Login`

**Qué mide:** el número de sesiones en la aplicación móvil al mes.

**Lectura del gráfico.**

- Tiene **asimetría de apenas 0,33**, de las más simétricas junto con `Monthly_Transactions`.
- Refleja un **hábito de consulta bastante uniforme** (rango de **2 a 71**, con **70 valores únicos**).
- **`breaks = 60`:** **no aparecen los huecos** de `EMI_Count` o `International_Transactions`, porque el rango es lo bastante amplio para llenar esos intervalos con datos reales.

#### `Credit_Score`

**Qué mide:** el puntaje crediticio.

**Lectura del gráfico.**

- Ya recibió un análisis completo al comienzo del módulo (secciones 4.1 y 4.2 del HTML). Se repite solo para documentar las 26 variables de forma uniforme.
- Lo único que añade este repaso es el contraste con el resto de la cartera: es **la única variable, junto con `Payment_Ratio`, con asimetría negativa (−0,58)**.
- Su rango (**367 a 792**) es corto comparado con las variables de dinero. Por diseño, un puntaje crediticio no puede dispararse en órdenes de magnitud como sí lo hacen un ingreso o un saldo.

### 3.5 Conclusión del Módulo 3

1. `Credit_Score` tiene media **629**, por debajo de su mediana (**638**). Es la primera señal de asimetría a la izquierda, que el histograma con Sturges ($k = 17$) confirma visualmente sin exagerarla ni esconderla.
2. El número de clases de un histograma es **una decisión del analista, no un hecho de los datos**. `breaks = 5` esconde la asimetría y `breaks = 60` la disuelve en ruido de muestreo. La regla de Sturges da un criterio objetivo, basado solo en $n$, para fijar ese número: aquí **$k = 17$ para las 26 variables numéricas**.
3. La misma comparación de tres anchos, con el ancho de barra expresado en las unidades de cada variable, se repitió sobre las 26 variables numéricas. El texto original de esta conclusión termina de forma **truncada** ("…queda documentado en la sección"), sin nombrar la sección. Se refiere a la sección "Histogramas de todas las variables numéricas" (4.4 del HTML).

**Lectura transversal para el negocio (síntesis de las 26 variables):**

- Las variables de **dinero** (ingreso, cupo, gasto, saldos y pagos) tienen colas derechas largas. Unos pocos clientes concentran montos muy grandes, y la media sobrestima al cliente típico.
- Las variables de **uso opcional** (avances en efectivo, compras internacionales, puntos redimidos) están **infladas en cero**. La decisión de *usar o no usar* es una señal en sí misma.
- Las de **conducta acotada** (`Credit_Utilization`, `Monthly_Transactions`, `Mobile_App_Login`) son compactas y casi simétricas.
- Las dos variables de **riesgo y conducta de pago** (`Credit_Score` y `Payment_Ratio`) son las únicas con cola a la izquierda. Esa minoría de la cola izquierda es la población objetivo del programa de seguimiento preventivo.

---

## Módulo 4: Densidad de kernel (S04)

**Motivación.** El Módulo 3 dejó un problema pendiente: el histograma no solo depende del número de cortes, sino también de **dónde empieza la primera caja** (el origen). Dos histogramas con el mismo ancho, pero corridos medio intervalo, pueden verse distintos sin ninguna justificación.

La **densidad de kernel** resuelve ese problema reemplazando las cajas por una **curva continua**, construida sumando una "montañita" (el **kernel**) centrada en cada observación. La decisión sobre la suavidad no desaparece: se **traslada íntegramente al ancho de banda $h$**.

**Conceptos.**

- **Kernel $K$.** Es una función simétrica, no negativa y con área 1. Aquí es la densidad normal estándar, una "campana" que reparte el peso de cada observación en su vecindad.
- **Ancho de banda $h$.** Es la "anchura" de cada montañita, en las unidades de la variable. Cumple el mismo papel que el ancho de barra del histograma:
  - un $h$ grande suaviza de más (sesgo);
  - un $h$ pequeño reproduce el ruido (varianza).

### 4.1 Cómo se escoge $h$ sin adivinar

**Regla de Silverman**, la que R usa por defecto:

$$h_{\text{Silverman}} = 0{,}9 \; \min\!\left(s,\; \frac{\text{RIC}}{1{,}34}\right) n^{-1/5}$$

**Componentes de la fórmula.**

- $s$ es la desviación estándar muestral.
- RIC es el **rango intercuartílico** ($Q_3 - Q_1$).
- El cociente $\text{RIC}/1{,}34$ es una estimación robusta de $\sigma$ bajo normalidad: en una normal, $\text{RIC} \approx 1{,}34\,\sigma$.
- El **$\min$** está ahí para que **un atípico no infle $s$** y ensanche la curva de más. Es la misma preocupación que en el Módulo 5 lleva a preferir `fivenum()` sobre la media.
- El factor $n^{-1/5}$ hace que $h$ se achique lentamente al crecer la muestra: con más datos, el estimador se permite más detalle.

**Cómo lo aplicamos.** R implementa esta fórmula en `bw.nrd0(x)`, y es la que se usa **en todo el módulo**, en vez de adivinar un valor.

### 4.2 Primero con una variable: `Credit_Score`

Igual que en el Módulo 3, se empieza por la variable de riesgo de referencia.

```r
var <- credit$Credit_Score
h <- bw.nrd0(var)
plot(density(var, bw = h), main = paste("h =", round(h, 4)), xlab = "Credit Score", lwd = 2)
rug(var)
```

`rug()` dibuja una "alfombra" de marcas verticales sobre el eje $x$, una por observación. Permite ver dónde están los datos reales bajo la curva.

**Resultado:** **$h = 7{,}076$** puntos.

**Lectura.** La curva confirma sin ambigüedad lo que el histograma con `breaks = 17` insinuaba: una forma **unimodal** con una **cola ligeramente más larga hacia la izquierda**. Ahora, además, **sin la arbitrariedad del origen de las cajas**, porque una curva de densidad no tiene "primera caja". Según la sección por variable, la **moda está cerca de 663,2**.

### 4.3 La fórmula detrás de `density()`

**Qué es.** La curva no es un dibujo: es un **estimador con fórmula**. Con $n$ observaciones $x_1,\dots,x_n$, un kernel $K$ y un ancho de banda $h$:

$$\hat f_h(x) = \frac{1}{n\,h}\sum_{i=1}^{n} K\!\left(\frac{x - x_i}{h}\right), \qquad K(u) = \frac{1}{\sqrt{2\pi}}\,e^{-u^{2}/2}$$

- Cada sumando es una **montañita gaussiana centrada en un cliente**.
- El factor $\frac{1}{nh}$ hace que **el área total sea 1**: el cambio de variable $u = (x - x_i)/h$ trae un factor $h$ que se cancela, y el $\frac1n$ promedia las $n$ montañitas, cada una de área 1.

**Cómo lo comprobamos.** Se programa la fórmula "a mano" y se compara con `density()` en cinco puntos:

```r
x_cs <- credit$Credit_Score
h_cs <- bw.nrd0(x_cs)
f_manual <- function(x0) sum(dnorm((x0 - x_cs) / h_cs)) / (length(x_cs) * h_cs)
puntos <- c(500, 580, 630, 680, 750)
d_cs <- density(x_cs, bw = h_cs)
data.frame(x = puntos,
           formula_a_mano = round(sapply(puntos, f_manual), 6),
           density_de_R   = round(approx(d_cs$x, d_cs$y, xout = puntos)$y, 6))
round(sum(d_cs$y) * diff(d_cs$x[1:2]), 4)   # área bajo la curva
```

- `dnorm()` es el kernel gaussiano $K$.
- `approx()` interpola linealmente la curva de `density()` en los puntos pedidos.
- El área se aproxima con una **suma de Riemann**: alturas por ancho de la rejilla.

**Resultados.**

- **Área bajo la curva = 1** (salida `[1] 1`).
- **Comparación en cinco puntos** (tabla paginada, recuperada del JSON del HTML):

| $x$ | Fórmula a mano | `density()` de R |
|---:|---:|---:|
| 500 | 0,001155 | 0,001156 |
| 580 | 0,003698 | 0,003701 |
| 630 | 0,005284 | 0,005283 |
| 680 | 0,005833 | 0,005829 |
| 750 | 0,000837 | 0,000837 |

- El informe afirma que **las dos columnas coinciden hasta el quinto decimal**. Las diferencias son de entre 0 y 4 millonésimas, y son exactas en $x = 750$. La densidad más alta de los cinco puntos está en $x = 680$, coherente con una moda cerca de 663.
- La pequeña diferencia viene de que `density()` evalúa la suma sobre una **rejilla de 512 puntos** y luego aproxima.

**Conclusión de la verificación.** $\hat f_h$ es **una densidad legítima, no un suavizado decorativo**.

### 4.4 $h$ decide lo que se ve: $h/3$, $h$ y $3h$

**Qué es y por qué.** El $h$ de Silverman es **una regla, no una verdad**: está deducido suponiendo normalidad. Por eso, como pide la sesión S04, se mira el mismo dato con $h/3$ y con $3h$ antes de decidir.

#### Caso 1: `Monthly_Transactions` (la variable en la que la decisión más cambia la lectura)

**Función auxiliar para contar picos:**

```r
contar_picos <- function(x, h) {
  d <- density(x, bw = h)
  i <- which(diff(sign(diff(d$y))) == -2) + 1   # máximos locales: la pendiente pasa de + a −
  i <- i[d$y[i] > 0.1 * max(d$y)]                # ignora bultos menores al 10 % del pico más alto
  round(d$x[i])
}
```

**Cómo detecta los picos:**

- `diff(d$y)` da la pendiente entre puntos consecutivos de la rejilla.
- `sign()` reduce cada pendiente a su signo.
- Un segundo `diff` igual a −2 marca el paso de subida a bajada, es decir, un máximo local.
- El filtro del 10 % descarta los bultos insignificantes.

**Gráfico:** tres paneles con `h/3`, `h (Silverman)` y `3h`, curvas en `steelblue` y `fig.width = 11`, `fig.height = 4`. Para no saturar el gráfico, el `rug` usa una **muestra aleatoria de 2.000 observaciones**, `sample(x_mt, 2000)`, con transparencia `rgb(0,0,0,0.2)`.

**Resultados.**

| Ancho de banda | Número de picos |
|---|---:|
| $h/3$ | 18 |
| $h$ (Silverman, $h = 4{,}35$) | 5 |
| $3h$ | 1 |

- Posición de los picos con $h$: **43, 64, 91, 143 y 166** transacciones.
- Mediana de transacciones por tipo de tarjeta, `sort(tapply(x_mt, credit$Card_Type, median))`:

| Basic | Silver | Gold | Platinum | Signature |
|---:|---:|---:|---:|---:|
| 38 | 62 | 91 | 116 | 120 |

**Lectura.**

- **Con $3h$:** 1 solo pico. La variable parece una campana ancha y la estructura se pierde por **exceso de sesgo** (sobre-suavizado).
- **Con $h/3$:** 18 picos, uno cada pocas transacciones. Es **varianza muestral, ruido**.
- **Con el $h$ de Silverman ($h = 4{,}35$):** 5 picos. Según el informe, los primeros (**43, 64 y 91**) **coinciden con las medianas de `Basic`, `Silver` y `Gold`** (38, 62 y 91). La coincidencia es exacta en Gold, cercana en Silver y aproximada en Basic, con 5 transacciones de diferencia. Los picos en 143 y 166 no se asocian a un nivel en el texto.
- **Criterio de la sesión para distinguir estructura de ruido:** un pico es real si **se sostiene al mover un poco $h$** y **tiene sentido en el tema de los datos**.
  - Los picos de $h$ son **la huella de los tipos de tarjeta mezclados en una sola variable**.
  - Los de $h/3$ no tienen ninguna explicación.

**Decisión.** Se reporta la densidad con el $h$ de Silverman, **declarado**, y se deja anotado que **`Monthly_Transactions` es en realidad una mezcla de poblaciones**. Esto reaparece en la **paradoja de Simpson del Módulo 12**.

**Negocio.** El número de transacciones mensuales depende fuertemente del tipo de tarjeta: Basic hace unas 38 compras al mes y Signature unas 120. Cualquier umbral de "actividad anormal" debe fijarse **por segmento de tarjeta** y no para la cartera total, porque la distribución global mezcla poblaciones distintas.

#### Caso 2: `Age` (la otra cara del problema)

```r
x_age <- credit$Age; h_age <- bw.nrd0(x_age)
# tres paneles h/3, h, 3h en color darkorange
c(picos_h3 = length(contar_picos(x_age, h_age / 3)), edades_distintas = length(unique(x_age)))
```

**Resultado.** Con $h/3 = 0{,}42$ años aparecen **51 picos**, frente a **53 edades distintas**.

**Lectura.** Hay prácticamente **un pico por cada edad entera**. No es una estructura de la cartera: la edad se registra en **años completos**, y un $h$ menor que 1 "ve" esa rejilla. **El ruido de un $h$ muy pequeño no siempre es aleatorio; a veces es la discretización de la variable.**

**Regla aplicada en todo el módulo:** cada densidad **declara su $h$**, y $h$ **nunca se baja por debajo de la resolución con la que se mide la variable**.

### 4.5 Aplicado a cada variable

**Cómo lo aplicamos.** El procedimiento se repite sobre las 25 variables restantes, cada una en su propio bloque de código y con una lectura específica:

1. calcular $h$ con `bw.nrd0()`;
2. graficar `density(x, bw = h)` con el título `"h = <valor>"`;
3. marcar los datos con `rug()`.

En la práctica se documentan las 26: `Credit_Score` remite a la sección inicial.

#### Tabla resumen

Valores citados en el texto del informe. Los marcados con † solo aparecían en el título de la imagen del gráfico; se recalcularon con `bw.nrd0()` sobre el CSV bronze, el mismo cálculo del informe (comprobación: `Age` da 1,265 ≈ 1,27, igual que el informe).

| Variable | $h$ (`bw.nrd0`) | Moda aprox. de la curva | Comentario clave |
|---|---:|---:|---|
| `Age` | 1,27 años | 31,9 años | Casi simétrica, cola derecha suave |
| `Annual_Income` | ≈ 77.600 ₹ | 1.045.364 ₹ | Moda muy por debajo de la media |
| `Credit_Limit` | 47.988,16 ₹ † | 86.922 ₹ | Moda lejísimos de la media (709.677) |
| `Card_Age_Months` | 3 meses | ≈ 35 meses | Cartera joven, sin segundo pico |
| `Monthly_Spending` | ≈ 4.350 ₹ | 18.592 ₹ | Moda < mediana < media |
| `Monthly_Transactions` | 4,35 | 64,1 | Unimodal en el gráfico por variable |
| `Avg_Transaction_Value` | 34,94 ₹ † | ≈ 472 ₹ | `rug` denso abajo y disperso arriba |
| `Online_Shopping_Spending` | ≈ 773 ₹ | 2.323 ₹ | Pico bajo, cola larga |
| `Grocery_Spending` | 1.175,99 ₹ † | 3.600 ₹ | Moda más alta de las categorías |
| `Fuel_Spending` | 704,28 ₹ † | ≈ 1.653 ₹ | Primer tramo más simétrico |
| `Dining_Spending` | ≈ 640 ₹ | ≈ 1.707 ₹ | Calco de Online |
| `Travel_Spending` | 446,37 ₹ † | 773 ₹ | La más apretada contra el origen |
| `Entertainment_Spending` | 543,35 ₹ † | ≈ 954 ₹ | Entre Travel y Dining |
| `Utility_Bill_Spending` | 812,48 ₹ † | ≈ 2.358 ₹ | Segunda moda más alta de las categorías |
| `Outstanding_Balance` | ≈ 20.390 ₹ | 32.949 ₹ | Tres centros muy separados |
| `Statement_Balance` | 23.528,08 ₹ † | 55.687 ₹ | Casi idéntica a Outstanding |
| `Payment_Amount` | 18.817,78 ₹ † | ≈ 39.820 ₹ | Cola hasta ≈ 6.000.000 ₹ |
| `Payment_Ratio` | ≈ 0,025 | ≈ 0,97 | Moda pegada al techo |
| `Credit_Utilization` | ≈ 0,021 | ≈ 0,38 | El $h$ más pequeño del dataset |
| `Cash_Advance_Amount` | 670,59 ₹ † | 369,6 ₹ | Masa puntual en cero mal representada |
| `EMI_Count` | 0,173 † | ≈ 2 | Curva continua sobre 7 enteros |
| `International_Transactions` | 0,154 † | pegada al origen | Masa en cero, cola hasta 14 |
| `Reward_Points_Earned` | 235,08 puntos † | ≈ 468 puntos | Igual a `Monthly_Spending` reescalada |
| `Reward_Points_Redeemed` | 56,40 puntos † | 7,5 puntos | Masa en cero, cola hasta 44.820 |
| `Mobile_App_Login` | 1,742 sesiones † | ≈ 24,6 sesiones | Casi simétrica |
| `Credit_Score` | 7,076 | ≈ 663,2 | Unimodal, cola izquierda |

**Qué es la moda de una densidad.** Es el valor de $x$ donde $\hat f_h(x)$ alcanza su máximo, es decir, el valor "más típico". A diferencia de la media, **no se deja arrastrar por la cola**. Por eso, en distribuciones con cola derecha, se cumple el orden **moda < mediana < media**.

#### `Age`

- **$h = 1{,}27$ años.**
- La curva confirma la forma **casi simétrica** del histograma, con su punto más alto cerca de **31,9 años** y una **cola derecha suave hacia los 70**.
- Sin las 60 barras del histograma, la ligera inclinación se ve todavía más limpia.

#### `Annual_Income`

- **$h \approx 77.600$ ₹.** Es un ancho de banda grande, coherente con una variable cuya dispersión (**desviación estándar de 1.407.257 ₹**) es de las mayores del dataset.
- La curva alcanza su punto más alto cerca de **1.045.364 ₹**, muy por debajo de la **media (1.479.318 ₹)**.
- **La moda, a diferencia de la media, no se deja arrastrar por la cola de altos ingresos.**

#### `Credit_Limit`

- La **moda (86.922 ₹)** queda muy cerca del mínimo de la escala de cupos usuales y muy lejos de la **media (709.677 ₹)**.
- La curva deja ver, mejor que el histograma escalonado, que **la mayoría de la cartera tiene cupos modestos** y que una minoría con cupos de varios millones estira la curva hacia la derecha **sin levantarla**.

#### `Card_Age_Months`

- **$h = 3$ meses.**
- Pico cerca de los **35 meses** (menos de 3 años) y decaimiento suave hasta los 240.
- Es una cartera de tarjetas mayoritariamente jóvenes, **sin el segundo pico** que tendría una cartera con una generación antigua de tarjetahabientes y otra reciente.

#### `Monthly_Spending`

- **$h \approx 4.350$ ₹.**
- La curva confirma la marcada asimetría a la derecha (**asimetría 3,00**) que acumula las colas de las siete categorías.
- La **moda cae cerca de 18.592 ₹**, muy por debajo de la **mediana (50.022 ₹)** y de la **media (73.872 ₹)**.
- La gran mayoría tiene consumos mensuales contenidos, mientras un grupo reducido se extiende **hasta más de 600.000 ₹**.

#### `Monthly_Transactions`

- Curva **unimodal y razonablemente simétrica**: la **moda (64,1)** está cerca de la **mediana (76)** y de la **media (83,0)**.
- El informe la llama "la variable con menor asimetría (0,54) de todo el dataset junto con `Mobile_App_Login`". Según el mismo informe, `Mobile_App_Login` (0,33) y `Credit_Utilization` (0,53) son algo menores.
- Su densidad lo confirma, sin las asperezas de las variables de gasto.

> **Matiz:** en esta gráfica individual, con el $h$ de Silverman y sin muestreo del `rug`, la curva se describe como unimodal. En la sección 4.4, la función `contar_picos` con el mismo $h = 4{,}35$ detecta 5 picos que superan el 10 % del máximo. Las dos lecturas conviven en el informe: la visión global es "una campana", y el detalle revela la mezcla de tipos de tarjeta.

#### `Avg_Transaction_Value`

- **Moda cerca de 472 ₹**, "casi calcada" de su mediana (617 ₹) según el informe.
- El `rug()` en la parte baja del eje se ve **denso y casi continuo**, mientras que hacia el **máximo (10.460 ₹)** las marcas se separan tanto que son casi invisibles.
- Es la representación más directa de un **cociente con cola pesada**.

#### `Online_Shopping_Spending`

- **$h \approx 773$ ₹.**
- La curva sube rápido cerca del origen (**moda 2.323 ₹**) y desciende con una cola larga y suave.
- Es el mismo patrón "pico bajo, cola larga" de todas las categorías de gasto discrecional, aquí **sin el escalonado que mostraba el histograma**.

#### `Grocery_Spending`

- La **moda (3.600 ₹)** es la **más alta de las siete categorías de gasto**, consistente con tener también la mediana más alta (**10.650 ₹**).
- El mercado es el único gasto que casi toda la cartera hace de forma sustancial, y la curva lo refleja con un **pico desplazado del origen**.

#### `Fuel_Spending`

- **Moda cerca de 1.653 ₹**, con una cola visible pero menos extendida que las de `Travel_Spending` o `Entertainment_Spending`.
- La curva sube y baja de forma **más simétrica en su primer tramo**, coherente con que el combustible es un **gasto de necesidad** para quien tiene vehículo y no puramente discrecional.

#### `Dining_Spending`

- **Moda cerca de 1.707 ₹** y **$h \approx 640$ ₹**.
- La curva es visualmente casi un **calco de la de `Online_Shopping_Spending`** (moda 2.323 ₹, $h \approx 773$ ₹).
- Son dos categorías de gasto discrecional distintas que comparten el mismo mecanismo generador de "**mayoría moderada, minoría intensiva**".

#### `Travel_Spending`

- De las siete categorías, es la curva **más apretada contra el origen** (**moda 773 ₹**, la más baja del grupo) y la de cola **más extendida y plana**.
- Es coherente con ser, según el texto de esta sección, "la variable de mayor asimetría (5,71) y mayor $Z$-máximo (19,4 σ) de todo el dataset". En asimetría, `Cash_Advance_Amount` (6,78) y `Reward_Points_Redeemed` (6,55) la superan según el propio informe.
- La mayoría casi no viaja, y el `rug()` muestra **marcas aisladas muy lejos** del grueso de la cartera.

#### `Entertainment_Spending`

- **Moda cerca de 954.** En el original aparece escrita como "\$954", una errata de símbolo monetario: la unidad es ₹.
- Queda entre la de `Travel_Spending` (773 ₹) y la de `Dining_Spending` (1.707 ₹).
- Es un gasto discrecional y ocasional que el `rug()` muestra **denso hasta unos pocos miles de rupias** y disperso mucho más allá.

#### `Utility_Bill_Spending`

- **Moda cerca de 2.358 ₹**, la más alta después de `Grocery_Spending` entre las categorías de gasto.
- Es coherente con tener también "la asimetría más baja del grupo (4,35, Módulo 3)".
- Domiciliar servicios públicos es una **práctica recurrente y de monto relativamente acotado**, menos discrecional que el entretenimiento o los viajes.

#### `Outstanding_Balance`

- **$h \approx 20.390$ ₹.**
- La **moda (32.949 ₹)** queda muy por debajo de la **mediana (145.300 ₹)** y de la **media (303.400 ₹)**.
- **Tres medidas de centro que se alejan cada vez más entre sí** son la firma de una cola derecha larga y pesada.

**Negocio:** el saldo "más frecuente" es pequeño, pero el saldo promedio está inflado por pocos deudores grandes. La exposición agregada depende de esa cola.

#### `Statement_Balance`

- La curva es **casi indistinguible** de la de `Outstanding_Balance` en su forma general: **moda 55.687 ₹** frente a 32.949 ₹, ambas muy por debajo de sus medias.
- Es la contraparte visual de compartir prácticamente la misma información ($r = 0{,}997$).

#### `Payment_Amount`

- **Moda cerca de 39.820 ₹**, con una cola que llega hasta **cerca de 6.000.000 ₹**.
- Pertenece a la misma familia de forma que `Outstanding_Balance` y `Statement_Balance`, coherente con que **el pago mensual es proporcional a lo que el cliente debe**.

#### `Payment_Ratio`

- **$h \approx 0{,}025$**, el ancho de banda más pequeño entre las variables de dinero y ratio, porque su rango es corto.
- La curva sube hasta un **pico cerca de 0,97** y **cae abruptamente después**.
- Es la **única variable de las 26 cuya moda está pegada al borde superior de su rango posible**: la contraparte visual exacta de su asimetría negativa.

**Negocio:** el comportamiento "normal" es pagar casi la totalidad. Alejarse de ese pico hacia la izquierda es una desviación de conducta relevante para el riesgo.

#### `Credit_Utilization`

- Curva **suave y unimodal**, con **pico cerca de 0,38** y sin ninguna de las asperezas de las variables de dinero.
- Tiene **el ancho de banda más pequeño de todo el dataset ($h \approx 0{,}021$)**, consistente con ser de las variables menos dispersas (**desviación estándar 0,206**).

#### `Cash_Advance_Amount`

Aquí **la densidad de kernel muestra su límite**.

- El **70,3 %** tiene exactamente cero, pero `density()` **no sabe dibujar una masa puntual**. La dibuja como una curva continua con un **pico pronunciado cerca de cero (moda 369,6)** que en realidad corresponde a una barra de altura finita en un histograma.
- La curva sirve para ver la **forma de la cola de quienes sí usan avances**, pero es **engañosa** si se lee como "la probabilidad de gastar exactamente 370 ₹".

#### `EMI_Count`

- Con solo **7 valores enteros posibles**, la densidad dibuja una curva continua sobre una variable que no lo es.
- El `rug()` muestra **7 columnas de marcas apiladas**, no un continuo.
- La curva suave entre ellas (**pico cerca de 2**) es una **aproximación conveniente**, no una descripción literal de cómo se distribuyen los datos.

#### `International_Transactions`

- Con el **59,3 %** de la cartera en cero, el pico está **prácticamente pegado al origen**, con una cola larga y baja hasta **14**.
- Es el mismo problema conceptual de `Cash_Advance_Amount`: la "montaña" cerca de cero es la forma en que `density()` traduce una **masa puntual discreta** a una curva continua. **No es evidencia de que existan valores fraccionarios** de transacciones internacionales.

#### `Reward_Points_Earned`

- **Moda cerca de 468 puntos.**
- La curva reproduce casi exactamente la forma de `Monthly_Spending` reescalada: otra vez, la contraparte visual de una **correlación de 0,980** entre ambas.

#### `Reward_Points_Redeemed`

- Con el **39,9 %** en cero, la **moda (7,5)** queda prácticamente pegada al origen. Es el mismo efecto de suavizado sobre una masa puntual de `Cash_Advance_Amount` e `International_Transactions`.
- La cola **hasta 44.820 puntos** corresponde a la minoría que redime en montos grandes.

#### `Mobile_App_Login`

- Curva **suave y casi simétrica**, con **pico cerca de 24,6 sesiones**, muy parecida en forma a la de `Monthly_Transactions`.
- Refleja otro **hábito de consulta razonablemente uniforme**, sin la cola pesada de las variables de dinero.

#### `Credit_Score`

- Ya se presentó al comienzo del módulo: **$h = 7{,}076$**, **moda cerca de 663,2**.
- Se repite solo para mantener el mismo orden de las 26 variables que en los Módulos 3 y 5. No hay nada nuevo que añadir.

#### Lectura de conjunto

- Vistas las 26 variables, **el ancho de banda $h$ varía en casi cinco órdenes de magnitud**: de **0,02** en los ratios acotados a **más de 77.000 ₹** en `Annual_Income`. Siempre lo calibra `bw.nrd0()` según la dispersión propia de cada variable.
- Las variables con una **masa de clientes en cero** comparten una **limitación real del método**: la curva continua no puede representar fielmente un valor discreto que concentra a un tercio o más de la cartera, y hay que leerla sabiendo eso. Son:
  - `Cash_Advance_Amount`;
  - `International_Transactions`;
  - `Reward_Points_Redeemed`;
  - en menor medida, `EMI_Count`.

**Decisiones del módulo.**

1. Usar siempre $h$ de Silverman (`bw.nrd0`) y declararlo en el título del gráfico.
2. No bajar $h$ por debajo de la resolución de medida de la variable.
3. Leer con cautela las densidades de las variables infladas en cero o discretas.

### 4.6 Conclusión del Módulo 4

1. La densidad de kernel resuelve el problema del **origen arbitrario** del histograma **sin eliminar la decisión**: la traslada al ancho de banda $h$, que aquí se calibra con la regla de Silverman (`bw.nrd0()`) en vez de fijarse a mano.
2. Sobre `Credit_Score`, la curva confirma con más nitidez la misma forma **unimodal y ligeramente asimétrica a la izquierda** que ya habían anticipado la media, la mediana (Módulo 3) y el histograma con Sturges.
3. Aplicada a las 26 variables, la densidad de kernel reproduce en una curva continua la misma clasificación de formas del diccionario del Módulo 1:
   - **picos pegados al origen** en las variables de gasto;
   - **forma acotada y compacta** en los ratios;
   - **barras discretas separadas** en los conteos de rango corto.

**Significado para la Gerencia de Riesgo de Crédito.**

- En casi todas las variables monetarias, la "moda" (el cliente más frecuente) está muy por debajo de la media. Los reportes de cartera basados en promedios describen a un cliente que casi no existe; conviene complementarlos con la mediana o la moda.
- `Monthly_Transactions` es una **mezcla de poblaciones por tipo de tarjeta**. Los umbrales de alerta de actividad deben fijarse por segmento.
- `Payment_Ratio` tiene su moda pegada a 0,97. El cliente que se aleja de pagar casi el total es una desviación de la norma de la cartera y una candidata natural a seguimiento preventivo.
- En las variables infladas en cero (avances, compras internacionales, redenciones), la información útil está en **si el cliente usa o no el producto** y en la **cola de quienes lo usan**, no en una curva suave.

---

### Notas de coherencia detectadas en las fuentes (Módulos 1 a 4)

Para no perder ningún detalle, se dejan registradas las inconsistencias internas del texto original. Ninguna afecta a los cálculos.

1. **Edad máxima.** El Módulo 1 dice "de 18 a 69 años", pero `summary()` y `range()` del Módulo 2 dan un máximo de **70**.
2. **Cardinalidad de las monetarias.** El rango "entre 40.475 y 50.000 valores únicos" se calcula solo sobre tres variables. `Cash_Advance_Amount` (14.826) y `Credit_Limit` (4.318) tienen menos, y ninguna monetaria alcanza 50.000.
3. **Ránking de asimetrías.** Varias frases no concuerdan entre sí:
   - "`Credit_Limit`, mayor asimetría del dataset (3,01)";
   - "`Travel_Spending`, mayor asimetría (5,71)" (Módulo 4);
   - "`Cash_Advance_Amount` (6,78), segunda más alta";
   - "`Reward_Points_Redeemed` (6,55), segunda más alta, superada solo por `Cash_Advance_Amount`".

   Con los valores reportados, el orden es Cash_Advance (6,78) > Reward_Points_Redeemed (6,55) > Travel (5,71) > Entertainment (5,01) > …
4. **Asimetría negativa.** `Payment_Ratio` se presenta como "la única con asimetría negativa", pero `Credit_Score` también lo es (−0,58). La sección de `Credit_Score` lo reconoce.
5. **`Utility_Bill_Spending`** se llama "la menor asimetría de las siete categorías (4,35)", pero `Grocery_Spending` se reporta con 4,01.
6. **`Monthly_Spending`** se presenta con una asimetría (3,00) "más alta que cualquier categoría individual", pero las siete categorías tienen asimetrías mayores, de 4,01 a 5,71 (tabla `Skew` del Módulo 15).
6b. **Variable más simétrica.** `Monthly_Transactions` (0,54) se llama "la de menor asimetría del dataset junto con `Mobile_App_Login`", pero `EMI_Count` (0,17, tabla `Skew` del Módulo 15) y `Mobile_App_Login` (0,33) son menores.
7. **`Online_Shopping_Spending`:** "mediana menos de un tercio de la media" no se ajusta a 6.163 / 11.240 ≈ 0,55.
8. **Orden de secciones.** La regla de Sturges se refiere a "la comparación anterior", que en el documento final aparece después.
9. **Conclusión 3 del Módulo 3** truncada ("…queda documentado en la sección").
10. **Errata "\$954"** en `Entertainment_Spending`: la unidad es ₹.
11. **Referencias hacia adelante.** Varias lecturas citan resultados de módulos posteriores: el Módulo 6 ($Z$-máximo de 19,4 σ), el Módulo 7 ($r = 0{,}974$ y $\eta^2$ de `Gender`), el Módulo 8 ($r = 0{,}997$ y $r = 0{,}980$), el Módulo 9 y el Módulo 12. Son vestigios de una reorganización: se usan como contexto y se demuestran en esos módulos.


---

## Módulo 5: Caja y Bigotes (Boxplots) y Detección Univariada de Atípicos (S03)

### Propósito del módulo y por qué se cambia de variable

El Módulo 3 trabajó con `Credit_Score`, una variable **casi simétrica**. Este módulo cambia **deliberadamente** a `Monthly_Spending` (gasto mensual total del cliente, en rupias ₹), que el diccionario del Módulo 1 describe como **fuertemente asimétrica a la derecha**: es la suma de siete categorías de gasto (`Online_Shopping`, `Grocery`, `Fuel`, `Dining`, `Travel`, `Entertainment`, `Utility_Bill`) que ya vienen sesgadas individualmente. Es el caso típico donde la caja y bigotes —y la regla de Tukey que la acompaña— se comporta distinto a como lo hace con una variable simétrica, y por eso se trata aparte como "caso de estudio" antes de extender el procedimiento a las otras 25 variables numéricas.

**Decisión:** empezar por una variable asimétrica (y no repetir `Credit_Score`) para mostrar justamente el escenario en el que la regla de Tukey puede engañar si se aplica mecánicamente.

**Significado para el negocio:** la Gerencia de Riesgo suele recibir "listas de atípicos" generadas automáticamente; este módulo enseña a leerlas correctamente antes de depurar, excluir o investigar clientes.

---

### 5.1 Los cinco números de Tukey (`fivenum`)

#### Concepto

El resumen de cinco números de John Tukey describe una distribución con cinco puntos de corte robustos, en lugar de media y desviación estándar:

$$
\big(\;\min,\; Q_1,\; \tilde{x},\; Q_3,\; \max\;\big)
$$

- $\min$ y $\max$: extremos observados.
- $Q_1$ (primer cuartil o "bisagra inferior"): deja el 25 % de los datos por debajo.
- $\tilde{x}$ (mediana): deja el 50 % por debajo.
- $Q_3$ (tercer cuartil o "bisagra superior"): deja el 75 % por debajo.

`fivenum()` de R usa las **bisagras de Tukey** (medianas de cada mitad), que pueden diferir ligeramente de `quantile()` en muestras pequeñas; con $n = 50\,000$ la diferencia es irrelevante.

**Intuición:** la elección es importante cuando la variable **no es simétrica**, porque los cuantiles **no se distorsionan** con una cola larga, mientras que la media sí es arrastrada por los valores extremos. La forma de la distribución se lee comparando las distancias entre los cinco números: si la distancia mediana→máximo es mucho mayor que mínimo→mediana, hay cola derecha larga.

#### Aplicación

```r
gasto <- credit$Monthly_Spending
f_gasto <- fivenum(gasto)
names(f_gasto) <- c("Mínimo", "Q1", "Mediana", "Q3", "Máximo")
f_gasto
```

#### Resultado

| Mínimo | Q1 | Mediana | Q3 | Máximo |
|---:|---:|---:|---:|---:|
| 2 235,63 ₹ | 26 646,33 ₹ | 50 022,38 ₹ | 83 032,36 ₹ | 691 687,96 ₹ |

**Lectura:** el salto de la mediana (**50.022 ₹**) al máximo (**691.688 ₹**) es enorme comparado con el salto del mínimo a la mediana (de 2.236 ₹ a 50.022 ₹) —la **firma numérica de una cola derecha larga**, consistente con lo que el diccionario del Módulo 1 ya anticipaba para esta variable.

**Negocio:** el "cliente típico" (mediana) gasta unas 50 mil rupias al mes, pero existe una minoría que gasta más de 13 veces esa cifra; cualquier política que use el promedio del gasto como referencia quedará sesgada por esa minoría.

---

### 5.2 Rango Intercuartílico ($RIC$) y Límites de Tukey

#### Concepto

El rango intercuartílico mide la dispersión del 50 % central de los datos, **ignorando las colas por construcción**:

$$
RIC = Q_3 - Q_1
$$

Tukey lo usa para trazar dos barreras ("vallas internas") más allá de las cuales un dato se considera **candidato** a atípico:

$$
\text{Límite Inferior} = Q_1 - 1.5 \cdot RIC \qquad \text{Límite Superior} = Q_3 + 1.5 \cdot RIC
$$

En el boxplot, la caja va de $Q_1$ a $Q_3$, la línea interior es la mediana, los bigotes llegan hasta el dato más extremo que todavía está dentro de las vallas, y los puntos sueltos son las observaciones fuera de ellas.

**Por qué 1,5:** el multiplicador no es arbitrario. Bajo una distribución normal, $Q_1 \approx \mu - 0{,}674\sigma$ y $Q_3 \approx \mu + 0{,}674\sigma$, así que $RIC \approx 1{,}349\sigma$ y las vallas quedan en $\mu \pm 2{,}698\sigma$; fuera de ellas cae, en promedio, **poco menos del 1 %** de los datos (el propio informe precisa más adelante "cerca de 0,7 % bajo normalidad"). Es, por tanto, una regla **pensada para variables aproximadamente simétricas**, algo que ya se sabe que `Monthly_Spending` no es.

#### Aplicación

```r
q1_gasto <- f_gasto["Q1"]
q3_gasto <- f_gasto["Q3"]
ric_gasto <- q3_gasto - q1_gasto
lim_inf_gasto <- q1_gasto - 1.5 * ric_gasto
lim_sup_gasto <- q3_gasto + 1.5 * ric_gasto
```

#### Resultado

| $Q_1$ | $Q_3$ | $RIC$ | Límite inferior | Límite superior |
|---:|---:|---:|---:|---:|
| 26 646,33 | 83 032,36 | 56 386,03 | **−57 932,71** | 167 611,40 |

**Lectura:** el límite inferior da **−57.933, un valor negativo, imposible para un gasto**, y el superior da **167.611 ₹**. Que el propio límite inferior sea un valor que la variable no puede tomar es ya una pista de que la regla de Tukey, pensada para variables simétricas, **se comporta de forma particular** sobre una variable con esta cola: en la práctica, solo la valla superior está activa.

---

### 5.3 Conteo de atípicos univariados

#### Concepto

Un **atípico univariado** (según Tukey) es una observación $x_i$ tal que $x_i < Q_1 - 1{,}5\,RIC$ o $x_i > Q_3 + 1{,}5\,RIC$. El porcentaje de atípicos es

$$
\%\,\text{atípicos} = 100 \cdot \frac{\#\{i : x_i < LI \;\lor\; x_i > LS\}}{n}.
$$

#### Aplicación

```r
atipicos_gasto <- gasto[gasto < lim_inf_gasto | gasto > lim_sup_gasto]
n_atipicos_gasto <- length(atipicos_gasto)
pct_atipicos_gasto <- (n_atipicos_gasto / length(gasto)) * 100

boxplot(gasto, horizontal = TRUE, col = "skyblue",
        main = "Diagrama de Caja: Gasto Mensual (Monthly_Spending)",
        xlab = "Gasto Mensual ($)")
abline(v = c(lim_inf_gasto, lim_sup_gasto), col = "red", lty = 2, lwd = 2)
```

Se dibuja un boxplot horizontal (azul cielo) con los dos límites de Tukey superpuestos como **líneas rojas discontinuas** (`lty = 2`, `lwd = 2`). (Detalle menor: la etiqueta del eje dice "$" aunque la unidad es la rupia ₹.)

#### Resultado

| N.º de atípicos | Porcentaje |
|---:|---:|
| **4 213** | **8,426 %** |

**Lectura del gráfico:** 4.213 clientes (**8,43 %** de la cartera) quedan marcados como atípicos, y **los tres cuartos de la caja se ven aplastados contra el lado izquierdo** del gráfico —efecto directo de que el bigote superior tiene que estirarse hasta **167.611 ₹** para alcanzar siquiera al **91,6 %** de los datos que sí caen dentro. Todos los atípicos están en la cola derecha (ninguno puede estar por debajo de un límite negativo).

**Observación clave:** esto **no es un caso aislado** de `Monthly_Spending`: se repite, con distinta intensidad, en la mayoría de las variables de gasto y saldo del dataset. Por eso, antes de juzgar caso por caso, conviene verlo en las 26 variables a la vez.

#### Procedimiento repetido para las 25 variables restantes

Se repite exactamente el mismo procedimiento —cinco números, límites de Tukey, conteo de atípicos, boxplot con esos límites— sobre las otras 25 variables numéricas, **cada una en su propio bloque de código** y con una lectura específica de lo que sus propios números dicen. El código-plantilla (ilustrado con `Age`, idéntico para todas cambiando el nombre de la variable) es:

```r
f <- fivenum(credit$Age); q1 <- f[2]; q3 <- f[4]; ric <- q3 - q1
li <- q1 - 1.5*ric; ls <- q3 + 1.5*ric
n_out <- sum(credit$Age < li | credit$Age > ls)
c(Q1 = q1, Q3 = q3, RIC = ric, Lim_Inferior = li, Lim_Superior = ls,
  N_Atipicos = n_out, Porcentaje = round(100*n_out/length(credit$Age), 3))

bp <- boxplot(credit$Age, plot = FALSE)
bp$stats[1,1] <- li; bp$stats[5,1] <- ls
bp$out <- credit$Age[credit$Age < li | credit$Age > ls]
bxp(bp, horizontal = TRUE, col = "skyblue", main = "Diagrama de Caja: Age", xlab = "Age")
abline(v = c(li, ls), col = "red", lty = 2, lwd = 2)
```

**Decisión técnica:** en vez de `boxplot()` directo, se calcula el objeto con `boxplot(..., plot = FALSE)` y se **sobrescriben** los extremos de los bigotes (`bp$stats[1,1]` y `bp$stats[5,1]`) con los límites teóricos de Tukey (`li`, `ls`) y la lista de puntos sueltos (`bp$out`) con los atípicos calculados a mano; luego se dibuja con `bxp()`. Así el gráfico muestra **exactamente** las vallas de la fórmula (no "el último dato dentro de las vallas", que es lo que hace `boxplot()` por defecto) y es coherente con el conteo numérico.

#### Tabla resumen de las 26 variables

| # | Variable | $Q_1$ | $Q_3$ | $RIC$ | Lím. inferior | Lím. superior | N.º atípicos | % |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | `Age` | 27 | 44 | 17 | 1,5 | 69,5 | 278 | 0,556 |
| 2 | `Annual_Income` | 657 770,5 | 1 663 677 | 1 005 906,5 | −851 089,25 | 3 172 536,75 | 4 037 | 8,074 |
| 3 | `Credit_Limit` | 157 000 | 779 000 | 622 000 | −776 000 | 1 712 000 | 4 173 | 8,346 |
| 4 | `Card_Age_Months` | 31 | 70 | 39 | −27,5 | 128,5 | 1 287 | 2,574 |
| 5 | `Monthly_Spending` | 26 646,33 | 83 032,36 | 56 386,03 | −57 932,71 | 167 611,40 | 4 213 | 8,426 |
| 6 | `Monthly_Transactions` | 49 | 108 | 59 | −39,5 | 196,5 | 0 | 0,000 |
| 7 | `Avg_Transaction_Value` | 448,37 | 901,27 | 452,90 | −230,98 | 1 580,62 | 4 286 | 8,572 |
| 8 | `Online_Shopping_Spending` | 2 800,675 | 12 820,420 | 10 019,745 | −12 228,942 | 27 850,037 | 4 045 | 8,090 |
| 9 | `Grocery_Spending` | 5 176,815 | 20 419,725 | 15 242,910 | −17 687,550 | 43 284,090 | 4 032 | 8,064 |
| 10 | `Fuel_Spending` | 2 432,140 | 11 560,985 | 9 128,845 | −11 261,128 | 25 254,253 | 4 176 | 8,352 |
| 11 | `Dining_Spending` | 2 089,505 | 10 381,865 | 8 292,360 | −10 349,035 | 22 820,405 | 4 202 | 8,404 |
| 12 | `Travel_Spending` | 1 076,960 | 6 862,885 | 5 785,925 | −7 601,928 | 15 541,773 | 4 315 | 8,630 |
| 13 | `Entertainment_Spending` | 1 570,085 | 8 612,840 | 7 042,755 | −8 994,048 | 19 176,972 | 4 276 | 8,552 |
| 14 | `Utility_Bill_Spending` | 2 978,380 | 13 510,045 | 10 531,665 | −12 819,118 | 29 307,543 | 4 056 | 8,112 |
| 15 | `Outstanding_Balance` | 55 640,71 | 319 985,76 | 264 345,05 | −340 876,85 | 716 503,33 | 4 570 | 9,140 |
| 16 | `Statement_Balance` | 82 467,305 | 387 442,010 | 304 974,705 | −374 994,753 | 844 904,068 | 4 591 | 9,182 |
| 17 | `Payment_Amount` | 55 193,18 | 299 100,96 | 243 907,77 | −310 668,47 | 664 962,61 | 4 535 | 9,070 |
| 18 | `Payment_Ratio` | 0,62 | 0,96 | 0,34 | 0,11 | 1,47 | 87 | 0,174 |
| 19 | `Credit_Utilization` | 0,27 | 0,56 | 0,29 | −0,165 | 0,995 | 0 | 0,000 |
| 20 | `Cash_Advance_Amount` | 0 | 8 692,19 | 8 692,19 | −13 038,285 | 21 730,475 | 9 549 | 19,098 |
| 21 | `EMI_Count` | 1 | 4 | 3 | −3,5 | 8,5 | 0 | 0,000 |
| 22 | `International_Transactions` | 0 | 2 | 2 | −3 | 5 | 4 769 | 9,538 |
| 23 | `Reward_Points_Earned` | 720 | 3 767 | 3 047 | −3 850,5 | 8 337,5 | 4 930 | 9,860 |
| 24 | `Reward_Points_Redeemed` | 0 | 731 | 731 | −1 096,5 | 1 827,5 | 5 708 | 11,416 |
| 25 | `Mobile_App_Login` | 20 | 44 | 24 | −16 | 80 | 0 | 0,000 |
| 26 | `Credit_Score` | 585 | 681 | 96 | 441 | 825 | 394 | 0,788 |

A continuación, la lectura específica de cada variable, en el mismo orden que en los Módulos 3 y 4.

#### 5.3.1 `Age`

- **Resultado:** $Q_1 = 27$, $Q_3 = 44$, $RIC = 17$ años; límites 1,5 y **69,5** años; **278 atípicos (0,556 %)**.
- **Lectura:** con un $RIC$ de 17 años (de 27 a 44), el límite superior cae en 69,5 años: apenas 278 clientes (0,56 %) superan esa edad, **todos en la cola derecha**, ya anticipada por la asimetría leve (**0,69**). Es de las variables con **menos atípicos univariados** del dataset, coherente con ser una cartera de adultos **sin valores extremos de edad**. El límite inferior (1,5 años) es irrelevante en la práctica.
- **Negocio:** la edad no requiere depuración; los mayores de 69,5 años son un segmento real (pocos clientes senior), no errores.

#### 5.3.2 `Annual_Income`

- **Resultado:** $Q_1 = 657.770,5$ ₹, $Q_3 = 1.663.677$ ₹, $RIC = 1.005.906,5$ ₹; límites **−851.089,25** y **3.172.536,75** ₹; **4.037 atípicos (8,074 %)**.
- **Lectura:** el límite inferior es **negativo** porque el $RIC$ (1.005.907 ₹) ya es grande frente al propio $Q_1$ (657.771 ₹), así que **todos los 4.037 atípicos están en la cola superior**: son los **clientes de ingresos altos, no errores de captura**, como se discute en la sección 5.4 sobre el porqué de tantos atípicos.
- **Negocio:** el 8 % de clientes con ingreso anual superior a ~3,17 millones de rupias es un segmento *premium* legítimo, no ruido.

#### 5.3.3 `Credit_Limit`

- **Resultado:** $Q_1 = 157.000$ ₹, $Q_3 = 779.000$ ₹, $RIC = 622.000$ ₹; límites **−776.000** y **1.712.000** ₹; **4.173 atípicos (8,346 %)**.
- **Lectura:** patrón **casi idéntico** al de `Annual_Income` (límite inferior negativo, todos los atípicos por arriba), consistente con que ambas variables están casi perfectamente ligadas ($r = 0{,}974$, Módulo 7). La caja se ve visualmente **aplastada contra la izquierda** porque la mediana (**396.000 ₹**) está mucho más cerca del mínimo (**16.000 ₹**) que del bigote superior (**1.712.000 ₹**).
- **Negocio:** los cupos altos atípicos son el reflejo directo de los ingresos altos (la política de cupo depende del ingreso).

#### 5.3.4 `Card_Age_Months`

- **Resultado:** $Q_1 = 31$, $Q_3 = 70$, $RIC = 39$ meses; límites −27,5 y **128,5** meses; **1.287 atípicos (2,574 %)**.
- **Lectura:** queda en un **punto intermedio** entre las variables muy asimétricas de dinero (8–19 % de atípicos) y las prácticamente simétricas (0–1 %), coherente con una **asimetría moderada (1,14)**: hay más tarjetas nuevas que antiguas, pero la cola hacia los **240 meses** no es tan extrema como la del gasto o los saldos.
- **Negocio:** las tarjetas con más de ~10,7 años de antigüedad son clientes muy leales, no anomalías.

#### 5.3.5 `Monthly_Spending`

Ya presentada como caso de estudio al comienzo del módulo: **4.213 atípicos (8,43 %)**, todos en la cola derecha, con límite inferior negativo (**−57.933 ₹**). Se incluye en la lista solo para que las 26 variables queden completas y en el mismo orden que en los Módulos 3 y 4.

#### 5.3.6 `Monthly_Transactions`

- **Resultado:** $Q_1 = 49$, $Q_3 = 108$, $RIC = 59$; límites −39,5 y **196,5**; **0 atípicos (0 %)**.
- **Lectura:** **cero atípicos**. El límite superior (196,5) queda **por encima del máximo real (179)**: la variable está **acotada** por lo que una persona alcanza a hacer en un mes, así que la regla de Tukey nunca llega a activarse; la caja se ve **simétrica y sin puntos sueltos**.
- **Negocio:** la frecuencia de uso es homogénea; no hay clientes con un número anómalo de transacciones (lo que también sugiere que no hay patrones de fraude masivo por volumen en esta variable).

#### 5.3.7 `Avg_Transaction_Value`

- **Resultado:** $Q_1 = 448,37$ ₹, $Q_3 = 901,27$ ₹, $RIC = 452,90$ ₹; límites −230,98 y **1.580,62** ₹; **4.286 atípicos (8,572 %)**.
- **Lectura:** 8,57 % de atípicos, con un máximo (**10.460 ₹**) que llega a casi **6,6 veces el límite superior** (1.581 ₹). Al ser un **cociente** entre una variable sesgada (`Monthly_Spending`) y una acotada (`Monthly_Transactions`), la caja **concentra toda la asimetría del numerador** sin la protección que el denominador acotado le da a otras variables.
- **Negocio:** los tickets promedio muy altos corresponden a clientes que hacen pocas compras pero grandes; es un perfil, no un error.

#### 5.3.8 `Online_Shopping_Spending`

- **Resultado:** $Q_1 = 2.800,675$, $Q_3 = 12.820,420$, $RIC = 10.019,745$ ₹; límites **−12.228,942** y **27.850,037** ₹; **4.045 atípicos (8,090 %)**.
- **Lectura:** 8,09 % de atípicos y un límite inferior **negativo** (−12.230 ₹), **típico de las categorías de gasto**: la caja queda comprimida entre 0 ₹ y 27.850 ₹, con el 8 % restante disperso en una cola que llega hasta **258.200 ₹**, casi **20 veces el bigote superior**.

#### 5.3.9 `Grocery_Spending`

- **Resultado:** $Q_1 = 5.176,815$, $Q_3 = 20.419,725$, $RIC = 15.242,910$ ₹; límites −17.687,550 y **43.284,090** ₹; **4.032 atípicos (8,064 %)**.
- **Lectura:** 8,06 % de atípicos, **el porcentaje más bajo entre las siete categorías de gasto**, consistente con tener la **mediana más alta del grupo (10.650 ₹)**: al ser un gasto que casi todos hacen de forma recurrente, la caja central es proporcionalmente más ancha que en categorías más discrecionales como `Travel_Spending`.
- **Negocio:** el mercado es gasto de primera necesidad, el más "estable" del portafolio de consumo.

#### 5.3.10 `Fuel_Spending`

- **Resultado:** $Q_1 = 2.432,140$, $Q_3 = 11.560,985$, $RIC = 9.128,845$ ₹; límites −11.261,128 y **25.254,253** ₹; **4.176 atípicos (8,352 %)**.
- **Lectura:** 8,35 % de atípicos (4.176 clientes) por encima de **25.250 ₹**: el grupo que **sí tiene vehículo y se desplaza mucho**, frente a la mayoría con gasto bajo (mediana **5.466 ₹**) que compone la caja compacta.

#### 5.3.11 `Dining_Spending`

- **Resultado:** $Q_1 = 2.089,505$, $Q_3 = 10.381,865$, $RIC = 8.292,360$ ₹; límites −10.349,035 y **22.820,405** ₹; **4.202 atípicos (8,404 %)**.
- **Lectura:** 8,40 % de atípicos, prácticamente el mismo porcentaje que `Online_Shopping_Spending` (8,09 %) y `Grocery_Spending` (8,06 %): las tres categorías de **gasto discrecional moderado** comparten no solo la forma de su distribución, sino **la proporción exacta de clientes que su cola derecha empuja fuera de los bigotes**.

#### 5.3.12 `Travel_Spending`

- **Resultado:** $Q_1 = 1.076,960$, $Q_3 = 6.862,885$, $RIC = 5.785,925$ ₹; límites −7.601,928 y **15.541,773** ₹; **4.315 atípicos (8,630 %)**.
- **Lectura:** 8,63 % de atípicos, **el porcentaje más alto de las siete categorías de gasto**, coherente con ser también la de **mayor asimetría (5,71)** y **mayor $Z$-máximo (19,4 $\sigma$, Módulo 6)**. El bigote superior (**15.540 ₹**) es más de **14 veces la mediana (2.883 ₹)**: la mayoría casi no viaja, y quienes sí lo hacen gastan **órdenes de magnitud más**.
- **Negocio:** el gasto en viajes identifica a un segmento minoritario de alto consumo esporádico (candidato a productos de viaje, seguros, millas).

#### 5.3.13 `Entertainment_Spending`

- **Resultado:** $Q_1 = 1.570,085$, $Q_3 = 8.612,840$, $RIC = 7.042,755$ ₹; límites −8.994,048 y **19.176,972** ₹; **4.276 atípicos (8,552 %)**.
- **Lectura:** 8,55 % de atípicos, **el segundo porcentaje más alto** después de `Travel_Spending`, consistente con ser también la **segunda variable con mayor asimetría (5,01)** entre las categorías de gasto. Gasto **discrecional y ocasional**: la mayoría se concentra por debajo de **8.613 ₹ ($Q_3$)** y la minoría que consume ocio de forma intensiva forma la cola marcada.

#### 5.3.14 `Utility_Bill_Spending`

- **Resultado:** $Q_1 = 2.978,380$, $Q_3 = 13.510,045$, $RIC = 10.531,665$ ₹; límites −12.819,118 y **29.307,543** ₹; **4.056 atípicos (8,112 %)**.
- **Lectura:** 8,11 % de atípicos. Domiciliar servicios en la tarjeta es **frecuente pero de monto acotado**, así que, aunque la proporción de atípicos es similar a las demás categorías, su **asimetría (4,35) es la más baja de las siete**: la cola existe, pero es relativamente **la menos extrema** del grupo de gastos.

#### 5.3.15 `Outstanding_Balance`

- **Resultado:** $Q_1 = 55.640,71$, $Q_3 = 319.985,76$, $RIC = 264.345,05$ ₹; límites −340.876,85 y **716.503,33** ₹; **4.570 atípicos (9,14 %)**.
- **Lectura:** 9,14 % de atípicos, **ya por encima del bloque de categorías de gasto individual (8–8,6 %)**: el saldo pendiente **acumula la variabilidad de siete gastos más el historial de pagos**, así que su cola es proporcionalmente más pesada. Comparte prácticamente el mismo patrón con `Statement_Balance` (9,18 %).
- **Negocio:** los saldos pendientes extremos son la exposición de mayor interés para Riesgo; aquí se ve que son un 9 % "estructural" de la cartera, no casos aislados.

#### 5.3.16 `Statement_Balance`

- **Resultado:** $Q_1 = 82.467,305$, $Q_3 = 387.442,010$, $RIC = 304.974,705$ ₹; límites −374.994,753 y **844.904,068** ₹; **4.591 atípicos (9,182 %)**.
- **Lectura:** 9,18 % de atípicos, **el más alto de las tres variables de saldo/pago** (`Outstanding_Balance`, `Statement_Balance`, `Payment_Amount`). La diferencia mínima entre las tres (**9,14 % vs. 9,18 % vs. 9,07 %**) confirma, en el conteo de atípicos, **la misma redundancia** que ya mostró su correlación de **0,997** con `Outstanding_Balance`.

#### 5.3.17 `Payment_Amount`

- **Resultado:** $Q_1 = 55.193,18$, $Q_3 = 299.100,96$, $RIC = 243.907,77$ ₹; límites −310.668,47 y **664.962,61** ₹; **4.535 atípicos (9,07 %)**.
- **Lectura:** 9,07 % de atípicos. El monto pagado es **proporcional a lo facturado**, así que su porcentaje de atípicos cae, como se esperaba, entre el de `Statement_Balance` (9,18 %) y el de las categorías de gasto individual: ni tan comprimido como éstas, ni tan extremo como el saldo del que depende directamente.

#### 5.3.18 `Payment_Ratio`

- **Resultado:** $Q_1 = 0,62$, $Q_3 = 0,96$, $RIC = 0,34$; límites **0,11** y **1,47**; **87 atípicos (0,174 %)**.
- **Lectura:** el límite superior da **1,47**, por encima del **máximo teórico posible (1,0)**, así que **ningún cliente puede quedar marcado por arriba**; los 87 atípicos (0,17 %) están **todos en la cola inferior**: los **pagadores parciales** que se alejan del grueso que paga cerca del 100 % de su saldo (mediana **0,84**).
- **Negocio:** este es uno de los pocos casos en los que el atípico univariado tiene lectura directa de riesgo: los 87 clientes que pagan menos del 11 % de lo que deben son una lista corta y accionable para seguimiento.

#### 5.3.19 `Credit_Utilization`

- **Resultado:** $Q_1 = 0,27$, $Q_3 = 0,56$, $RIC = 0,29$; límites **−0,165** y **0,995**; **0 atípicos**.
- **Lectura:** **cero atípicos**. El límite inferior (−0,165) es negativo y el superior (0,995) queda por encima del **máximo real (0,95)**: la variable, **acotada por las políticas de cupo del banco**, nunca se acerca a sus propios límites de Tukey.

#### 5.3.20 `Cash_Advance_Amount`

- **Resultado:** $Q_1 = 0$, $Q_3 = 8.692,19$, $RIC = 8.692,19$ ₹; límites −13.038,285 y **21.730,475** ₹; **9.549 atípicos (19,098 %)**.
- **Lectura:** **el porcentaje de atípicos más alto de todo el dataset: 19,10 % (9.549 clientes)**. Con $Q_1 = 0$ (el **70,3 %** de los clientes nunca hace avances), el $RIC$ se calcula casi enteramente sobre la minoría que sí los usa, y eso hace que el límite superior (21.730 ₹) sea **muy bajo en relación con el máximo real (1.212.849 ₹)**. Una **masa puntual en cero** exagera, mecánicamente, el conteo de atípicos de Tukey en el resto de la variable.
- **Negocio:** los avances en efectivo son tradicionalmente una señal de estrés financiero; pero el 19 % "atípico" es un artefacto de la masa en cero, no una alarma por sí mismo. Para esta variable conviene separar "usa / no usa avances" de "cuánto usa".

#### 5.3.21 `EMI_Count`

- **Resultado:** $Q_1 = 1$, $Q_3 = 4$, $RIC = 3$; límites −3,5 y **8,5**; **0 atípicos**.
- **Lectura:** **cero atípicos**. Con solo **7 valores posibles (0 a 6)**, el límite superior (8,5) queda muy por encima del máximo real: un conteo discreto de rango tan corto **no le da a la regla de Tukey ningún margen para activarse**.

#### 5.3.22 `International_Transactions`

- **Resultado:** $Q_1 = 0$, $Q_3 = 2$, $RIC = 2$; límites −3 y **5**; **4.769 atípicos (9,538 %)**.
- **Lectura:** 9,54 % de atípicos, **muy distinto de `EMI_Count` a pesar de ser también un conteo de rango corto**: aquí $Q_1 = 0$ (el **59,3 %** nunca compra en el exterior) y $Q_3 = 2$, así que el límite superior (5) **sí queda dentro del rango real (hasta 14)**, y toda la minoría que compra más de 5 veces en el exterior queda marcada.

#### 5.3.23 `Reward_Points_Earned`

- **Resultado:** $Q_1 = 720$, $Q_3 = 3.767$, $RIC = 3.047$ puntos; límites −3.850,5 y **8.337,5**; **4.930 atípicos (9,86 %)**.
- **Lectura:** 9,86 % de atípicos, que el informe describe como "muy cercano" al 8,43 % de `Monthly_Spending`, la variable de la que se deriva directamente ($r = 0{,}980$). Al ser una **función del gasto**, hereda casi la misma proporción de clientes que su cola derecha empuja fuera de los bigotes.

#### 5.3.24 `Reward_Points_Redeemed`

- **Resultado:** $Q_1 = 0$, $Q_3 = 731$, $RIC = 731$; límites −1.096,5 y **1.827,5**; **5.708 atípicos (11,416 %)**.
- **Lectura:** 11,42 % de atípicos, **el segundo porcentaje más alto del dataset** después de `Cash_Advance_Amount`, por el **mismo mecanismo**: $Q_1 = 0$ (**39,9 %** nunca redime puntos) comprime el $RIC$ y hace que el límite superior (1.827,5) sea bajo frente al máximo real (**44.820**).

#### 5.3.25 `Mobile_App_Login`

- **Resultado:** $Q_1 = 20$, $Q_3 = 44$, $RIC = 24$; límites −16 y **80**; **0 atípicos**.
- **Lectura:** **cero atípicos**, igual que `Monthly_Transactions`, `EMI_Count` y `Credit_Utilization`: un hábito de consulta razonablemente **uniforme** entre clientes (rango de **2 a 71 sesiones**) que no genera ninguna cola lo bastante larga para activar la regla de Tukey.

#### 5.3.26 `Credit_Score`

- **Resultado:** $Q_1 = 585$, $Q_3 = 681$, $RIC = 96$; límites **441** y **825**; **394 atípicos (0,788 %)**.
- **Lectura:** 0,79 % de atípicos (394 clientes) y, **a diferencia de todas las variables de dinero, esos atípicos están en la cola inferior** (límite inferior 441, superior 825): son **los perfiles de mayor riesgo**, consistentes con la **asimetría negativa (−0,58)** documentada en el Módulo 3.
- **Negocio:** es el segundo caso (junto con `Payment_Ratio`) en que el atípico univariado coincide directamente con un cliente de alto riesgo: 394 clientes con puntaje inferior a 441.

---

### 5.4 ¿Por qué hay tantos "atípicos" en los boxplots?

#### Aplicación

El conteo de `Monthly_Spending` (8,43 %) no es una excepción rara. Para verlo de conjunto se calcula el porcentaje de atípicos de Tukey de las 26 variables numéricas con un solo `sapply()` y se ordena de mayor a menor:

```r
numeric_cols <- names(credit)[sapply(credit, is.numeric)]
pct_atipicos_todas <- sapply(numeric_cols, function(v) {
  x <- credit[[v]]
  f <- fivenum(x); ric <- f[4] - f[2]
  li <- f[2] - 1.5 * ric; ls <- f[4] + 1.5 * ric
  100 * sum(x < li | x > ls) / length(x)
})
round(sort(pct_atipicos_todas, decreasing = TRUE), 2)
```

#### Resultado (ranking)

| Puesto | Variable | % atípicos | | Puesto | Variable | % atípicos |
|---:|---|---:|---|---:|---|---:|
| 1 | `Cash_Advance_Amount` | 19,10 | | 14 | `Credit_Limit` | 8,35 |
| 2 | `Reward_Points_Redeemed` | 11,42 | | 15 | `Utility_Bill_Spending` | 8,11 |
| 3 | `Reward_Points_Earned` | 9,86 | | 16 | `Online_Shopping_Spending` | 8,09 |
| 4 | `International_Transactions` | 9,54 | | 17 | `Annual_Income` | 8,07 |
| 5 | `Statement_Balance` | 9,18 | | 18 | `Grocery_Spending` | 8,06 |
| 6 | `Outstanding_Balance` | 9,14 | | 19 | `Card_Age_Months` | 2,57 |
| 7 | `Payment_Amount` | 9,07 | | 20 | `Credit_Score` | 0,79 |
| 8 | `Travel_Spending` | 8,63 | | 21 | `Age` | 0,56 |
| 9 | `Avg_Transaction_Value` | 8,57 | | 22 | `Payment_Ratio` | 0,17 |
| 10 | `Entertainment_Spending` | 8,55 | | 23 | `Monthly_Transactions` | 0,00 |
| 11 | `Monthly_Spending` | 8,43 | | 24 | `Credit_Utilization` | 0,00 |
| 12 | `Dining_Spending` | 8,40 | | 25 | `EMI_Count` | 0,00 |
| 13 | `Fuel_Spending` | 8,35 | | 26 | `Mobile_App_Login` | 0,00 |

#### Lectura: dos grupos nítidos

1. **Grupo de cola larga (8 %–19 % de atípicos):** encabezado por `Cash_Advance_Amount` (19,1 %) y `Reward_Points_Redeemed` (11,4 %); incluye prácticamente todas las variables de **gasto, saldo y conteo con cola derecha larga** (18 variables).
2. **Grupo simétrico o acotado (< 3 %):** `Age`, `Credit_Score`, `Card_Age_Months`, `Payment_Ratio`, `Credit_Utilization`, `Monthly_Transactions`, `EMI_Count` y `Mobile_App_Login`; cuatro de ellas (`Credit_Utilization`, `Monthly_Transactions`, `EMI_Count`, `Mobile_App_Login`) tienen **exactamente cero**.

#### Explicación (causa)

**La causa no es un error de captura en ninguno de los dos grupos.** La regla de Tukey ($Q_3 + 1{,}5 \cdot RIC$) se calibró para distribuciones **aproximadamente simétricas**, y su tasa nominal de "falsos positivos" (**cerca de 0,7 % bajo normalidad**) solo se cumple cuando esa condición se satisface.

- **Primer grupo — fuertemente asimétrico a la derecha** (ver Módulo 1): en una variable así, el $RIC$ (calculado sobre el 50 % central, que vive en la parte "apretada" de la distribución) es **pequeño en relación con lo larga que es la cola derecha real**. El límite superior termina cayendo **dentro de esa cola, no en su punta**, y por eso marca como "atípico" a una **fracción grande y genuina de la población**, no a errores.
- **Segundo grupo — simétrico o acotado por construcción:** `Credit_Utilization` y `Payment_Ratio` viven en $[0,1]$ por definición; `EMI_Count` y `Monthly_Transactions` son conteos con rango corto y sin cola; `Age` y `Mobile_App_Login` son razonablemente simétricas. En estos casos la cola simplemente **no existe**, así que la regla de Tukey no tiene nada que marcar.

#### Decisión: no eliminar los atípicos

**Conclusión práctica:** un porcentaje alto de "atípicos" en una variable de gasto **no es, por sí solo, evidencia de errores de captura**: es la **firma esperable de la asimetría** de esa variable, ya identificada en el diccionario del Módulo 1. Antes de tratar esas observaciones como errores (o de eliminarlas), habría que:

- **transformar la variable** (por ejemplo, con un logaritmo), o
- usar una **regla de atípicos que sí tenga en cuenta la asimetría**.

Por eso **no se borra ningún cliente** en este módulo. Borrar el 8–19 % de la cartera eliminaría precisamente a los clientes de mayor ingreso, gasto y saldo —el segmento más relevante en exposición— y sesgaría todo análisis posterior.

**Significado para el negocio:** si la Gerencia de Riesgo aplicara un filtro automático de Tukey para "limpiar" la base, perdería casi uno de cada diez clientes en cada variable monetaria —y en `Cash_Advance_Amount`, uno de cada cinco—, justamente los de mayor exposición. Los únicos atípicos univariados con lectura directa de riesgo están en las variables de comportamiento: la cola **inferior** de `Credit_Score` (394 clientes) y de `Payment_Ratio` (87 clientes).

---

### 5.5 Conclusión del Módulo 5

1. `Monthly_Spending`, elegida deliberadamente por su asimetría (a diferencia de `Credit_Score` en el Módulo 3), tiene **4.213 observaciones (8,43 %)** fuera de los límites de Tukey —**no errores, sino la cola derecha real del gasto**.
2. La misma regla, aplicada a las 26 variables numéricas, separa con nitidez **dos grupos**: variables de gasto/saldo con cola larga (**8 % a 19 %** de atípicos) y variables simétricas o acotadas por construcción (**0 % a 3 %**).
3. Un porcentaje alto de atípicos univariados es **diagnóstico de asimetría, no necesariamente de error**: la decisión correcta depende de la naturaleza de cada variable, documentada ya en el diccionario del Módulo 1.

---

## Módulo 6: Comparación Multivariada Estandarizada mediante Boxplots (S03)

### Motivación: el problema de las escalas

Los Módulos 3 a 5 miraron **una variable a la vez**. El siguiente paso natural en la taxonomía de S01 es **comparar varias variables en un solo gráfico**. Pero un boxplot compara posiciones en el eje vertical, y eso **solo tiene sentido si todas las variables están en la misma unidad**. Aquí no lo están: `Annual_Income` se mide en rupias (cientos de miles), `Card_Age_Months` en meses (decenas) y `Payment_Ratio` es una proporción entre 0 y 1. Antes de graficar nada, se cuantifica qué tan distintas son esas escalas.

#### Aplicación

```r
cols_num <- sapply(credit, is.numeric)
credit_num <- credit[, cols_num]
sds <- sort(sapply(credit_num, sd), decreasing = TRUE)
round(head(sds, 3), 1)
round(tail(sds, 3), 3)
```

#### Resultado

| Las 3 desviaciones estándar más grandes | $s_j$ | | Las 3 más pequeñas | $s_j$ |
|---|---:|---|---|---:|
| `Annual_Income` | 1 407 257,5 | | `EMI_Count` | 1,673 |
| `Credit_Limit` | 1 009 854,4 | | `Payment_Ratio` | 0,240 |
| `Statement_Balance` | 559 547,6 | | `Credit_Utilization` | 0,206 |

**Lectura:** la desviación estándar de `Annual_Income` es **1.407.257** y la de `Credit_Utilization` es **0,206**: una razón de **6.835.059 veces** entre la variable más dispersa y la menos dispersa. Graficar las 26 variables juntas en su escala original, con esa diferencia de magnitud, es **literalmente imposible de leer**, como muestra el primer panel del gráfico siguiente.

---

### 6.1 Qué hace la estandarización, y por qué

#### Concepto: el $Z$-score

La estandarización convierte cada valor en **su número de desviaciones estándar respecto a la media de su propia variable**:

$$
z_{ij} = \frac{x_{ij} - \bar x_j}{s_j}, \qquad \bar x_j = \frac{1}{n}\sum_{i=1}^n x_{ij}, \qquad s_j = \sqrt{\frac{1}{n-1}\sum_{i=1}^n (x_{ij}-\bar x_j)^2}.
$$

Propiedades:

- Toda variable estandarizada tiene **media 0 y desviación estándar 1**, sin importar su unidad o escala original: un peso (rupia), un mes o una proporción se convierten los tres en "cuántas desviaciones estándar por encima o por debajo de lo típico **en esa misma variable**".
- **No cambia la forma de la distribución**: es una transformación lineal (resta una constante y divide por otra), así que una variable sesgada **sigue sesgada** después de estandarizar, y su asimetría y curtosis no se alteran. Solo cambia la escala, para que todas "hablen el mismo idioma" y se puedan comparar en un solo eje.
- Es **exactamente la misma decisión** que separa un PCA sobre la matriz de covarianzas $\mathbf{S}$ de uno sobre la matriz de correlaciones $\mathbf{R}$: la matriz de covarianzas de los datos estandarizados es $\mathbf{R}$.

En forma matricial, con $\mathbf{D} = \operatorname{diag}(s_1,\dots,s_p)$: $\mathbf{Z} = (\mathbf{X} - \mathbf{1}\bar{\mathbf{x}}^\top)\,\mathbf{D}^{-1}$.

#### Decisión: usar las 26 variables, no un subconjunto

Se aplican ambas versiones —sin estandarizar y estandarizada— sobre **las 26 variables numéricas**, no sobre un subconjunto: el objetivo de este módulo es precisamente comparar **toda la matriz de una vez**, y una selección parcial escondería justo las variables más pequeñas que la estandarización viene a rescatar.

#### Aplicación

```r
par(mfrow = c(1, 2), mar = c(8, 4, 3, 1))

# 1. Sin estandarizar
boxplot(credit_num, las = 2, col = "lightgray", cex.axis = 0.7,
        main = "Sin Estandarizar (26 variables, escalas dispares)",
        ylab = "Valor Original")

# 2. Estandarizado (Z-scores: media 0, varianza 1)
credit_scale <- scale(credit_num)
boxplot(credit_scale, las = 2, col = "thistle", cex.axis = 0.7,
        main = "Estandarizado con scale() (26 variables)",
        ylab = "Desviaciones Estándar (Z)")
abline(h = 0, col = "blue", lty = 3)
abline(h = c(-3, 3), col = "red", lty = 2)
par(mfrow = c(1, 1))
```

Figura de 14×7 pulgadas con dos paneles lado a lado; nombres de variables rotados (`las = 2`). En el panel estandarizado se añaden una línea azul punteada en $z = 0$ (la media) y dos líneas rojas discontinuas en $z = \pm 3$ (referencia clásica de "3 sigmas").

#### Resultado (lo que muestra el gráfico)

- **Panel izquierdo (sin estandarizar):** **24 de las 26 cajas se ven como una línea plana pegada al cero**, no porque no varíen, sino porque `Annual_Income` y `Credit_Limit`, con desviaciones del orden de los cientos de miles, estiran el eje vertical hasta que todo lo demás queda invisible.
- **Panel derecho (tras `scale()`):** las 26 variables comparten el mismo eje (desviaciones estándar) y **por primera vez se pueden comparar simultáneamente su dispersión y la longitud relativa de sus colas**.

Es el mismo fenómeno que la sesión de clase mostró con las 11 variables del dataset de vinos, aquí con una diferencia de escala todavía mayor ($10^6$ contra $10^{-1}$).

---

### 6.2 Diagnóstico de colas máximas ($Z$-score máximo)

#### Concepto

Para cada variable se calcula $Z_{\max,j} = \max_i z_{ij} = (\max_i x_{ij} - \bar x_j)/s_j$: a cuántas desviaciones estándar de su propia media está su valor más alto. Bajo normalidad, con $n = 50\,000$, el máximo esperado ronda las 4 desviaciones; valores muy superiores indican colas pesadas.

#### Aplicación

```r
z_max <- apply(credit_scale, 2, max)
round(sort(z_max, decreasing = TRUE), 2)
top_zmax <- names(sort(z_max, decreasing = TRUE))[1]   # bloque oculto (echo = FALSE)
```

#### Resultado

| Puesto | Variable | $Z_{\max}$ | | Puesto | Variable | $Z_{\max}$ |
|---:|---|---:|---|---:|---|---:|
| 1 | `Travel_Spending` | 19,37 | | 14 | `Reward_Points_Earned` | 8,14 |
| 2 | `Reward_Points_Redeemed` | 18,65 | | 15 | `Monthly_Spending` | 7,33 |
| 3 | `Utility_Bill_Spending` | 17,14 | | 16 | `Card_Age_Months` | 5,97 |
| 4 | `Entertainment_Spending` | 16,93 | | 17 | `Credit_Limit` | 5,82 |
| 5 | `Dining_Spending` | 15,92 | | 18 | `International_Transactions` | 4,80 |
| 6 | `Cash_Advance_Amount` | 15,26 | | 19 | `Annual_Income` | 4,63 |
| 7 | `Online_Shopping_Spending` | 14,88 | | 20 | `Age` | 2,77 |
| 8 | `Fuel_Spending` | 14,53 | | 21 | `Credit_Utilization` | 2,54 |
| 9 | `Grocery_Spending` | 14,14 | | 22 | `Credit_Score` | 2,38 |
| 10 | `Payment_Amount` | 12,57 | | 23 | `Monthly_Transactions` | 2,28 |
| 11 | `Avg_Transaction_Value` | 12,35 | | 24 | `Mobile_App_Login` | 2,25 |
| 12 | `Outstanding_Balance` | 10,98 | | 25 | `EMI_Count` | 2,12 |
| 13 | `Statement_Balance` | 10,25 | | 26 | `Payment_Ratio` | 0,99 |

**Lectura:** `Travel_Spending` tiene el máximo más extremo en unidades de desviación estándar (**19,4 $\sigma$** por encima de su media), consistente con lo ya anotado en el diccionario del Módulo 1: *"Es el gasto más esporádico de todos (la mediana es la más baja de las categorías): la mayoría viaja poco o nada en el mes, y los pocos que viajan lo hacen con montos grandes, lo que produce la cola más larga del grupo"*. En el otro extremo, variables como `Mobile_App_Login`, `Monthly_Transactions` o `Credit_Utilization` tienen su máximo apenas a **2–3 $\sigma$**, la marca de una variable **acotada y sin cola** (`Payment_Ratio`, con 0,99, ni siquiera llega a 1 $\sigma$ por encima de su media, porque su masa está pegada al techo de 1,0).

Este ranking **coincide**, en unidades comparables, con el mismo grupo de variables de cola larga que el Módulo 5 identificó con el conteo de atípicos de Tukey; aquí se ve de un solo vistazo sobre las 26 a la vez, en vez de variable por variable.

**Matiz:** el orden interno no es idéntico al del Módulo 5 (por ejemplo, `Utility_Bill_Spending` es 3.ª en $Z_{\max}$ pese a tener la menor asimetría de las categorías de gasto; `Monthly_Spending` y `Annual_Income` tienen $Z_{\max}$ relativamente moderados, 7,33 y 4,63), porque el $Z_{\max}$ depende de **un solo dato extremo** mientras que el porcentaje de Tukey depende del **grosor** de toda la cola. Ambos coinciden, sin embargo, en qué grupo de variables tiene cola larga.

**Negocio:** sin mirar 26 gráficos, el banco sabe qué variables necesitan transformación (log) o técnicas robustas antes de entrar a cualquier modelo de riesgo, y que las variables de comportamiento (utilización, ratio de pago, puntaje) son "bien portadas".

---

### 6.3 Conclusión del Módulo 6

1. Las 26 variables numéricas de la cartera difieren en desviación estándar por un factor de **6.835.059**, lo que vuelve **inútil** un boxplot conjunto sin estandarizar.
2. La estandarización $z = (x-\bar x)/s$ **no cambia la forma** de cada variable, solo su escala: después de aplicarla, las 26 comparten un mismo eje (desviaciones estándar) y se pueden comparar de verdad.
3. El ranking de $Z$-máximo identifica, sin necesidad de mirar 26 gráficos por separado, cuáles variables tienen la cola derecha más extrema, y **coincide con el mismo grupo** que el Módulo 5 había señalado por su alto porcentaje de atípicos de Tukey: **dos rutas distintas** (conteo de atípicos, cola en desviaciones estándar) que llegan a la misma conclusión sobre las mismas variables.

---

## Módulo 7: Análisis Bivariado, Correlación y el "Punto Imposible" (S01 & S03 & S04)

### 7.1 Selección objetiva de las variables para el análisis bivariado

#### Problema

Con la matriz ya estandarizada y comparada como conjunto en el Módulo 6, toca bajar un nivel: **mirar pares de variables**. Con $p = 26$ variables numéricas hay

$$
\binom{26}{2} = \frac{26 \cdot 25}{2} = 325
$$

pares posibles, y si se suman las 4 cualitativas hay decenas de combinaciones numérica–categórica más. Mirarlos todos uno por uno **no es factible ni informativo** (S04: "por qué no basta con mirar todos los pares"). Hace falta un **criterio objetivo, no una elección a mano**, para decidir qué pares merecen un análisis bivariado profundo.

**Decisión:** usar **dos criterios distintos**, porque hay dos tipos de par en el dataset —numérica con numérica, y numérica con categórica— y cada uno necesita su propia medida de asociación.

#### 7.1.1 Criterio 1: correlación entre variables numéricas

##### Concepto: correlación de Pearson

$$
r_{jk} = \frac{\sum_{i=1}^n (x_{ij}-\bar x_j)(x_{ik}-\bar x_k)}{\sqrt{\sum_{i=1}^n (x_{ij}-\bar x_j)^2}\;\sqrt{\sum_{i=1}^n (x_{ik}-\bar x_k)^2}}, \qquad -1 \le r_{jk} \le 1.
$$

El criterio es el **valor absoluto** $|r|$: cuanto más alto, más fuerte la relación **lineal**, y más probable que sea una **redundancia contable** o un **mecanismo real de negocio**. Se ordenan los 325 pares y, **por separado**, se mira con qué se correlaciona específicamente `Credit_Score` —la variable de riesgo del dataset— porque **no es lo mismo "el par más correlacionado del dataset" que "lo que mejor explica el riesgo"**.

##### Aplicación

```r
R_completa <- cor(credit_num, use = "pairwise.complete.obs")
pares <- as.data.frame(as.table(R_completa))
names(pares) <- c("v1", "v2", "r")
pares <- pares[as.character(pares$v1) < as.character(pares$v2), ]   # cada par una sola vez
pares <- pares[order(-abs(pares$r)), ]
print(head(pares, 8), row.names = FALSE)

r_credit_score <- sort(R_completa[, "Credit_Score"], decreasing = TRUE)
r_credit_score <- r_credit_score[names(r_credit_score) != "Credit_Score"]
print(round(head(r_credit_score[order(-abs(r_credit_score))], 5), 3))
```

El truco `v1 < v2` (orden alfabético) se queda con el triángulo de la matriz, para no contar cada par dos veces ni la diagonal: así resultan exactamente **325 pares**.

##### Resultado: Top 8 pares por $|r|$ (de 325 posibles)

| v1 | v2 | $r$ |
|---|---|---:|
| `Outstanding_Balance` | `Statement_Balance` | 0,9970756 |
| `Monthly_Spending` | `Reward_Points_Earned` | 0,9796848 |
| `Annual_Income` | `Credit_Limit` | 0,9741659 |
| `Credit_Limit` | `Reward_Points_Earned` | 0,9581162 |
| `Annual_Income` | `Monthly_Spending` | 0,9450576 |
| `Credit_Limit` | `Monthly_Spending` | 0,9403474 |
| `Payment_Amount` | `Statement_Balance` | 0,9358754 |
| `Outstanding_Balance` | `Payment_Amount` | 0,9324401 |

##### Resultado: las 5 correlaciones más fuertes (en $|r|$) con `Credit_Score`

| Variable | $r$ con `Credit_Score` |
|---|---:|
| `Payment_Ratio` | **0,767** |
| `Credit_Utilization` | **−0,599** |
| `Outstanding_Balance` | −0,145 |
| `Statement_Balance` | −0,125 |
| `Card_Age_Months` | 0,052 |

##### Lectura y decisión

1. **El par numérico más fuerte que no es una redundancia contable es `Annual_Income` – `Credit_Limit` ($r = 0{,}974$).** Por encima de él solo aparecen pares como `Outstanding_Balance`–`Statement_Balance` o `Monthly_Spending`–`Reward_Points_Earned`, que son **casi la misma cantidad de dinero contada dos veces** (ya excluidos del análisis de dependencia lineal genuina en el Módulo 10). `Annual_Income` y `Credit_Limit`, en cambio, **sí son dos decisiones de negocio distintas** (lo que el cliente gana vs. lo que el banco le aprueba) que resultan casi perfectamente ligadas: por eso se les dedica el análisis bivariado completo, incluido el "punto imposible".
2. **Las variables que de verdad explican el riesgo (`Credit_Score`) no son las de dinero.** `Payment_Ratio` ($r = 0{,}767$) y `Credit_Utilization` ($r = -0{,}599$) son, **por un margen enorme**, las dos correlaciones más fuertes con `Credit_Score` de las 25 variables numéricas restantes; el texto original dice que "la siguiente más fuerte (`Card_Age_Months`) no llega ni a $r = 0{,}06$" (matiz: en rigor, por $|r|$ las siguientes son los saldos, `Outstanding_Balance` con $-0{,}145$ y `Statement_Balance` con $-0{,}125$, y `Card_Age_Months`, con 0,052, es la quinta; en cualquier caso todas son débiles frente a 0,767 y −0,599). Ingreso, cupo y gasto mensual —que dominan visualmente el dataset y encabezan el ranking de $|r|$— tienen correlaciones con el puntaje de **apenas 0,03, prácticamente ruido**. Por eso `Payment_Ratio` y `Credit_Utilization` son las variables bivariadas **prioritarias** frente a `Credit_Score`, y no `Annual_Income`, pese a ser la variable "más grande" del dataset.

#### 7.1.2 Criterio 2: asociación entre una variable numérica y una categórica

##### Concepto: $\eta^2$ (eta al cuadrado)

Entre una variable numérica y una categórica no existe $r$ de Pearson. El criterio análogo es $\eta^2$ de un **ANOVA de un factor**: qué proporción de la varianza de la variable numérica queda explicada por saber a qué grupo pertenece cada cliente. Con $G$ grupos de tamaños $n_g$, medias $\bar y_g$ y media global $\bar y$:

$$
\eta^2 = \frac{SC_{\text{entre}}}{SC_{\text{total}}} = \frac{\sum_{g=1}^{G} n_g\,(\bar y_g - \bar y)^2}{\sum_{i=1}^{n} (y_i - \bar y)^2}, \qquad SC_{\text{total}} = SC_{\text{entre}} + SC_{\text{dentro}}, \qquad 0 \le \eta^2 \le 1.
$$

Es, en escala de 0 a 1, **el mismo tipo de medida que $r^2$**, pero para cuando un lado no es numérico (de hecho, si la categórica tiene solo dos niveles codificados 0/1, $\eta^2 = r^2$).

##### Aplicación

```r
eta2 <- function(y, g) {
  s <- summary(aov(y ~ g))[[1]][["Sum Sq"]]   # SC entre y SC dentro (residual)
  s[1] / sum(s)
}
tabla_eta2 <- data.frame(
  Comparacion = c("Annual_Income ~ Occupation", "Annual_Income ~ Card_Type",
                  "Credit_Limit ~ Card_Type", "Credit_Score ~ Card_Type",
                  "Credit_Score ~ Occupation", "Annual_Income ~ Gender", "Credit_Score ~ Gender"),
  Eta2 = c(eta2(credit$Annual_Income, credit$Occupation), ...))
tabla_eta2$Eta2 <- round(tabla_eta2$Eta2, 4)
tabla_eta2[order(-tabla_eta2$Eta2), ]
```

##### Resultado (tabla ordenada, valores del HTML renderizado)

| Comparación | $\eta^2$ |
|---|---:|
| `Credit_Limit ~ Card_Type` | **0,7997** |
| `Annual_Income ~ Card_Type` | 0,6837 |
| `Annual_Income ~ Occupation` | **0,6367** |
| `Credit_Score ~ Card_Type` | 0,0023 |
| `Credit_Score ~ Occupation` | 0,0009 |
| `Annual_Income ~ Gender` | 0,0001 |
| `Credit_Score ~ Gender` | 0,0001 |

##### Lectura y decisión

3. **Entre las categóricas, `Occupation` explica el 63,7 % de la varianza de `Annual_Income`** (de **251.605 ₹** promedio en `Student` a **4.369.221 ₹** en `Business Owner`, seis niveles con medias muy separadas), mientras que **`Gender` explica menos del 0,01 %** de esa misma variable y del **0,01 %** de `Credit_Score`. **Por eso `Occupation` recibe un análisis de grupos (boxplot por categoría) y `Gender` no**: con una diferencia de ese tamaño, agrupar por género no aportaría nada que no se viera ya en la variable global.
4. **Dato que confirma la coherencia interna del dataset simulado:** tanto `Card_Type` como `Occupation` explican bien las variables de dinero (`Card_Type` explica el **80,0 %** de `Credit_Limit`) pero **casi nada de `Credit_Score`** (**0,23 %** y **0,09 %** respectivamente). Es la misma conclusión del punto 2 vista desde el lado categórico: **el riesgo crediticio en este dataset no depende de cuánto gana o gasta el cliente, sino de cómo paga.**

(Nota: aunque `Annual_Income ~ Card_Type`, con 0,684, supera numéricamente a `Annual_Income ~ Occupation`, el par numérica–categórica elegido es el de `Occupation`; el texto lo describe como "par numérica-categórica más fuerte". `Card_Type` se trata aparte en la Tendencia 4 y en la sección Anscombe, como variable **ordinal** ligada a la política de cupos.)

**Negocio:** el género no aporta información de riesgo ni de ingreso en esta cartera, lo cual además es deseable desde la perspectiva de equidad y cumplimiento regulatorio (no hay que segmentar por género para nada).

#### 7.1.3 Selección final

Con los dos criterios ya aplicados, el resto del módulo se dedica **exclusivamente** a los pares señalados, y a ningún otro:

| Par | Criterio | Valor | Por qué se analiza |
|---|---|---:|---|
| `Annual_Income` – `Credit_Limit` | $\lvert r \rvert$ | 0,974 | par numérico más fuerte no redundante |
| `Payment_Ratio` – `Credit_Score` | $\lvert r \rvert$ | 0,767 | predictor #1 del riesgo |
| `Credit_Utilization` – `Credit_Score` | $\lvert r \rvert$ | −0,599 | predictor #2 del riesgo |
| `Annual_Income` – `Occupation` | $\eta^2$ | 0,637 | par numérica–categórica más fuerte |

---

### 7.2 Correlación bivariada y dispersión

#### Aplicación

Se empieza por la relación entre el Ratio de Pago (`Payment_Ratio`) y el Puntaje Crediticio (`Credit_Score`), y luego se construye una tabla de correlación de las cinco variables de interés:

```r
r_pr_cs <- cor(credit$Payment_Ratio, credit$Credit_Score)   # 0.7671463

# Solo variables numéricas: Occupation es nominal, y numerar sus niveles
# (1 = Business Owner, 2 = Government Employee, ...) daría una correlación
# que cambia con el orden alfabético. Para ella ya se usó eta^2.
variables_interes <- credit[, c("Annual_Income", "Credit_Limit", "Payment_Ratio",
                                "Credit_Score", "Credit_Utilization")]
tabla_correlacion <- round(cor(variables_interes), 2)
```

**Decisión:** `Occupation` se excluye de la tabla de Pearson porque es **nominal**: asignarle códigos 1, 2, 3… produciría una correlación que **cambia con el orden alfabético** de las categorías, es decir, un número sin significado. Para ella se usa $\eta^2$.

#### Resultado

$r(\texttt{Payment\_Ratio}, \texttt{Credit\_Score}) = 0{,}7671463$.

| | `Annual_Income` | `Credit_Limit` | `Payment_Ratio` | `Credit_Score` | `Credit_Utilization` |
|---|---:|---:|---:|---:|---:|
| `Annual_Income` | 1,00 | 0,97 | 0,00 | 0,03 | 0,00 |
| `Credit_Limit` | 0,97 | 1,00 | 0,00 | 0,04 | 0,00 |
| `Payment_Ratio` | 0,00 | 0,00 | 1,00 | 0,77 | 0,00 |
| `Credit_Score` | 0,03 | 0,04 | 0,77 | 1,00 | −0,60 |
| `Credit_Utilization` | 0,00 | 0,00 | 0,00 | −0,60 | 1,00 |

**Lectura:** el límite de crédito está determinado **casi exclusivamente por el ingreso** del cliente ($r = 0{,}97$). Sin embargo, un buen puntaje crediticio depende del **comportamiento financiero**: pagar altos porcentajes de la deuda ($r = 0{,}77$) y mantener una baja utilización de la tarjeta ($r = -0{,}60$). **El nivel de ingresos por sí solo no garantiza un buen score ($r = 0{,}03$).** Además, `Payment_Ratio` y `Credit_Utilization` son prácticamente incorrelacionadas entre sí (0,00) y con ingreso/cupo: son dos dimensiones de comportamiento independientes del tamaño del cliente.

---

### 7.3 Covarianza y correlación: de dónde sale $r$ (S04)

#### Concepto: covarianza

Todas las cifras anteriores son coeficientes de Pearson, la pieza con la que se construyen la matriz $\mathbf{R}$ (Módulo 8), la matriz $\mathbf{S}$ (Módulo 10) y el PCA (Módulos 16 y 17). Para dos variables $j$ y $k$ medidas sobre los mismos $n$ clientes, la **covarianza** es

$$
s_{jk} = \frac{1}{n-1}\sum_{i=1}^{n}\bigl(x_{ij}-\bar x_j\bigr)\bigl(x_{ik}-\bar x_k\bigr).
$$

Cada sumando es el producto de dos desviaciones respecto de la media: **positivo** si el cliente está del mismo lado de la media en las dos variables, **negativo** si está en lados opuestos. La covarianza suma esa evidencia a favor y en contra de "van juntas". Como $s_{jj} = s_j^2$, **la varianza es la covarianza de una variable consigo misma**.

#### Aplicación 1: covarianza a mano vs. `cov()`

```r
x_ui <- credit$Credit_Utilization
y_cs <- credit$Credit_Score
n_cred <- nrow(credit)
c(a_mano  = sum((x_ui - mean(x_ui)) * (y_cs - mean(y_cs))) / (n_cred - 1),
  con_cov = cov(x_ui, y_cs))
```

| A mano | Con `cov()` |
|---:|---:|
| −8,445789 | −8,445789 |

La fórmula manual reproduce exactamente la función de R. El signo negativo confirma que a más utilización, menos puntaje.

#### Aplicación 2: la covarianza depende de las unidades

Si el ingreso se expresa en **miles de rupias** en vez de rupias, la relación ingreso–cupo no cambia en nada, pero la covarianza se divide por mil:

```r
rbind(
  ingreso_en_rupias       = c(cov = cov(credit$Annual_Income, credit$Credit_Limit),
                              r   = cor(credit$Annual_Income, credit$Credit_Limit)),
  ingreso_en_miles_rupias = c(cov = cov(credit$Annual_Income / 1000, credit$Credit_Limit),
                              r   = cor(credit$Annual_Income / 1000, credit$Credit_Limit)))
```

| Escala del ingreso | Covarianza | $r$ |
|---|---:|---:|
| Rupias | $1{,}384412 \times 10^{12}$ | 0,9741659 |
| Miles de rupias | $1{,}384412 \times 10^{9}$ | 0,9741659 |

#### Concepto: de covarianza a correlación

Por eso se divide por las dos desviaciones estándar:

$$
r_{jk} = \frac{s_{jk}}{s_j\,s_k} = \frac{\sum (x_{ij}-\bar x_j)(x_{ik}-\bar x_k)}{\sqrt{\sum (x_{ij}-\bar x_j)^2}\;\sqrt{\sum (x_{ik}-\bar x_k)^2}}, \qquad -1 \le r_{jk} \le 1.
$$

**Lectura:** la covarianza pasó de un número del orden de $10^{12}$ a uno **mil veces menor** sin que la cartera cambiara; la correlación se quedó **exactamente en 0,9742**. Esa es la razón de que **todo el análisis de relaciones del informe se haga con $r$ y no con $s_{jk}$**: con variables en rupias, conteos y proporciones, una covarianza "grande" no dice nada sin las escalas.

La cota $|r_{jk}| \le 1$ **no es un convenio**: es la **desigualdad de Cauchy–Schwarz** aplicada a los dos vectores de desviaciones $\mathbf{d}_j = \mathbf{x}_j - \bar x_j\mathbf{1}$ y $\mathbf{d}_k$:

$$
|\langle \mathbf{d}_j, \mathbf{d}_k\rangle| \le \|\mathbf{d}_j\|\,\|\mathbf{d}_k\| \;\Longrightarrow\; |r_{jk}| = \frac{|\langle \mathbf{d}_j, \mathbf{d}_k\rangle|}{\|\mathbf{d}_j\|\,\|\mathbf{d}_k\|} \le 1,
$$

y $|r| = 1$ solo se alcanza si los puntos caen **exactamente sobre una recta**. Geométricamente, $r_{jk} = \cos\theta$, el coseno del ángulo entre los dos vectores de desviaciones.

---

### 7.4 ¿El gráfico confirma el número? (Anscombe, S04)

#### Concepto: el cuarteto de Anscombe

Francis Anscombe (1973) construyó cuatro conjuntos de datos con **la misma media y varianza de $x$ e $y$, la misma correlación (≈ 0,816) y la misma recta de regresión**, pero con nubes completamente distintas: una relación lineal con ruido, una curva perfecta, una recta perfecta con un atípico que baja $r$, y una nube vertical con un solo punto palanca que fabrica la correlación. La sesión S04 cerró con esta lección: **$r$ mide relación *lineal*, no relación, y siempre se grafica**.

#### Aplicación al par con el $r$ más alto de la selección

Si $r = 0{,}974$ entre `Annual_Income` y `Credit_Limit` fuera "una recta casi perfecta", el cociente cupo/ingreso sería prácticamente el mismo para todos los clientes. Se comprueba de **tres formas**:

1. **Correlación de rangos de Spearman** (no depende de los valores extremos; es Pearson aplicado a los rangos).
2. **Quitar el 1 % de ingresos más altos** (`quantile(ai, 0.99)`) y recalcular Pearson.
3. **Mirar la nube por tipo de tarjeta**, con la mediana de la razón cupo/ingreso por `Card_Type`.

```r
ai <- credit$Annual_Income; cl <- credit$Credit_Limit
top_1 <- ai > quantile(ai, 0.99)
c(pearson           = cor(ai, cl),
  spearman          = cor(ai, cl, method = "spearman"),
  pearson_sin_top_1 = cor(ai[!top_1], cl[!top_1]))

razon_cupo <- cl / ai
round(sapply(split(razon_cupo, credit$Card_Type), median), 3)[c("Basic","Silver","Gold","Platinum","Signature")]

orden_tarjeta <- c("Basic", "Silver", "Gold", "Platinum", "Signature")
col_tarjeta <- c("#9E9E9E", "#5B8DB8", "#D4A017", "#2E7D32", "#8E24AA")
set.seed(4)
idx_m <- sample(nrow(credit), 6000)
plot(ai[idx_m], cl[idx_m], pch = 16, cex = 0.45,
     col = adjustcolor(col_tarjeta[match(credit$Card_Type[idx_m], orden_tarjeta)], 0.5),
     xlab = "Annual_Income (₹)", ylab = "Credit_Limit (₹)",
     main = "r = 0,974, pero no es una sola recta")
legend("topleft", orden_tarjeta, col = col_tarjeta, pch = 16, bty = "n", title = "Card_Type")
```

Decisión técnica: el gráfico usa una **muestra aleatoria de 6.000 clientes** (`set.seed(4)`) para evitar la sobreimpresión de 50.000 puntos, coloreados por tipo de tarjeta con transparencia 0,5.

#### Resultado

| Pearson | Spearman | Pearson sin el top 1 % de ingresos |
|---:|---:|---:|
| 0,9741659 | 0,9797185 | 0,9717142 |

| Tipo de tarjeta | Basic | Silver | Gold | Platinum | Signature |
|---|---:|---:|---:|---:|---:|
| Mediana de cupo/ingreso | 0,18 | 0,28 | 0,40 | 0,55 | 0,75 |

#### Lectura

Los tres números confirman que la relación es **fuerte** y **no la fabrica un puñado de clientes extremos** (sin el 1 % de ingresos más altos, $r$ apenas baja a **0,972**; Spearman incluso es mayor, 0,980). **Pero el gráfico muestra algo que ningún número de la tabla dice: no hay una recta, hay cinco.** Cada tipo de tarjeta tiene su propia proporción de cupo sobre ingreso —un `Basic` recibe en mediana **0,18 rupias de cupo por rupia de ingreso**, un `Signature` **0,75**— y el $r$ global mezcla esos **cinco abanicos** en uno. Es el conjunto 1 de Anscombe **solo en apariencia**: la política de cupos del banco es

$$
\text{cupo} \approx \text{ingreso} \times \text{factor del tipo de tarjeta},
$$

y esa estructura **solo se ve graficando**.

**Decisión:** el par se sigue usando como el más fuerte de la cartera, pero **cualquier modelo de cupo tiene que incluir `Card_Type`**, y el Módulo 12 vuelve sobre esta mezcla de poblaciones.

**Negocio:** la Gerencia puede leer aquí su propia política de cupos: el factor cupo/ingreso crece de forma escalonada con la categoría de tarjeta (0,18 → 0,28 → 0,40 → 0,55 → 0,75). Un modelo que solo use el ingreso asignaría cupos erróneos a cada segmento.

---

### 7.5 Construcción y demostración del "Punto Imposible" (S03 – Sesión 4)

#### Concepto: atípico multivariante

Uno de los conceptos fundamentales que distingue la **Estadística Multivariante** de la univariada es que **un individuo puede ser perfectamente normal en cada variable por separado y, sin embargo, ser un valor atípico imposible en el espacio conjunto**. Un filtro univariado (como Tukey) examina cada eje por separado, es decir, comprueba si el punto cae dentro de un **rectángulo** $[LI_1, LS_1] \times [LI_2, LS_2]$; pero cuando dos variables están correlacionadas, los datos no llenan el rectángulo sino una **región elongada** (una "elipse" de correlación) a lo largo de la diagonal. Un punto en una esquina vacía del rectángulo pasa todos los filtros univariados y aun así está en una zona de densidad prácticamente nula. Detectarlo requiere una medida que tenga en cuenta la covarianza (la distancia de Mahalanobis, Módulo 13).

#### 7.5.1 Paso 1: verificación de los límites univariados de Tukey (par `Payment_Ratio`–`Credit_Score`)

```r
f_pr <- fivenum(credit$Payment_Ratio); f_cs <- fivenum(credit$Credit_Score)
iqr_pr <- f_pr[4] - f_pr[2];          iqr_cs <- f_cs[4] - f_cs[2]
lim_pr <- c(f_pr[2] - 1.5 * iqr_pr, f_pr[4] + 1.5 * iqr_pr)
lim_cs <- c(f_cs[2] - 1.5 * iqr_cs, f_cs[4] + 1.5 * iqr_cs)
```

| Variable | Límite inferior | Límite superior |
|---|---:|---:|
| `Payment_Ratio` | 0,11 | 1,47 |
| `Credit_Score` | 441 | 825 |

#### 7.5.2 Paso 2: creación del cliente hipotético contradictorio

Se diseña un cliente con:

- `Payment_Ratio = 0.95` (paga casi el 100 % de su saldo).
- `Credit_Score = 460` (puntaje extremadamente bajo / de alto riesgo).

```r
punto_pr <- 0.95; punto_cs <- 460
dentro_pr <- punto_pr >= lim_pr[1] & punto_pr <= lim_pr[2]
dentro_cs <- punto_cs >= lim_cs[1] & punto_cs <= lim_cs[2]
```

| Variable | Valor | Lím. inferior | Lím. superior | ¿Normal univariado? |
|---|---:|---:|---:|:---:|
| `Payment_Ratio` | 0,95 | 0,11 | 1,47 | TRUE |
| `Credit_Score` | 460,00 | 441,00 | 825,00 | TRUE |

**Ambos valores están estrictamente dentro de los bigotes univariados. Ningún filtro univariado lo marcaría como anómalo.** (Nótese que 460 está cerca del límite inferior de 441, pero dentro.)

#### 7.5.3 Paso 3: visualización bivariada — el "Punto Rojo"

```r
plot(credit$Payment_Ratio, credit$Credit_Score,
     pch = 16, col = rgb(0.2, 0.4, 0.8, 0.15),
     xlab = "Payment Ratio (Proporción de Pago)",
     ylab = "Credit Score (Puntaje Crediticio)",
     main = "El Punto Imposible: Normal Univariado vs. Atípico Multivariado")
points(punto_pr, punto_cs, col = "red", pch = 19, cex = 2.2)
points(punto_pr, punto_cs, col = "black", pch = 1, cex = 2.2, lwd = 2)
text(punto_pr - 0.03, punto_cs - 20, labels = "Cliente Imposible\n(0.95, 460)", col = "red", font = 2, pos = 2)
abline(v = mean(credit$Payment_Ratio), col = "gray50", lty = 2)
abline(h = mean(credit$Credit_Score), col = "gray50", lty = 2)
```

Se grafican los 50.000 clientes en azul semitransparente (alfa 0,15), el cliente hipotético como un **punto rojo grande** con borde negro y su etiqueta, y dos líneas grises discontinuas en las medias de cada variable que dividen el plano en cuadrantes de referencia.

**Explicación conceptual:** la combinación es contradictoria porque **viola la covarianza del sistema**: en esta población, cualquier cliente que paga el 95 % de su deuda (`Payment_Ratio = 0.95`) tiene un puntaje **superior a 650**. Asignarle un puntaje de 460 lo sitúa en una **región del plano con densidad nula**, demostrando que **la normalidad marginal no garantiza la normalidad conjunta**.

#### 7.5.4 Punto Imposible en `Annual_Income` vs. `Credit_Limit`

Se repite la demostración con el par numérico más fuerte no redundante ($r = 0{,}974$). Cliente diseñado: `Annual_Income = 3.000.000` (ingreso alto, **pero no récord**) y `Credit_Limit = 200` (un cupo casi simbólico, muy por debajo de cualquier tarjeta real de la cartera).

**Paso 1 — límites de `Annual_Income`:**

| $Q_1$ | $Q_3$ | $RIC$ | Lím. inferior | Lím. superior |
|---:|---:|---:|---:|---:|
| 657 770,5 | 1 663 677,0 | 1 005 906,5 | −851 089,2 | 3 172 536,8 |

El límite superior da **3.172.537 ₹** (el texto renderizado lo muestra con símbolo "$"), así que el ingreso propuesto (3.000.000 ₹) queda **cómodamente por debajo**: nada raro, todavía.

**Paso 2 — límites de `Credit_Limit`:**

| $Q_1$ | $Q_3$ | $RIC$ | Lím. inferior | Lím. superior |
|---:|---:|---:|---:|---:|
| 157 000 | 779 000 | 622 000 | −776 000 | 1 712 000 |

El límite inferior da **−776.000**, negativo porque el $RIC$ es grande frente a $Q_1$. Un cupo de **200 ₹** —muy por debajo del **mínimo real de toda la cartera, 16.000 ₹**— **tampoco se marca como atípico**: a la regla de Tukey le basta con que su límite calculado sea más laxo que el rango observado; **no necesita que el dato sea físicamente real para dejarlo pasar**.

**Paso 3 — verificación conjunta:**

| Variable | Valor | Lím. inferior | Lím. superior | ¿Normal univariado? |
|---|---:|---:|---:|:---:|
| `Annual_Income` | 3 000 000 | −851 089,2 | 3 172 537 | TRUE |
| `Credit_Limit` | 200 | −776 000,0 | 1 712 000 | TRUE |

Las dos columnas dan `TRUE`: **ningún filtro variable-por-variable detecta nada extraño** en este cliente.

**Gráfico:** dispersión de `Annual_Income` vs. `Credit_Limit` (50.000 clientes, azul semitransparente), con el cliente imposible en rojo, etiquetado "Cliente Imposible (3000000, 200)", y líneas grises en las medias.

**Lectura del resultado:** con $r = 0{,}974$ entre ambas variables, **ningún cliente con ingresos de 3.000.000 ₹ tiene en la práctica un cupo de 200 ₹**: el punto rojo cae **fuera de la nube**, lejos de donde vive la elipse de correlación, aunque esté dentro del rango de cada eje por separado. Es la misma lección del par `Payment_Ratio`/`Credit_Score`, esta vez con un **mecanismo económico distinto**: ingreso y cupo aprobado.

**Significado para el negocio:** los controles de calidad o de fraude que validan **cada campo por separado** (rangos permitidos) no detectan registros incoherentes entre campos: un cliente con alto ingreso y cupo ínfimo, o un "buen pagador" con puntaje de alto riesgo, puede ser un error de captura, una manipulación o un caso que requiere revisión manual. La validación debe ser **multivariada** (Mahalanobis, Módulo 13).

---

### 7.6 Confirmando la selección: `Credit_Utilization` frente a `Credit_Score`

La segunda variable prioritaria de la selección objetiva es `Credit_Utilization` ($r = -0{,}599$ con `Credit_Score`, la segunda correlación más fuerte con la variable de riesgo). Se grafica para completar el cuadro de las dos variables que sí predicen el puntaje:

```r
r_cu_cs <- cor(credit$Credit_Utilization, credit$Credit_Score)
plot(credit$Credit_Utilization, credit$Credit_Score,
     pch = 16, col = rgb(0.7, 0.2, 0.2, 0.15),
     xlab = "Credit_Utilization (Proporción del cupo usada)",
     ylab = "Credit_Score (Puntaje Crediticio)",
     main = paste0("Credit_Utilization vs. Credit_Score (r = ", round(r_cu_cs, 3), ")"))
abline(lm(credit$Credit_Score ~ credit$Credit_Utilization), col = "firebrick", lwd = 2)
```

Dispersión en rojo semitransparente con la **recta de regresión de mínimos cuadrados** superpuesta (`lm`, color *firebrick*).

**Lectura:** la nube **desciende con pendiente clara y negativa** ($r = -0{,}599$): a mayor proporción del cupo utilizada, menor puntaje. Junto con `Payment_Ratio`, estas dos variables de **comportamiento de pago y de uso del cupo** —no las de ingreso o gasto— son las que efectivamente mueven `Credit_Score` en este dataset, confirmando con el gráfico lo que ya indicaba el ranking de correlaciones.

---

### 7.7 Comparación por grupos: boxplot numérica ~ categórica (S03)

#### Concepto

El **boxplot condicionado** a una variable categórica (`boxplot(numérica ~ categórica)`) dibuja una caja por cada nivel de la categórica. Es la primera herramienta bivariada del curso que combina un tipo de variable con otro, y es la contraparte gráfica de $\eta^2$: si las cajas están separadas, la variabilidad *entre* grupos es grande frente a la variabilidad *dentro* de ellos ($\eta^2$ alto); si se traslapan por completo, $\eta^2 \approx 0$.

#### Aplicación

Se aplica **únicamente** a los pares que la tabla de $\eta^2$ ya señaló: `Annual_Income` según `Occupation` (el par con más varianza explicada, $\eta^2 = 0{,}637$) y, **como contraste deliberado**, `Credit_Score` según la misma `Occupation` ($\eta^2 = 0{,}0009$), para mostrar cómo se ve en un boxplot una categórica que **no discrimina nada**.

```r
par(mfrow = c(1, 2), mar = c(8, 4, 3, 1))
orden_ocup <- names(sort(tapply(credit$Annual_Income, credit$Occupation, median)))
eta2_ai_ocup <- eta2(credit$Annual_Income, credit$Occupation)
eta2_cs_ocup <- eta2(credit$Credit_Score, credit$Occupation)
boxplot(Annual_Income ~ factor(Occupation, levels = orden_ocup), data = credit, las = 2,
        col = "lightgoldenrod", main = bquote("Annual_Income ~ Occupation  (" * eta^2 * " = " * .(round(eta2_ai_ocup, 3)) * ")"))
boxplot(Credit_Score ~ factor(Occupation, levels = orden_ocup), data = credit, las = 2,
        col = "lightblue", main = bquote("Credit_Score ~ Occupation  (" * eta^2 * " = " * .(round(eta2_cs_ocup, 4)) * ")"))
par(mfrow = c(1, 1))
```

**Decisión técnica:** las ocupaciones se **ordenan por la mediana del ingreso** (no alfabéticamente) y se usa **el mismo orden en ambos paneles**, para que la "escalera" del ingreso sea visible y la comparación con el puntaje sea directa. El valor de $\eta^2$ se imprime en el título de cada panel con `bquote()`.

#### Resultado

- **Panel izquierdo (ingreso):** las cajas **prácticamente no se traslapan** y **suben en escalera**, de `Student` (mediana más baja) a `Business Owner` (mediana más alta), con una razón de **casi 17 a 1** entre las medias de ambos grupos (**251.605 ₹ frente a 4.369.221 ₹**). Eso es lo que significa $\eta^2 = 0{,}637$: el **63,7 %** de toda la variabilidad de `Annual_Income` en la cartera se explica solo con saber la ocupación del cliente.
- **Panel derecho (puntaje):** las **seis cajas** de `Credit_Score` son **visualmente indistinguibles** entre sí y todas se traslapan casi por completo, consistente con que la ocupación explica **apenas el 0,09 %** de la varianza del puntaje.

**Lectura:** la **misma variable categórica es informativa para una variable y ruido puro para otra**, y eso solo se decide **calculando $\eta^2$**, no mirando el boxplot primero.

**Negocio:** la ocupación sirve para estimar capacidad de ingreso (y, por tanto, cupo), pero no para predecir el riesgo de impago: un estudiante y un empresario tienen la misma distribución de puntaje.

---

### 7.8 Tendencias bivariadas de la cartera

Todo el análisis bivariado de este módulo, más las lecturas de la matriz de dispersión del Módulo 8, se resumen en **seis patrones geométricos** distintos. No son seis observaciones sueltas: son las seis formas básicas que puede tomar la nube de puntos de dos variables, y cada una tiene una consecuencia práctica distinta para un modelo posterior. En este módulo se grafican cuatro (lineal directa, lineal inversa, cuña y diferenciación ordinal); las otras dos (**independencia** —bloques cuadrados— y **embudo**) aparecen en la matriz de dispersión del Módulo 8 (sección 8.5).

#### Tendencia 1 — Lineal fuerte directa

`Annual_Income` y `Credit_Limit` ($r = 0{,}974$, el par numérico más fuerte no redundante).

```r
plot(credit$Annual_Income, credit$Credit_Limit, pch = 16, cex = 0.4,
     col = rgb(0.1, 0.5, 0.2, 0.15), main = "Tendencia 1: lineal fuerte directa")
abline(lm(Credit_Limit ~ Annual_Income, data = credit), col = "darkgreen", lwd = 2)
```

A más ingreso, más cupo, en proporción casi constante: la nube es una **banda angosta que sube** de izquierda a derecha (con recta de regresión verde oscuro). **Consecuencia:** cualquier modelo que use ambas variables sin corregirlo **va a duplicar, en la práctica, la misma información** (multicolinealidad).

#### Tendencia 2 — Lineal inversa

`Credit_Utilization` y `Credit_Score` ($r = -0{,}599$, ya graficada en la sección 7.6; el gráfico se repite aquí con la misma recta de regresión en rojo): la nube **desciende** de izquierda a derecha —a mayor uso del cupo, menor puntaje. **Consecuencia:** es, junto con `Payment_Ratio`, una relación con **signo de negocio claro y aprovechable** para explicar riesgo.

#### Tendencia 3 — Efecto cuña / límite superior

`Credit_Limit` y `Outstanding_Balance` ($r = 0{,}866$): la nube **llena un triángulo, no un rectángulo**. Ningún cliente debe más del 98 % de su cupo: el **máximo real de la razón saldo/cupo es 0,978**.

```r
plot(credit$Credit_Limit, credit$Outstanding_Balance, pch = 16, cex = 0.4,
     col = rgb(0.1, 0.3, 0.6, 0.15), main = "Tendencia 3: efecto cuña / límite superior")
max_ratio <- max(credit$Outstanding_Balance / credit$Credit_Limit, na.rm = TRUE)
abline(a = 0, b = max_ratio, col = "darkblue", lty = 2, lwd = 2)
```

Se dibuja la recta $\text{saldo} = 0{,}978 \times \text{cupo}$ (azul oscuro discontinua) que representa el **techo físico real** de los saldos: todos los puntos quedan por debajo de ella, y por debajo de la recta los saldos pueden tomar cualquier valor desde cero.

**Consecuencia:** la relación es **real pero asimétrica**: `Credit_Limit` actúa como **techo físico** de `Outstanding_Balance`, **no como su causa proporcional**. La varianza del saldo crece con el cupo (heterocedasticidad), así que una regresión lineal simple la describiría mal.

#### Tendencia 4 — Diferenciación por grupos ordinales

`Card_Type` (ordinal: Basic < Silver < Gold < Platinum < Signature) sobre `Credit_Limit`:

```r
orden_tipo <- c("Basic", "Silver", "Gold", "Platinum", "Signature")
boxplot(Credit_Limit ~ factor(Card_Type, levels = orden_tipo), data = credit,
        col = colorRampPalette(c("grey80", "#1E7F63"))(5),
        main = "Tendencia 6: diferenciación por grupos ordinales", ...)
```

(Detalle: el título interno del gráfico dice "Tendencia 6", heredado de una numeración anterior de seis tendencias; en el texto es la Tendencia 4.) Se usa una paleta en degradé de gris a verde que refuerza visualmente el orden.

Las **cinco cajas suben en el mismo orden que la jerarquía de la tarjeta, sin ninguna inversión**: la mediana de `Signature` es varias veces la de `Basic`. **Consecuencia:** a diferencia de `Occupation` (que discrimina `Annual_Income` pero **no tiene un orden intrínseco**), aquí la propia estructura ordinal de la categórica se refleja en la variable numérica, lo que la hace **candidata a tratarse como una variable ordinal codificada** en un modelo (p. ej., Basic = 1 … Signature = 5), no solo como grupos separados ($\eta^2 = 0{,}80$).

#### Resumen de las seis formas

| Forma | Ejemplo en la cartera | Consecuencia para modelar |
|---|---|---|
| Lineal directa | `Annual_Income`–`Credit_Limit` ($r = 0{,}974$) | redundancia: no usar ambas sin corrección |
| Lineal inversa | `Credit_Utilization`–`Credit_Score` ($r = -0{,}599$) | predictor de riesgo aprovechable |
| Independencia (bloque cuadrado) | ingreso/gasto vs. `Credit_Score` (Módulo 8) | la variable no aporta a explicar la otra |
| Cuña / techo | `Credit_Limit`–`Outstanding_Balance` ($r = 0{,}866$, techo 0,978) | relación asimétrica, heterocedástica |
| Embudo | `Monthly_Spending`–`Payment_Ratio` (Módulo 8) | la dispersión cambia con el nivel |
| Diferenciación ordinal | `Card_Type`–`Credit_Limit` | codificar la categórica como ordinal |

---

### 7.9 Conclusión del Módulo 7

1. **La selección de pares no fue arbitraria:** `Annual_Income`–`Credit_Limit` por ser el par numérico más fuerte sin ser redundancia contable; `Payment_Ratio` y `Credit_Utilization` por ser, con enorme margen, **las únicas variables numéricas que de verdad predicen `Credit_Score`** ($r = 0{,}767$ y $r = -0{,}599$ frente a $r \approx 0{,}03$ del resto); y `Occupation` por ser la categórica con mayor $\eta^2$ sobre una variable de dinero.
2. **El comportamiento de pago es el motor del riesgo, no el dinero.** El "punto imposible" mostró que un cliente puede ser perfectamente normal en cada variable por separado (`Payment_Ratio`/`Credit_Score` o `Annual_Income`/`Credit_Limit`) y aun así representar una combinación que **la covarianza real de la cartera no permite**.
3. Ese mismo patrón se repite con una variable categórica: `Occupation` explica el **63,7 %** de la varianza de `Annual_Income` pero **menos del 0,1 %** de la de `Credit_Score` —la misma conclusión de fondo (el riesgo depende del comportamiento de pago, no del dinero que entra) confirmada desde el lado categórico.
4. Las **seis formas bivariadas** de la cartera (lineal directa, lineal inversa, independencia, cuña, embudo, diferenciación ordinal) no son solo una taxonomía descriptiva: cada una implica algo distinto sobre qué relaciones son **redundantes**, cuáles son **aprovechables** y cuáles requieren un modelo que capture **algo más que un coeficiente de correlación**.

**Mensaje para la Gerencia de Riesgo:** para anticipar el riesgo, el banco debe vigilar **qué proporción de la deuda paga el cliente** y **qué proporción del cupo utiliza**, no cuánto gana ni cuánto gasta. La política de cupos sí depende del ingreso y del tipo de tarjeta, y esa relación está bien estructurada (cinco factores escalonados).

---

## Módulo 8: Estructura Multivariada Conjunta (S01 & S03 & S05)

### Motivación

El Módulo 7 miró pares de variables, uno a la vez, eligiéndolos con un criterio explícito. Pero un dataset de $p = 26$ variables numéricas no se agota en unos pocos pares: hay $\binom{26}{2} = 325$ posibles, y **ningún analista revisa 325 diagramas de dispersión uno por uno** (S05). Este módulo resuelve ese problema convirtiendo todos los pares en **un solo objeto** —la matriz de correlación $\mathbf{R}$— y después en **tres representaciones visuales** distintas de esa misma matriz, cada una útil para ver algo que las otras no ven:

1. el **mapa de calor** (bloques de variables parecidas),
2. las **coordenadas paralelas** (patrones de más de dos variables a la vez),
3. la **matriz de dispersión** (la forma real de cada relación, no solo su número).

---

### 8.1 Matriz de correlaciones completa ($\mathbf{R}$)

#### Concepto

La matriz de correlación reúne todas las correlaciones de Pearson entre las $p$ variables:

$$
\mathbf{R} = \begin{pmatrix} 1 & r_{12} & \cdots & r_{1p} \\ r_{21} & 1 & \cdots & r_{2p} \\ \vdots & \vdots & \ddots & \vdots \\ r_{p1} & r_{p2} & \cdots & 1 \end{pmatrix} = \mathbf{D}^{-1}\,\mathbf{S}\,\mathbf{D}^{-1}, \qquad \mathbf{D} = \operatorname{diag}(s_1,\dots,s_p),
$$

donde $\mathbf{S}$ es la matriz de covarianzas. Equivalentemente, $\mathbf{R}$ es la matriz de covarianzas de los datos estandarizados: $\mathbf{R} = \frac{1}{n-1}\mathbf{Z}^\top\mathbf{Z}$.

#### Decisión: primero una submatriz de 10 variables

Una tabla de 26×26 no se lee a simple vista, así que primero se calcula sobre las **10 variables de mayor interés de negocio** —las mismas del Módulo 7 (ingreso, cupo, gasto, saldos, ratios de pago/utilización y el puntaje)— para tener una **referencia numérica exacta** antes de pasar al mapa de calor completo.

```r
vars_interes <- c("Annual_Income", "Credit_Limit", "Monthly_Spending",
                  "Outstanding_Balance", "Statement_Balance", "Payment_Amount",
                  "Payment_Ratio", "Credit_Utilization", "Reward_Points_Earned", "Credit_Score")
mat_cor <- cor(credit_num[, vars_interes], use = "complete.obs")
round(mat_cor, 3)
```

#### Resultado (submatriz 10×10)

| | AI | CL | MS | OB | SB | PA | PR | CU | RPE | CS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **AI** `Annual_Income` | 1,000 | 0,974 | 0,945 | 0,843 | 0,874 | 0,819 | 0,002 | 0,005 | 0,924 | 0,032 |
| **CL** `Credit_Limit` | 0,974 | 1,000 | 0,940 | 0,866 | 0,894 | 0,839 | 0,001 | 0,005 | 0,958 | 0,035 |
| **MS** `Monthly_Spending` | 0,945 | 0,940 | 1,000 | 0,814 | 0,855 | 0,805 | 0,003 | 0,005 | 0,980 | 0,033 |
| **OB** `Outstanding_Balance` | 0,843 | 0,866 | 0,814 | 1,000 | 0,997 | 0,932 | −0,002 | 0,293 | 0,830 | −0,145 |
| **SB** `Statement_Balance` | 0,874 | 0,894 | 0,855 | 0,997 | 1,000 | 0,936 | −0,001 | 0,262 | 0,866 | −0,125 |
| **PA** `Payment_Amount` | 0,819 | 0,839 | 0,805 | 0,932 | 0,936 | 1,000 | 0,192 | 0,246 | 0,815 | 0,031 |
| **PR** `Payment_Ratio` | 0,002 | 0,001 | 0,003 | −0,002 | −0,001 | 0,192 | 1,000 | 0,005 | 0,003 | 0,767 |
| **CU** `Credit_Utilization` | 0,005 | 0,005 | 0,005 | 0,293 | 0,262 | 0,246 | 0,005 | 1,000 | 0,005 | −0,599 |
| **RPE** `Reward_Points_Earned` | 0,924 | 0,958 | 0,980 | 0,830 | 0,866 | 0,815 | 0,003 | 0,005 | 1,000 | 0,036 |
| **CS** `Credit_Score` | 0,032 | 0,035 | 0,033 | −0,145 | −0,125 | 0,031 | 0,767 | −0,599 | 0,036 | 1,000 |

**Lectura:** ya se pueden leer en esta submatriz los **dos hallazgos** que se repiten en todo el módulo:

1. **Bloques de variables casi redundantes** entre sí (`Outstanding_Balance`–`Statement_Balance` = **0,997**).
2. **La separación** entre las variables de dinero y las que realmente predicen `Credit_Score` (`Payment_Ratio` = **0,767** frente a `Annual_Income` = **0,032**).

Otros detalles visibles: la utilización se asocia moderadamente con los saldos (0,293 con `Outstanding_Balance`, 0,262 con `Statement_Balance`) y el ratio de pago con el monto pagado (0,192), pero ambos son prácticamente nulos (≤ 0,005) frente a ingreso, cupo, gasto y puntos. El resto del módulo extiende esta lectura a las 26 variables.

---

### 8.2 Mapa de calor de correlaciones

#### Concepto

Una tabla de 26×26 números (**325 celdas únicas** fuera de la diagonal) es formalmente correcta pero ilegible. El **mapa de calor** codifica cada correlación como **color** en vez de número (escala divergente: azul para positivas, rojo para negativas, intensidad proporcional a $|r|$) y **reordena las variables por similitud** mediante **agrupamiento jerárquico** (`order = "hclust"`, la misma idea de la sesión S05): las variables que se parecen quedan juntas y forman **bloques visibles** a lo largo de la diagonal.

#### Aplicación

```r
vars_numericas <- names(credit)[sapply(credit, is.numeric)]
credit_num <- credit[, vars_numericas]
matriz_cor <- cor(credit_num, use = "complete.obs", method = "pearson")
library(corrplot)   # se instala desde CRAN si no está disponible
corrplot(matriz_cor, method = "color", type = "upper", order = "hclust",
         tl.col = "black", tl.cex = 0.75, tl.srt = 45,
         addCoef.col = "black", number.cex = 0.55, diag = FALSE,
         title = "Mapa de calor de correlaciones entre variables numéricas",
         mar = c(0, 0, 2, 0))
```

Parámetros: solo el **triángulo superior** (`type = "upper"`, porque la matriz es simétrica), **sin la diagonal** (siempre 1), el coeficiente impreso en cada celda (`addCoef.col`), etiquetas rotadas 45°, figura de 12×10 pulgadas.

#### 8.2.1 Síntesis de correlaciones observadas

**Colinealidad casi perfecta ($r > 0{,}95$):**

- `Outstanding_Balance` y `Statement_Balance` ($r = 0{,}997$)
- `Monthly_Spending` y `Reward_Points_Earned` ($r = 0{,}980$)
- `Credit_Limit` y `Annual_Income` ($r = 0{,}974$)

**Determinantes del riesgo:**

- `Payment_Ratio` con `Credit_Score` ($r = 0{,}767$)
- `Credit_Utilization` con `Credit_Score` ($r = -0{,}599$)

#### 8.2.2 Relaciones fuertes y positivas (valores cercanos a 1,00)

- **Ingresos y capacidad financiera:** correlación altísima entre `Annual_Income`, `Credit_Limit` (**0,974**) y `Monthly_Spending` (**0,945**). A mayores ingresos, los clientes reciben un límite de crédito proporcionalmente más alto y gastan más dinero mensualmente.
- **Deuda y saldos:** `Outstanding_Balance` y `Statement_Balance` tienen una correlación casi perfecta de **0,997**. Además, ambas tienen una relación muy fuerte con `Payment_Amount` (**~0,93**): quienes acumulan más saldo también realizan pagos más grandes.
- **Puntos de recompensa y gasto:** `Reward_Points_Earned` está fuertemente ligada a `Monthly_Spending` (**0,980**) y `Credit_Limit` (**0,958**). El sistema de recompensas funciona de manera **lineal**: a mayor gasto y mayor límite de tarjeta, se acumulan muchos más puntos.

#### 8.2.3 Relaciones moderadas a fuertes negativas (camino inverso)

- **Historial crediticio vs. uso de la tarjeta:** la correlación entre `Credit_Score` y `Credit_Utilization` es **−0,599**. Esta relación negativa moderada/fuerte confirma la teoría financiera: **a mayor porcentaje de uso de la línea de crédito, menor tiende a ser el puntaje crediticio**.

#### 8.2.4 El factor clave del `Credit_Score`

- **El ratio de pago es vital:** la correlación más alta y positiva con `Credit_Score` es `Payment_Ratio` (**0,767**). Lo más efectivo para tener un buen puntaje no es cuánto se gana, sino **el porcentaje de la deuda que se paga a tiempo**.
- **Independencia de los ingresos y gastos:** sorprendentemente, `Annual_Income` (**0,032**), `Credit_Limit` (**0,035**) y `Monthly_Spending` (**0,033**) tienen correlaciones casi nulas con el puntaje. **Tener mucho dinero o gastar mucho no garantiza un buen Credit Score.**

#### 8.2.5 Variables prácticamente aisladas

`Payment_Ratio` y `Credit_Utilization` tienen correlaciones cercanas a **0,00** con casi todas las variables de volumen de dinero (ingresos, límites, gastos). El **comportamiento de pago** de una persona (si paga el total o solo el mínimo, o qué porcentaje de su tarjeta usa) es **independiente de si es de ingresos altos o bajos**.

**Negocio:** en el mapa se ven dos "mundos": un gran bloque de **tamaño financiero** (ingreso, cupo, gasto, saldos, pagos, puntos), altamente redundante, y un pequeño bloque de **comportamiento/riesgo** (ratio de pago, utilización, puntaje), casi ortogonal al primero. Esto anticipa que un PCA encontrará al menos un componente de "tamaño" y otro de "comportamiento".

---

### 8.3 Verificación de las propiedades de $\mathbf{R}$ (S05)

#### Concepto

Antes de construir nada más sobre esta matriz —el PCA de unidades posteriores y, en el Módulo 13, la distancia de Mahalanobis— hay que confirmar que $\mathbf{R}$ cumple las propiedades que la teoría exige (Everitt & Hothorn):

1. **Diagonal de unos:** $r_{jj} = s_{jj}/(s_j s_j) = 1$ por definición.
2. **Simetría:** $r_{jk} = r_{kj}$, es decir $\mathbf{R} = \mathbf{R}^\top$.
3. **Semidefinida positiva:** para todo vector $\mathbf{a} \in \mathbb{R}^p$,
   $$\mathbf{a}^\top \mathbf{R}\, \mathbf{a} = \operatorname{Var}\!\Big(\sum_j a_j Z_j\Big) \ge 0,$$
   porque es la varianza de una combinación lineal de las variables estandarizadas, y una varianza nunca es negativa. Equivale a que **todos los valores propios** $\lambda_1 \ge \dots \ge \lambda_p$ sean $\ge 0$. Garantiza que $\mathbf{R}$ no produce varianzas negativas; si además todos son $> 0$, $\mathbf{R}$ es **definida positiva e invertible**.

Relaciones útiles con los valores propios:

$$
\operatorname{tr}(\mathbf{R}) = \sum_{j=1}^p \lambda_j = p, \qquad \det(\mathbf{R}) = \prod_{j=1}^p \lambda_j, \qquad 0 \le \det(\mathbf{R}) \le 1.
$$

El **determinante** de $\mathbf{R}$ mide el "volumen" de la nube estandarizada: vale 1 si las variables son incorrelacionadas y tiende a 0 cuando hay redundancia lineal; un valor propio casi nulo arrastra el determinante a casi cero y hace la matriz **casi singular** (difícil de invertir de forma estable).

#### Aplicación

```r
diagonal_unos <- all(abs(diag(matriz_cor) - 1) < 1e-9)
es_simetrica <- isSymmetric(matriz_cor)
valores_propios <- eigen(matriz_cor)$values
semidefinida_positiva <- all(valores_propios > -1e-8)
c(Diagonal_de_unos = diagonal_unos, Es_simetrica = es_simetrica,
  Semidefinida_positiva = semidefinida_positiva,
  Valor_propio_minimo = round(min(valores_propios), 4),
  Valor_propio_maximo = round(max(valores_propios), 4))
```

**Decisiones técnicas:** las comparaciones usan **tolerancias numéricas** (`1e-9` para la diagonal, `-1e-8` para los valores propios) porque la aritmética de punto flotante puede producir valores como $0{,}9999999999$ o $-10^{-15}$ que son, en rigor, 1 y 0.

#### Resultado

| Propiedad | Resultado |
|---|---|
| Diagonal de unos | TRUE (1) |
| Es simétrica | TRUE (1) |
| Semidefinida positiva | TRUE (1) |
| Valor propio mínimo | **0,0000** (redondeado a 4 decimales) |
| Valor propio máximo | **12,7507** |

(El determinante de $\mathbf{R}$ **no se reporta** explícitamente en el informe.)

**Lectura:** las tres propiedades se cumplen sobre las 26 variables numéricas: la diagonal es exactamente 1 en las 26 posiciones, la matriz es simétrica, y el valor propio más pequeño es 0 a cuatro decimales —**positivo, aunque muy cercano a cero**. Ese valor propio casi nulo **no es un error**: es la **huella numérica de que hay variables casi redundantes** entre sí (`Outstanding_Balance` con `Statement_Balance`, `Monthly_Spending` con `Reward_Points_Earned`, ya señaladas en la síntesis del mapa de calor; además, `Monthly_Spending` es la suma exacta de las siete categorías de gasto, Módulo 10). Anticipa por qué el **Módulo 10 tiene que excluir columnas derivadas antes de invertir la matriz de covarianzas** para la distancia de Mahalanobis.

Como $\operatorname{tr}(\mathbf{R}) = 26$, el valor propio máximo (12,7507) concentra por sí solo cerca de la mitad de la varianza estandarizada total (12,7507/26 ≈ 49 %, cálculo derivado de las cifras reportadas): señal de que un solo eje —el de "tamaño financiero"— resume gran parte de la información.

**Negocio:** la base tiene información duplicada; varias columnas no aportan nada nuevo. Para cualquier modelo de riesgo, el banco debe elegir **una** variable de cada bloque redundante (p. ej., un solo saldo), so pena de modelos inestables.

---

### 8.4 Coordenadas paralelas

#### Concepto

El mapa de calor y la matriz de dispersión comparten una limitación: **solo muestran relaciones de a dos variables**. Un patrón que solo aparece al mirar cinco o seis variables a la vez no se ve en ningún panel de esos dos gráficos. Las **coordenadas paralelas** (Inselberg) resuelven exactamente eso: se dibuja **un eje vertical por variable**, colocados uno junto a otro, y **cada cliente es una línea poligonal** que cruza todos los ejes a la altura de su valor en cada variable. Líneas que van "juntas" revelan grupos; cruces en X entre dos ejes adyacentes revelan correlación negativa; líneas paralelas, correlación positiva. El costo: cada variable se **normaliza a su propio rango**, así que lo que se lee son **patrones relativos, no magnitudes originales**.

#### Aplicación

```r
library(MASS)
set.seed(123)
indices_muestra <- sample(1:nrow(credit), size = 5000)
credit_subset <- credit[indices_muestra, ]

vars_paralelas <- c("Annual_Income", "Credit_Limit", "Monthly_Spending",
  "Monthly_Transactions", "Avg_Transaction_Value", "Outstanding_Balance",
  "Statement_Balance", "Payment_Amount", "Payment_Ratio", "Credit_Utilization",
  "Cash_Advance_Amount", "Credit_Score")
X_par <- credit_subset[, vars_paralelas, drop = FALSE]
X_par_scaled <- scale(X_par)

cal <- cut(credit_subset$Credit_Score, breaks = c(-Inf, 579, 669, Inf),
           labels = c("Bajo", "Medio", "Alto"), include.lowest = TRUE)
col <- c("Bajo" = "#B0442FA0",   # rojo semitransparente
         "Medio" = "#BEBEBE15",  # gris muy transparente (para que no estorbe)
         "Alto" = "#1E7F63A0")   # verde semitransparente
col_clientes <- col[as.character(cal)]

par(mar = c(7, 4, 4, 2) + 0.1)
parcoord(X_par_scaled, col = col_clientes, lwd = 0.4,
         main = "Coordenadas paralelas — Comportamiento financiero y riesgo (Muestra n=5000)",
         xaxt = "n")
text(x = 1:ncol(X_par_scaled), y = par("usr")[3] - 0.1, labels = colnames(X_par_scaled),
     srt = 45, adj = 1, xpd = TRUE, cex = 0.8)
title(xlab = "Variables", ylab = "Valor estandarizado (z-score)")
legend("topright", legend = c("Credit Score bajo", "Credit Score medio", "Credit Score alto"),
       col = c("#B0442F", "grey75", "#1E7F63"), lwd = 2, bty = "n")
```

**Decisiones:**

- **Muestra aleatoria de 5.000 clientes** (`set.seed(123)`) para que 50.000 líneas no saturen el gráfico. (Los comentarios del código dicen "2,000 registros", pero el código y el título usan **5.000**.)
- **12 variables** que cubren tamaño (ingreso, cupo, gasto), actividad (transacciones, ticket promedio), deuda (saldos, pago), comportamiento (ratio de pago, utilización, avances en efectivo) y, al final, el puntaje.
- **Tres grupos de riesgo por `Credit_Score`**: Bajo (≤ 579), Medio (580–669) y Alto (≥ 670), según los cortes `c(-Inf, 579, 669, Inf)`.
- **Colores con transparencia diferenciada:** rojo y verde semitransparentes para los extremos, y el grupo medio en gris **casi invisible** (alfa hexadecimal `15`) para que no tape los patrones de los extremos.
- Se estandariza con `scale()`; además, `MASS::parcoord()` reescala internamente cada eje a su rango [mín, máx], de modo que lo que se compara es la posición relativa dentro del rango de cada variable (por eso el texto habla de "normalizar cada variable a su propio rango", aunque la etiqueta del eje diga "z-score").
- Eje X dibujado a mano con etiquetas rotadas 45° (`xaxt = "n"` + `text(..., srt = 45, xpd = TRUE)`) para que los nombres de las 12 variables sean legibles; figura de 14×8 pulgadas.

#### 8.4.1 ¿Qué se puede interpretar?

A pesar del desorden, las coordenadas paralelas son excelentes para detectar **patrones extremos y comportamientos grupales**. Al mirar los extremos de los colores:

- **El grupo "Credit Score Bajo" (rojo) está concentrado abajo en variables clave:**
  - Hacia el final del gráfico (lado derecho) se nota una **masa roja muy densa que cae drásticamente hacia el suelo** en la última variable (`Credit_Score`), como es lógico por construcción.
  - En puntos intermedios como `Payment_Ratio` (porcentaje de la deuda que pagan al mes), **la gran masa roja se queda abajo**: los clientes con peor score **pagan muy poco de sus saldos pendientes**.
- **El grupo "Credit Score Alto" (verde) domina las partes altas de estabilidad:**
  - Las líneas verdes **suben con fuerza al final** hacia el tope de `Credit_Score`.
  - En variables de comportamiento como `Payment_Ratio` se ven **picos verdes que logran subir**: este grupo liquida un porcentaje mucho mayor de sus deudas.
- **El solapamiento central:** en las variables del medio (como saldos de estados de cuenta o valores promedio de transacciones), **los tres colores están sumamente mezclados**. El gasto mensual por sí solo o el saldo de la tarjeta **no discriminan** de forma directa si alguien es de alto o bajo riesgo; **lo que importa es la relación entre lo que gastan, lo que ganan y cómo lo pagan**.

**Negocio:** el gráfico permite "ver" el perfil completo del cliente de alto riesgo de un vistazo: no se distingue por su tamaño (ingreso, cupo, gasto), sino por hundirse en `Payment_Ratio`; es el perfil que un modelo de *scoring* debería capturar.

---

### 8.5 Matriz de dispersión multivariada (`pairs`)

#### Concepto

La **matriz de dispersión** (*scatterplot matrix*) dispone en una cuadrícula $k \times k$ todos los diagramas de dispersión de $k$ variables tomadas de dos en dos: la celda $(i, j)$ muestra la variable $j$ en el eje X contra la $i$ en el eje Y. Permite ver **la forma real** de cada relación (lineal, curva, cuña, bloque), que un solo coeficiente $r$ no distingue (lección de Anscombe).

#### Aplicación (versión de tres paneles, S05)

En vez del `pairs()` plano, se usa la versión de tres paneles:

- **Panel inferior:** la nube de puntos (azul semitransparente, alfa 0,15).
- **Panel superior:** la correlación, con **tamaño de letra proporcional a $|r|$** (`cex = 0.8 + 1.6 * abs(r)`), para que las relaciones fuertes salten a la vista sin leer número por número.
- **Diagonal:** el **histograma** de cada variable (barras grises normalizadas al máximo), para no perder la forma univariada mientras se mira lo bivariado.

```r
panel.cor <- function(x, y, ...) {
  usr <- par("usr"); on.exit(par(usr = usr))
  par(usr = c(0, 1, 0, 1))
  r <- cor(x, y, use = "pairwise.complete.obs")
  txt <- format(round(r, 2), nsmall = 2)
  text(0.5, 0.5, txt, cex = 0.8 + 1.6 * abs(r))
}
panel.hist <- function(x, ...) {
  usr <- par("usr"); on.exit(par(usr = usr))
  par(usr = c(usr[1:2], 0, 1.5))
  h <- hist(x, plot = FALSE)
  rect(h$breaks[-length(h$breaks)], 0, h$breaks[-1],
       h$counts / max(h$counts), col = "grey80", border = "white")
}
```

#### 8.5.1 Primera matriz: variables clave

```r
vars_pairs <- c("Annual_Income", "Monthly_Spending", "Credit_Limit",
                "Payment_Ratio", "Credit_Utilization", "Credit_Score")
pairs(credit_num[, vars_pairs], lower.panel = function(x, y, ...) points(x, y, pch = 16, cex = 0.5,
      col = rgb(0.1, 0.4, 0.7, 0.15)), upper.panel = panel.cor, diag.panel = panel.hist,
      main = "Matriz de Dispersion (pairs) - Variables Clave")
```

Se grafican los **50.000 clientes** (sin muestreo) para seis variables: tres de tamaño y tres de comportamiento/riesgo.

##### Relaciones lineales y fuertes (diagonal hacia arriba)

- **`Annual_Income` vs. `Monthly_Spending`** (esquina superior izquierda): relación lineal positiva muy fuerte, descrita en el informe como "perfecta". Es una **banda muy apretada** que sube de izquierda a derecha: a medida que suben los ingresos, la capacidad y el volumen de gasto mensual aumentan de forma proporcional.
- **`Payment_Ratio` vs. `Credit_Score`** (penúltima fila, última columna): **banda diagonal ascendente muy bien definida**. A mayor ratio de pago, mayor puntaje. La forma compacta de la banda demuestra que es una de las variables con **mayor peso e impacto directo** para predecir el score.

##### Relaciones negativas (diagonal hacia abajo)

- **`Credit_Utilization` vs. `Credit_Score`** (cuarta fila, última columna): **banda diagonal descendente** muy nítida. Es la "prueba reina" de que un mayor uso de la línea de crédito **destruye** el puntaje. Al ser una banda limpia sin mucha dispersión lateral, sugiere **una regla estricta en el algoritmo del score**.
- **`Payment_Ratio` vs. `Credit_Utilization`** (cruce de la 3.ª y 4.ª variables): se nota una **ligera dispersión o caída en diagonal invertida en las esquinas**: quienes tienen ratios de utilización muy extremos tienden a comportarse de forma inversa con sus ratios de pago. (Matiz: la correlación global entre ambas es prácticamente nula, 0,005, así que se trata de un efecto local en los extremos, no de una tendencia lineal.)

##### Distribuciones en bloque cuadrado (sin relación / independencia)

- **`Annual_Income` y `Monthly_Spending` vs. `Credit_Score`:** un **bloque rectangular**: se encuentran personas con puntajes excelentes (800) o pésimos (400) **sin importar si ganan mucho o poco**. El dinero que ingresa **no define la responsabilidad financiera**.
- **`Annual_Income` y `Monthly_Spending` vs. `Payment_Ratio` / `Credit_Utilization`:** bloques completamente cuadrados y uniformes. El nivel de ingresos **no influye** en qué porcentaje del cupo decide usar el cliente ni en qué porcentaje de su deuda decide pagar mes a mes.

(Esta es la **forma "independencia"** de las seis tendencias del Módulo 7.)

##### Patrones de "efecto embudo" o techo

- **`Monthly_Spending` vs. `Payment_Ratio`:** los puntos se concentran fuertemente en la parte inferior cuando el gasto es muy alto. Sugiere que, a volúmenes de gasto extremadamente altos, es más difícil mantener un `Payment_Ratio` perfecto de 1,0, creando un sutil efecto de dispersión o **"embudo"**. (Es la **forma "embudo"** de las seis tendencias.)

#### 8.5.2 Segunda matriz: variables de interés (saldos y puntos)

```r
vars_impairs <- c("Credit_Limit", "Outstanding_Balance", "Statement_Balance",
                  "Payment_Amount", "Reward_Points_Earned")
pairs(credit[, vars_impairs], lower.panel = ..., upper.panel = panel.cor,
      diag.panel = panel.hist, main = "Matriz de Dispersion - Variables De Interes")
```

##### Relación lineal perfecta (línea recta exacta)

- **`Outstanding_Balance` vs. `Statement_Balance`** (fila 2, columna 3 y viceversa): los puntos forman una **línea recta diagonal perfecta y ultra delgada**, que confirma visualmente la correlación de **0,997**. El saldo acumulado (`Outstanding_Balance`) y el saldo de corte del estado de cuenta (`Statement_Balance`) reflejan **exactamente la misma información económica**. Tener ambas variables en un modelo predictivo causaría un **problema grave de multicolinealidad** (redundancia).

##### Patrones de "cuña" o "triángulo inferior" (límite físico)

En varios gráficos, los puntos llenan un triángulo pero dejan un **espacio vacío perfecto** en la mitad superior o inferior: una variable actúa como **techo o límite insuperable** para la otra.

- **`Credit_Limit` vs. saldos y pagos** (fila 1 con columnas 2, 3 y 4): al cruzar el límite de crédito con el saldo pendiente, el saldo del estado de cuenta y los montos de pago, la gráfica dibuja una **cuña con una base diagonal recta**. Los saldos y los pagos pueden ser bajos o altos, pero están **estrictamente topados por el límite de crédito asignado**: nadie puede deber ni pagar más del cupo que el banco le otorgó (Tendencia 3 del Módulo 7: techo en 0,978 del cupo para el saldo).
- **Saldos vs. `Payment_Amount`** (intersecciones entre filas 2/3 y columna 4): comportamiento similar. El monto pagado crece a medida que crece la deuda, pero hay un **vacío en la parte superior** porque los clientes rara vez o nunca pagan más de lo que deben.

##### El efecto especial de los puntos de recompensa (última fila/columna)

- **`Reward_Points_Earned` vs. `Credit_Limit` / saldos:** la última fila muestra una dispersión que se asemeja a una **"aleta de tiburón"** o una curva que se **expande hacia la derecha**. Los puntos crecen a medida que aumentan el límite y los saldos, pero la dispersión se vuelve **más ancha al final**: en los segmentos de líneas de crédito muy altas, la acumulación de puntos se vuelve **más variable** entre usuarios (heterocedasticidad).

**Negocio:** la matriz de dispersión confirma visualmente que (a) los saldos `Outstanding` y `Statement` son la misma variable para fines de modelado; (b) el cupo es un techo duro de la exposición, de modo que la utilización (saldo/cupo) es la medida natural del riesgo de uso; (c) los clientes de cupos altos son más heterogéneos en su respuesta al programa de recompensas.

---

### 8.6 Conclusión del Módulo 8

1. La matriz $\mathbf{X}$ tiene una **interdependencia lineal alta pero muy desigual**: bloques de variables casi redundantes ($r > 0{,}95$: `Outstanding_Balance`–`Statement_Balance`, `Monthly_Spending`–`Reward_Points_Earned`) conviven con variables prácticamente **independientes** del resto (`Payment_Ratio`, `Credit_Utilization` frente a las de dinero). La matriz de correlación tiene un **valor propio casi nulo** (sección 8.3), que es la huella numérica exacta de esa redundancia.
2. **Las tres visualizaciones muestran cosas distintas de la misma matriz:** el **mapa de calor** agrupa variables parecidas en bloques; las **coordenadas paralelas** muestran patrones de más de dos variables a la vez (el grupo de riesgo —puntaje bajo— hundido en `Payment_Ratio`); y **`pairs`** muestra la forma real de cada relación (bandas, cuñas, bloques cuadrados) que un solo número de correlación no distingue.
3. Esta **alta redundancia entre variables de dinero** es la razón concreta por la que el **Módulo 10 tiene que excluir columnas derivadas** antes de invertir la matriz de covarianzas para la distancia de Mahalanobis: **una matriz casi singular no se puede invertir de forma estable**.

**Mensaje para la Gerencia de Riesgo:** la información de la cartera se organiza en dos dimensiones casi independientes: el **tamaño** del cliente (ingreso, cupo, gasto, saldos, puntos, todos redundantes entre sí) y su **comportamiento de pago** (ratio de pago, utilización), que es el que explica el puntaje. Para gestionar riesgo, basta con una variable representativa del tamaño y las dos de comportamiento; acumular más variables de dinero no añade capacidad predictiva y sí inestabilidad numérica.


---

## Módulo 9: Vector de medias, centroide y el límite de la distancia euclidiana (S06)

### Contexto y propósito del módulo

Hasta el Módulo 8 el informe describió la **forma** de la nube de $n = 50\,000$ clientes en $p$ dimensiones (matriz de correlación, coordenadas paralelas, `pairs`). Una nube de puntos se describe con dos cosas: su forma y **dónde está su centro**. Este módulo atiende lo segundo y abre una pregunta que recorre los módulos siguientes: ¿qué tan lejos está cada cliente de ese centro, cuando la distancia se mide **respetando la forma de la nube** y no con una regla ciega? Corresponde a la sesión 7 del curso (`S06_Clase_Vector_de_Medias.Rmd`).

**Para el negocio:** la Gerencia de Riesgo necesita saber qué es un cliente "típico" de la cartera y cuándo un cliente es "raro" (posible fraude, error de captura o perfil de riesgo atípico). El centroide es la referencia de "lo típico" y la distancia al centroide es la medida de "lo raro". Este módulo muestra que esa referencia tiene trampas: el promedio global puede no representar a nadie, se rompe con errores de captura y la distancia en línea recta engaña.

### 9.1 La matriz de datos y el vector de medias

#### Qué es

La submatriz numérica de la base se trata como una matriz $\mathbf{X}$ de tamaño $n \times p$ (filas = clientes, columnas = variables), no como una simple tabla. El **vector de medias** (o centroide) tiene la media de cada columna:

$$\bar x_j = \frac{1}{n}\sum_{i=1}^{n} x_{ij}, \qquad \bar{\mathbf{x}} = (\bar x_1, \dots, \bar x_p)'$$

y se puede escribir en forma matricial como

$$\bar{\mathbf{x}} = \frac{1}{n}\,\mathbf{X}'\mathbf{1},$$

donde $\mathbf{1}$ es un vector columna de $n$ unos. Intuición: multiplicar $\mathbf{X}'$ por un vector de unos suma cada columna; dividir por $n$ la convierte en promedio.

#### Cómo se aplicó

Se usó el par de variables identificado previamente como el más importante para el análisis bivariado numérico: `Annual_Income` y `Credit_Limit`, con correlación $r = 0.974$.

```r
X_centroide <- as.matrix(credit[, c("Annual_Income", "Credit_Limit")])
n_c <- nrow(X_centroide)
centroide <- colMeans(X_centroide)
uno <- rep(1, n_c)
media_matricial <- (1 / n_c) * t(X_centroide) %*% uno
cbind(colMeans = centroide, forma_matricial = as.vector(media_matricial))
```

Se comparó `colMeans()` (definición por columnas) con el producto matricial $\frac{1}{n}\mathbf{X}'\mathbf{1}$.

#### Resultado

| Variable | `colMeans` | Forma matricial |
|---|---|---|
| Annual_Income | 1 479 317.9 | 1 479 317.9 |
| Credit_Limit | 709 677.2 | 709 677.2 |

Las dos columnas son idénticas hasta el último decimal: el centroide es `Annual_Income` ≈ 1.479.318 ₹ y `Credit_Limit` ≈ 709.677 ₹.

#### Por qué importa

No es una curiosidad algebraica: la forma matricial $\frac{1}{n}\mathbf{X}'\mathbf{1}$ es la que se generaliza después a la distancia de Mahalanobis (Módulo 13). Se verifica aquí para que el resto de la teoría matricial se apoye en algo comprobado con los datos reales.

> Nota de presentación: en varios pasajes del informe los montos aparecen con el símbolo "$", pero todas las variables monetarias están en rupias indias (INR, ₹).

### 9.2 El centroide, geométricamente

#### Qué es

El centroide es el punto que **minimiza la suma de distancias al cuadrado** a toda la nube:

$$\bar{\mathbf{x}} = \arg\min_{\mathbf{a}} \sum_{i=1}^{n} \lVert \mathbf{x}_i - \mathbf{a}\rVert^2$$

No es una definición decorativa: es la razón misma de que el promedio sea el promedio. Cualquier otro punto candidato a "centro" deja, en total, más distancia cuadrática a los clientes.

#### Cómo se aplicó

1. **Gráfico:** dispersión de los 50 000 clientes en el plano `Annual_Income` × `Credit_Limit` (puntos azules semitransparentes, `pch = 19`, `cex = 0.4`) con el centroide marcado con una cruz roja grande (`pch = 4`, color `#B0442F`), título "La nube de 50.000 clientes y su centroide". Muestra visualmente dónde cae el centro en la nube alargada de ingreso–cupo.
2. **Verificación numérica:** se definió la función `suma_cuad(a)` = suma de distancias al cuadrado de todos los clientes al punto `a`, y se evaluó en el centroide y en dos puntos desplazados un 1 % de la desviación estándar de cada variable, hacia arriba y hacia abajo:

```r
suma_cuad <- function(a) sum(rowSums(sweep(X_centroide, 2, a)^2))
sd_c <- apply(X_centroide, 2, sd)
c(en_el_centroide  = suma_cuad(centroide),
  desplazado_mas   = suma_cuad(centroide + 0.01 * sd_c),
  desplazado_menos = suma_cuad(centroide - 0.01 * sd_c))
```

#### Resultado

| Punto evaluado | Suma de distancias al cuadrado |
|---|---|
| En el centroide | 1.50006 × 10¹⁷ |
| Desplazado +1 % de sd | 1.50021 × 10¹⁷ |
| Desplazado −1 % de sd | 1.50021 × 10¹⁷ |

Cualquier desplazamiento, en cualquier dirección, aumenta la suma de distancias al cuadrado. El mínimo está exactamente donde la teoría dice que debe estar. (El aumento es simétrico: ambos desplazamientos dan el mismo valor, como corresponde a una función cuadrática con mínimo en el centroide.)

### 9.3 ¿Un centro o varios? Medias por grupo

#### Qué es

El centroide global describe al **conjunto**, no necesariamente a cada cliente ni a cada segmento. Si la población es una mezcla de subpoblaciones con centros distintos, el promedio global puede caer en una zona donde no hay casi nadie.

#### Cómo se aplicó

Se usó `Card_Type`, la variable categórica que en el Módulo 7 resultó ser la de mayor $\eta^2$ sobre las variables de dinero. Se calcularon las medias por grupo con `aggregate()` y se compararon con las globales:

```r
medias_grupo <- aggregate(cbind(Annual_Income, Credit_Limit, Credit_Score) ~ Card_Type,
                          data = credit, FUN = mean)
```

#### Resultado

Medias por tipo de tarjeta (salida tal como la ordena R, alfabéticamente):

| Card_Type | Annual_Income (₹) | Credit_Limit (₹) | Credit_Score |
|---|---|---|---|
| Basic | 411 787.9 | 74 073.09 | 628.5177 |
| Gold | 1 394 818.9 | 557 586.21 | 626.7820 |
| Platinum | 2 643 462.6 | 1 454 719.10 | 634.2303 |
| Signature | 5 487 830.9 | 4 114 792.73 | 637.3171 |
| Silver | 873 847.2 | 244 612.14 | 627.1335 |

Medias globales:

| Global_Annual_Income | Global_Credit_Limit | Global_Credit_Score |
|---|---|---|
| 1 479 317.9136 | 709 677.2200 | 628.9846 |

#### Interpretación

- **`Credit_Limit`: el centroide global (709.677 ₹) no representa a nadie.** Un cliente `Basic` tiene en promedio 74.073 ₹ de cupo —casi una décima parte del promedio global— mientras que uno `Signature` tiene 4.114.793 ₹, casi seis veces el promedio. Es la misma historia que el $\eta^2 = 0.80$ del Módulo 7, vista ahora directamente en las medias: **hay cinco centros, no uno**.
- **`Credit_Score`: sí existe un solo centro real.** Los cinco promedios de grupo van de 626.8 a 637.3, todos pegados al promedio global de 629. Es consistente con que `Card_Type` explica apenas el 0.23 % de la varianza del puntaje.

**Para el negocio:** hablar del "cupo promedio de la cartera" es engañoso; cualquier referencia de cupo o ingreso "normal" debe darse por segmento de tarjeta. En cambio, para el puntaje de crédito sí tiene sentido una referencia única de cartera: el tipo de tarjeta no segmenta el riesgo.

### 9.4 Fragilidad de la media ante atípicos, y alternativas robustas

#### Qué es

La media usa todos los valores con el mismo peso, por lo que un valor extremo la arrastra. Su **punto de ruptura** (la fracción de datos contaminados que basta para llevarla a cualquier valor) es prácticamente cero. Las alternativas **robustas** resisten esa contaminación:

- **Mediana marginal:** la mediana de cada variable por separado.
- **Media recortada al 10 %:** se descarta el 10 % más bajo y el 10 % más alto y se promedia el resto (`mean(x, trim = 0.10)`).

#### Cómo se aplicó: dos escenarios simulados de corrupción

Sobre `Annual_Income`, **siempre sobre una copia y nunca sobre el `credit` original**:

- **Escenario A — un solo error de digitación:** a la fila 1 se le multiplica el ingreso por 100 (equivale a "pegarle" ceros de más). `Xa[1] <- Xa[1] * 100`.
- **Escenario B — bug sistemático de unidades en el 0.5 % de las filas:** con `set.seed(1)` se eligen al azar 250 de las 50 000 filas (`round(0.005 * 50000)`) y su ingreso se multiplica por 1000 (simula una conversión de unidades mal aplicada, p. ej. miles de rupias tomadas como rupias).

Se compararon media, mediana marginal y media recortada al 10 % en el original y en cada escenario.

#### Resultado

| Estadístico | Original | Escenario A (1 fila) | Escenario B (250 filas) |
|---|---|---|---|
| Media | 1 479 318 | 1 480 877 | 8 040 387 |
| Mediana marginal | 1 127 630 | 1 127 651 | 1 133 216 |
| Media recortada 10 % | 1 186 498 | 1 186 547 | 1 196 623 |

#### Interpretación

- Con **un solo** registro corrupto de 50 000 (0.002 % de las filas), la media apenas se mueve 1.559 unidades (0.11 % del total): la $n$ grande diluye un error aislado.
- Con un **bug sistemático** en 250 filas (0.5 % de la cartera; el tipo de error que S02 advertía con los códigos de faltante y las conversiones de unidad), la media salta de 1.479.318 ₹ a 8.040.387 ₹, **un aumento del 444 %**.
- La **mediana marginal** prácticamente no se entera en ninguno de los dos escenarios (pasa de 1.127.630 ₹ a apenas 1.133.216 ₹ en el peor caso), y la **media recortada al 10 %** queda en un punto intermedio (de 1.186.498 ₹ a 1.196.623 ₹).
- Advertencia de la clase, confirmada con números reales: **la mediana marginal no es la mediana multivariante** (se calcula columna por columna y el punto resultante puede no corresponder a ningún cliente), pero es la que hay que mirar cuando se sospecha un error de captura, no la media.
- Observación adicional implícita en los datos: incluso en el original, la media (1.48 M) está muy por encima de la mediana (1.13 M), reflejo de la asimetría a la derecha del ingreso.

**Para el negocio:** un fallo de integración que afecte a una fracción mínima de registros puede multiplicar por cinco el "ingreso promedio" reportado y distorsionar cualquier política de cupos basada en promedios. Los tableros de monitoreo de cartera deberían reportar la mediana (o la media recortada) junto a la media; una divergencia súbita entre ambas es una alarma de calidad de datos.

### 9.5 Por qué la distancia euclidiana no basta

#### Qué es

La **distancia euclidiana** al centroide es la distancia "en línea recta":

$$d_E(\mathbf{x}, \bar{\mathbf{x}}) = \sqrt{(\mathbf{x}-\bar{\mathbf{x}})'(\mathbf{x}-\bar{\mathbf{x}})}$$

Trata todas las direcciones por igual e **ignora que las variables están correlacionadas**. La **distancia de Mahalanobis** incorpora la forma de la nube a través de la inversa de la matriz de covarianzas:

$$d_M(\mathbf{x}, \bar{\mathbf{x}}) = \sqrt{(\mathbf{x}-\bar{\mathbf{x}})'\,\mathbf{S}^{-1}\,(\mathbf{x}-\bar{\mathbf{x}})}$$

Intuición: la nube de ingreso–cupo no es un círculo sino una elipse muy alargada (correlación 0.974). Alejarse a lo largo del eje de la elipse es "normal"; alejarse perpendicularmente a ese eje es raro, aunque la distancia en línea recta sea la misma.

#### Cómo se aplicó

Se construyeron dos **clientes hipotéticos** a la misma distancia euclidiana del centroide:

- **Punto A:** centroide + (0.5·sd de ingreso, **+**0.5·sd de cupo) → ingreso alto, cupo alto: **a favor** de la correlación.
- **Punto B:** centroide + (0.5·sd de ingreso, **−**0.5·sd de cupo) → ingreso alto, cupo bajo: **en contra** de la correlación.

Se calcularon ambas distancias; la de Mahalanobis con `mahalanobis()` y `S_ai_cl <- cov(X_centroide)` (la función devuelve la distancia al cuadrado, por eso se toma `sqrt`).

#### Resultado

| | A (a favor de r) | B (en contra de r) |
|---|---|---|
| Euclidiana | 866 051 | 866 051 |
| Mahalanobis | 0.503 | 4.399 |

**Gráfico:** "Misma distancia euclidiana, forma de la nube distinta": la nube ingreso–cupo con el centroide (cruz negra), A en verde (`#1E7F63`) sobre la diagonal de la nube y B en rojo (`#B0442F`) por debajo, fuera de la elipse.

#### Interpretación

A y B están, por construcción, exactamente a la misma distancia euclidiana del centroide (866.051 en ambos casos). Pero A sigue la dirección natural de la correlación de $r = 0.974$ y su distancia de Mahalanobis es apenas 0.5; B va en contra y su distancia de Mahalanobis es 4.4, **casi 8.7 veces mayor**. La regla euclidiana ve a A y B como igual de "raros"; la que respeta la forma de la nube (la elipse de correlación, no el círculo) sabe que solo B lo es de verdad. Es formalmente la misma idea del "punto imposible" del Módulo 7, ahora con una distancia que lo **mide** en vez de solo mostrarlo.

Además, la distancia euclidiana en rupias está dominada por la variable de mayor escala (el ingreso), otro defecto que Mahalanobis corrige al dividir por las varianzas.

La pieza que falta para medir así sobre toda la cartera es $\mathbf{S}^{-1}$: hay que definir la matriz de covarianzas, ver sus propiedades y comprobar que se puede invertir (Módulo 10). La distancia de Mahalanobis sobre los 50 000 clientes, con su prueba $\chi^2$ y su gráfico Q-Q, es el Módulo 13.

**Para el negocio:** un cliente con ingreso alto y cupo bajo (B) es justamente el tipo de caso que merece revisión (cupo mal asignado, ingreso declarado inflado o error de captura). Un sistema de alertas basado en distancia euclidiana no lo distinguiría de un cliente perfectamente coherente (A).

### 9.6 Conclusión del Módulo 9

- $\bar{\mathbf{x}} = \frac{1}{n}\mathbf{X}'\mathbf{1}$ es el centroide: el punto que minimiza la suma de distancias al cuadrado a la nube, verificado numéricamente sobre `Annual_Income`/`Credit_Limit`.
- **El centroide describe al conjunto, no a cada segmento:** representa bien a `Credit_Score` (grupos de `Card_Type` casi idénticos) y representa mal a `Credit_Limit` (grupos de `Card_Type` con medias que van de 74.073 ₹ a 4.114.793 ₹).
- **La media tiene punto de ruptura próximo a cero** frente a errores sistemáticos (250 filas de 50 000 bastan para dispararla un 444 %), mientras que la mediana marginal y la media recortada resisten. Ninguna de las dos reemplaza, sin embargo, a una mediana multivariante genuina.
- **La distancia euclidiana ignora la correlación entre variables;** la de Mahalanobis la incorpora a través de $\mathbf{S}^{-1}$, y por eso distingue a un cliente "raro" de uno perfectamente típico aunque ambos estén a la misma distancia en línea recta del centro. Para usarla sobre toda la cartera hace falta $\mathbf{S}$, tema del módulo siguiente.

---

## Módulo 10: Dispersión y dependencia — la matriz de covarianzas (S07)

### Contexto y propósito del módulo

El Módulo 9 dejó la nube con un centro, $\bar{\mathbf{x}}$, y una pregunta abierta: para medir qué tan lejos está un cliente del centro respetando la forma de la nube hace falta $\mathbf{S}^{-1}$. Este módulo:

1. define $\mathbf{S}$;
2. demuestra con los datos sus tres propiedades;
3. muestra el problema de unidades que obliga a pasar a $\mathbf{R}$ (la matriz de correlación del Módulo 8);
4. resume la dispersión total con traza y determinante y descubre la singularidad causada por `Monthly_Spending`;
5. termina verificando que, con las variables correctas, $\mathbf{S}$ sí se puede invertir.

Con esto la nube queda completamente descrita: el **centro** ($\bar{\mathbf{x}}$) y la **forma** ($\mathbf{S}$). Corresponde a la sesión S07.

### 10.1 Definición y forma matricial

#### Qué es

La **matriz de covarianzas muestral** reúne en una sola tabla todas las varianzas (diagonal) y covarianzas (fuera de la diagonal):

$$\mathbf{S} = \begin{pmatrix}
s_1^2 & s_{12} & \cdots & s_{1p}\\
s_{21} & s_2^2 & \cdots & s_{2p}\\
\vdots & \vdots & \ddots & \vdots\\
s_{p1} & s_{p2} & \cdots & s_p^2
\end{pmatrix}
\qquad
\mathbf{S} = \frac{1}{n-1}\,\mathbf{X}_c'\,\mathbf{X}_c$$

donde $\mathbf{X}_c$ es la **matriz centrada** (a cada columna se le resta su media) y $s_{jk} = \frac{1}{n-1}\sum_i (x_{ij}-\bar x_j)(x_{ik}-\bar x_k)$.

- **Varianza** $s_j^2$: cuánto se dispersa una variable alrededor de su media.
- **Covarianza** $s_{jk}$: si dos variables tienden a estar a la vez por encima (o por debajo) de sus medias (positiva) o en lados opuestos (negativa).
- **Corrección de Bessel:** se divide por $n-1$ y no por $n$ porque la media se estimó con los mismos datos, y eso "gasta" un grado de libertad.

#### Cómo se aplicó

Se trabajó con cuatro variables que resumen la historia del informe: **capacidad** (`Annual_Income`, `Credit_Limit`), **deuda** (`Statement_Balance`) y **riesgo** (`Credit_Score`). Se centró la matriz con `scale(X_S, center = TRUE, scale = FALSE)` (centrar, **no** escalar), se calculó $\mathbf{X}_c'\mathbf{X}_c/(n-1)$ y se comparó con `cov()`.

#### Resultado (con 3 cifras significativas)

| | Annual_Income | Credit_Limit | Statement_Balance | Credit_Score |
|---|---|---|---|---|
| **Annual_Income** | 1.98e+12 | 1.38e+12 | 6.88e+11 | 3 120 000 |
| **Credit_Limit** | 1.38e+12 | 1.02e+12 | 5.05e+11 | 2 450 000 |
| **Statement_Balance** | 6.88e+11 | 5.05e+11 | 3.13e+11 | −4 810 000 |
| **Credit_Score** | 3.12e+06 | 2.45e+06 | −4.81e+06 | 4 680 |

`all.equal(S_matricial, cov(X_S), check.attributes = FALSE)` → `TRUE`.

#### Interpretación

- Las dos formas (matricial y `cov()`) dan la misma matriz.
- En la diagonal están las varianzas: la de `Annual_Income` es del orden de $10^{12}$ rupias², la de `Credit_Score` apenas 4.685 puntos².
- La covarianza de `Statement_Balance` con `Credit_Score` es la **única negativa** de la tabla: a más deuda facturada, menor puntaje; la misma dirección que se vio con `Credit_Utilization` en el Módulo 7.

### 10.2 Las tres propiedades, y por qué la tercera es el PCA

#### Qué son

1. **La diagonal son las varianzas**, porque $s_{jj} = s_j^2$.
2. **Es simétrica** ($s_{jk} = s_{kj}$), porque $(x_{ij}-\bar x_j)(x_{ik}-\bar x_k)$ no depende del orden.
3. **Es semidefinida positiva:** para cualquier vector de pesos $\mathbf{a}$, $\mathbf{a}'\mathbf{S}\mathbf{a} \ge 0$ (equivalente: todos sus valores propios son $\ge 0$).

#### Cómo se aplicó

```r
S4 <- cov(X_S)
c(diagonal_son_varianzas = isTRUE(all.equal(diag(S4), apply(X_S, 2, var), check.attributes = FALSE)),
  es_simetrica           = isSymmetric(S4),
  semidefinida_positiva  = all(eigen(S4)$values >= -1e-8 * max(eigen(S4)$values)))
```

La semidefinición positiva se comprobó con los valores propios usando una tolerancia relativa (`-1e-8 × mayor valor propio`) para no confundir errores de redondeo en coma flotante con valores negativos reales.

Resultado: `diagonal_son_varianzas = TRUE`, `es_simetrica = TRUE`, `semidefinida_positiva = TRUE`.

#### La tercera propiedad, con significado de negocio

Se tomó la combinación lineal **"ingreso menos cupo"**, $\mathbf{a} = (1, -1, 0, 0)'$: la parte del ingreso que el banco **no** convirtió en cupo. Se calculó su varianza de dos formas:

```r
a <- c(1, -1, 0, 0)
combinacion <- as.vector(X_S %*% a)   # Annual_Income - Credit_Limit, cliente por cliente
c(varianza_directa = var(combinacion), formula_a_S_a = as.numeric(t(a) %*% S4 %*% a))
```

| Varianza directa | $\mathbf{a}'\mathbf{S}\mathbf{a}$ |
|---|---|
| 231 356 130 197 | 231 356 130 197 |

**Interpretación:** $\mathbf{a}'\mathbf{S}\mathbf{a}$ es la varianza de la combinación lineal $\mathbf{X}\mathbf{a}$, y como ninguna varianza puede ser negativa, $\mathbf{S}$ tiene que ser semidefinida positiva. Aquí está el **PCA completo, adelantado**: buscar la combinación de variables que más separa a los clientes es maximizar $\mathbf{a}'\mathbf{S}\mathbf{a}$ sujeto a $\mathbf{a}'\mathbf{a} = 1$, y la solución es el vector propio de $\mathbf{S}$ asociado al mayor valor propio. Es exactamente lo que hacen los Módulos 16 y 17.

### 10.3 El problema de unidades, y por qué el informe trabaja con R

#### Qué es

La covarianza depende de las unidades de medida: si una variable se reexpresa en miles, su covarianza con cualquier otra se divide por mil. La **correlación** no depende de las unidades, porque divide la covarianza por las desviaciones estándar:

$$r_{jk}=\frac{s_{jk}}{s_j s_k}
\qquad\Longrightarrow\qquad
\mathbf{R}=\mathbf{D}^{-1/2}\,\mathbf{S}\,\mathbf{D}^{-1/2},
\qquad \mathbf{D}=\operatorname{diag}(s_1^2,\dots,s_p^2)$$

#### Cómo se aplicó

1. **Cambio de unidades:** se pasó `Annual_Income` de rupias a miles de rupias (dividido por 1000) y se recalculó covarianza y correlación con `Credit_Limit`.

| | Covarianza | Correlación |
|---|---|---|
| En rupias | 1.384412e+12 | 0.9741659 |
| En miles | 1.384412e+09 | 0.9741659 |

La covarianza se divide por mil; la correlación no se mueve.

2. **Dominancia por escala:** fracción de la varianza total (traza de $\mathbf{S}$) que se lleva cada variable, `100 * diag(S4) / sum(diag(S4))`:

| Variable | % de la varianza total en $\mathbf{S}$ |
|---|---|
| Annual_Income | 59.7709 |
| Credit_Limit | 30.7794 |
| Statement_Balance | 9.4497 |
| Credit_Score | 0.0000 (≈ 0.00000014 %) |

`Annual_Income` sola se lleva el 59.8 % de la varianza total y `Credit_Score` el 0.00000014 %. Cualquier técnica que trabaje sobre $\mathbf{S}$ con estas unidades mezcladas —un PCA sin estandarizar, por ejemplo— va a "descubrir" que lo importante de la cartera es el ingreso **solo porque se mide en números más grandes**.

3. **Corrección: estandarizar.** Se construyó $\mathbf{D}^{-1/2}$ con `diag(1 / sqrt(diag(S4)))` y se calculó $\mathbf{R} = \mathbf{D}^{-1/2}\mathbf{S}\mathbf{D}^{-1/2}$:

| | Annual_Income | Credit_Limit | Statement_Balance | Credit_Score |
|---|---|---|---|---|
| **Annual_Income** | 1.000 | 0.974 | 0.874 | 0.032 |
| **Credit_Limit** | 0.974 | 1.000 | 0.894 | 0.035 |
| **Statement_Balance** | 0.874 | 0.894 | 1.000 | −0.125 |
| **Credit_Score** | 0.032 | 0.035 | −0.125 | 1.000 |

Verificaciones: `R_igual_a_cor = TRUE` (reproduce `cor()` exactamente) y `cov_de_Z_igual_a_R = TRUE` (la covarianza de los datos tipificados con `scale()` también es $\mathbf{R}$).

#### Interpretación

**La matriz de correlación es la matriz de covarianzas de los datos estandarizados.** Es la misma operación que el Módulo 6 hizo con los boxplots (estandarizar para comparar), ahora escrita como álgebra matricial. Se aprecian además las relaciones de fondo: capacidad y deuda casi colineales (0.87–0.97) y el puntaje prácticamente desconectado de ellas salvo una leve relación negativa con el saldo facturado (−0.125).

#### Decisión: S o R

| | Usar $\mathbf{S}$ | Usar $\mathbf{R}$ |
|---|---|---|
| **Cuándo** | Todas las variables en la misma unidad, y las diferencias de escala son información | Unidades distintas, o una variable domina por su magnitud |
| **En esta cartera** | Nunca: hay rupias, conteos, meses, años, proporciones y un puntaje | Siempre |
| **En PCA** | Componentes sobre covarianzas | PCA normado (Módulos 16 y 17) |

**Por qué el informe trabaja con R:** la base mezcla rupias (con varianzas de $10^{12}$), conteos, meses, años, proporciones y un puntaje; sobre $\mathbf{S}$, el resultado de cualquier técnica reflejaría las unidades y no la estructura de la cartera.

### 10.4 Dos resúmenes de la dispersión total: traza y determinante

#### Qué son

Con $p$ variables hay $p$ varianzas; a veces hace falta un solo número:

- **Varianza total** = **traza**: $\operatorname{tr}(\mathbf{S}) = \sum_j s_j^2$ = suma de los valores propios. Suma las dispersiones individuales e **ignora las covarianzas**.
- **Varianza generalizada** = **determinante**: $|\mathbf{S}| = \prod_j \lambda_j$ = producto de los valores propios. Mide el "volumen" de la nube y **sí tiene en cuenta las covarianzas**: si la nube es plana en alguna dirección (un valor propio ≈ 0), el determinante ≈ 0.

#### Cómo se aplicó

Como $\mathbf{S}$ en rupias está dominada por el ingreso, ambos resúmenes se calcularon sobre $\mathbf{R}$ (la covarianza de los datos estandarizados), primero con las **26 variables numéricas** y después **sin las cinco columnas derivadas o duplicadas** que el Módulo 8 ya había señalado: `Monthly_Spending`, `Payment_Ratio`, `Credit_Utilization`, `Reward_Points_Earned`, `Outstanding_Balance`. También se reportó el menor valor propio.

#### Resultado

| Matriz | p | Varianza total (traza) | Varianza generalizada (det) | Menor valor propio |
|---|---|---|---|---|
| R con las 26 numéricas | 26 | 26 | 8.65 × 10⁻³⁰ | 6.56 × 10⁻¹⁵ |
| R sin las 5 derivadas (21) | 21 | 21 | 1.75 × 10⁻⁸ | 1.80 × 10⁻² (0.018) |

Comprobación de la causa: `max(abs(credit$Monthly_Spending - rowSums(credit[, cat_gasto])))` = **0.03**, donde `cat_gasto` son las siete categorías de gasto: `Online_Shopping_Spending`, `Grocery_Spending`, `Fuel_Spending`, `Dining_Spending`, `Travel_Spending`, `Entertainment_Spending`, `Utility_Bill_Spending`.

#### Interpretación

- **La traza vale exactamente $p$ en las dos matrices** (cada variable estandarizada aporta 1) y no se entera de nada: ignora las covarianzas.
- **El determinante con las 26 variables es 8.7 × 10⁻³⁰, prácticamente cero**, y su menor valor propio también. La razón es literal: **`Monthly_Spending` es la suma de las siete categorías de gasto** (la diferencia máxima entre ambas es 0.03 rupias, puro redondeo), así que la nube de 26 dimensiones es **plana en al menos una dirección**: vive en menos dimensiones de las que dice tener.
- **Quitando las cinco derivadas el determinante sube a 1.8 × 10⁻⁸.** Sigue siendo pequeño porque es el producto de 21 valores propios y varios son menores que 1 (las variables de dinero siguen muy correlacionadas). El indicador que importa es el **menor valor propio**, que pasa de 6.6 × 10⁻¹⁵ —un cero numérico— a 0.018: ya no queda ninguna dirección plana.
- Un determinante casi nulo es la señal de **multicolinealidad**, y es exactamente lo que hace que $\mathbf{S}^{-1}$ no exista o sea inestable; la distancia de Mahalanobis la necesita.
- La traza reaparecerá en el PCA: la suma de los valores propios es la traza, es decir, la información total que las componentes se reparten.

**Para el negocio:** la base trae columnas que son cálculos de otras (totales, ratios). No aportan información nueva y, si se meten en un modelo multivariante, lo rompen numéricamente. Es una cuestión de diseño de datos que la Gerencia debería conocer al construir modelos internos.

### 10.5 Antes de invertir S: verificación de la submatriz

#### Qué se hizo

Antes de calcular covarianzas y distancias de Mahalanobis sobre toda la cartera hay que verificar que la submatriz numérica sea invertible. Se escribió la función `revisar(ruta, quitar)` que lee el CSV, se queda con las columnas numéricas (excluyendo las indicadas) y revisa **cinco puntos críticos**:

1. **Variables numéricas utilizadas** (cuántas y cuáles).
2. **Relación $n/p$:** ≥ 10 "OK", entre 5 y 10 "justo", < 5 "PROBLEMA".
3. **Datos faltantes:** porcentaje y número de filas completas (≥ 100 "OK").
4. **Estructura correlacional:** $|r|$ máxima fuera de la diagonal (≥ 0.5 "OK", 0.3–0.5 "justo", < 0.3 "PROBLEMA") y número de pares con $|r| > 0.5$. Sin correlaciones apreciables no tiene sentido un análisis multivariante.
5. **Redundancia:** **número de condición** = mayor valor propio / menor valor propio de la covarianza de los datos **estandarizados**; < 1000 "OK", 1000–10⁵ "revisar", ≥ 10⁵ "REDUNDANCIA". Si es ≥ 1000, lista los pares con $|r| > 0.95$ ("pares casi idénticos").

Se aplicó sobre `../data/bronze/synthetic_credit_card_customer_behavior_dataset.csv` quitando las cinco variables excluidas.

#### Resultado

```
1. variables numéricas usadas: 21
   Age, Annual_Income, Credit_Limit, Card_Age_Months, Monthly_Transactions,
   Avg_Transaction_Value, Online_Shopping_Spending, Grocery_Spending, Fuel_Spending,
   Dining_Spending, Travel_Spending, Entertainment_Spending, Utility_Bill_Spending,
   Statement_Balance, Payment_Amount, Cash_Advance_Amount, EMI_Count,
   International_Transactions, Reward_Points_Redeemed, Mobile_App_Login, Credit_Score
2. n = 50000 | p = 21 | n/p = 2381  OK
3. faltantes: 0 % | filas completas: 50000  OK
4. |r| máxima: 0.97  OK
   pares con |r|>0.5: 75
5. número de condición (sobre datos estandarizados): 560  OK
```

#### Decisiones y por qué

| Variable excluida | Motivo |
|---|---|
| `Monthly_Spending` | Es la suma exacta de las siete categorías de gasto |
| `Payment_Ratio` | Derivada: = `Payment_Amount` / `Statement_Balance` |
| `Credit_Utilization` | Derivada: = `Outstanding_Balance` / `Credit_Limit` |
| `Reward_Points_Earned` | Correlación casi perfecta con el gasto |
| `Outstanding_Balance` | Correlación casi perfecta con el saldo facturado (`Statement_Balance`) |

Las tres primeras son columnas derivadas que no aportan información nueva y vuelven singular la matriz de covarianzas; las dos últimas se retiran por redundancia casi perfecta.

**Por qué el número de condición se calcula sobre datos estandarizados:** en su escala original las variables monetarias (cientos de miles) y los conteos (0 a 30) lo inflarían artificialmente sin que exista redundancia real.

**Lectura:** sobre las 21 variables restantes, $n/p$ es enorme (2381 observaciones por variable), cero faltantes, correlación estructural suficiente ($|r|$ máxima 0.97, muy por encima de 0.5, con 75 pares por encima de 0.5) y un número de condición (560) que, aunque no es 1, está lejos de la zona de redundancia severa: **la matriz es invertible y está lista para Mahalanobis**.

### 10.6 Conclusión del Módulo 10

- $\mathbf{S} = \frac{1}{n-1}\mathbf{X}_c'\mathbf{X}_c$ tiene las varianzas en la diagonal, es simétrica y es **semidefinida positiva**, porque $\mathbf{a}'\mathbf{S}\mathbf{a}$ es la varianza de la combinación $\mathbf{X}\mathbf{a}$ —verificado con "ingreso menos cupo"—. Maximizar esa varianza es el PCA de los Módulos 16 y 17.
- **La covarianza depende de las unidades y la correlación no.** Con solo cuatro variables, `Annual_Income` se lleva el 60 % de la varianza total de $\mathbf{S}$ y `Credit_Score` prácticamente nada, solo por las unidades; por eso el informe trabaja con $\mathbf{R}=\mathbf{D}^{-1/2}\mathbf{S}\mathbf{D}^{-1/2}$, que es la covarianza de los datos estandarizados.
- **Traza = varianza total**, ciega a la dependencia. **Determinante = varianza generalizada:** con las 26 numéricas es prácticamente cero porque `Monthly_Spending` es la suma exacta de sus categorías.
- Sin las cinco columnas derivadas o duplicadas, **la submatriz de 21 variables es invertible**: es la que usan Mahalanobis (Módulo 13) y el PCA (Módulos 15 a 17).

---

## Módulo 11: Variable aleatoria multivariante — distribución conjunta y marginales (S08 y S09)

### Contexto y propósito del módulo

Hasta el Módulo 10 el trabajo fue **descriptivo**: la nube de 50 000 clientes quedó resumida por su centro $\bar{\mathbf{x}}$ y su forma $\mathbf{S}$. Aquí cambia la pregunta: ya no es "¿cómo resumo estos datos?" sino "**¿de qué mecanismo salieron?**". Ese mecanismo es la **distribución conjunta** del vector aleatorio $\mathbf{X} = (X_1, \dots, X_p)'$. $\bar{\mathbf{x}}$ y $\mathbf{S}$ dejan de ser el objeto de estudio y pasan a ser dos resúmenes de algo más grande: sus dos primeros momentos (media y covarianza).

**Variable aleatoria multivariante:** un vector de variables aleatorias que se observan juntas sobre el mismo individuo (aquí, las 30 columnas de cada cliente). Su comportamiento completo lo describe la distribución conjunta; cada variable por separado tiene su distribución marginal.

La pregunta que ordena el módulo es la de la sesión S08:

> **¿Basta con conocer cada variable por separado para conocerlas juntas?**

### 11.1 Caso discreto: la conjunta es una tabla

#### Qué es

Con dos variables discretas, la **distribución conjunta** es la tabla de doble entrada de proporciones:

$$p_{jk} = P(\text{Card\_Type} = j,\ \text{Riesgo} = k), \qquad \sum_j\sum_k p_{jk} = 1$$

#### Cómo se aplicó

Para el banco, el riesgo no se lee punto por punto del `Credit_Score` sino por **bandas**. Se usaron los cortes habituales de la industria:

| Banda de riesgo | Credit_Score |
|---|---|
| Alto | menos de 580 |
| Medio | 580 a 669 |
| Bajo | 670 a 739 |
| Muy bajo | 740 o más |

(`cut(credit$Credit_Score, breaks = c(-Inf, 579, 669, 739, Inf))`). La banda se cruzó con el tipo de tarjeta, ordenado `Basic < Silver < Gold < Platinum < Signature`, con `table()` y `addmargins()`.

#### Resultado: conteos

| Card_Type | Alto | Medio | Bajo | Muy bajo | Total |
|---|---|---|---|---|---|
| Basic | 2 359 | 4 700 | 3 027 | 175 | 10 261 |
| Silver | 2 888 | 5 441 | 3 533 | 194 | 12 056 |
| Gold | 3 979 | 7 728 | 4 930 | 258 | 16 895 |
| Platinum | 1 710 | 3 651 | 2 688 | 235 | 8 284 |
| Signature | 513 | 1 064 | 834 | 93 | 2 504 |
| **Total** | **11 449** | **22 584** | **15 012** | **955** | **50 000** |

#### Resultado: distribución conjunta (en %)

| Card_Type | Alto | Medio | Bajo | Muy bajo |
|---|---|---|---|---|
| Basic | 4.72 | 9.40 | 6.05 | 0.35 |
| Silver | 5.78 | 10.88 | 7.07 | 0.39 |
| Gold | 7.96 | 15.46 | 9.86 | 0.52 |
| Platinum | 3.42 | 7.30 | 5.38 | 0.47 |
| Signature | 1.03 | 2.13 | 1.67 | 0.19 |

`sum(conjunta_tr)` = 1.

**Lectura:** cada casilla es la proporción de clientes con esa combinación de tarjeta y banda de riesgo; la más poblada es **Gold · riesgo medio, con el 15.5 % de la cartera**. La tabla suma 1: es una distribución de probabilidad legítima sobre las 20 combinaciones posibles.

### 11.2 Las marginales viven en los márgenes

#### Qué es

La **distribución marginal** se llama así literalmente porque se escribe en el margen de la tabla. Se obtiene **sumando en la dirección de la variable que se quiere eliminar**:

$$p_{j\cdot} = \sum_k p_{jk} \qquad\qquad p_{\cdot k} = \sum_j p_{jk}$$

#### Cómo se aplicó

`rowSums(conjunta_tr)` (se suma sobre el riesgo → queda la tarjeta) y `colSums(conjunta_tr)` (se suma sobre la tarjeta → queda el riesgo). Se graficaron como dos diagramas de barras grises lado a lado: "Marginal de Card_Type" y "Marginal de la banda de riesgo" (eje en %).

#### Resultado

Marginal de `Card_Type` (%):

| Basic | Silver | Gold | Platinum | Signature |
|---|---|---|---|---|
| 20.5 | 24.1 | 33.8 | 16.6 | 5.0 |

Marginal de la banda de riesgo (%):

| Alto | Medio | Bajo | Muy bajo |
|---|---|---|---|
| 22.9 | 45.2 | 30.0 | 1.9 |

**Lectura:** el 22.9 % de la cartera está en **riesgo alto** y apenas el 1.9 % en **muy bajo**; Gold es la tarjeta más común (33.8 %) y Signature la más rara (5 %). Cada marginal es una distribución de una sola variable (no negativa, suma 1). **Cada histograma y cada tabla de frecuencias de los Módulos 2 y 3 eran exactamente esto: marginales empíricas**, calculadas "integrando", sin decirlo, sobre las otras 29 columnas.

**Para el negocio:** casi uno de cada cuatro clientes está en la banda de riesgo alto (puntaje < 580), y la banda de mejor calidad es casi inexistente (1.9 %). Es una cartera con un perfil de riesgo exigente.

### 11.3 Las marginales no reconstruyen la conjunta (S09)

#### Qué es

Si dos variables fueran **independientes**, la conjunta sería el producto de las marginales en todas las casillas:

$$p_{jk} = p_{j\cdot}\,p_{\cdot k}$$

Cuando no lo son, conocer las marginales no basta para recuperar la conjunta.

#### Cómo se aplicó

Se definió `desvio_de_independencia(tab)`: calcula la tabla de proporciones, el producto exterior de sus marginales (`outer(rowSums(f), colSums(f))`, "lo que habría si fueran independientes") y el máximo desvío absoluto. Se aplicó a dos pares de categóricas: **tarjeta × banda de riesgo** y **ocupación × tarjeta**.

#### Resultado

| Par | Máximo desvío |p_jk − p_j· p_·k| |
|---|---|
| Tarjeta vs. riesgo | 0.004016237 (0.4 pp) |
| Ocupación vs. tarjeta | 0.062310752 (6.2 pp) |

Para ocupación × tarjeta, casilla por casilla (conjunta real menos producto de marginales, en puntos porcentuales):

| Occupation | Basic | Silver | Gold | Platinum | Signature |
|---|---|---|---|---|---|
| Business Owner | −2.48 | −2.52 | −2.19 | 2.79 | 4.40 |
| Government Employee | −1.83 | 0.50 | 1.90 | 0.19 | −0.76 |
| Private Employee | −1.40 | 3.38 | 2.45 | −2.33 | −2.10 |
| Retired | 1.08 | 1.35 | −0.68 | −1.34 | −0.41 |
| Self-Employed | −1.60 | −0.82 | 1.17 | 1.99 | −0.75 |
| Student | 6.23 | −1.89 | −2.65 | −1.30 | −0.39 |

#### Interpretación

Los dos pares se comportan de forma opuesta:

- **Tarjeta × riesgo:** ninguna casilla se aparta del producto de las marginales más de 0.4 puntos porcentuales. Con las dos marginales en la mano se reconstruye la tabla casi perfectamente, porque el tipo de tarjeta casi no dice nada del riesgo (lo mismo que mostró el $\eta^2$ del Módulo 7).
- **Ocupación × tarjeta:** el desvío llega a 6.2 puntos. Hay casillas que el producto de marginales llena y que en la cartera están vacías: **ningún `Student` tiene una tarjeta distinta de `Basic`, y ningún `Business Owner` tiene una `Basic`**. Con las dos marginales no hay forma de recuperar esa estructura: la información de cómo se combinan las variables se perdió al sumar. **Las marginales son una proyección, y las proyecciones no se invierten.**

**Para el negocio:** la asignación de tipo de tarjeta sigue reglas fuertes por ocupación (estudiantes solo Basic; empresarios nunca Basic, mayoritariamente Platinum/Signature). Cualquier comparación entre tarjetas lleva implícita una comparación entre ocupaciones.

### 11.4 Caso continuo: la conjunta es una superficie

#### Qué es

Con variables continuas la tabla se vuelve una **densidad conjunta** $f(x, y)$ y la suma se vuelve integral, con la misma lógica:

$$f_X(x) = \int_{-\infty}^{\infty} f(x,y)\, dy \qquad\qquad f_Y(y) = \int_{-\infty}^{\infty} f(x,y)\, dx$$

#### Cómo se aplicó

Se tomó el **par de riesgo del Módulo 7**: `Credit_Utilization` (proporción del cupo usada) y `Credit_Score`. Panel de tres gráficos:

1. Histograma (40 clases) de `Credit_Utilization` — marginal.
2. Histograma (40 clases) de `Credit_Score` — marginal.
3. `smoothScatter()` de la nube conjunta (densidad suavizada), con líneas punteadas en las dos medias.

#### Interpretación

Ninguno de los dos histogramas dice que los clientes que usan más cupo tienen peor puntaje; la tercera figura lo muestra a simple vista, con **la nube inclinada hacia abajo**. **Toda la información sobre la relación está en la conjunta, y ninguna marginal la contiene.**

### 11.5 La prueba de que las marginales no determinan la conjunta: barajar

#### Qué es

**Barajar** (permutar) `Credit_Score` es reordenar sus valores al azar entre los clientes. Barajar no cambia qué valores hay ni cuántas veces aparece cada uno —**las dos marginales quedan idénticas**—; lo único que destruye es **con quién estaba emparejado cada valor**, es decir, la conjunta. Es un experimento que separa limpiamente "marginales" de "dependencia".

#### Cómo se aplicó

`set.seed(7); cs_barajado <- sample(cs)`. Se compararon media, desviación y mediana del puntaje antes y después; y, para la conjunta, la correlación de Pearson con `Credit_Utilization` y la proporción de **concordantes** (clientes que están del mismo lado de la media en las dos variables), con la función `concordantes(x, y) = mean((x > mean(x)) == (y > mean(y)))`. Se graficaron dos `smoothScatter` lado a lado: "Conjunta real (r = −0.60)" y "Barajada (r = 0.00)".

#### Resultado

Marginales:

| | Media | Desviación | Mediana |
|---|---|---|---|
| Original | 628.9846 | 68.44425 | 638 |
| Barajado | 628.9846 | 68.44425 | 638 |

Conjunta:

| | r | Concordantes |
|---|---|---|
| Original | −0.5993382589 | 0.28980 |
| Barajado | 0.0007766297 | 0.49424 |

#### Interpretación

Media, desviación y mediana del puntaje son idénticas antes y después de barajar, pero la correlación pasa de −0.599 a 0.001. La proporción de clientes del mismo lado de la media en las dos variables pasa de 29 % a 49.4 %, que es lo que da el azar. En los datos reales, **en 71 de cada 100 clientes las dos variables quedan en lados opuestos de su media** (mucho uso del cupo con poco puntaje, o al revés). **Mismas marginales, conjuntas distintas. Esa diferencia es la dependencia.**

### 11.6 Dónde queda S

#### Cómo se aplicó

Se calculó la matriz de covarianzas 2×2 de (`Credit_Utilization`, `Credit_Score`) con el puntaje original y con el barajado.

| Original | Credit_Utilization | Credit_Score |
|---|---|---|
| Credit_Utilization | 0.042 | −8.446 |
| Credit_Score | −8.446 | 4684.615 |

| Barajado | Credit_Utilization | Credit_Score |
|---|---|---|
| Credit_Utilization | 0.042 | 0.011 |
| Credit_Score | 0.011 | 4684.615 |

#### Interpretación

Las diagonales son iguales —las varianzas marginales no cambiaron— y lo único que se movió es la covarianza cruzada. **En $\mathbf{S}$, toda la información sobre la conjunta que las marginales no tienen está fuera de la diagonal.** Pero $\mathbf{S}$ tampoco es la conjunta completa: solo captura **dependencia lineal**, y dos conjuntas muy distintas pueden compartir la misma $\mathbf{S}$. El Módulo 12 muestra un ejemplo de lo que $\mathbf{S}$ no ve (`Payment_Amount` × `Credit_Score`).

### 11.7 Marginalizar no es neutro: un adelanto de Simpson (S09)

#### Qué es

Marginalizar sobre una variable equivale a afirmar que esa variable no importa. La **paradoja de Simpson** ocurre cuando una relación observada en el total se invierte dentro de cada subgrupo.

#### Cómo se aplicó

Se correlacionaron `Monthly_Transactions` (número de transacciones al mes) y `Avg_Transaction_Value` (valor promedio por transacción) sobre los 50 000 clientes juntos —es decir, marginalizando sobre el tipo de tarjeta— y luego dentro de cada tipo de tarjeta (`split(credit, tarjeta)`).

#### Resultado

| Grupo | r(transacciones, valor medio) |
|---|---|
| Toda la cartera | 0.1355016 |
| Basic | −0.209 |
| Silver | −0.354 |
| Gold | −0.411 |
| Platinum | −0.357 |
| Signature | −0.611 |

#### Interpretación

Con toda la cartera junta, $r = 0.136$: "quien compra más veces, compra más caro". **Dentro de cada tipo de tarjeta la correlación es negativa:** entre clientes con la misma tarjeta, quien hace más transacciones las hace de menor valor. Sumar sobre el tipo de tarjeta no solo borró la relación, **le dio la vuelta**. Es la paradoja de Simpson; su mecanismo —qué hace el tipo de tarjeta para producirla— se resuelve en el Módulo 12 con la herramienta contraria a marginalizar: **condicionar**.

### 11.8 Conclusión del Módulo 11

- **La conjunta lo contiene todo:** tabla en el caso discreto (tarjeta × banda de riesgo), densidad en el continuo (uso del cupo × puntaje). $\bar{\mathbf{x}}$ y $\mathbf{S}$ son solo sus dos primeros momentos.
- **Las marginales se obtienen sumando (o integrando)** sobre lo que se quiere eliminar, y viven literalmente en los márgenes de la tabla. Cada histograma del informe era una marginal empírica.
- **Las marginales no determinan la conjunta.** Ocupación y tarjeta tienen casillas vacías que ningún producto de marginales predice, y al barajar el puntaje las marginales quedan idénticas mientras la correlación con el uso del cupo pasa de −0.6 a cero.
- **Marginalizar es una decisión, no una operación neutra:** sobre toda la cartera, más transacciones van con transacciones más caras; dentro de cada tipo de tarjeta, pasa lo contrario.

---

## Módulo 12: Distribución condicional e independencia (S10)

### Contexto y propósito del módulo

El Módulo 11 terminó con una deuda: sobre toda la cartera, más transacciones van con transacciones más caras, y dentro de cada tipo de tarjeta pasa lo contrario. Juntar los tipos de tarjeta era **marginalizar**, y marginalizar dio vuelta a la conclusión. La herramienta de este módulo es la operación contraria: en lugar de sumar sobre la variable que estorba, **se fija su valor** y se mira qué pasa con lo demás. Eso es **condicionar**. Con ella se resuelven tres cosas: la definición correcta de independencia, la paradoja de Simpson de la cartera y la ley de la varianza total. Corresponde a la sesión S10.

### 12.1 Caso discreto: condicionar es dividir por la marginal

#### Qué es

$$f(y \mid x) = \frac{f(x,y)}{f_X(x)} \qquad\text{siempre que } f_X(x) > 0$$

En una tabla: se toma una fila de la conjunta y **se reescala para que sume 1**. La distribución condicional responde "entre los que tienen $X = x$, ¿cómo se reparte $Y$?".

#### Cómo se aplicó

Con la tabla ocupación × tarjeta del Módulo 11, usando `prop.table(tabla_ot, margin = 1)` para $P(\text{Card\_Type} \mid \text{Occupation})$ (filas suman 1) y `prop.table(tabla_ot, margin = 2)` para $P(\text{Occupation} \mid \text{Card\_Type})$ (columnas suman 1).

#### Resultado: P(Card_Type | Occupation), en %

| Occupation | Basic | Silver | Gold | Platinum | Signature |
|---|---|---|---|---|---|
| Business Owner | 0.0 | 3.2 | 15.6 | 39.6 | 41.5 |
| Government Employee | 8.5 | 27.4 | 46.3 | 17.8 | 0.0 |
| Private Employee | 17.2 | 32.2 | 39.6 | 11.0 | 0.0 |
| Retired | 33.8 | 40.7 | 25.4 | 0.0 | 0.0 |
| Self-Employed | 9.8 | 18.6 | 41.7 | 30.0 | 0.0 |
| Student | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 |

`rowSums()` = 1 en las seis filas.

#### Resultado: P(Occupation | Card_Type), en %

| Occupation | Basic | Silver | Gold | Platinum | Signature |
|---|---|---|---|---|---|
| Business Owner | 0.0 | 1.6 | 5.6 | 28.9 | 100.0 |
| Government Employee | 6.3 | 17.3 | 20.8 | 16.3 | 0.0 |
| Private Employee | 35.1 | 55.9 | 49.2 | 27.9 | 0.0 |
| Retired | 13.3 | 13.7 | 6.1 | 0.0 | 0.0 |
| Self-Employed | 7.1 | 11.5 | 18.3 | 26.9 | 0.0 |
| Student | 38.2 | 0.0 | 0.0 | 0.0 | 0.0 |

#### Interpretación

- Cada fila de la primera tabla es una distribución completa del tipo de tarjeta, una por ocupación: **hay seis condicionales y una sola marginal**.
- Otras observaciones de las tablas: Signature es exclusiva de Business Owner (100 % de los Signature son empresarios); Retired nunca tiene Platinum ni Signature; solo Business Owner tiene Signature.
- **Las dos direcciones no son lo mismo:** el 100 % de los estudiantes tiene una Basic ($P(\text{Basic} \mid \text{Student})$), pero de los clientes Basic solo el 38 % son estudiantes ($P(\text{Student} \mid \text{Basic})$). Confundir $P(Y \mid X)$ con $P(X \mid Y)$ —"si casi todos los estudiantes son Basic, casi todos los Basic son estudiantes"— es **el error más caro de la estadística aplicada**.

**Para el negocio:** un área comercial que quiera "encontrar estudiantes" filtrando por tarjeta Basic se equivocaría con 62 de cada 100 clientes.

### 12.2 Independencia: tres definiciones que son la misma

#### Qué es

$X$ e $Y$ son independientes si y solo si se cumple cualquiera de estas (y entonces se cumplen las tres):

| | Forma | En palabras |
|---|---|---|
| 1 | $f(x,y) = f_X(x)\,f_Y(y)$ para todo $x, y$ | La conjunta es el producto de las marginales |
| 2 | $f(y \mid x) = f_Y(y)$ para todo $x$ | Saber $X$ no cambia nada sobre $Y$ |
| 3 | $f(x \mid y) = f_X(x)$ para todo $y$ | Saber $Y$ no cambia nada sobre $X$ |

La segunda es la que se entiende: si todas las filas condicionales son iguales entre sí, e iguales a la marginal, no hay dependencia.

Complementos usados:

- **Prueba $\chi^2$ de independencia:** contrasta la tabla observada con la esperada bajo independencia, $\chi^2 = \sum \frac{(O-E)^2}{E}$, con $(f-1)(c-1)$ grados de libertad.
- **V de Cramér:** mide el **tamaño** de la dependencia en escala 0–1: $V = \sqrt{\dfrac{\chi^2}{n\,(\min(f, c) - 1)}}$.

#### Cómo se aplicó

Se calcularon las condicionales $P(\text{Riesgo} \mid \text{Card\_Type})$ y se apilaron con la marginal del riesgo. Se escribió `v_cramer(tab)` que corre `chisq.test()` (silenciando advertencias) y devuelve $\chi^2$, gl, p-valor y V; se aplicó a los dos pares.

#### Resultado: P(Riesgo | Card_Type) frente a la marginal, en %

| | Alto | Medio | Bajo | Muy bajo |
|---|---|---|---|---|
| Basic | 23.0 | 45.8 | 29.5 | 1.7 |
| Silver | 24.0 | 45.1 | 29.3 | 1.6 |
| Gold | 23.6 | 45.7 | 29.2 | 1.5 |
| Platinum | 20.6 | 44.1 | 32.4 | 2.8 |
| Signature | 20.5 | 42.5 | 33.3 | 3.7 |
| **Marginal** | **22.9** | **45.2** | **30.0** | **1.9** |

#### Resultado: prueba χ² y V de Cramér

| Par | χ² | gl | p-valor | V de Cramér |
|---|---|---|---|---|
| Tarjeta vs. riesgo | 175.2296 | 12 | 4.057808 × 10⁻³¹ | 0.0341789 |
| Ocupación vs. tarjeta | 43 311.6643 | 20 | 0 | 0.4653583 |

#### Interpretación y decisión

- Las cinco filas de riesgo son casi iguales entre sí y casi iguales a la marginal: Platinum y Signature tienen un par de puntos más en las bandas de riesgo bajo, y nada más.
- La $\chi^2$ rechaza la independencia ($p = 4.1 \times 10^{-31}$), pero con $n = 50\,000$ eso detecta hasta la diferencia más pequeña (la misma advertencia que el informe hace sobre las pruebas de normalidad con muestras grandes): **el tamaño de la dependencia, $V = 0.034$, es prácticamente cero**. Significancia estadística no es relevancia práctica.
- Entre ocupación y tarjeta, $V = 0.465$: una dependencia **fuerte**, la de las casillas vacías del Módulo 11.
- **Decisión:** para el riesgo, el tipo de tarjeta puede tratarse como casi independiente; para la ocupación, no: **cualquier análisis por tipo de tarjeta está mezclando ocupaciones**.

**Para el negocio:** el tipo de tarjeta no es un indicador de riesgo crediticio; segmentar la política de riesgo por tarjeta no aportaría discriminación.

### 12.3 Caso continuo: se condiciona con una rebanada

#### Qué es

En el caso continuo la fórmula es la misma, pero la imagen cambia: condicionar en $X = x$ es **cortar la nube con una rebanada** en ese $x$ y mirar la distribución de $Y$ dentro de ella. Con datos, la rebanada se hace cortando $X$ en **terciles**, y se contestan las tres preguntas de la sesión: **¿se mueve el centro? ¿cambia el ancho? ¿cambia la forma?**

#### Cómo se aplicó

Funciones auxiliares:

- `asim(v)`: asimetría $\frac{1}{n}\sum\left(\frac{v_i-\bar v}{s}\right)^3$.
- `rebanar(x, y)`: corta `x` en terciles (`quantile` en 0, 1/3, 2/3, 1; etiquetas bajo/medio/alto) y, para `y` dentro de cada tercil, devuelve n, media, sd, asimetría, percentil 10 y percentil 90.

Se aplicó al **par de riesgo**: `Credit_Score` según el tercil de `Credit_Utilization`. Gráficos: boxplots de `Credit_Score` por tercil de uso (verde/ámbar/rojo) y las tres densidades condicionales superpuestas ("Las tres condicionales").

#### Resultado

| Tercil de uso | n | Media | sd | Asimetría | p10 | p90 |
|---|---|---|---|---|---|---|
| Bajo | 17 422 | 670.74 | 56.60 | −0.84 | 584 | 731 |
| Medio | 16 022 | 633.34 | 55.43 | −0.88 | 547 | 691 |
| Alto | 16 556 | 580.83 | 60.26 | −0.72 | 491 | 650 |

#### Interpretación (las tres preguntas)

- **El centro se mueve, y mucho:** el puntaje medio pasa de 670.74 con uso bajo del cupo a 580.83 con uso alto.
- **El ancho cambia poco:** la desviación estándar se queda entre 55.43 y 60.26 en las tres rebanadas.
- **La forma tampoco:** las tres condicionales tienen la misma cola izquierda (asimetrías entre −0.88 y −0.72); la curva entera se desplaza sin deformarse.

Es la huella de una **dependencia lineal**: lo que cambia con el uso del cupo es el nivel del puntaje, no su dispersión.

**Para la Gerencia de Riesgo:** el tercil de uso del cupo, por sí solo, ya mueve el puntaje esperado en 90 puntos (de 671 a 581, cruzando el umbral de riesgo alto de 580).

### 12.4 La normal bivariada: la condicional tiene fórmula

#### Qué es

Si $(X, Y)$ fuera normal bivariada, la condicional sería otra normal con **media sobre una recta** y **varianza constante**:

$$Y \mid X = x \;\sim\; N\!\left(\mu_Y + \rho\,\frac{\sigma_Y}{\sigma_X}(x - \mu_X),\;\; \sigma_Y^2\,(1 - \rho^2)\right)$$

La media condicional es exactamente la recta de regresión de $Y$ sobre $X$; la varianza condicional no depende de $x$ y es menor que la marginal por el factor $(1-\rho^2)$.

#### Cómo se aplicó

Se estimaron $\mu_X, \sigma_X, \mu_Y, \sigma_Y, \rho$ con la cartera (`X` = `Credit_Utilization`, `Y` = `Credit_Score`) y se compararon las predicciones de la fórmula con rebanadas reales **más finas**: clientes con uso del cupo a menos de 0.02 de 0.2, 0.4, 0.6 y 0.8.

#### Resultado

| Uso | n | Media real | Media fórmula | sd real | sd fórmula |
|---|---|---|---|---|---|
| 0.2 | 2 968 | 673.6 | 674.1 | 54.9 | 54.8 |
| 0.4 | 4 035 | 634.6 | 634.2 | 53.7 | 54.8 |
| 0.6 | 1 365 | 591.6 | 594.4 | 54.8 | 54.8 |
| 0.8 | 820 | 553.2 | 554.5 | 55.2 | 54.8 |

| sd marginal | sd condicional (fórmula) |
|---|---|
| 68.44425 | 54.78934 |

#### Interpretación

La media condicional real sigue de cerca la recta de la fórmula y la desviación dentro de cada rebanada se mantiene cerca de $\sigma_Y\sqrt{1-\rho^2} = 54.8$, menor que la marginal (68.4) por el factor $\sqrt{1 - \rho^2}$: **saber el uso del cupo reduce la incertidumbre sobre el puntaje**. Las diferencias que aparecen en los extremos (p. ej. 591.6 frente a 594.4 en uso 0.6) vienen de que `Credit_Score` no es normal (cola izquierda, Módulo 3): la fórmula describe el centro de la cartera mejor que sus bordes.

### 12.5 La trampa: correlación casi cero no es independencia

#### Qué es

La sesión S10 advierte que una correlación nula (o una media condicional quieta) **no prueba independencia**, porque la definición 2 pide que **toda** la distribución condicional sea igual a la marginal, no solo su centro. La correlación solo mide dependencia lineal en la media.

#### Cómo se aplicó

Caso de la cartera: `Payment_Amount` (el monto que el cliente paga) y `Credit_Score`. Se calculó $r$ y se aplicó `rebanar()` por terciles de `Payment_Amount`, con los mismos boxplots y densidades condicionales superpuestas.

#### Resultado

$r$ de Pearson = **0.03109983**.

| Tercil de pago | n | Media | sd | Asimetría | p10 | p90 |
|---|---|---|---|---|---|---|
| Bajo | 16 667 | 619.01 | 76.06 | −0.45 | 512 | 712 |
| Medio | 16 666 | 635.28 | 67.66 | −0.67 | 541 | 715 |
| Alto | 16 667 | 632.67 | 59.49 | −0.50 | 554 | 705 |

#### Interpretación

La correlación es $r = 0.031$ y el centro apenas se mueve entre terciles (de 619.01 a 635.28). Si solo se mirara $r$ o la media, la conclusión sería "el monto pagado no tiene nada que ver con el puntaje". Pero **el ancho sí cambia**: la desviación estándar del puntaje baja de 76.06 entre quienes pagan poco a 59.49 entre quienes pagan mucho, y el percentil 10 sube de 512 a 554 mientras el percentil 90 casi no se mueve (712 → 705). **La dependencia está en la cola de riesgo:** los puntajes más bajos de la cartera se concentran entre quienes pagan montos pequeños.

| Lo que se mira | ¿Detecta la dependencia Payment_Amount–Credit_Score? |
|---|---|
| Correlación | No: $r \approx 0.03$ |
| Media condicional | Apenas: se mueve menos de 20 puntos |
| Distribución condicional completa | **Sí: la cola izquierda se alarga cuando el pago es bajo** |

**Para el negocio:** un análisis que filtre variables por correlación descartaría `Payment_Amount` como irrelevante para el riesgo, y se perdería justamente la señal de la cola peligrosa (clientes de muy bajo puntaje entre quienes pagan poco). Este es también el ejemplo de lo que $\mathbf{S}$ no ve, anunciado en el Módulo 11.

### 12.6 Simpson, resuelto

#### Cómo se aplicó

Se condicionó en el tipo de tarjeta: para cada `Card_Type`, número de clientes, media de transacciones, valor medio de transacción y correlación dentro del grupo. Luego se compararon tres correlaciones: la global, la **entre centros** (entre las cinco medias de grupo) y el promedio de las correlaciones dentro de grupo.

#### Resultado

| Card_Type | n | Transacciones (media) | Valor medio (₹) | r dentro |
|---|---|---|---|---|
| Basic | 10 261 | 41.22 | 425.83 | −0.21 |
| Silver | 12 056 | 68.57 | 593.43 | −0.35 |
| Gold | 16 895 | 96.54 | 732.59 | −0.41 |
| Platinum | 8 284 | 117.08 | 1 280.59 | −0.36 |
| Signature | 2 504 | 120.33 | 2 911.43 | −0.61 |

| r global | r entre centros | r dentro (promedio) |
|---|---|---|
| 0.1355016 | 0.7448525 | −0.3882109 |

**Gráfico:** "Dentro de cada tarjeta la nube baja; entre tarjetas, sube". Muestra aleatoria de 5 000 clientes (`set.seed(11)`), eje Y en escala logarítmica, coloreados por tarjeta; los cinco centros de grupo como rombos grandes unidos por una línea discontinua que sube.

#### Interpretación: las tres piezas del mecanismo

1. **Condicionando en la tarjeta, la relación es negativa siempre** (de −0.21 a −0.61): entre clientes con la misma tarjeta, más transacciones van con transacciones más pequeñas. Es la comparación honesta, iguales contra iguales.
2. **El tipo de tarjeta empuja las dos variables hacia arriba a la vez:** un Signature hace en promedio 120 transacciones de 2.911 ₹; un Basic, 41 de 426 ₹. Los cinco centros (rombos) suben juntos ($r$ entre centros = 0.745).
3. **Al juntar las tarjetas, la tendencia entre centros se impone a la de dentro de cada grupo**, y el $r$ global sale positivo (0.136).

`Card_Type` es una **variable confusora**: afecta a la vez a cuántas transacciones se hacen y a cuánto vale cada una. **Regla:** cuando una variable empuja a las dos que se comparan, se condiciona en ella.

**Para el banco:** un modelo de gasto que use transacciones y valor medio sin `Card_Type` llegaría a la conclusión exactamente equivocada sobre cómo se relacionan.

### 12.7 La ley de la varianza total

#### Qué es

La varianza de una variable se parte en dos: lo que varía **dentro** de cada rebanada y lo que se mueven los **centros entre** rebanadas:

$$\operatorname{Var}(Y) \;=\; \underbrace{E\big[\operatorname{Var}(Y \mid X)\big]}_{\text{dentro}} \;+\; \underbrace{\operatorname{Var}\big(E[Y \mid X]\big)}_{\text{entre centros}}$$

#### Cómo se aplicó

Con el puntaje y los terciles de uso del cupo. **Decisión:** todas las varianzas se calcularon con denominador $n$ (`var_n(v) = mean((v - mean(v))^2)`) en lugar de $n-1$, para que la identidad sea exacta. "Dentro" = promedio ponderado (por la proporción de cada tercil) de las varianzas por tercil; "entre" = varianza ponderada de las medias de tercil alrededor de la media global.

#### Resultado

| Componente | Valor |
|---|---|
| Varianza total | 4684.52150 |
| Dentro | 3302.93243 |
| Entre | 1381.58907 |
| Suma (dentro + entre) | 4684.52150 |
| % explicado por terciles | 29.49264 |

#### Interpretación

La suma reproduce exactamente la varianza total. De ella, **el 29.5 % es "entre centros"**: la parte del puntaje que se explica con solo saber en qué tercil de uso del cupo está el cliente. Es un $\eta^2$ como los del Módulo 7, con el tercil como grupo, ahora deducido desde las condicionales; y si la rebanada fuera infinitamente fina, tendería a $\rho^2 = 0.359$ (la fórmula de la normal bivariada).

### 12.8 Condicionales en p dimensiones

#### Qué es

Para la normal multivariante la condicional tiene forma cerrada. Se parte el vector en dos bloques, $\mathbf{X} = (\mathbf{X}_1, \mathbf{X}_2)$:

$$\mathbf{X}_1 \mid \mathbf{X}_2 = \mathbf{x}_2 \;\sim\; N\!\left(\boldsymbol\mu_1 + \boldsymbol\Sigma_{12}\boldsymbol\Sigma_{22}^{-1}(\mathbf{x}_2 - \boldsymbol\mu_2),\;\; \boldsymbol\Sigma_{11} - \boldsymbol\Sigma_{12}\boldsymbol\Sigma_{22}^{-1}\boldsymbol\Sigma_{21}\right)$$

La **marginal** era **tachar** filas y columnas de $\boldsymbol\Sigma$; la **condicional** es **tachar y corregir**: la media se corre según cuánto se aleja $\mathbf{x}_2$ de su media, y la covarianza se reduce en lo que $\mathbf{X}_2$ explica de $\mathbf{X}_1$.

#### Cómo se aplicó

Se escribió `condicional_normal(mu, Sigma, i, j, x2)` que extrae los bloques $\Sigma_{11}$, $\Sigma_{12}$, $\Sigma_{22}$ y calcula media y desviación condicionales usando `solve()` (resuelve el sistema en vez de invertir explícitamente). Variables: `Credit_Score`, `Credit_Utilization`, `Payment_Ratio`, con vector de medias y matriz $\mathbf{S}$ de la cartera. Tres escenarios para el puntaje:

1. Sin saber nada.
2. Sabiendo que el cliente usa el 80 % de su cupo (`Credit_Utilization = 0.80`).
3. Sabiendo además que paga el 40 % de lo facturado (`Payment_Ratio = 0.40`).

Y se contrastó con clientes reales: uso a menos de 0.03 de 0.80 **y** proporción pagada a menos de 0.03 de 0.40.

#### Resultado

| Escenario | Media | sd |
|---|---|---|
| Sin saber nada | 628.9846 | 68.44425 |
| Sabiendo uso = 0.80 | 554.5102 | 54.78934 |
| Sabiendo uso = 0.80 y pago = 0.40 | 474.1434 | 15.00829 |

| Clientes reales con ese perfil | n | Media real | sd real |
|---|---|---|---|
| | 39 | 475.07692 | 17.09476 |

#### Interpretación

Sin saber nada, el puntaje esperado es 629 con desviación 68.4. Saber que el cliente usa el 80 % de su cupo baja la media a 555 y la desviación a 54.8. Saber además que paga solo el 40 % de lo facturado la baja a 474, con desviación de apenas 15 puntos, y **los 39 clientes reales con ese perfil tienen un puntaje medio de 475** (sd 17.1): la fórmula acierta. **Cada variable que se conoce corre el centro y angosta la campana**, y estas dos juntas (que entre sí casi no están correlacionadas, $r = 0.005$) dejan el puntaje casi determinado: **la varianza condicional es el 4.8 % de la marginal**.

**Para la Gerencia de Riesgo esto es central:** el puntaje del buró está contenido casi por completo en dos conductas de pago que el banco observa directamente cada mes (uso del cupo y proporción pagada). El banco puede anticipar el deterioro del puntaje con datos propios, antes de que el buró lo refleje.

#### 12.8.1 El requisito escondido: Σ22 tiene que invertirse

##### Qué es

La fórmula exige $\boldsymbol\Sigma_{22}^{-1}$. Si las variables en las que se condiciona son linealmente dependientes, $\boldsymbol\Sigma_{22}$ es singular y la condicional no existe (o no se puede calcular).

##### Cómo se aplicó

1. Se construyó el gasto total recalculado como **suma exacta** de las siete categorías (`rowSums(credit[, cat_gasto])`) y se intentó condicionar `Credit_Score` en ese total **y** sus siete categorías a la vez (evaluando en las medias), dentro de `tryCatch`.
2. Con el `Monthly_Spending` guardado en la base (redondeado a centavos), se calculó el número de condición exacto de la covarianza (`kappa(..., exact = TRUE)`) de `Monthly_Spending` + las siete categorías, y el menor valor propio de su correlación.

##### Resultado

```
"ERROR: sistema es computacionalmente singular: número de condición recíproco = 4.05894e-18"
```

| Número de condición | Menor valor propio de R |
|---|---|
| 1.121085 × 10¹⁵ | 5.816212 × 10⁻¹⁵ |

##### Interpretación y decisión

- Si se condiciona en el gasto total y en sus siete categorías a la vez, $\boldsymbol\Sigma_{22}$ es **singular** —el total es la suma exacta de las otras siete— y `solve()` falla: **no hay distribución condicional que calcular**.
- Con el `Monthly_Spending` que trae la base, R no protesta **solo porque está redondeado a centavos** (Módulo 10): el número de condición es del orden de $10^{15}$, es decir, R invierte una matriz que solo deja de ser singular por el ruido del redondeo, y **cualquier resultado que salga de ahí es numéricamente basura**. Que R no dé error no significa que el resultado sea válido.
- Es la misma razón por la que esas columnas **se excluyen antes de Mahalanobis (Módulo 13) y del PCA (Módulo 15)**.

### 12.9 Conclusión del Módulo 12

- **Condicionar es fijar y reescalar:** cada fila de la tabla dividida por su total. $P(\text{Basic} \mid \text{Student})$ y $P(\text{Student} \mid \text{Basic})$ son cosas distintas, y en la cartera difieren en más de 60 puntos (100 % frente a 38 %).
- **Independencia es que todas las condicionales sean iguales a la marginal, completas.** Tarjeta y banda de riesgo son prácticamente independientes ($V$ de Cramér casi 0, aunque la $\chi^2$ rechace por el tamaño de muestra); ocupación y tarjeta no lo son.
- **Las rebanadas responden tres preguntas:** con el uso del cupo se mueve el centro del puntaje y no el ancho (dependencia lineal); con el monto pagado, $r \approx 0$ pero cambia el ancho y la cola de riesgo: **correlación cero no es independencia**.
- **Simpson, resuelto:** `Card_Type` es confusora de transacciones y valor medio; condicionando en ella, la relación es negativa en las cinco tarjetas.
- **Varianza total = dentro + entre centros**, verificada exactamente (29.5 % explicado por los terciles de uso); y en $p$ dimensiones la condicional es "tachar y corregir", con la condición de que $\boldsymbol\Sigma_{22}$ sea invertible.


---

## Módulo 13: Normal multivariante, distancia de Mahalanobis y gráfico Q-Q

### Punto de partida y pregunta del módulo

Este módulo junta tres piezas de módulos anteriores:

- el **Módulo 7** construyó a mano un "punto imposible": un cliente que es normal en cada variable por separado pero queda fuera de la nube cuando las variables se miran juntas;
- el **Módulo 9** mostró que la distancia euclidiana no distingue a ese cliente de uno típico;
- el **Módulo 10** dejó lista una matriz de covarianzas $\mathbf{S}$ **invertible**, la pieza que faltaba (sin ella no existe $\mathbf{S}^{-1}$).

La pregunta, la de la sesión de normal multivariante aplicada a la cartera, es:

> **¿Hay clientes que son raros en la *combinación* de sus variables, aunque ninguna por separado sea extrema? ¿Quiénes son, y qué se hace con ellos?**

### 13.1 Concepto: la distribución normal multivariante

Un vector aleatorio $\mathbf{x} = (x_1,\dots,x_p)'$ sigue una normal multivariante $\mathcal{N}_p(\boldsymbol\mu, \boldsymbol\Sigma)$ si su densidad es

$$
f(\mathbf{x}) = \frac{1}{(2\pi)^{p/2}\,|\boldsymbol\Sigma|^{1/2}}\exp\!\left\{-\tfrac12(\mathbf{x}-\boldsymbol\mu)'\boldsymbol\Sigma^{-1}(\mathbf{x}-\boldsymbol\mu)\right\}.
$$

- $\boldsymbol\mu$ es el vector de medias (el centro de la nube) y $\boldsymbol\Sigma$ la matriz de covarianzas (la forma y la orientación de la nube).
- La densidad depende de $\mathbf{x}$ **solo a través de la forma cuadrática** $(\mathbf{x}-\boldsymbol\mu)'\boldsymbol\Sigma^{-1}(\mathbf{x}-\boldsymbol\mu)$: todos los puntos con el mismo valor de esa cantidad tienen la misma densidad. Las curvas de nivel son, por tanto, **elipses** (en $p=2$) o **elipsoides** (en $p>2$), centradas en $\boldsymbol\mu$ y alargadas en la dirección de la correlación.
- Intuición: es la "campana de Gauss" en varias dimensiones. Cada variable por separado es normal, pero además la nube conjunta tiene una forma elíptica precisa, y la rareza de un punto se mide respecto de esa forma, no respecto de cada eje por separado.

Para estimarla con datos se reemplaza $\boldsymbol\mu$ por $\bar{\mathbf{x}}$ y $\boldsymbol\Sigma$ por $\mathbf{S}$.

### 13.2 La matriz con la que se trabaja

**Qué exige el método.** Mahalanobis necesita el vector **completo** de cada cliente: un solo hueco deja la fila por fuera. El Módulo 2 ya había mostrado que la cartera no tiene faltantes, así que entran todos los clientes.

**Cómo se aplicó.** Se usan las variables numéricas no redundantes verificadas en el Módulo 10 (`vars_mahal <- setdiff(numeric_cols, variables_excluidas)`), en **dos versiones**:

1. `X_mahal`: las variables **tal como vienen**.
2. `X_log`: la misma matriz con `log1p()` (es decir, $\log(x+1)$) aplicado a las variables cuya asimetría, calculada como $\frac1n\sum\left(\frac{x_i-\bar x}{s}\right)^3$, supera 1 en valor absoluto (el mismo criterio que formaliza el Módulo 15).

**Por qué dos versiones.** Una distancia construida con $\mathbf{S}$ **hereda la asimetría** de las variables: si las variables son muy torcidas, la nube no es elíptica y las distancias no siguen la ley teórica.

**Resultado:**

| clientes | filas completas | variables ($p$) | variables con log |
|---:|---:|---:|---:|
| 50 000 | 50 000 | 21 | 16 |

Las 21 variables son las mismas que el Módulo 15 retiene para PCA (lista completa en la sección 15.3), y las 16 transformadas son las 16 marcadas con `log(x+1) + scale()` en la tabla 15.2.

### 13.3 Por qué variable por variable no alcanza

#### 13.3.1 La revisión de siempre (columna por columna)

**Concepto.** La forma habitual de buscar casos raros (la del Módulo 6) es estandarizar cada variable, $z_{ij} = (x_{ij}-\bar x_j)/s_j$, y señalar a quien tenga $|z_{ij}|>3$ en alguna columna.

**Cómo se aplicó.** `Z_log <- scale(X_log)`; `extremo_univariado <- apply(abs(Z_log) > 3, 1, any)` (sobre la versión con log).

**Resultado:** **2 516 clientes (5,03 %)** tienen al menos una variable a más de tres desviaciones.

**Lectura.** Es un número razonable, pero esta revisión **solo ve una columna a la vez**: no puede preguntar si la *combinación* de valores tiene sentido.

#### 13.3.2 El caso del plano, con la elipse de concentración

**Concepto: elipse de concentración del 95 %.** Si un par de variables fuera normal bivariado, el conjunto

$$
\{\mathbf{x} : (\mathbf{x}-\bar{\mathbf{x}})'\mathbf{S}^{-1}(\mathbf{x}-\bar{\mathbf{x}}) \le \chi^2_{2;\,0{,}95}\}
$$

es la elipse dentro de la cual caería el 95 % de los clientes. Su frontera se dibuja como $\bar{\mathbf{x}} + \sqrt{\chi^2_{2;0{,}95}}\;\mathbf{u}'\,\mathbf{L}$, donde $\mathbf{u}$ recorre el círculo unitario y $\mathbf{L}$ es el factor de Cholesky de $\mathbf{S}$ (`chol(S)`): se "estira y gira" un círculo con la raíz de la matriz de covarianzas.

**Cómo se aplicó.** Se tomó el par de riesgo del Módulo 7, `Credit_Utilization` y `Credit_Score` (correlación $r=-0{,}599$):

- `mahalanobis(par_riesgo, centro_par, S_par)` da $d^2$ de cada cliente en el plano; `fuera_elipse <- d2_par > qchisq(0.95, df = 2)`.
- Encima, las bandas de $\pm 2$ desviaciones de cada variable (lo que vigilaría una revisión columna por columna): `fuera_bandas <- |z1| > 2 | |z2| > 2`.
- Gráfico [figura: dispersión de 6 000 clientes elegidos con `set.seed(13)`, elipse roja del 95 %, bandas azules punteadas de ±2 desviaciones y en naranja los clientes fuera de la elipse pero dentro de las bandas].

**Resultado:**

| Situación | Clientes |
|---|---:|
| Fuera de la elipse, con las dos variables dentro de ±2 desviaciones | 868 |
| Dentro de la elipse, con una variable fuera de ±2 desviaciones | 1 847 |
| Fuera de la elipse (total) | 2 806 |

**Lectura.**

- **868 clientes** (los puntos naranja) quedan **fuera de la elipse aunque sus dos variables están dentro de las bandas**: uso del cupo y puntaje "corrientes" por separado, pero en una combinación que la cartera casi no produce. Casi todos son clientes con **poco** uso del cupo **y** puntaje bajo, justo lo contrario de lo que dice la correlación negativa.
- Al revés, **1 847 clientes** tienen una variable fuera de las bandas pero están **dentro** de la elipse: llevan las dos variables al extremo **en la dirección de la correlación** (mucho uso y poco puntaje), es decir, son coherentes con la nube.
- Las dos revisiones **no señalan a la misma gente**: la columna por columna se pierde a unos (868) y da falsas alarmas con otros (1 847). Se necesita una medida que mida **en elipses**.

**Significado para el negocio.** Un cliente con poco uso del cupo y mal puntaje no dispara ninguna alarma en un tablero de indicadores sueltos, pero es una combinación anómala para la cartera; viceversa, un cliente muy endeudado con puntaje bajo es "extremo" pero esperable.

### 13.4 La distancia de Mahalanobis frente a la euclidiana

**Concepto.** La distancia euclidiana mide cuánto se aleja un cliente del promedio tratando a las variables como independientes y en sus unidades. La de Mahalanobis hace dos ajustes antes de medir:

| Ajuste | Qué hace | Por qué |
|---|---|---|
| **Por la escala** | Cuenta la distancia en desviaciones, no en rupias | 10 000 rupias de ingreso no valen lo mismo que 10 000 de gasto en combustible |
| **Por la compañía** | Descuenta lo que las variables ya comparten | Si ingreso y cupo van juntos, tener los dos altos no es *dos* rarezas: es una sola |

$$
d_M(\mathbf{x}_i) = \sqrt{(\mathbf{x}_i - \bar{\mathbf{x}})'\,\mathbf{S}^{-1}\,(\mathbf{x}_i - \bar{\mathbf{x}})}
\qquad\text{frente a}\qquad
d_E(\mathbf{x}_i)=\sqrt{\sum_{j=1}^p z_{ij}^2}=\sqrt{(\mathbf{x}_i - \bar{\mathbf{x}})'\,\mathbf{D}^{-1}\,(\mathbf{x}_i - \bar{\mathbf{x}})},
$$

donde $\mathbf{D}=\operatorname{diag}(s_1^2,\dots,s_p^2)$. La euclidiana sobre variables estandarizadas solo corrige la escala; Mahalanobis usa la matriz completa $\mathbf{S}$ y corrige también la correlación. Todos los puntos de la elipse roja de la sección anterior están a la **misma** distancia de Mahalanobis del centro.

**Cómo se aplicó.** Sobre las 21 variables a la vez, versión con log:

- `d2_log <- mahalanobis(X_log, colMeans(X_log), cov(X_log))`;
- `d_euclid <- sqrt(rowSums(Z_log^2))` (euclidiana sobre las variables ya estandarizadas, para que no la domine el ingreso);
- se comparan los 500 clientes más lejanos (top 1 %) según cada una.

**Resultado:**

| Indicador | Valor |
|---|---:|
| Correlación entre $d_E$ y $d_M$ | 0,488 |
| Clientes en el top 1 % | 500 |
| Coinciden en el top 1 % | 26 |

**Lectura.** Las dos distancias se correlacionan 0,49, pero de los 500 clientes más lejanos según cada una **solo 26 son los mismos**. La euclidiana encuentra sobre todo a los clientes de los extremos de tamaño: la mitad de su lista tiene un ingreso por encima del **percentil 98** de la cartera, clientes **grandes en todo** (mucho ingreso, mucho cupo, mucho gasto) que están lejos pero son coherentes. Mahalanobis encuentra a los que combinan sus variables de una forma que la cartera no produce.

**Significado para el negocio.** Una lista de "clientes lejanos" hecha con distancia euclidiana sería, en la práctica, una lista de clientes de alto patrimonio; la de Mahalanobis es una lista de **perfiles inconsistentes**, que es lo que interesa a Riesgo.

### 13.5 Las distancias sobre toda la cartera y el corte $\chi^2$

**Concepto.** Si $\mathbf{x}\sim\mathcal{N}_p(\boldsymbol\mu,\boldsymbol\Sigma)$, entonces

$$
d_M^2 = (\mathbf{x}-\boldsymbol\mu)'\boldsymbol\Sigma^{-1}(\mathbf{x}-\boldsymbol\mu)\sim\chi^2_p .
$$

Intuición: al "blanquear" los datos con $\boldsymbol\Sigma^{-1/2}$ se obtienen $p$ normales estándar independientes, y $d_M^2$ es la suma de sus cuadrados, que por definición es una $\chi^2$ con $p$ grados de libertad (media $p$, varianza $2p$). Con $n=50\,000$ la sustitución de $\boldsymbol\mu,\boldsymbol\Sigma$ por $\bar{\mathbf{x}},\mathbf{S}$ es irrelevante. Esto convierte "está lejos" en un **umbral**: con $p=21$, el cuantil $\chi^2_{21;\,0{,}975}$ deja por fuera, en teoría, al 2,5 % de los clientes.

**Cómo se aplicó (variables tal como vienen).** `d2 <- mahalanobis(X_mahal, colMeans(X_mahal), cov(X_mahal))`; `corte_chi2 <- qchisq(0.975, df = 21)`.

**Resultado:**

| $p$ | Corte $\chi^2_{21;0{,}975}$ | Clientes por encima | % |
|---:|---:|---:|---:|
| 21 | 35,5 | 4 398 | 8,8 % |

**Comparación completa de cortes, cruda frente a transformada:**

| Corte | Valor de $d^2$ | Esperado (%) | Observado, crudo (%) | Observado, con log (%) |
|---|---:|---:|---:|---:|
| 95 % | 32,67 | 5,0 | 9,32 | 7,88 |
| 99 % | 38,93 | 1,0 | 8,33 | 3,28 |
| 99,9 % | 46,80 | 0,1 | 7,54 | 1,15 |

[Figura: dos histogramas de $d^2$ truncados en 150, uno para las variables crudas y otro con log(x+1), con la densidad $\chi^2_{21}$ en rojo y una línea punteada en el corte del 99 %.]

**Lectura con cifras exactas.**

- Con las variables crudas, el corte del 97,5 % (35,5) deja por fuera **4 398 clientes, el 8,8 %**, cuando la teoría espera 2,5 %; en el 99,9 % se observa el **7,54 % contra 0,1 %**. La curva roja no sigue al histograma: la cola es muchísimo más pesada de lo que una $\chi^2_{21}$ permite.
- Con `log(x+1)` el histograma se acerca a la curva y el exceso cae a **3,28 %** en el corte del 99 % (contra **8,33 %** sin transformar).
- La causa del exceso **no es un error de cálculo**: es la que ya documentó el Módulo 3. Variables como `Cash_Advance_Amount`, `Dining_Spending` o `Travel_Spending` son fuertemente asimétricas a la derecha (varias infladas en cero), y Mahalanobis hereda esa asimetría.

### 13.6 El gráfico Q-Q: ¿la cartera es una campana multivariante?

**Concepto.** Un gráfico cuantil-cuantil (Q-Q) compara los cuantiles observados de una muestra con los cuantiles teóricos de una distribución de referencia. Aquí: en el eje horizontal, los cuantiles teóricos de $\chi^2_{21}$ evaluados en las probabilidades `ppoints(n)` (aprox. $(i-0{,}5)/n$), es decir, la distancia que **debería** tener cada cliente si la cartera fuera normal multivariante; en el vertical, las $d^2$ **observadas** ordenadas. Si los datos se portan, los puntos caen sobre la recta de 45°.

**Cómo se aplicó.** `teoricos <- qchisq(ppoints(length(d2)), df = 21)`; `qqplot(teoricos, d2)` y `qqplot(teoricos, d2_log)` en paneles lado a lado, con la recta $y=x$ en rojo y una línea vertical en $\chi^2_{21;0{,}99}$. [Figura: dos gráficos Q-Q, crudo y con log.]

**Resultado (cuantiles):**

| Percentil | Teórica $\chi^2_{21}$ | Observada, cruda | Observada, con log |
|---|---:|---:|---:|
| 50 % | 20,3 | 8,9 | 19,5 |
| 75 % | 24,9 | 16,0 | 24,7 |
| 90 % | 29,6 | 30,3 | 31,0 |
| 95 % | 32,7 | 89,4 | 35,8 |
| 99 % | 38,9 | 247,8 | 47,7 |
| 99,9 % | 46,8 | 480,3 | 64,0 |

**Lectura.**

- En la versión **cruda** los puntos se apartan de la recta **desde el cuerpo**, no solo en la cola: la mediana observada es **8,9** cuando la teórica es **20,3** (la mayoría de los clientes queda *más cerca* del centro de lo que una campana permite), la curva cruza la recta cerca del percentil 90 y después se dispara: en el 99,9 % la observada es **480,3 contra 46,8**. Es el patrón "se curva desde el principio": variables torcidas, con mucha masa apretada cerca de cero y colas larguísimas.
- Con **`log(x+1)`** el cuerpo se acomoda sobre la recta (mediana **19,5 contra 20,3**, percentil 75 **24,7 contra 24,9**) y lo que queda despegado es la **cola superior** (47,7 contra 38,9 en el 99 %; 64,0 contra 46,8 en el 99,9 %).

**Guía de lectura de un Q-Q de distancias** (incluida en el informe):

| Qué se ve en el Q-Q | Qué significa | Qué se hace |
|---|---|---|
| Se despega **solo en la cola** | Hay casos raros, el cuerpo está bien | Identificarlos y decidir sobre ellos; seguir |
| Se curva **desde el principio** (versión cruda) | Alguna variable está torcida | Transformarla (logaritmo, raíz) y volver a mirar |
| Dos tramos con pendientes distintas | Hay **dos grupos** mezclados | Separarlos y analizar cada uno |
| Se despega **hacia abajo** | Menos dispersión de la esperada | Sospechar de un tope o un piso en la escala |

**Decisión.** El corte $\chi^2$ se usa **sobre la versión transformada**, y **solo como guía**: la normalidad multivariante exacta se pone a prueba formalmente en el Módulo 14. Lo que sí es información real y utilizable en cualquier caso es el **orden** que produce $d^2$ (quién está más lejos que quién).

### 13.7 Quiénes son los casos raros de verdad

**Regla adoptada.** Caso raro = cliente con $d^2_{\log} > \chi^2_{21;\,0{,}99} = 38{,}93$ (`raros <- d2_log > qchisq(0.99, df = 21)`).

#### 13.7.1 Cruce con la revisión univariada

| | No raro en la combinación | Raro en la combinación | Total |
|---|---:|---:|---:|
| Sin variable extrema ($\lvert z\rvert\le3$) | 46 429 | 1 055 | 47 484 |
| Con alguna variable extrema ($\lvert z\rvert>3$) | 1 930 | 586 | 2 516 |
| Total | 48 359 | 1 641 | 50 000 |

**Lectura.** De los **1 641 casos raros** (3,28 % de la cartera), **1 055 (64 %) no tienen ninguna variable a más de tres desviaciones**: son invisibles para la revisión columna por columna. Y de los **2 516** clientes con alguna variable extrema, **1 930 no son raros** en la combinación (son extremos coherentes).

#### 13.7.2 Perfil de los raros frente al resto (medianas)

| | Annual_Income | Credit_Limit | Statement_Balance | Payment_Amount | Monthly_Transactions | Credit_Score | Payment_Ratio | Credit_Utilization |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Raros | 1 489 286 | 592 000 | 291 570,5 | 105 745,1 | 86 | 573 | 0,57 | 0,39 |
| Resto | 1 119 841 | 393 000 | 190 646,3 | 137 147,9 | 75 | 639 | 0,85 | 0,40 |

(Montos en rupias INR.) Los raros ganan más, tienen más cupo y más saldo, pero **pagan menos** en monto absoluto, pagan una proporción mucho menor del extracto (0,57 vs 0,85) y tienen un puntaje mediano **66 puntos más bajo** (573 vs 639).

#### 13.7.3 Los diez clientes más lejanos

Para cada uno se listan las dos variables en las que más se aparta (en desviaciones estándar de la escala logarítmica, `Z_log`):

| # | Cliente | Tarjeta | $d^2$ | Se aparta en |
|---:|---|---|---:|---|
| 1 | CC145327 | Platinum | 92,5 | Fuel_Spending (−5,1), Mobile_App_Login (+1,9) |
| 2 | CC107443 | Silver | 90,1 | Online_Shopping_Spending (−4,1), Monthly_Transactions (+2,1) |
| 3 | CC139311 | Gold | 87,4 | Travel_Spending (−4,6), Monthly_Transactions (+2,2) |
| 4 | CC102360 | Silver | 79,1 | Travel_Spending (−5,1), Mobile_App_Login (+2,0) |
| 5 | CC111198 | Gold | 78,1 | Dining_Spending (−3,6), Monthly_Transactions (+2,1) |
| 6 | CC140420 | Basic | 77,7 | Utility_Bill_Spending (−3,4), Payment_Amount (−2,4) |
| 7 | CC112045 | Basic | 76,6 | Entertainment_Spending (−5,6), Dining_Spending (−3,1) |
| 8 | CC102122 | Silver | 75,1 | Fuel_Spending (−4,9), Age (+2,7) |
| 9 | CC145049 | Basic | 74,4 | Travel_Spending (−4,9), Credit_Score (−2,5) |
| 10 | CC106625 | Platinum | 74,3 | Travel_Spending (−3,8), Monthly_Transactions (+2,2) |

#### 13.7.4 Tipo de tarjeta de los raros frente al resto (% por fila)

| | Basic | Silver | Gold | Platinum | Signature |
|---|---:|---:|---:|---:|---:|
| Raros | 20,1 | 15,1 | 27,2 | 24,1 | 13,5 |
| Resto | 20,5 | 24,4 | 34,0 | 16,3 | 4,7 |

**Lectura.**

- Los diez más lejanos **no son clientes enormes ni diminutos**: casi todos tienen **una categoría de gasto prácticamente en cero** (combustible, viajes, entretenimiento, compras en línea, servicios, restaurantes) a cuatro o cinco desviaciones por debajo de lo normal **en escala logarítmica**, mientras el resto de su perfil es corriente o alto (más transacciones, más ingresos a la app). Es el **"perfil disparejo"** de la sesión: un cliente que gasta en todo menos en una cosa rompe la regla de la cartera, donde todas las categorías suben juntas con el ingreso.
- El grupo de raros **no sale al azar**: puntaje mediano 573 contra 639, proporción pagada 0,57 contra 0,85, y las tarjetas `Platinum` (24,1 % vs 16,3 %) y `Signature` (13,5 % vs 4,7 %, casi el triple) están **sobrerrepresentadas**, mientras `Silver` y `Gold` están subrepresentadas.

**Significado para el negocio.** Para la Gerencia de Riesgo, **la lista de casos raros es también una lista con más riesgo que el promedio**: concentran tarjetas de gama alta, pagan menos de lo que deben y tienen peor puntaje.

### 13.8 La decisión: ¿se borran?

**Cómo se evaluó.** Se compara la matriz de correlación con y sin los raros (`R_con <- cor(X_log)`; `R_sin <- cor(X_log[!raros, ])`) y la media de `Credit_Score`. Además se crea la tabla `credit_marcas` (`Customer_ID`, `d2_mahalanobis`, `caso_raro`).

**Resultado:**

| Indicador | Valor |
|---|---:|
| Cambio máximo en cualquier correlación de $\mathbf{R}$ | 0,02 |
| Media de Credit_Score con todos | 629,0 |
| Media de Credit_Score sin los raros | 630,6 |
| `caso_raro = FALSE` / `TRUE` | 48 359 / 1 641 |

**Lectura.** Quitando los 1 641 casos raros, ninguna correlación se mueve más de **0,02** y el puntaje medio pasa de **629 a 630,6**. **Borrarlos no arreglaría nada, porque no están rompiendo nada**, y haría desaparecer del informe a un grupo con más riesgo que el promedio. Ninguno es un error de captura: la base no tiene faltantes, duplicados ni valores imposibles (Módulo 2).

**Decisión final:**

| Grupo | Cuántos | Qué es | Qué se hace |
|---|---:|---|---|
| Errores de captura | 0 | No hay (Módulo 2) | — |
| Perfil disparejo (una categoría de gasto casi en cero) | 1 641 | **Atípico real**: clientes de verdad | Se **dejan y se marcan** (`caso_raro`, que en la tabla *silver* se llama `Caso_Raro_Mahalanobis`); son un hallazgo, con más riesgo que el promedio |

La frase de la sesión, ahora con una herramienta que la aplica: ***un atípico se estudia; un error se corrige.***

**Significado para el negocio.** Riesgo no pierde a nadie de la cartera ni distorsiona los promedios, y gana una bandera operativa (`Caso_Raro_Mahalanobis`) para revisión manual o seguimiento.

### Conclusión del Módulo 13

1. **Variable por variable no alcanza:** el 64 % de los casos raros no tiene ninguna variable extrema, y en el plano de riesgo hay 868 clientes fuera de la elipse con las dos variables dentro de las bandas.
2. **Mahalanobis mide con la forma de la nube:** separa al cliente grande pero coherente (lejano en euclidiana; solo 26 de 500 coinciden) del cliente disparejo.
3. **El Q-Q dice hasta dónde confiar en el corte $\chi^2$:** con las variables crudas la cartera se aparta de la campana desde el cuerpo (asimetría; 8,8 % fuera del corte del 97,5 %); con `log(x+1)` el cuerpo se acomoda y queda una cola de casos a revisar.
4. **La decisión:** no hay errores que corregir; los 1 641 casos raros se marcan y se conservan, porque no mueven la estructura de correlación (cambio máximo 0,02) y concentran más riesgo que el resto de la cartera.

---

## Módulo 14: Pruebas de hipótesis

### Punto de partida

El gráfico Q-Q del Módulo 13 dejó una **sospecha visual**: los puntos se despegaban de la recta de 45°, señal de que la cartera no es normal multivariante. Este módulo convierte esa sospecha en **tres pruebas formales**, cada una con su hipótesis nula explícita, su estadístico y su $p$-valor:

1. normalidad univariada;
2. normalidad multivariante (Mardia);
3. significancia de las correlaciones usadas en los Módulos 7 y 8.

### 14.1 Concepto: prueba de hipótesis y $p$-valor

- **Hipótesis nula $H_0$:** la afirmación "sin efecto" que se intenta refutar (p. ej., "la variable es normal"). **Alternativa $H_1$:** su negación.
- **Estadístico de prueba:** un número calculado con los datos cuya distribución se conoce si $H_0$ es cierta.
- **$p$-valor:** probabilidad, suponiendo $H_0$ cierta, de obtener un estadístico tan extremo o más que el observado. Si $p<\alpha$ (habitualmente 0,05) se rechaza $H_0$.
- **$p<2{,}2\times10^{-16}$:** es el menor número que R muestra (`format.pval(..., eps = 2.2e-16)`, el épsilon de máquina); significa "prácticamente cero", y en la salida aparece como `<2e-16`.
- **Por qué con $n=50\,000$ casi todo sale significativo:** el error estándar de cualquier estimación se reduce como $1/\sqrt n$. Una prueba de bondad de ajuste o de correlación compara una desviación observada contra ese error estándar; con $n$ enorme, hasta desviaciones minúsculas, sin ninguna importancia práctica, quedan muchas veces por encima de su error y se declaran "significativas". La **significancia estadística** no equivale a **importancia práctica**; por eso en este informe las decisiones se toman por la **magnitud** (asimetría, $r$, forma del Q-Q), no por el $p$-valor.

### 14.2 Normalidad univariada

**Hipótesis.** $H_0$: la variable proviene de una normal, $X\sim\mathcal{N}(\mu,\sigma^2)$; $H_1$: no proviene de una normal.

**Variables puestas a prueba** (las cuatro que sirven de hilo conductor en el informe):

| Variable | Por qué se eligió |
|---|---|
| `Credit_Score` | La más simétrica (asimetría −0,58) |
| `Age` | Asimetría leve |
| `Annual_Income` | Fuertemente sesgada (asimetría 2,55) |
| `Payment_Ratio` | Acotada y con asimetría negativa |

#### 14.2.1 Las pruebas usadas

- **Kolmogorov–Smirnov (KS):** compara la función de distribución empírica $F_n(x)$ con la teórica $F_0(x)$ mediante $D=\sup_x |F_n(x)-F_0(x)|$, la mayor separación vertical entre ambas curvas acumuladas.
- **Lilliefors:** es KS cuando $\mu$ y $\sigma$ **se estiman de los datos** (lo que siempre ocurre en la práctica). Al estimar los parámetros la normal ajustada queda "más pegada" a los datos, así que los valores críticos del KS clásico serían demasiado indulgentes; Lilliefors usa valores críticos corregidos. **No tiene límite de tamaño muestral**, así que se aplicó sobre los **50 000** clientes (`nortest::lillie.test()`).
- **Shapiro–Wilk:** $W=\dfrac{\left(\sum_i a_i x_{(i)}\right)^2}{\sum_i (x_i-\bar x)^2}$, donde $x_{(i)}$ son los datos ordenados y $a_i$ coeficientes derivados de los valores esperados de los estadísticos de orden de una normal. Mide qué tan bien se alinean los datos en un Q-Q normal: $W$ cercano a 1 indica normalidad. Es de las más potentes, pero en R `shapiro.test()` **no admite $n>5\,000$**, así que se aplicó sobre una **submuestra aleatoria de exactamente 5 000** clientes, con `set.seed(42)` para que sea reproducible.
- (Anderson–Darling no se usó en este módulo.)

#### 14.2.2 Resultados

| Variable | Lilliefors $D$ | $p$ Lilliefors | Shapiro–Wilk $W$ ($n=5\,000$) | $p$ Shapiro |
|---|---:|---|---:|---|
| Credit_Score | 0,0570 | <2e-16 | 0,9713 | <2e-16 |
| Age | 0,0899 | <2e-16 | 0,9544 | <2e-16 |
| Annual_Income | 0,2210 | <2e-16 | 0,7166 | <2e-16 |
| Payment_Ratio | 0,1616 | <2e-16 | 0,8515 | <2e-16 |

**Lectura.** Las cuatro variables **rechazan $H_0$** con $p<2{,}2\times10^{-16}$ en las dos pruebas, **incluida `Credit_Score`**, que es visualmente la más cercana a una campana de Gauss de todo el dataset (asimetría apenas −0,58): su $W=0{,}9713$ rechaza la normalidad con la misma contundencia ($p$) que `Annual_Income`, cuya asimetría (2,55) es evidente a simple vista. La **magnitud** de los estadísticos sí ordena bien a las variables: $D$ va de 0,057 (Credit_Score) a 0,221 (Annual_Income), y $W$ de 0,971 a 0,717.

**Por qué el rechazo es casi automático a este tamaño de muestra.** La potencia de una prueba de bondad de ajuste crece con $n$. Con 50 000 observaciones, hasta una desviación mínima de la normalidad (una cola apenas más pesada, un exceso de curtosis casi imperceptible al ojo) es estadísticamente detectable, porque el error estándar con el que se estima esa desviación se achica con $\sqrt n$. **El rechazo no dice "esta variable está mal" ni contradice el análisis descriptivo de los Módulos 3 a 5**: dice que, a $n=50\,000$, casi ninguna variable real pasa una prueba formal de normalidad exacta.

**Decisión.** El criterio práctico para decidir qué tan "normal" es una variable sigue siendo el usado en todo el informe: **histograma, asimetría numérica y Q-Q**, no el $p$-valor.

### 14.3 Normalidad multivariante: asimetría y curtosis de Mardia

**Hipótesis.** $H_0$: $\mathbf{x}=(x_1,\dots,x_p)'$ proviene de una normal multivariante, $\mathbf{X}\sim\mathcal{N}_p(\boldsymbol\mu,\boldsymbol\Sigma)$.

**Concepto.** Mardia (1970) generaliza la asimetría y la curtosis a $p$ dimensiones usando los productos de Mahalanobis

$$
g_{ij}=(\mathbf{x}_i-\bar{\mathbf{x}})'\mathbf{S}^{-1}(\mathbf{x}_j-\bar{\mathbf{x}}),
\qquad
b_{1,p}=\frac{1}{n^2}\sum_{i=1}^n\sum_{j=1}^n g_{ij}^3,
\qquad
b_{2,p}=\frac1n\sum_{i=1}^n g_{ii}^2 .
$$

- $g_{ii}$ es exactamente la $d^2$ de Mahalanobis del cliente $i$; $b_{2,p}$ es la media de las $d^4$ (curtosis multivariante: ¿hay más masa en las colas de lo que una normal permite?).
- $b_{1,p}$ mide la asimetría multivariante (para una normal es 0).
- Bajo $H_0$: $\dfrac{n}{6}\,b_{1,p}\;\approx\;\chi^2$ con $\dfrac{p(p+1)(p+2)}{6}$ grados de libertad, y $b_{2,p}\approx\mathcal{N}\!\left(p(p+2),\;\dfrac{8p(p+2)}{n}\right)$, de donde $z=\dfrac{b_{2,p}-p(p+2)}{\sqrt{8p(p+2)/n}}\sim\mathcal{N}(0,1)$.

**Por qué una submuestra.** Calcular $g_{ij}$ para todos los pares exige una matriz $n\times n$: con $n=50\,000$ son más de **2 500 millones de celdas**, computacionalmente inviable. Por la misma razón práctica que obliga a submuestrear para Shapiro–Wilk, Mardia se aplica sobre una **submuestra aleatoria de 1 500 clientes** (`set.seed(42)`) y las **21 variables no redundantes** del Módulo 10 (todas las numéricas menos `Monthly_Spending`, `Payment_Ratio`, `Credit_Utilization`, `Reward_Points_Earned`, `Outstanding_Balance`).

**Cómo se aplicó.** Implementación a mano en R: `G_m <- Xc_m %*% solve(S_m) %*% t(Xc_m)`, `b1p <- sum(G_m^3)/m^2`, `b2p <- mean(diag(G_m)^2)`; $p$-valores con `pchisq(..., lower.tail = FALSE)` y `2*pnorm(-abs(z))`. Grados de libertad: $21\cdot22\cdot23/6=1\,771$; media teórica de $b_{2,p}$: $21\cdot23=483$.

**Resultado (variables tal como vienen):**

| Estadístico | Valor | Referencia | $p$-valor |
|---|---:|---|---|
| Asimetría de Mardia ($\tfrac n6 b_{1,p}$) | 180 827,90 | $\chi^2$, gl = 1 771 | <2e-16 |
| Curtosis de Mardia ($z$ de $b_{2,p}$) | 1 158,15 | $\mathcal{N}(0,1)$ | <2e-16 |

**Lectura.** Asimetría y curtosis multivariantes rechazan $H_0$ con $p<2{,}2\times10^{-16}$. El estadístico de asimetría (180 828) es **más de 100 veces** su grado de libertad esperado bajo $H_0$ (1 771; la media de una $\chi^2$ es su gl), y la curtosis se aleja **1 158 desviaciones estándar** de lo que una normal multivariante predeciría. Es la **confirmación formal, no solo visual**, de lo que el Q-Q del Módulo 13 insinuaba: con 21 variables que incluyen varias fuertemente asimétricas a la derecha (`Cash_Advance_Amount`, `Travel_Spending` y el resto de categorías de gasto), la cartera se aleja de la normalidad multivariante de forma contundente. Es también la razón por la que el corte $\chi^2$ de Mahalanobis marcaba **8,8 %** de atípicos en vez del 2,5 % teórico.

#### 14.3.1 ¿Y con `log(x+1)`?

Se repitió Mardia (función `mardia()` escrita en el informe) sobre la **misma submuestra de 1 500 clientes** (`set.seed(42)`), ahora comparando las variables crudas (`vars_mahal`) con la versión transformada `X_log` del Módulo 13.

| Versión | Asimetría ($\tfrac n6 b_{1,p}$) | gl | $p$ asimetría | Curtosis $z$ | $p$ curtosis |
|---|---:|---:|---:|---:|---:|
| Tal como vienen | 180 828 (180 800 a 4 cifras) | 1 771 | 0 (bajo el mínimo representable) | 1 158,2 | 0 |
| Con log(x+1) | 7 979 | 1 771 | 0 (bajo el mínimo representable) | 13,75 | $4{,}955\times10^{-43}$ |

**Lectura.** La transformación reduce la asimetría de **180 828 a 7 979** (unas 23 veces) y la curtosis de **1 158,2 a 13,8** desviaciones, pero la prueba **sigue rechazando** la normalidad multivariante. La lectura coincide con la del Q-Q: `log(x+1)` acerca mucho la cartera a una campana (lo suficiente para que el cuerpo de las distancias siga la $\chi^2$), pero las variables **infladas en cero** (`Cash_Advance_Amount`, `International_Transactions`) no se vuelven normales con ningún logaritmo: un logaritmo de una masa de ceros sigue siendo una masa en un punto.

**Decisión.** El informe usa la normal multivariante como **referencia**, no como supuesto exacto, y por eso el PCA de los Módulos 16 y 17, que **no necesita normalidad**, es la técnica adecuada para lo que sigue.

### 14.4 Pruebas de correlación

**Concepto.** $H_0:\rho=0$ (no hay correlación lineal en la población) contra $H_1:\rho\neq0$. Bajo $H_0$ y normalidad aproximada,

$$
t=\frac{r\sqrt{n-2}}{\sqrt{1-r^2}}\sim t_{n-2}.
$$

Se aplicó con `cor.test()` (Pearson) a los tres pares que el Módulo 7 ya había seleccionado con un criterio objetivo.

**Resultado:**

| Par | $r$ | $t$ | gl | $p$-valor |
|---|---:|---:|---:|---|
| Annual_Income – Credit_Limit | 0,974 | 964,5 | 49 998 | <2e-16 |
| Payment_Ratio – Credit_Score | 0,767 | 267,4 | 49 998 | <2e-16 |
| Credit_Utilization – Credit_Score | −0,599 | −167,4 | 49 998 | <2e-16 |

**Lectura.** Los tres pares rechazan $H_0:\rho=0$ con $p<2{,}2\times10^{-16}$ y estadísticos $t$ de varios cientos en valor absoluto (hasta **965** para `Annual_Income`–`Credit_Limit`). Con $n=50\,000$ incluso una correlación poblacional pequeña sería significativa (con $n-2=49\,998$, cualquier $|r|$ mayor que aproximadamente 0,009 ya rechaza al 5 %), así que lo relevante nunca fue si el $p$-valor rechazaba, sino la **magnitud** de $r$, ya discutida en el Módulo 6: **0,974, 0,767 y −0,599**, muy por encima de cualquier umbral de significancia práctica.

**Significado para el negocio.** Ingreso y cupo van prácticamente de la mano (la política de cupos sigue al ingreso); pagar una mayor proporción del extracto se asocia fuertemente con mejor puntaje, y usar más el cupo con peor puntaje. Estas relaciones no son ruido estadístico: son grandes y estables.

### Conclusión del Módulo 14

1. Las cuatro variables univariadas puestas a prueba, incluida `Credit_Score` (la más simétrica del dataset), rechazan formalmente la normalidad ($p<2{,}2\times10^{-16}$ en Lilliefors y Shapiro–Wilk), pero eso es principalmente un **efecto del tamaño muestral**: a $n=50\,000$ la prueba detecta desviaciones mínimas que el histograma y la asimetría numérica ya habían calificado de leves.
2. La prueba de **Mardia** confirma formalmente (no solo con el Q-Q del Módulo 13) que la cartera **no es normal multivariante**, ni en asimetría (180 828 vs gl 1 771) ni en curtosis ($z=1\,158$), calculada sobre una submuestra de 1 500 clientes por la misma razón computacional que obliga a submuestrear para Shapiro–Wilk. Con `log(x+1)` mejora muchísimo (7 979 y $z=13{,}75$) pero sigue rechazando, por las variables infladas en cero.
3. Las tres correlaciones clave del Módulo 7 rechazan $H_0:\rho=0$ con enorme margen, pero a este tamaño de muestra esa prueba es casi un trámite: la decisión de qué variables importan siempre se apoyó en la **magnitud de $r$**, no en si el test rechazaba.

---

## Módulo 15: Preparación de datos para PCA y clustering

### Punto de partida

Todo el informe hasta aquí describió la cartera tal como es. Este módulo cierra el análisis exploratorio con la pregunta que importa para lo que sigue (reducción de dimensionalidad con PCA, segmentación con *clustering*):

> **¿Qué se hace, en concreto, con cada una de las 30 variables antes de alimentarlas a esos algoritmos?**

PCA y la mayoría de algoritmos de *clustering* asumen tres condiciones que la matriz cruda **todavía no cumple**:

1. variables **numéricas** (hay 4 de texto);
2. en una **escala comparable** (hay rupias, conteos, puntajes y proporciones; además, muchas variables muy asimétricas);
3. **sin redundancia lineal exacta** (hay sumas y cocientes de otras columnas).

### 15.1 Conceptos previos

- **Estandarización (`scale()`):** $z_{ij}=(x_{ij}-\bar x_j)/s_j$. Deja cada variable con media 0 y desviación 1, para que ninguna domine por sus unidades (equivale a trabajar con la matriz de correlación $\mathbf{R}$ en lugar de $\mathbf{S}$).
- **Transformación $\log(x+1)$ (`log1p()`):** comprime la cola derecha de variables positivas muy asimétricas; el "+1" permite aplicarla a ceros ($\log(0+1)=0$). Se aplica **antes** de estandarizar.
- **Redundancia / colinealidad:** si una columna es (casi) combinación lineal de otras, $\mathbf{S}$ es (casi) singular: determinante ≈ 0, un valor propio ≈ 0, no invertible. En PCA produce componentes sin información; en Mahalanobis o regresión impide invertir $\mathbf{S}$.

### 15.2 ¿Cómo se va a transformar cada variable numérica?

**Regla reproducible (no a mano).** Para cada una de las 26 variables numéricas:

1. si ya se identificó como **redundante o derivada** (Módulo 10, función `revisar()`), se marca **Excluir**;
2. si no, y su asimetría $|\text{skew}|>1$, se recomienda **`log(x+1)` + `scale()`** (el mismo umbral, en espíritu, que separó los dos grupos de atípicos del Módulo 5);
3. en otro caso, solo **`scale()`**.

Código: `skew <- function(x) mean(((x - mean(x)) / sd(x))^3)`; `excluir_num <- c("Monthly_Spending", "Payment_Ratio", "Credit_Utilization", "Reward_Points_Earned", "Outstanding_Balance")`; la columna `Transformacion` se arma con `ifelse` anidados.

**Resultado (tabla de transformación por variable):**

| Variable | Tipo en R | Asimetría | Transformación |
|---|---|---:|---|
| Age | integer | 0,69 | scale() |
| Annual_Income | integer | 2,55 | log(x+1) + scale() |
| Credit_Limit | numeric | 3,01 | log(x+1) + scale() |
| Card_Age_Months | integer | 1,14 | log(x+1) + scale() |
| Monthly_Spending | numeric | 3,00 | Excluir (redundante/derivada) |
| Monthly_Transactions | integer | 0,54 | scale() |
| Avg_Transaction_Value | numeric | 3,90 | log(x+1) + scale() |
| Online_Shopping_Spending | numeric | 4,56 | log(x+1) + scale() |
| Grocery_Spending | numeric | 4,01 | log(x+1) + scale() |
| Fuel_Spending | numeric | 4,69 | log(x+1) + scale() |
| Dining_Spending | numeric | 4,64 | log(x+1) + scale() |
| Travel_Spending | numeric | 5,71 | log(x+1) + scale() |
| Entertainment_Spending | numeric | 5,01 | log(x+1) + scale() |
| Utility_Bill_Spending | numeric | 4,35 | log(x+1) + scale() |
| Outstanding_Balance | numeric | 4,02 | Excluir (redundante/derivada) |
| Statement_Balance | numeric | 3,80 | log(x+1) + scale() |
| Payment_Amount | numeric | 4,20 | log(x+1) + scale() |
| Payment_Ratio | numeric | −1,04 | Excluir (redundante/derivada) |
| Credit_Utilization | numeric | 0,53 | Excluir (redundante/derivada) |
| Cash_Advance_Amount | numeric | 6,78 | log(x+1) + scale() |
| EMI_Count | integer | 0,17 | scale() |
| International_Transactions | integer | 2,11 | log(x+1) + scale() |
| Reward_Points_Earned | integer | 3,50 | Excluir (redundante/derivada) |
| Reward_Points_Redeemed | integer | 6,55 | log(x+1) + scale() |
| Mobile_App_Login | integer | 0,33 | scale() |
| Credit_Score | integer | −0,58 | scale() |

**Resumen:**

| Tratamiento | Nº | Variables |
|---|---:|---|
| `log(x+1)` + `scale()` | 16 | Annual_Income, Credit_Limit, Card_Age_Months, Avg_Transaction_Value, las 7 categorías de gasto, Statement_Balance, Payment_Amount, Cash_Advance_Amount, International_Transactions, Reward_Points_Redeemed |
| Solo `scale()` | 5 | Age, Monthly_Transactions, EMI_Count, Mobile_App_Login, Credit_Score |
| Excluir | 5 | Monthly_Spending, Outstanding_Balance, Payment_Ratio, Credit_Utilization, Reward_Points_Earned |
| **Total** | **26** | |

**Lectura.** 16 de las 26 variables numéricas quedan marcadas para transformación logarítmica: casi todas las de gasto, saldo y conteo con masa en cero, exactamente el grupo que el Módulo 5 había señalado con más del 8 % de atípicos univariados bajo la regla de Tukey (la más asimétrica es `Cash_Advance_Amount`, 6,78). Cinco variables son razonablemente simétricas y solo necesitan estandarizarse. Las cinco restantes se excluyen **no porque tengan mala calidad**, sino porque el Módulo 10 demostró que vuelven casi singular la matriz de covarianzas. (Nótese que `Payment_Ratio`, con −1,04, y `Credit_Utilization`, con 0,53, se excluyen por redundancia, no por su asimetría.)

#### 15.2.1 Las cuatro variables cualitativas

Ni el logaritmo ni `scale()` tienen sentido sobre texto; se tratan aparte:

| Variable | Tipo en R | Naturaleza real | Transformación |
|---|---|---|---|
| Customer_ID | chr | Identificador nominal único | Quitar (no es variable de análisis) |
| Gender | chr | Nominal (2 niveles) | `factor()` |
| Occupation | chr | Nominal (6 niveles) | `factor()`; one-hot para PCA y clustering |
| Card_Type | chr | Ordinal (5 niveles) | `factor(ordered = TRUE)` o codificación entera 1 a 5 (Basic = 1 … Signature = 5), aprovechando la Tendencia 6 del Módulo 7 |

### 15.3 ¿Con cuáles variables nos quedamos, y por qué?

La decisión combina tres criterios ya aplicados por separado: la clasificación de variables (Módulo 1), la verificación de redundancia antes de invertir $\mathbf{S}$ (Módulo 10) y la selección objetiva de variables bivariadas (Módulo 7). Código: `retenidas <- setdiff(numeric_cols, excluir_num)`.

#### 15.3.1 Variables numéricas retenidas (21)

`Age, Annual_Income, Credit_Limit, Card_Age_Months, Monthly_Transactions, Avg_Transaction_Value, Online_Shopping_Spending, Grocery_Spending, Fuel_Spending, Dining_Spending, Travel_Spending, Entertainment_Spending, Utility_Bill_Spending, Statement_Balance, Payment_Amount, Cash_Advance_Amount, EMI_Count, International_Transactions, Reward_Points_Redeemed, Mobile_App_Login, Credit_Score`

| Bloque | Variables |
|---|---|
| Capacidad financiera | Annual_Income, Credit_Limit |
| Gasto por categoría (7) | Online_Shopping, Grocery, Fuel, Dining, Travel, Entertainment, Utility_Bill (todas `_Spending`) |
| Saldos y pagos no redundantes | Statement_Balance, Payment_Amount |
| Historial de comportamiento | Cash_Advance_Amount, EMI_Count, International_Transactions, Reward_Points_Redeemed, Mobile_App_Login, Card_Age_Months, Monthly_Transactions, Avg_Transaction_Value |
| Demografía | Age |
| Riesgo | Credit_Score |

Son la base de gasto, capacidad e historial que efectivamente varía de forma independiente entre sí: según el Módulo 8, la matriz de correlación de estas variables ya no tiene el valor propio casi nulo que sí tenía la matriz completa.

#### 15.3.2 Variables descartadas y su motivo

| Variable | Motivo |
|---|---|
| `Customer_ID` | Identificador nominal único (Módulo 1): no mide nada, no aporta varianza informativa |
| `Monthly_Spending` | Es la **suma exacta** de las siete categorías de gasto que se retienen por separado; incluirla junto con sus componentes es colinealidad garantizada ($r=1$ con su propia suma) |
| `Outstanding_Balance` | Correlación **0,997** con `Statement_Balance` (Módulo 8): la misma información económica medida dos veces; se retiene `Statement_Balance` como representante del par |
| `Reward_Points_Earned` | Correlación **0,980** con `Monthly_Spending` (a su vez excluida): función casi lineal del gasto, sin información propia |
| `Payment_Ratio` | Cociente derivado, aproximadamente `Payment_Amount`/`Statement_Balance`; con sus componentes vuelve $\mathbf{S}$ casi singular (Módulo 10) |
| `Credit_Utilization` | Cociente derivado, aproximadamente `Outstanding_Balance`/`Credit_Limit`; mismo problema |

**Caso especial: `Payment_Ratio` y `Credit_Utilization`.** Se excluyen **de la matriz numérica que construye el PCA**, pero precisamente por ser las dos variables que de verdad predicen `Credit_Score` (Módulo 7) se recomienda reincorporarlas después como **variables suplementarias**: proyectarlas sobre los componentes o perfilar los clusters con ellas, para **interpretarlos**, no para construirlos.

**Las tres categóricas** (`Gender`, `Occupation`, `Card_Type`) no entran a un PCA clásico sobre la matriz de correlación (que asume variables continuas), pero se conservan aparte para dos usos: perfilar los clusters que resulten de las 21 numéricas (¿un cluster de alto riesgo se concentra en alguna `Occupation`?) y, en el caso de `Card_Type`, como candidata a codificarse como entero ordinal 1–5 y agregarse a la matriz numérica, dado que la Tendencia 6 del Módulo 7 mostró que su orden se refleja linealmente en `Credit_Limit`.

### 15.4 Codificación *one-hot* de las variables categóricas

**Concepto.** Una variable nominal no se puede convertir en número asignando 1, 2, …, 6 a sus niveles: eso inventaría un **orden** (¿`Retired` está "entre" `Private Employee` y `Self-Employed`?) y una **distancia** (¿`Student` está "el doble de lejos" de `Business Owner` que `Government Employee`?) que no existen, y cualquier resultado cambiaría con solo reordenar los niveles. La codificación correcta es **one-hot**: una columna 0/1 por cada nivel, que vale 1 si el cliente pertenece a ese nivel y 0 si no. Para una variable con $k$ niveles,

$$
D_{i\ell}=\mathbb{1}\{x_i=\text{nivel }\ell\},\qquad \ell=1,\dots,k .
$$

**Cómo se aplicó.**

- `categoricas`: `Gender` y `Occupation` como `factor()`; `Card_Type` como `factor(..., levels = orden_tarjeta)` (orden Basic → Silver → Gold → Platinum → Signature).
- Función `one_hot(f, prefijo)` con `model.matrix(~ f - 1)`: el `- 1` quita el intercepto y pide **todos** los niveles (sin categoría de referencia); las columnas se nombran `prefijo_nivel`.
- `D_onehot <- cbind(D_gender, D_ocup, D_card)`.

**Resultado.** `dim(D_onehot)` = **50 000 × 13**: 2 columnas de género (`Gender_F`, `Gender_M`), 6 de ocupación (`Occupation_Business Owner`, `_Government Employee`, `_Private Employee`, `_Retired`, `_Self-Employed`, `_Student`) y 5 de tarjeta (`Card_Type_Basic`, `_Silver`, `_Gold`, `_Platinum`, `_Signature`).

Primeras cuatro filas (género y tarjeta):

| Fila | Gender_F | Gender_M | Basic | Silver | Gold | Platinum | Signature |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| 2 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| 3 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |
| 4 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |

**Verificaciones:**

| Verificación | Resultado |
|---|---|
| Cada cliente tiene exactamente un 1 por bloque (`rowSums == 1` en los tres bloques) | TRUE |
| Los conteos por columna coinciden con las tablas de frecuencia del Módulo 2 (tarjeta y ocupación) | TRUE |

**Lectura.** Las 3 variables categóricas se convierten en 13 columnas 0/1 y la codificación no perdió ni inventó a ningún cliente.

#### 15.4.1 La trampa de las *dummies*: el mismo problema del Módulo 10

**Concepto.** Dentro de cada bloque, las columnas **siempre suman 1** (todo cliente pertenece a exactamente un nivel):

$$
\sum_{\ell=1}^{k} D_{i\ell}=1\quad\forall i .
$$

Es una **combinación lineal exacta** (multicolinealidad perfecta): cualquier columna se obtiene como 1 menos la suma de las otras. Es la misma situación de `Monthly_Spending` frente a sus siete categorías de gasto. En regresión con intercepto, además, la suma de las $k$ dummies reproduce la columna de unos del intercepto. Consecuencia: la matriz de covarianzas/correlación del bloque es **singular** (determinante 0, un valor propio 0).

**Cómo se comprobó.** `R_card <- cor(D_card)`; `det(R_card)`; `min(eigen(R_card)$values)`. Luego, con $k-1$ columnas (`model.matrix(~ Card_Type)[, -1]`, que usa `Basic` como referencia), `det(cor(D_card_k1))`.

**Resultado:**

| Codificación de Card_Type | Determinante de $\mathbf{R}$ | Menor valor propio |
|---|---:|---:|
| $k=5$ columnas | $3{,}73\times10^{-16}$ | $2{,}66\times10^{-15}$ |
| $k-1=4$ columnas | 0,5154 | no reportado |

**Lectura.** Con las 5 columnas de tarjeta, el determinante y el menor valor propio son prácticamente cero (ruido numérico de máquina): la nube de las *dummies* es **plana en una dirección**. Con $k-1$ columnas la dependencia desaparece (determinante 0,515).

**Reglas que se aplican en el resto del informe:**

| Uso | Codificación | Por qué |
|---|---|---|
| Regresión, Mahalanobis, cualquier cosa que invierta $\mathbf{S}$ | $k-1$ columnas (una categoría de referencia) | Con las $k$ columnas $\mathbf{S}$ es singular |
| PCA y *clustering* | Las $k$ columnas, **ponderadas por $1/\sqrt{k}$** después de estandarizar | Todas las categorías quedan simétricas (ninguna es "la referencia"), y las $k$ columnas de una variable pesan juntas lo que pesa **una** variable numérica (si cada una tiene varianza 1, las $k$ ponderadas suman $k\cdot\frac1k=1$); la dependencia exacta solo produce una última componente con varianza cero, no rompe nada |

`Card_Type` admite además una codificación **ordinal 1 a 5** (Basic = 1, …, Signature = 5), porque su orden se refleja en el cupo (Tendencia 6 del Módulo 7). El Módulo 17 usa la versión one-hot ponderada para comparar el mapa de clientes con y sin el tipo de tarjeta.

### 15.5 La matriz final

**Cómo se armó.**

- `vars_log_pca`: las 16 variables marcadas `log(x+1) + scale()`.
- `X_transf <- credit[, retenidas]`; se aplica `log1p` a las 16; `Z_pca <- scale(X_transf)`.

**Resultado (verificación):**

| clientes | variables numéricas | con log | dummies | medias = 0 | desviaciones = 1 |
|---:|---:|---:|---:|---|---|
| 50 000 | 21 | 16 | 13 | TRUE | TRUE |

(Medias y desviaciones verificadas con tolerancia $10^{-10}$.) `Z_pca` es la matriz que entra al PCA del Módulo 16 (`prcomp(Z_pca)`, equivalente a trabajar sobre $\mathbf{R}$ con log).

### 15.6 Exportación: arquitectura medallion bronze / silver / gold (sesión S02)

**Concepto.** La arquitectura *medallion* organiza los datos en capas de calidad creciente, y exige que **toda limpieza quede en código** y que **el dato crudo no se toque**:

| Capa | Qué contiene | En este proyecto |
|---|---|---|
| **Bronze** | Dato crudo, tal como llegó; nunca se edita | `data/bronze/synthetic_credit_card_customer_behavior_dataset.csv` |
| **Silver** | Tabla limpia y **tipada** (factores, orden, marcas de calidad), todavía en unidades originales | `data/silver/credit_card_silver.csv` y `.rds` |
| **Gold** | Tabla lista para el modelo / el consumidor final | `data/gold/credit_card_gold_pca.csv` |

**Cómo se aplicó.**

- *Silver:* `credit_silver` = `credit` con `Gender` y `Occupation` como factores, `Card_Type` como `factor(..., ordered = TRUE)` en el orden Basic < Silver < Gold < Platinum < Signature, y dos columnas nuevas: `Banda_Riesgo` (la banda de riesgo construida en un módulo anterior, objeto `credit_banda`) y `Caso_Raro_Mahalanobis` (la marca `raros` del Módulo 13). Se guarda con `write.csv()` y con `saveRDS()`.
- *Gold:* `credit_gold` = `Customer_ID` + `round(Z_pca, 6)` + `D_onehot` (dummies 0/1 sin ponderar; la ponderación $1/\sqrt k$ se aplica al usarlas en el módulo de PCA), con `write.csv()`.
- Se crean las carpetas con `dir.create()` si no existen.

**Estructura de los archivos exportados:**

| Archivo | Filas de datos | Columnas | Contenido |
|---|---:|---:|---|
| `data/silver/credit_card_silver.csv` | 50 000 (+ cabecera) | 32 | Las 30 originales en unidades originales + `Banda_Riesgo` + `Caso_Raro_Mahalanobis` |
| `data/silver/credit_card_silver.rds` | 50 000 | 32 | Lo mismo, conservando factores y el orden de `Card_Type` |
| `data/gold/credit_card_gold_pca.csv` | 50 000 (+ cabecera) | 35 | `Customer_ID` + 21 numéricas transformadas y estandarizadas (6 decimales) + 13 dummies |

Ejemplo de la primera fila de *silver*: cliente `CC100000`, 33 años, `M`, ingreso 787 406, `Self-Employed`, `Silver`, cupo 220 000, …, `Credit_Score` 492, `Banda_Riesgo = "Alto"`, `Caso_Raro_Mahalanobis = FALSE`.

Columnas de *gold*, en orden: `Customer_ID`, `Age`, `Annual_Income`, `Credit_Limit`, `Card_Age_Months`, `Monthly_Transactions`, `Avg_Transaction_Value`, las 7 `*_Spending`, `Statement_Balance`, `Payment_Amount`, `Cash_Advance_Amount`, `EMI_Count`, `International_Transactions`, `Reward_Points_Redeemed`, `Mobile_App_Login`, `Credit_Score`, `Gender_F`, `Gender_M`, las 6 `Occupation_*` y las 5 `Card_Type_*`.

**Verificación de ida y vuelta** (se relee lo escrito y se compara):

| Verificación | Resultado |
|---|---|
| Dimensiones de silver releído (`.rds`) = originales | TRUE |
| `Card_Type` sigue siendo ordinal en silver releído | TRUE |
| Dimensiones de gold releído = originales | TRUE |
| Todas las columnas de gold (salvo `Customer_ID`) son numéricas | TRUE |

**Lectura y decisiones.**

- *Silver* va en **`.csv`** (para intercambiar, por ejemplo con Python) y en **`.rds`** (que conserva los factores y el orden de `Card_Type`, cosa que el `.csv` pierde).
- *Gold* es puramente numérica: 21 columnas estandarizadas más 13 dummies, con `Customer_ID` para poder volver a cada cliente.
- Las dos se **regeneran cada vez que se teje el informe**, así que nunca se editan a mano; *bronze* no se toca.

**Significado para el negocio.** La Gerencia de Riesgo recibe una tabla *silver* auditable (los mismos 50 000 clientes, en rupias, con la banda de riesgo y la bandera de caso raro) y una tabla *gold* lista para segmentar, ambas reproducibles desde el dato crudo con un solo comando, y trazables cliente por cliente por `Customer_ID`.

### Conclusión del Módulo 15

1. La matriz que entra a PCA y clustering no es la matriz cruda de 26 variables numéricas, sino un subconjunto de **21** que ya pasó, en los Módulos 7 a 10, las pruebas de redundancia y colinealidad que una matriz casi singular no pasaría; 16 de ellas con `log(x+1)` y todas estandarizadas.
2. Ninguna exclusión fue por baja calidad de los datos: las **cinco** variables numéricas descartadas son estadísticamente impecables, simplemente redundantes o derivadas de otras que ya están en el modelo.
3. `Payment_Ratio` y `Credit_Utilization` son un caso especial: se excluyen de la construcción de componentes/clusters por colinealidad, pero son las más útiles para **interpretarlos** después (como suplementarias), porque son las que más se relacionan con el riesgo.
4. Las tres categóricas se codifican en **one-hot** (13 columnas 0/1), nunca numerando sus niveles. Con las $k$ columnas de una variable la matriz es singular (la misma trampa de `Monthly_Spending`; determinante $3{,}7\times10^{-16}$ para tarjeta), así que se usan $k-1$ cuando hay que invertir $\mathbf{S}$ y las $k$ ponderadas por $1/\sqrt k$ en PCA.
5. El resultado queda exportado por código: la tabla limpia y tipada en `data/silver/` y la matriz lista para modelar en `data/gold/`, sin tocar el archivo crudo de `data/bronze/`.


---

## Módulo 16: Componentes Principales I — ¿Un número o varios?

> **Fuente:** `Entrega/analisis_synthetic_credit_card.Rmd`, líneas 5903–6175 (capítulo 17 del HTML renderizado el 2 de noviembre). Todas las cifras de este módulo provienen de la salida renderizada.

### 16.1 El encargo

A partir de este módulo el informe deja de ser solo descriptivo y empieza a trabajar **para un cliente concreto: la Gerencia de Riesgo de Crédito del banco emisor** de las 50.000 tarjetas.

**Situación de negocio planteada:**

- Cada mes la Gerencia decide qué clientes entran a un **programa de seguimiento preventivo**. Las acciones de ese programa son: llamada del gestor, congelar aumentos de cupo y ofrecer refinanciación **antes** de que el cliente caiga en mora.
- Hoy revisa, para cada cliente, una **ficha de 21 variables numéricas** — exactamente las retenidas en el Módulo 15 (las 26 numéricas menos las 5 excluidas por redundantes o derivadas: `Monthly_Spending`, `Payment_Ratio`, `Credit_Utilization`, `Reward_Points_Earned`, `Outstanding_Balance`).

**La pregunta del cliente** (la de la sesión de PCA I):

> *«No tengo tiempo de mirar 21 columnas por cliente. ¿Puedo ordenar la cartera con un solo número? ¿Y a quién me estoy perdiendo si lo hago?»*

**Herramienta:** el **análisis de componentes principales (PCA)**. La idea, antes del nombre: buscar el **mejor resumen posible** de las variables y **medir qué se queda por fuera**.

#### Qué es el PCA (marco conceptual)

Dada una matriz de datos $\mathbf{X}$ de $n$ clientes por $p$ variables (aquí $p = 21$), el PCA busca combinaciones lineales

$$Y_k = w_{1k}X_1 + w_{2k}X_2 + \dots + w_{pk}X_p = \mathbf{w}_k^{\top}\mathbf{x}, \qquad \|\mathbf{w}_k\| = 1,$$

tales que $Y_1$ tenga la **máxima varianza posible**, $Y_2$ la máxima varianza entre las combinaciones **no correlacionadas** con $Y_1$, y así sucesivamente. La solución es la **descomposición espectral** de la matriz de covarianzas (o de correlaciones):

$$\mathbf{R} = \mathbf{W}\boldsymbol\Lambda\mathbf{W}^{\top}, \qquad \boldsymbol\Lambda = \operatorname{diag}(\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_p),$$

- Los **autovectores** (columnas de $\mathbf{W}$) son los **pesos** o *loadings* de cada componente: dicen cuánto entra cada variable en ella. En R: `prcomp(...)$rotation`.
- Los **autovalores** $\lambda_k$ son las **varianzas de las componentes**: cuánta información guarda cada una. En R: `prcomp(...)$sdev^2`.
- Los **scores** son las coordenadas de cada cliente en las nuevas variables, $\mathbf{y}_i = \mathbf{W}^{\top}\mathbf{z}_i$. En R: `prcomp(...)$x`.

La intuición: las componentes son un **giro de ejes** de la nube de clientes, de modo que el primer eje apunte en la dirección de mayor dispersión, el segundo en la siguiente perpendicular, etc. No se crean ni destruyen datos: se re-expresan.

### 16.2 ¿Se repiten? Por qué se puede resumir

**Concepto.** Si las variables fueran independientes, **no habría forma de resumirlas**: cada una traería información que las demás no tienen, y cada componente guardaría exactamente $1/p$ de la información. **Se pueden resumir porque se repiten** (están correlacionadas). El Módulo 8 ya había mostrado dónde; aquí se cuantifica en la escala de trabajo definitiva (`log(x+1)` en las asimétricas, Módulo 15).

**Cómo se aplicó.** Se calculó la matriz de correlaciones de la matriz final `Z_pca` (21 variables, 16 de ellas con `log1p` y todas estandarizadas con `scale()`, construida en el Módulo 15), se anuló la diagonal, y para cada variable se tomó **su mayor correlación absoluta con cualquier otra**:

```r
R_pca <- cor(Z_pca)
fuera_diag <- R_pca; diag(fuera_diag) <- NA
mayor_r <- apply(abs(fuera_diag), 1, max, na.rm = TRUE)
sort(round(mayor_r, 2))
```

**Resultado (mayor $|r|$ de cada variable con alguna otra, ordenado):**

| Variable | Mayor $\lvert r\rvert$ con otra |
|---|---:|
| `Age` | 0,01 |
| `Card_Age_Months` | 0,05 |
| `Cash_Advance_Amount` | 0,07 |
| `Credit_Score` | 0,17 |
| `Reward_Points_Redeemed` | 0,23 |
| `Travel_Spending` | 0,62 |
| `EMI_Count` | 0,66 |
| `International_Transactions` | 0,66 |
| `Entertainment_Spending` | 0,67 |
| `Monthly_Transactions` | 0,68 |
| `Dining_Spending` | 0,72 |
| `Fuel_Spending` | 0,74 |
| `Online_Shopping_Spending` | 0,76 |
| `Mobile_App_Login` | 0,76 |
| `Utility_Bill_Spending` | 0,77 |
| `Avg_Transaction_Value` | 0,78 |
| `Grocery_Spending` | 0,84 |
| `Payment_Amount` | 0,93 |
| `Statement_Balance` | 0,94 |
| `Annual_Income` | 0,98 |
| `Credit_Limit` | 0,98 |

**Lectura:**

- **16 de las 21 variables** tienen al menos una compañera con $|r| > 0{,}6$: ingreso, cupo, saldo, pagos, las siete categorías de gasto, transacciones y uso de la app **cuentan casi la misma historia: el tamaño del cliente**.
- En el otro extremo quedan `Age`, `Card_Age_Months`, `Cash_Advance_Amount` y `Credit_Score`, que con ninguna otra variable pasan de **0,17**. (`Reward_Points_Redeemed`, con 0,23, también está lejos del umbral.)
- Entre las solitarias está **`Credit_Score`, la variable que más le importa a la Gerencia: va sola**.

**Anticipo del resultado del módulo:** un resumen del tamaño va a ser muy bueno, y va a decir **muy poco del riesgo**.

### 16.3 ¿Estandarizar? La decisión se toma antes de correr

**Concepto: PCA sobre $\mathbf{S}$ vs PCA sobre $\mathbf{R}$.**

- PCA **no normado** (sobre la matriz de covarianzas $\mathbf{S}$): cada variable entra con su varianza original. Si una variable se mide en números grandes (rupias), su varianza domina y la primera componente prácticamente la copia.
- PCA **normado** (sobre la matriz de correlaciones $\mathbf{R}$, equivalente a estandarizar cada variable a media 0 y desviación 1): todas las variables parten con el mismo peso (varianza 1), y las componentes reflejan **co-variación**, no unidades.

El Módulo 10 ya había decidido trabajar con $\mathbf{R}$ porque en esta cartera conviven **rupias, conteos, meses, años, proporciones y un puntaje**. Aquí se **demuestra** la decisión corriendo el PCA de tres maneras y mirando cuánto guarda la primera componente y qué variable manda en ella.

**Cómo se aplicó:**

```r
pca_sin_escala <- prcomp(credit[, retenidas], scale. = FALSE)   # sobre S, en rupias
pca_sin_log    <- prcomp(credit[, retenidas], scale. = TRUE)    # sobre R, sin log
pca            <- prcomp(Z_pca)                                 # sobre R, con log (Módulo 15)
guarda_1 <- function(pc) 100 * pc$sdev[1]^2 / sum(pc$sdev^2)     # % de varianza de C1
manda_1  <- function(pc) names(which.max(abs(pc$rotation[, 1]))) # variable de mayor peso en C1
```

Nótese que `Z_pca` ya viene centrada y escalada, por lo que `prcomp(Z_pca)` (sin `scale. = TRUE`) equivale a un PCA sobre $\mathbf{R}$ de las variables transformadas.

**Resultado:**

| Versión | % que guarda C1 | Variable que más pesa en C1 | Peso de esa variable |
|---|---:|---|---:|
| Sin estandarizar ($\mathbf{S}$, en rupias) | 95,5 | `Annual_Income` | 0,762 |
| Estandarizado, sin log ($\mathbf{R}$) | 48,0 | `Annual_Income` | 0,304 |
| `log(x+1)` + estandarizado ($\mathbf{R}$ con log) | 50,1 | `Credit_Limit` | 0,299 |

**Lectura:**

- **Sin estandarizar**, la primera componente "guarda" 95,5 de cada 100 partes de la información y una sola variable tiene peso 0,76: la componente **no es un resumen de la cartera, es `Annual_Income` con otro nombre**, simplemente porque el ingreso anual se mide en los números más grandes. El 95,5 % es un espejismo de unidades.
- **Estandarizando**, la primera componente guarda alrededor de la mitad y **ninguna variable manda sola** (el peso máximo baja a ≈0,30; con 21 variables, un peso perfectamente repartido sería $1/\sqrt{21} \approx 0{,}22$).
- Con **`log(x+1)`** el resultado casi no cambia en cantidad (48,0 frente a 50,1), pero **evita que unos pocos clientes enormes decidan la dirección de las componentes** (conclusión de los Módulos 5 y 13 sobre colas largas y casos raros).

**Decisión:** el PCA del informe es el de la **tercera fila**: `log(x+1)` en las 16 asimétricas + estandarización, es decir, `prcomp(Z_pca)`.

### 16.4 ¿Cuánta información guarda cada componente?

**Concepto: varianza explicada.** Las componentes **no crean ni destruyen información: la reparten**. Si $\lambda_1, \dots, \lambda_p$ son las varianzas de las componentes,

$$\lambda_1 + \lambda_2 + \dots + \lambda_p \;=\; \operatorname{tr}(\mathbf{R}) \;=\; p$$

(la traza del Módulo 10: con datos estandarizados cada variable aporta varianza 1). Entonces

$$\text{proporción explicada por } C_k = \frac{\lambda_k}{p}, \qquad \text{acumulada hasta } C_m = \frac{\sum_{k=1}^{m}\lambda_k}{p}.$$

**Criterios de retención** usados:

- **Kaiser:** retener componentes con $\lambda_k > 1$, es decir, las que guardan **más que una variable original** (cada variable estandarizada aporta 1).
- **Umbral acumulado:** cuántas componentes se necesitan para superar el 80 % de la información.
- **Gráfico de sedimentación / codo:** buscar dónde la caída de $\lambda_k$ se aplana (se dibujaron barras por componente y la curva acumulada con la línea del 80 %).

**Cómo se aplicó:**

```r
lambda <- pca$sdev^2
c(suma_lambdas = sum(lambda), traza_R = sum(diag(R_pca)))
reparto <- data.frame(componente, lambda, de_cada_100 = 100*lambda/sum(lambda), acumulado = ...)
c(componentes_con_lambda_mayor_a_1 = sum(lambda > 1),
  componentes_para_pasar_de_80     = which(cumsum(lambda)/sum(lambda) > 0.80)[1])
```

**Verificación:** `suma_lambdas = 21`, `traza_R = 21`. Se confirma que la suma de autovalores es la traza.

**Resultado (primeras 10 componentes):**

| Componente | $\lambda$ | De cada 100 | Acumulado |
|---|---:|---:|---:|
| C1 | 10,519 | 50,1 | 50,1 |
| C2 | 1,112 | 5,3 | 55,4 |
| C3 | 1,002 | 4,8 | 60,2 |
| C4 | 0,993 | 4,7 | 64,9 |
| C5 | 0,942 | 4,5 | 69,4 |
| C6 | 0,937 | 4,5 | 73,8 |
| C7 | 0,867 | 4,1 | 78,0 |
| C8 | 0,606 | 2,9 | 80,9 |
| C9 | 0,596 | 2,8 | 83,7 |
| C10 | 0,533 | 2,5 | 86,2 |

| Criterio | Resultado |
|---|---:|
| Componentes con $\lambda > 1$ (Kaiser) | **3** |
| Componentes para pasar de 80 % | **8** |

**Gráfico** [IMG]: barras con el porcentaje de cada una de las primeras 12 componentes (C1 en azul, C2 en naranja, resto en gris), con la curva acumulada en naranja y una línea punteada en 80.

**Lectura:**

- **C1 guarda 50,1 de cada 100** partes de la información de las 21 variables; **C2, 5,3**; a partir de ahí cada componente agrega muy poco y casi lo mismo (≈4–5 % de C3 a C7). El codo es muy marcado después de C1.
- Solo **3 componentes** tienen $\lambda > 1$ (C3 por muy poco: 1,002), y para pasar de 80 de cada 100 hacen falta **8**.
- **Para la Gerencia:** un solo número resume **la mitad** de lo que dice la ficha — mucho para un número, pero la otra mitad no cabe en él.
- **Advertencia clave:** que la segunda componente guarde poco **no quiere decir que no importe**. Lo que importa es **qué mide**, y eso es la sección siguiente.

### 16.5 ¿Qué mide cada componente?

**Concepto: pesos (cargas) y signo arbitrario.** Los pesos $w_{jk}$ dicen qué mide cada componente: si muchas variables pesan parecido y en la misma dirección, la componente es un "promedio" de ellas; si una sola manda, la componente es esa variable. El **signo de una componente es arbitrario**: $\mathbf{w}_k$ y $-\mathbf{w}_k$ son igualmente autovectores, y `prcomp()` podría devolver todos los pesos con el signo contrario y seguiría siendo la misma componente. Por eso se **ancla** el signo para que la lectura sea fácil:

- **C1 positiva = cliente más grande** (se fuerza que la suma de pesos de C1 sea positiva).
- **C2 positiva = más riesgo**, es decir, **peor puntaje** (se fuerza que el peso de `Credit_Score` en C2 sea negativo).
- **C3 positiva = más edad** (se fuerza que el peso de `Age` en C3 sea positivo).

```r
signo1 <- sign(sum(pca$rotation[, 1]))
signo2 <- -sign(pca$rotation["Credit_Score", 2])
signo3 <- sign(pca$rotation["Age", 3])
pesos      <- sweep(pca$rotation[, 1:3], 2, c(signo1, signo2, signo3), "*")
scores_pca <- sweep(pca$x[, 1:3],        2, c(signo1, signo2, signo3), "*")
```

Los mismos signos se aplican a pesos y scores, de modo que la orientación es coherente en todo el informe (Módulos 17 y 18 usan `scores_pca`).

**Resultado — pesos de C1, C2 y C3 (ordenados por $|$peso en C1$|$):**

| Variable | C1 | C2 | C3 |
|---|---:|---:|---:|
| `Credit_Limit` | 0,30 | −0,01 | 0,00 |
| `Annual_Income` | 0,30 | 0,00 | 0,00 |
| `Statement_Balance` | 0,29 | 0,14 | 0,02 |
| `Payment_Amount` | 0,27 | −0,07 | −0,01 |
| `Grocery_Spending` | 0,27 | −0,01 | 0,00 |
| `Mobile_App_Login` | 0,25 | −0,02 | 0,00 |
| `Utility_Bill_Spending` | 0,25 | −0,01 | 0,00 |
| `Avg_Transaction_Value` | 0,24 | −0,01 | 0,00 |
| `Online_Shopping_Spending` | 0,24 | 0,00 | 0,00 |
| `Fuel_Spending` | 0,24 | −0,01 | −0,01 |
| `Dining_Spending` | 0,23 | −0,01 | 0,01 |
| `EMI_Count` | 0,22 | 0,04 | 0,02 |
| `Monthly_Transactions` | 0,22 | −0,01 | 0,00 |
| `Entertainment_Spending` | 0,22 | −0,01 | 0,02 |
| `International_Transactions` | 0,21 | −0,05 | −0,02 |
| `Travel_Spending` | 0,20 | −0,01 | 0,00 |
| `Reward_Points_Redeemed` | 0,08 | −0,02 | 0,02 |
| `Cash_Advance_Amount` | 0,02 | **0,49** | 0,12 |
| `Credit_Score` | 0,01 | **−0,78** | −0,12 |
| `Age` | 0,00 | −0,05 | **0,93** |
| `Card_Age_Months` | 0,00 | **−0,34** | 0,32 |

**Gráfico** [IMG]: tres paneles de barras horizontales con los pesos de cada variable en "C1 · tamaño del cliente", "C2 · riesgo" y "C3 · edad" (azul positivo, naranja negativo).

#### Variables suplementarias

**Concepto.** Una variable **suplementaria** (o ilustrativa) **no participa en la construcción** de las componentes (no está en la matriz que se descompone), pero se **proyecta** sobre ellas calculando su correlación con los scores. Sirve para **interpretar** las componentes con información externa sin contaminar el cálculo. El Módulo 15 había excluido `Payment_Ratio`, `Credit_Utilization` y `Monthly_Spending` del conjunto activo (por ser derivadas de otras) y recomendó reincorporarlas aquí como suplementarias.

```r
sup <- credit[, c("Payment_Ratio", "Credit_Utilization", "Monthly_Spending")]
round(cor(sup, scores_pca), 2)
round(cor(credit$Credit_Score, scores_pca), 3)
```

**Resultado — correlación de las suplementarias con los scores:**

| Variable suplementaria | C1 | C2 | C3 |
|---|---:|---:|---:|
| `Payment_Ratio` | 0,04 | **−0,59** | −0,10 |
| `Credit_Utilization` | 0,06 | **0,47** | 0,08 |
| `Monthly_Spending` | **0,80** | −0,03 | −0,01 |

**Correlación de `Credit_Score` (variable activa) con los scores:** C1 = 0,017; C2 = **−0,822**; C3 = −0,123.

**Lectura (qué mide cada componente):**

- **C1 es el tamaño del cliente.** Todas las variables de dinero y de actividad pesan parecido (0,20–0,30) y en la misma dirección: ingreso, cupo, saldo, pagos, las siete categorías de gasto, transacciones y uso de la app. `Credit_Score`, la edad y la antigüedad de la tarjeta pesan casi cero. C1 sube cuando sube todo lo que se mide en rupias o en frecuencia. Su correlación con el **gasto mensual total** (`Monthly_Spending`), que no entró a construirla, es **0,80**: confirmación externa del nombre.
- **C2 es el riesgo.** La manda `Credit_Score` (peso **−0,78**: más C2 = peor puntaje), acompañada por `Cash_Advance_Amount` en la misma dirección de riesgo (peso 0,49; los avances en efectivo son señal de liquidez apretada) y por la antigüedad de la tarjeta en contra (peso −0,34; las tarjetas viejas son de clientes más estables). Las dos suplementarias de pago, que no participaron en construirla, lo confirman: **`Payment_Ratio` se correlaciona −0,59 con C2** (quien paga una proporción menor de su saldo está más arriba en riesgo) y **`Credit_Utilization` 0,47** (quien usa más su cupo, también).
- **C3 es la edad**, casi sola (peso **0,93**): una dimensión demográfica que no se parece a ninguna otra variable (recordar: `Age` tenía como mayor $|r|$ apenas 0,01). La antigüedad de la tarjeta la acompaña con 0,32.

**Conclusión de la sección:** lo que el primer número deja por fuera **no es ruido, tiene nombre**: es el **riesgo**, justamente lo que la Gerencia necesita ver.

### 16.6 El costo de decidir con un solo número

**Concepto.** Pasar de "partes de información" (porcentaje de varianza) a **clientes**: un resumen con mucho porcentaje de varianza puede ser inútil para una decisión concreta si la variable relevante para la decisión vive en una componente "pequeña". Se mide el costo como **tasa de captura**: de los clientes que de verdad interesan, ¿cuántos quedan dentro de la selección hecha con cada número?

**Planteamiento:** la Gerencia mete al programa de seguimiento al **20 % de la cartera** (el 20 % más alto del número que use), y el grupo que de verdad le interesa es el **20 % con peor puntaje** (`Credit_Score` ≤ percentil 20).

```r
en_riesgo <- credit$Credit_Score <= quantile(credit$Credit_Score, 0.20)
seleccion <- function(v) v >= quantile(v, 0.80)       # el 20 % más alto del número usado
```

**Resultado:**

| Ordenando por | Clientes en riesgo | Los encuentra | Se le escapan | De cada 100 se escapan |
|---|---:|---:|---:|---:|
| C1 (el mejor resumen de un número) | 10.046 | 1.832 | 8.214 | 81,8 |
| C2 (riesgo) | 10.046 | 6.580 | 3.466 | 34,5 |

(Hay 10.046 y no 10.000 clientes "en riesgo" porque hay empates en el percentil 20 del puntaje.)

**Gráfico** [IMG]: barras horizontales apiladas "los encuentra" (azul) / "se le escapan" (naranja) para C1 y C2.

**Lectura:**

- Ordenar por **C1** —el mejor resumen posible de un solo número— encuentra **1.832 de 10.046: el 18 %**, **lo mismo que se obtendría escogiendo clientes al azar** (al azar se esperaría el 20 %). C1 no sabe nada del riesgo: su correlación con el puntaje es **0,017**.
- Ordenar por **C2** encuentra al **66 %** (6.580; se escapan 34,5 de cada 100).

**Decisión para la Gerencia:** **un número no le basta**. El resumen mínimo de la ficha son **dos números**:

- **C1** para saber **cuánto pesa el cliente en la cartera** (exposición).
- **C2** para saber **qué tan riesgoso es**.

Con uno solo, ordenaría la cartera por tamaño y dejaría el riesgo por fuera.

### 16.7 Qué no es una componente

- **No es una causa.** Que C1 sea "el tamaño" no demuestra que exista una variable oculta que produzca el ingreso, el cupo y el gasto; dice solamente que **se mueven juntos**. (El análisis factorial sí pregunta por esas variables latentes; el PCA no. Se hace en el Módulo 18.)
- **No es un nombre que pone la técnica.** "Tamaño", "riesgo" y "edad" son nombres que se pusieron **mirando los pesos y las suplementarias**, y se discuten con el cliente.
- **No reemplaza a los datos.** Es un resumen para ordenar y para ver qué se pierde; las variables originales siguen disponibles en la tabla `silver` (`data/silver/`, Módulo 15).

### 16.8 Conclusión del Módulo 16

1. **Se puede resumir porque las variables se repiten:** 16 de 21 comparten información fuerte ($|r| > 0{,}6$) con alguna otra; `Credit_Score`, la edad y la antigüedad van solas.
2. **Estandarizar no es un detalle:** sin hacerlo, la primera componente (95,5 %) es solo `Annual_Income` con otro nombre.
3. **La primera componente guarda 50,1 de cada 100** partes de la información; **3** componentes tienen $\lambda > 1$ y hacen falta **8** para pasar de 80.
4. **C1 = tamaño, C2 = riesgo, C3 = edad.** El mejor resumen de un número no ve el riesgo: encuentra a los clientes de peor puntaje como lo haría el azar (18 % vs. 66 % de C2). **La Gerencia necesita al menos dos números.**

---

## Módulo 17: Componentes Principales II — el mapa de la cartera

> **Fuente:** `Entrega/analisis_synthetic_credit_card.Rmd`, líneas 6176–6464 (capítulo 18 del HTML). Todas las cifras provienen de la salida renderizada.

**Planteamiento.** La Gerencia de Riesgo recibió la respuesta del Módulo 16 (un número no basta; hacen falta dos: tamaño y riesgo) y vuelve con la pregunta de la sesión de PCA II:

> *«Entendido: dos números. Si pongo a cada cliente en un mapa con esos dos ejes, ¿qué tipos de cliente aparecen? ¿Los segmentos que ya manejo —tipo de tarjeta, ocupación— ocupan zonas distintas? ¿Y cuántos clientes le tocan a cada nivel de seguimiento?»*

### 17.1 El mapa y sus dos direcciones

**Concepto: plano factorial (mapa de individuos).** Cada cliente es un punto con coordenadas $(C1_i, C2_i)$ = sus scores en las dos primeras componentes. El mapa es la **proyección** de la nube de 21 dimensiones sobre el plano que mejor la representa (el de máxima varianza). La calidad global del mapa es la proporción acumulada $(\lambda_1 + \lambda_2)/p$.

Con los signos fijados en el Módulo 16: **ir a la derecha = cliente más grande**; **ir hacia arriba = cliente más riesgoso**.

**Cómo se aplicó:**

```r
guarda_mapa <- sum(lambda[1:2]) / sum(lambda) * 100
set.seed(17)
idx_mapa <- sample(nrow(scores_pca), 6000)   # muestra de 6.000 puntos solo para dibujar
plot(scores_pca[idx_mapa, "C1"], scores_pca[idx_mapa, "C2"], ..., asp = 1)
```

Decisión técnica: se dibuja una **muestra aleatoria de 6.000 clientes** (semilla 17) con transparencia, porque 50.000 puntos saturan el gráfico; `asp = 1` mantiene la misma escala en los dos ejes para no deformar distancias. Todos los cálculos numéricos usan los 50.000 clientes.

**Resultado:** el mapa guarda **55,4 de cada 100** partes de la información. [IMG: nube de puntos "El mapa de la cartera (guarda 55.4 de cada 100)".]

**Lectura:**

- 55,4 es poco más que la primera componente sola (50,1), porque la segunda guarda poco (5,3); **pero esa poca información es justamente la del riesgo**.
- La nube **no es una mancha redonda**: se estira a lo largo de C1 (tamaño) con **varios lóbulos**, y en C2 se reparte de forma **continua, sin huecos**.

### 17.2 El biplot: clientes y variables en el mismo dibujo

**Concepto.** El **biplot** superpone en el mismo plano los **individuos** (puntos = scores) y las **variables** (flechas). La coordenada de la flecha de la variable $j$ es su peso multiplicado por la desviación de cada componente:

$$\big(w_{j1}\sqrt{\lambda_1},\; w_{j2}\sqrt{\lambda_2}\big).$$

Como el PCA se hizo sobre datos estandarizados, esas coordenadas son **exactamente la correlación de la variable con cada eje**: $\operatorname{cor}(Z_j, C_k) = w_{jk}\sqrt{\lambda_k}$. De ahí las reglas de lectura:

- La flecha **apunta hacia donde crece** la variable.
- Es **más larga cuanto mejor la representa el mapa**: su largo es $\sqrt{r_{j1}^2 + r_{j2}^2}$, la raíz de la proporción de la varianza de la variable que el plano recoge (máximo 1, el círculo de correlaciones).
- **El ángulo entre dos flechas dice cuánto van juntas**: pequeño = juntas (correlación positiva alta); recto = nada que ver (≈ 0); abierto (cercano a 180°) = en contra (correlación negativa). Esto vale en la medida en que las dos flechas estén bien representadas (largas).

**Cómo se aplicó y verificación:**

```r
flechas <- sweep(pesos[, 1:2], 2, sqrt(lambda[1:2]), "*")
all.equal(unname(flechas), unname(cor(Z_pca, scores_pca[, 1:2])))   # TRUE: son correlaciones
largo <- sqrt(rowSums(flechas^2))
```

La salida de `all.equal` es **`TRUE`**: queda verificado numéricamente que las flechas son correlaciones.

**Resultado — coordenadas de las flechas (= correlación con C1 y C2) y largo:**

| Variable | C1 | C2 | Largo |
|---|---:|---:|---:|
| `Credit_Limit` | 0,97 | −0,01 | 0,97 |
| `Annual_Income` | 0,97 | 0,00 | 0,97 |
| `Statement_Balance` | 0,94 | 0,14 | 0,95 |
| `Payment_Amount` | 0,89 | −0,07 | 0,89 |
| `Grocery_Spending` | 0,86 | −0,01 | 0,86 |
| `Mobile_App_Login` | 0,83 | −0,02 | 0,83 |
| `Credit_Score` | 0,02 | **−0,82** | 0,82 |
| `Utility_Bill_Spending` | 0,80 | −0,01 | 0,80 |
| `Avg_Transaction_Value` | 0,79 | −0,01 | 0,79 |
| `Online_Shopping_Spending` | 0,79 | 0,00 | 0,79 |
| `Fuel_Spending` | 0,77 | −0,01 | 0,77 |
| `Dining_Spending` | 0,75 | −0,01 | 0,75 |
| `EMI_Count` | 0,73 | 0,05 | 0,73 |
| `Monthly_Transactions` | 0,72 | −0,01 | 0,72 |
| `Entertainment_Spending` | 0,71 | −0,01 | 0,71 |
| `International_Transactions` | 0,67 | −0,05 | 0,67 |
| `Travel_Spending` | 0,66 | −0,01 | 0,66 |
| `Cash_Advance_Amount` | 0,08 | **0,52** | 0,53 |
| `Card_Age_Months` | −0,01 | **−0,36** | 0,36 |
| `Reward_Points_Redeemed` | 0,26 | −0,02 | 0,26 |
| `Age` | −0,01 | −0,06 | 0,06 |

**Decisiones del gráfico:** solo se dibujan las variables con largo > 0,3 ("bien representadas"; quedan fuera `Reward_Points_Redeemed` y `Age`); las flechas se multiplican por un factor de escala `k_flecha = 4.5` para que se vean sobre la nube (cambia el tamaño, no la dirección ni las proporciones); se etiquetan en rojo oscuro las tres variables de riesgo (puntaje, avances efectivo, antigüedad) y con una sola etiqueta colectiva el abanico de "ingreso, cupo, saldo, pagos, gasto, transacciones, app". [IMG: "Biplot: clientes como puntos, variables como flechas".]

**Ángulos medidos entre flechas** (función `angulo(a, b) = acos(a·b / (|a||b|))` en grados):

| Par de flechas | Ángulo |
|---|---:|
| Ingreso vs cupo | 0,16° (≈ 0°) |
| Ingreso vs puntaje | 88,5° (≈ 89°) |
| Puntaje vs avances en efectivo | 170,2° (≈ 170°) |

**Lectura:**

- Las flechas de **dinero y actividad** apuntan casi todas al mismo lado, a lo largo de C1: ingreso y cupo forman un ángulo de **0°** (van juntos, como el $r = 0{,}97$ del Módulo 7).
- La flecha del **puntaje** apunta hacia **abajo** (recordar: arriba = más riesgo = peor puntaje), en ángulo **casi recto con el ingreso (89°)**: nada que ver, como el $r = 0{,}03$ del Módulo 7.
- La de los **avances en efectivo** apunta hacia **arriba**, casi **opuesta al puntaje (170°)**.
- El biplot dibuja en una figura lo que el informe fue encontrando por partes: **el dinero es una dirección y el riesgo es otra, perpendicular**.
- Las **flechas cortas** (edad 0,06; puntos redimidos 0,26) son variables que el mapa **no representa**: viven en C3 y más allá.

### 17.3 ¿Los grupos que la Gerencia conoce se separan en el mapa?

**Concepto: separar vs. desplazar.** La sesión distinguió dos situaciones:

- Grupos que **se separan**: una nube aparte, con un hueco entre grupos (como *setosa* en el dataset iris).
- Grupos que **solo se desplazan**: nubes que se montan una sobre otra aunque sus centros difieran (como los estratos en los datos Saber).

**Medida usada:** para cada eje, la posición del **centro de cada grupo en unidades de desviación estándar dentro de grupo** (desviación agrupada, *pooled*):

$$\text{posición}_g = \frac{\bar{y}_g}{s_{\text{dentro}}}, \qquad s_{\text{dentro}} = \sqrt{\frac{\sum_g \sum_{i \in g} (y_i - \bar{y}_g)^2}{n - G}}.$$

La diferencia entre las posiciones de dos grupos es un tamaño de efecto tipo *d* de Cohen: diferencias de 2 o más desviaciones implican poco solapamiento; diferencias de décimas implican nubes montadas.

```r
separacion <- function(score, grupo) {
  medias <- tapply(score, grupo, mean)
  sd_dentro <- sqrt(sum(tapply(score, grupo, function(v) sum((v - mean(v))^2))) /
                    (length(score) - nlevels(grupo)))
  round(sort(medias) / sd_dentro, 2)
}
```

#### Por tipo de tarjeta

| Eje | Basic | Silver | Gold | Platinum | Signature |
|---|---:|---:|---:|---:|---:|
| C1 · tamaño | −2,97 | −0,88 | 0,60 | 2,39 | 4,44 |
| C2 · riesgo | −0,03 | 0,02 | 0,05 | −0,08 | −0,10 |

**Gráfico** [IMG]: a la izquierda el mapa coloreado por tipo de tarjeta; a la derecha las densidades de C1 por tipo de tarjeta.

**Lectura:**

- En **tamaño (C1)**, los tipos de tarjeta se ordenan de `Basic` a `Signature` y cada centro queda a **entre 1,5 y 2 desviaciones del siguiente** (−2,97 → −0,88 → 0,60 → 2,39 → 4,44: saltos de 2,09; 1,48; 1,79; 2,05). Las densidades de tarjetas vecinas se tocan, pero las no vecinas casi no se solapan, y **`Signature` queda prácticamente aparte**: son **los lóbulos** que se veían en el mapa. Es lo más parecido a *setosa* que tiene esta cartera, y tiene sentido: **el tipo de tarjeta es una decisión del banco basada en el ingreso**.
- En **riesgo (C2)**, los cinco centros quedan a **menos de dos décimas de desviación** entre sí (de −0,10 a 0,05): las nubes se montan completas.
- Es la misma conclusión del $V$ de Cramér del Módulo 12, vista ahora en el mapa: **el tipo de tarjeta dice cuánto pesa un cliente, no qué tan riesgoso es**.

#### Por ocupación

| Eje | Student | Retired | Private Employee | Government Employee | Self-Employed | Business Owner |
|---|---:|---:|---:|---:|---:|---:|
| C1 · tamaño | −2,66 | −0,94 | −0,23 | 0,17 | 0,51 | 2,32 |
| C2 · riesgo | −0,06 | −0,06 | −0,02 | 0,01 | 0,03 | 0,03 |

**Lectura:** con la ocupación pasa lo mismo, más suave. En tamaño, `Student` y `Retired` quedan a la izquierda y `Business Owner` a la derecha (la ocupación explica el ingreso, Módulo 7); en riesgo, las seis ocupaciones tienen el centro prácticamente en el mismo lugar (de −0,06 a 0,03). **Diferencia no es separación**, y aquí, en riesgo, **ni siquiera hay diferencia**.

**Decisión:** la Gerencia **no puede escoger a quién seguir por tipo de tarjeta ni por ocupación**; lo que sirve es **el lugar de cada cliente en el eje de riesgo**.

### 17.4 La decisión: el mapa de seguimiento

**Concepto.** Como el riesgo **no viene en grupos hechos** (C2 es un continuo), la Gerencia los define con **cortes** sobre el mapa. Se propone un esquema sencillo de dos cortes y tres zonas:

- **Corte de riesgo:** más de **una desviación típica por encima en C2** ($C2 > \operatorname{sd}(C2)$; como C2 tiene media 0, equivale a un $z > 1$) = "riesgo alto".
- **Corte de tamaño:** la **mediana de C1** separa clientes grandes (más exposición) de pequeños.

| Zona | Regla |
|---|---|
| **A** · riesgo alto, cliente grande | $C2 > \operatorname{sd}(C2)$ y $C1 > \operatorname{mediana}(C1)$ |
| **B** · riesgo alto, cliente pequeño | $C2 > \operatorname{sd}(C2)$ y $C1 \le \operatorname{mediana}(C1)$ |
| **C** · sin seguimiento | $C2 \le \operatorname{sd}(C2)$ |

**Resultado:**

| Zona | Clientes | De cada 100 | Puntaje medio | Cupo mediano (INR) |
|---|---:|---:|---:|---:|
| A · riesgo alto, cliente grande | 4.226 | 8,5 | 541 | 718.000 |
| B · riesgo alto, cliente pequeño | 3.969 | 7,9 | 532 | 167.000 |
| C · sin seguimiento | 41.805 | 83,6 | 647 | 394.000 |

**¿Cuántos del 20 % con peor puntaje caen en las zonas A o B?**

| Indicador | Valor |
|---|---:|
| Clientes del 20 % de peor puntaje dentro de A o B | **5.811** |
| De cada 100 de ese grupo | **57,8** |

(Por cuenta propia, a partir de estas cifras: de los 8.195 clientes en A+B, 5.811 pertenecen al 20 % de peor puntaje, es decir ≈ 70,9 % de la lista de seguimiento son efectivamente clientes de peor puntaje; este porcentaje no aparece en el informe, se deriva de las cifras renderizadas.)

**Gráfico** [IMG]: "El mapa de seguimiento: dos cortes, tres zonas", con A en rojo oscuro, B en naranja y C en gris, y las líneas punteadas de los cortes.

**Lectura:**

- El corte deja **8.195 clientes en seguimiento (16,4 % de la cartera)**, con un puntaje medio (541 y 532) **muy por debajo** del resto (647).
- Encuentra al **57,8 % del 20 % con peor puntaje** — con **menos cupos** (16,4 % de la cartera) que el 20 % usado en el Módulo 16.
- La zona **A es la prioridad**: clientes con riesgo alto **y** cupo grande (cupo mediano 718.000 INR, frente a 167.000 en B), **donde una mora pesa más**. La zona **B** puede atenderse con un seguimiento más barato (mensajes, no llamadas).
- **El corte de "una desviación" es una decisión de la Gerencia, no de la técnica**: si tiene menos gestores, lo sube (y la lista se achica).

### 17.5 Con y sin *one-hot*: ¿cambia el mapa si entra el tipo de tarjeta?

**Concepto.** El Módulo 15 dejó el tipo de tarjeta codificado en **one-hot** (5 *dummies*: `Card_Type_Basic`, `Silver`, `Gold`, `Platinum`, `Signature`). Dos problemas de meter dummies en un PCA:

1. **Trampa de las dummies:** las 5 suman siempre 1, así que hay una combinación lineal exacta → un autovalor igual a 0 (la matriz es singular). En PCA esto no rompe el cálculo; solo sobra esa componente.
2. **Peso desproporcionado:** 5 dummies estandarizadas aportan 5 unidades de varianza total, es decir, **pesan como cinco variables** para una sola variable categórica. La **regla del Módulo 15** es ponderarlas por $1/\sqrt{k}$ (aquí $1/\sqrt{5}$) para que juntas pesen como una variable.

**Cómo se aplicó:** se compararon tres versiones.

```r
D_card_z     <- scale(D_card)
pca_oh_pleno <- prcomp(cbind(Z_pca, D_card_z))                       # 5 dummies tal cual
pca_oh_pond  <- prcomp(cbind(Z_pca, D_card_z / sqrt(ncol(D_card)))) # ponderadas por 1/sqrt(5)
```

Para cada versión se registró el % de C1 y C2, la correlación absoluta de sus C1 y C2 con las del PCA original y el último autovalor.

**Resultado:**

| Versión | Columnas | % C1 | % C2 | $\lvert r\rvert$ C1 con original | $\lvert r\rvert$ C2 con original | Último $\lambda$ |
|---|---:|---:|---:|---:|---:|---:|
| Sin one-hot | 21 | 50,1 | 5,3 | 1 | 1 | 0,0043 |
| Con one-hot (5 dummies) | 26 | 44,3 | 6,2 | 0,999 | **0,1289** | 2,3 × 10⁻³⁰ |
| Con one-hot ponderado | 26 | 48,7 | 5,1 | 1 | 0,9994 | 2,1 × 10⁻³⁰ |

**¿En qué componente se mete el tipo de tarjeta?** (correlación de cada dummy con las tres primeras componentes del PCA ponderado; los signos son los crudos de `prcomp`, sin anclar):

| Dummy | PC1 | PC2 | PC3 |
|---|---:|---:|---:|
| `Card_Type_Basic` | 0,67 | 0,03 | 0,02 |
| `Card_Type_Silver` | 0,22 | −0,02 | −0,01 |
| `Card_Type_Gold` | −0,19 | −0,06 | −0,03 |
| `Card_Type_Platinum` | −0,48 | 0,05 | 0,01 |
| `Card_Type_Signature` | −0,45 | 0,04 | 0,03 |

**Lectura:**

- Las dos versiones con one-hot tienen un **último valor propio prácticamente cero** (≈ 10⁻³⁰): las cinco dummies suman 1 y el PCA lo detecta como una dirección sin varianza (la trampa de las dummies del Módulo 15). Con PCA no rompe nada, solo sobra esa componente. (Sin one-hot el último autovalor es 0,0043: pequeño pero no nulo.)
- **Con las dummies ponderadas, el mapa no cambia:** sus dos primeras componentes se correlacionan **1** y **0,999** con las originales.
- **Sin ponderar, la segunda componente deja de ser el riesgo:** su correlación con la C2 original **cae a 0,13**. Las cinco dummies, que pesan como cinco variables, se adueñan de ella. Además le restan protagonismo al resto de la ficha: la C1 guarda **44,3 en vez de 50,1**.
- El tipo de tarjeta se mete **entero en C1** (`Basic` en un extremo, `Platinum` y `Signature` en el otro; en la tabla PC1 tiene el signo invertido respecto al anclaje de "tamaño") y **nada en C2**: lo que dice la tarjeta **ya estaba contenido en el ingreso y el cupo**.

**Decisión:** el mapa de la Gerencia se queda **sin** el tipo de tarjeta como variable activa; la tarjeta se usa como **variable para colorear y leer el mapa** (ilustrativa), que es donde aporta.

### 17.6 Qué no dice el mapa

- **No dice que haya tipos de cliente en riesgo.** En C2 la nube es un continuo; las zonas de seguimiento las definimos nosotros con cortes.
- **No muestra todo.** Guarda 55,4 de cada 100: la edad (C3) y varias dimensiones pequeñas no están dibujadas.
- **No explica por qué.** Que los avances en efectivo apunten hacia el riesgo no dice que los causen; puede ser al revés (quien está en apuros pide avances).

### 17.7 Conclusión del Módulo 17

1. El mapa de dos componentes (55,4 % de la información) ordena a cada cliente por **tamaño** (a la derecha) y **riesgo** (hacia arriba); las flechas del dinero van a lo largo de C1 y las del riesgo (puntaje, avances, antigüedad) a lo largo de C2, **casi perpendiculares** (ingreso–puntaje: 89°).
2. El tipo de tarjeta **separa** a los clientes en tamaño —lo más parecido a *setosa* de esta cartera— y **no los separa en absoluto** en riesgo; la ocupación, igual. Ninguno sirve para escoger a quién seguir.
3. Dos cortes en el mapa producen una **lista de seguimiento con prioridad** (8.195 clientes, 16,4 %; zona A: riesgo alto y cliente grande, 4.226 clientes) que captura el 57,8 % del 20 % de peor puntaje, y que la Gerencia puede ajustar moviendo el corte según sus cupos.
4. Meter el tipo de tarjeta con one-hot **ponderado** no cambia el mapa: su información ya estaba en C1. **Sin ponderar**, las cinco dummies desplazan al riesgo de la segunda componente — la razón de la regla $1/\sqrt{k}$ del Módulo 15.

---

## Módulo 18: Análisis Factorial — ¿Hay algo detrás de las variables?

> **Fuente:** `Entrega/analisis_synthetic_credit_card.Rmd`, líneas 6465–6901 (capítulo 19 del HTML). **El Módulo 18 sí aparece renderizado en el HTML del 2 de noviembre**, de modo que todas las cifras de este módulo provienen de la salida real. El paquete usado es `psych` (llamado siempre como `psych::` sin `library()`, para no tapar funciones usadas antes en el informe; se instala desde CRAN si no está).

**Planteamiento.** El Módulo 16 cerró con una advertencia: que C1 sea "el tamaño" **no demuestra** que exista una variable oculta que produzca el ingreso, el cupo y el gasto. La Gerencia de Riesgo toma esa advertencia como pregunta:

> *«Si el ingreso, el cupo y el gasto se mueven juntos, ¿es porque hay un rasgo del cliente que no medimos y que los mueve a todos? ¿Y el riesgo también es un rasgo así, algo que se manifiesta en varias columnas de la ficha a la vez?»*

Esa es la pregunta del **análisis factorial (AF)**. El PCA busca el **mejor resumen** de las variables; el análisis factorial propone un **modelo de dónde salen**.

### 18.1 El modelo: lo común y lo propio

**Concepto.** Cada variable estandarizada se escribe como una combinación de unos pocos **factores comunes** $f_1, \dots, f_m$ (no observados, latentes) más una parte que es **solo suya**:

$$x_j \;=\; \lambda_{j1} f_1 + \dots + \lambda_{jm} f_m + \varepsilon_j$$

Los $\lambda_{jk}$ son las **cargas factoriales**. Si los factores son independientes entre sí (y de varianza 1) e independientes de los $\varepsilon_j$, la matriz de correlaciones queda partida en dos:

$$\mathbf{R} \;=\; \boldsymbol\Lambda \boldsymbol\Lambda^{\top} + \boldsymbol\Psi, \qquad \boldsymbol\Psi \text{ diagonal}.$$

- **En la diagonal:** la varianza de cada variable (que vale 1) se reparte en
  - $h_j^2 = \sum_k \lambda_{jk}^2$, la **comunalidad**: lo que la variable comparte con las demás a través de los factores;
  - $\psi_j = 1 - h_j^2$, la **unicidad**: lo que es solo suyo (su variación específica más el error de medida).
- **Fuera de la diagonal** dice algo más fuerte: **toda la correlación entre dos variables tiene que pasar por los factores**: $r_{jl} = \sum_k \lambda_{jk}\lambda_{lk}$ para $j \ne l$.

**Diferencia con el PCA:** el PCA reparte **toda** la varianza, incluida la propia de cada variable (descompone $\mathbf{R}$ con unos en la diagonal); el AF solo intenta explicar la parte **común** (descompone $\mathbf{R} - \boldsymbol\Psi$). Una variable que no se parece a ninguna otra **puede mandar en una componente del PCA** (como la edad en C3); en un AF **no define ningún factor**, porque no tiene nada en común que explicar.

### 18.2 ¿Hay algo común que explicar? KMO y Bartlett

**Concepto.** Antes de extraer factores se verifica que valga la pena. Dos pruebas clásicas:

- **Esfericidad de Bartlett:** contrasta $H_0: \mathbf{R} = \mathbf{I}$ (las variables no se correlacionan en absoluto). Estadístico: $\chi^2 = -\left(n - 1 - \frac{2p+5}{6}\right)\ln|\mathbf{R}|$, con $p(p-1)/2$ grados de libertad. Si no se rechaza, no hay nada que factorizar.
- **KMO (Kaiser–Meyer–Olkin):** compara las correlaciones simples $r_{jl}$ con las **parciales** $a_{jl}$ (la correlación de dos variables descontando todas las demás):

$$\text{KMO} = \frac{\sum_{j\ne l} r_{jl}^2}{\sum_{j\ne l} r_{jl}^2 + \sum_{j\ne l} a_{jl}^2}.$$

  Si dos variables se correlacionan porque comparten un factor con el resto, al descontar el resto su correlación parcial debe ser pequeña → KMO cercano a 1. Va de 0 a 1; **por debajo de 0,5 el AF no es apropiado; por encima de 0,8 es bueno**. El **MSA** (*measure of sampling adequacy*) es el mismo índice calculado **para cada variable** (sumando solo sobre su fila).
- Complementariamente se calcula la **SMC** (*squared multiple correlation*): el $R^2$ de cada variable regresada sobre todas las demás, que es la **comunalidad inicial** clásica.

**Cómo se aplicó** (sobre la misma matriz del PCA, $\mathbf{R}$ de `Z_pca`, 21 variables, $n = 50.000$):

```r
R_fa <- cor(Z_pca); n_fa <- nrow(Z_pca)
bartlett <- psych::cortest.bartlett(R_fa, n = n_fa)
kmo <- psych::KMO(R_fa)
smc <- psych::smc(R_fa)
```

**Resultado — Bartlett y KMO global:**

| Prueba | Resultado |
|---|---:|
| Bartlett $\chi^2$ | 1.061.045 |
| Grados de libertad | 210 |
| p-valor | 0 |
| **KMO global** | **0,855** |

**Resultado — MSA por variable y $R^2$ con las demás (SMC), ordenado por MSA:**

| Variable | MSA | $R^2$ con las demás |
|---|---:|---:|
| `Credit_Score` | **0,025** | **0,901** |
| `Card_Age_Months` | **0,032** | 0,027 |
| `Cash_Advance_Amount` | **0,287** | 0,052 |
| `Age` | 0,669 | **0,000** |
| `Monthly_Transactions` | 0,735 | 0,878 |
| `Avg_Transaction_Value` | 0,762 | 0,914 |
| `Payment_Amount` | 0,776 | 0,980 |
| `Statement_Balance` | 0,785 | 0,993 |
| `Credit_Limit` | 0,866 | 0,983 |
| `Grocery_Spending` | 0,898 | 0,792 |
| `Utility_Bill_Spending` | 0,913 | 0,678 |
| `Online_Shopping_Spending` | 0,914 | 0,663 |
| `Fuel_Spending` | 0,916 | 0,630 |
| `Dining_Spending` | 0,923 | 0,595 |
| `Entertainment_Spending` | 0,924 | 0,525 |
| `Travel_Spending` | 0,933 | 0,447 |
| `Annual_Income` | 0,937 | 0,974 |
| `International_Transactions` | 0,943 | 0,499 |
| `EMI_Count` | 0,950 | 0,539 |
| `Mobile_App_Login` | 0,973 | 0,677 |
| `Reward_Points_Redeemed` | 0,996 | **0,056** |

**Gráfico** [IMG]: barras horizontales del MSA por variable (naranja si < 0,5), con líneas en 0,5 y 0,8.

**Lectura:**

- **Bartlett rechaza** con un $\chi^2$ de 1.061.045, pero con 50.000 clientes rechazaría casi cualquier correlación por pequeña que fuera (la lección del Módulo 14 sobre $n$ grande): **solo dice que $\mathbf{R}$ no es la identidad, no que haya factores**.
- El **KMO global es 0,85, bueno**, pero el detalle por variable muestra que **tres variables están muy por debajo de 0,5**: `Credit_Score` (0,03), `Card_Age_Months` (0,03) y `Cash_Advance_Amount` (0,29) — **justamente las tres que formaban la C2 de "riesgo" del PCA**.
- `Age` y `Reward_Points_Redeemed` tienen un MSA aceptable (0,67 y 0,996) pero un $R^2$ con las demás de **0** y **0,06**: **no comparten nada con nadie** (un MSA alto en una variable aislada no significa que tenga algo común; significa que sus parciales también son ≈ 0).

#### El caso de `Credit_Score`: MSA ≈ 0 con $R^2$ = 0,90

Parece una contradicción: su MSA es casi cero, pero su $R^2$ con las demás es **0,90**, el de una variable muy bien explicada. Se examinaron las correlaciones parciales:

```r
P_fa <- -cov2cor(solve(R_fa)); diag(P_fa) <- 1      # correlaciones parciales
```

(La matriz de correlaciones parciales se obtiene de la inversa de $\mathbf{R}$: $a_{jl} = -\dfrac{(\mathbf{R}^{-1})_{jl}}{\sqrt{(\mathbf{R}^{-1})_{jj}(\mathbf{R}^{-1})_{ll}}}$.)

**Resultado — las 4 variables con mayor correlación parcial con `Credit_Score`:**

| | `Statement_Balance` | `Payment_Amount` | `Credit_Limit` | `Cash_Advance_Amount` |
|---|---:|---:|---:|---:|
| Correlación simple | −0,169 | 0,108 | 0,026 | −0,070 |
| Correlación parcial | **−0,947** | **0,921** | 0,524 | −0,215 |

**Lectura:** con el saldo y con el pago, `Credit_Score` casi no se correlaciona por separado (−0,17 y 0,11), pero **descontando lo demás** las correlaciones son **−0,95 y 0,92**. **El puntaje no sigue al saldo ni al pago, sigue a la diferencia entre los dos**: con `log(x+1)`,

$$\log(\text{pago}) - \log(\text{saldo}) = \log\!\left(\frac{\text{pago}}{\text{saldo}}\right),$$

que es el logaritmo de la **proporción pagada**, la variable que el Módulo 7 encontró detrás del puntaje. Es un **contraste** entre dos variables que, por lo demás, van juntas; **un factor común no puede producir eso**, porque un factor empuja a las variables en la misma dirección. El MSA bajo lo detecta: correlaciones parciales grandes con correlaciones simples pequeñas.

**Decisión:** las cinco variables `Credit_Score`, `Card_Age_Months`, `Cash_Advance_Amount`, `Age` y `Reward_Points_Redeemed` **quedan fuera del modelo factorial**. No se borran: se usan después como **variables suplementarias** para leerlo (igual que `Payment_Ratio` en el Módulo 16).

**Verificación con las 16 restantes:**

```r
fuera_fa <- c("Credit_Score", "Card_Age_Months", "Cash_Advance_Amount", "Age", "Reward_Points_Redeemed")
Z_fa <- Z_pca[, setdiff(colnames(Z_pca), fuera_fa)]
R_fa2 <- cor(Z_fa); kmo2 <- psych::KMO(R_fa2)
```

| Indicador | Valor |
|---|---:|
| Variables | 16 |
| KMO global | **0,905** |
| MSA mínimo | 0,731 |

Con las 16 restantes el KMO **sube a 0,91** (excelente) y ninguna variable queda por debajo de **0,73**.

### 18.3 ¿Cuántos factores?

**Concepto — tres criterios (de la sesión):**

1. **Kaiser** ($\lambda > 1$ en $\mathbf{R}$): heredado del PCA, rápido y conocido por **quedarse corto o pasarse**.
2. **Análisis paralelo (Horn):** compara los valores propios de los datos con los que saldrían de datos **sin ninguna estructura** (aleatorios, del mismo tamaño $n \times p$). Se retiene un factor **mientras el de los datos supere al del azar**.
3. **Ajuste del modelo:** con **máxima verosimilitud** se puede medir qué tan bien reproduce $\mathbf{R}$ cada número de factores. Referencias usuales: **TLI** (índice de Tucker–Lewis) cerca de 1 (≥ 0,90–0,95) y **RMSEA** (error de aproximación cuadrático medio) bajo 0,08. También se reporta el **residuo medio** (RMSR, `rms`).

**Cómo se aplicó:**

```r
lambda_fa <- eigen(R_fa2)$values
c(kaiser = sum(lambda_fa > 1))
set.seed(18)
idx_fa <- sample(n_fa, 5000)            # el análisis paralelo simula: con 5.000 basta
paralelo <- psych::fa.parallel(Z_fa[idx_fa, ], fa = "fa", plot = FALSE)
ajuste <- sapply(1:4, function(k) psych::fa(R_fa2, nfactors = k, n.obs = n_fa, fm = "ml", rotate = "varimax") ...)
```

Decisión técnica: el análisis paralelo se corre sobre una **submuestra de 5.000 clientes** (semilla 18) porque simula muchas matrices aleatorias y con 5.000 basta para estabilizarlo.

**Resultados:**

| Criterio | Factores sugeridos |
|---|---:|
| Kaiser | **1** (primer autovalor = 10,5; el segundo ya está bajo 1) |
| Análisis paralelo | **3** (salida: "Parallel analysis suggests that the number of factors = 3 and the number of components = NA") |

**Ajuste por máxima verosimilitud (rotación varimax):**

| Factores | TLI | RMSEA | Residuo medio |
|---:|---:|---:|---:|
| 1 | 0,843 | 0,157 | 0,030 |
| 2 | 0,882 | 0,136 | 0,017 |
| 3 | 0,908 | 0,120 | 0,016 |
| 4 | 0,948 | 0,090 | 0,014 |

**Gráfico** [IMG]: "Análisis paralelo: datos frente a azar", valores propios de los primeros 6 factores (escala log) de los datos (azul) frente a los de datos sin estructura (naranja punteado).

**Examen del tercer factor** (solución de 3 factores, ML + varimax):

| Factor dominante (donde cada variable tiene su carga más alta) | Nº de variables |
|---|---:|
| ML1 | 3 |
| ML2 | 13 |
| (el tercer factor) | **0** |

Cargas más altas en el factor más débil (el de menor suma de cargas al cuadrado):

| Variable | Carga |
|---|---:|
| `Statement_Balance` | 0,61 |
| `Payment_Amount` | 0,59 |
| `Credit_Limit` | 0,35 |
| `Annual_Income` | 0,31 |

**Lectura:**

- Los criterios **no coinciden, y es normal**. Kaiser da **1**: el primer valor propio es enorme (**10,5**) y el segundo ya está bajo 1. El análisis paralelo da **3**.
- El ajuste mejora con cada factor que se agrega (TLI de 0,843 a 0,948; RMSEA de 0,157 a 0,090), pero con 50.000 clientes **ningún modelo pequeño pasa las pruebas formales** (otra vez $n$ grande), así que el RMSEA se lee como **tendencia**. El salto en residuo medio es grande de 1 a 2 factores (0,030 → 0,017) y casi nulo de 2 a 3 (0,017 → 0,016).
- El **tercer factor, mirado de cerca, es débil**: **ninguna variable tiene en él su carga más alta**, y las que más cargan en él son **solo dos**, el saldo y el pago (0,61 y 0,59), cuando una regla básica pide **al menos tres variables por factor** para que no sea un par de variables parecidas con otro nombre.

**Decisión: dos factores.** El tercero queda anotado: saldo y pago comparten algo más allá de los otros dos factores, lo que tiene sentido **porque el pago se calcula sobre el saldo**.

### 18.4 Extracción y rotación: qué es cada factor

**Concepto.**

- **Extracción por máxima verosimilitud (ML):** se estiman $\boldsymbol\Lambda$ y $\boldsymbol\Psi$ suponiendo normalidad multivariante, maximizando la verosimilitud de $\mathbf{R}$ bajo el modelo $\boldsymbol\Lambda\boldsymbol\Lambda^{\top} + \boldsymbol\Psi$. Permite índices de ajuste (TLI, RMSEA).
- **Rotación varimax:** la solución factorial no es única: para cualquier matriz ortogonal $\mathbf{T}$, $\boldsymbol\Lambda\mathbf{T}$ reproduce igual $\mathbf{R}$, porque $(\boldsymbol\Lambda\mathbf{T})(\boldsymbol\Lambda\mathbf{T})^{\top} = \boldsymbol\Lambda\boldsymbol\Lambda^{\top}$. **La rotación no cambia el ajuste** (comunalidades y $\boldsymbol\Lambda\boldsymbol\Lambda^{\top}$ quedan iguales); **gira los ejes** para que cada variable cargue fuerte en un factor y poco en los demás, que es lo que permite ponerles nombre. Varimax elige el giro ortogonal que **maximiza la varianza de las cargas al cuadrado** dentro de cada factor.
- **Puntajes factoriales por regresión** (`scores = "regression"`, método de Thurstone): estiman el valor de cada factor para cada cliente, $\hat{\mathbf{f}}_i = \boldsymbol\Lambda^{\top}\mathbf{R}^{-1}\mathbf{z}_i$.

**Cómo se aplicó y anclaje de orden/signo** (análogo al del PCA):

```r
fa2 <- psych::fa(Z_fa, nfactors = 2, fm = "ml", rotate = "varimax", scores = "regression")
# F2 = el factor donde carga Monthly_Transactions; signos tales que la suma de cargas sea positiva
f_frec <- which.max(abs(cargas["Monthly_Transactions", ]))
orden_f <- c(setdiff(1:2, f_frec), f_frec)
signos_f <- sign(colSums(cargas[, orden_f]))
```

Aquí `fa()` recibe los datos (`Z_fa`, 50.000 × 16) y no solo la matriz, para poder calcular puntajes por cliente.

**Resultado — cargas varimax, comunalidad y unicidad** (ordenado de "más F1" a "más F2"):

| Variable | F1 | F2 | Comunalidad $h^2$ | Unicidad $\psi$ |
|---|---:|---:|---:|---:|
| `Avg_Transaction_Value` | **0,91** | 0,04 | 0,83 | 0,17 |
| `Annual_Income` | **0,84** | 0,52 | 0,98 | 0,02 |
| `Credit_Limit` | **0,84** | 0,53 | 0,98 | 0,02 |
| `Statement_Balance` | **0,80** | 0,51 | 0,90 | 0,10 |
| `Payment_Amount` | **0,75** | 0,48 | 0,79 | 0,21 |
| `International_Transactions` | 0,56 | 0,33 | 0,42 | 0,58 |
| `Grocery_Spending` | 0,68 | 0,50 | 0,72 | 0,28 |
| `Utility_Bill_Spending` | 0,63 | 0,47 | 0,61 | 0,39 |
| `Online_Shopping_Spending` | 0,62 | 0,46 | 0,59 | 0,41 |
| `Fuel_Spending` | 0,60 | 0,44 | 0,56 | 0,44 |
| `Dining_Spending` | 0,58 | 0,44 | 0,53 | 0,47 |
| `Entertainment_Spending` | 0,54 | 0,41 | 0,46 | 0,54 |
| `Travel_Spending` | 0,50 | 0,38 | 0,40 | 0,60 |
| `EMI_Count` | 0,49 | 0,49 | 0,47 | 0,53 |
| `Mobile_App_Login` | 0,56 | 0,56 | 0,63 | 0,37 |
| `Monthly_Transactions` | 0,18 | **0,98** | **1,00** | **0,00** |

**Varianza común explicada por cada factor:**

| | F1 | F2 | Total |
|---|---:|---:|---:|
| Varianza común ($\sum_j \lambda_{jk}^2$) | 6,83 | 4,05 | 10,88 |
| De cada 100 (sobre 16 variables) | 42,66 | 25,29 | **≈ 68** |

**Gráfico** [IMG]: "Cargas factoriales (varimax): cada punto es una variable", plano F1–F2 con la diagonal punteada.

**Lectura — los dos factores tienen nombre claro:**

- **F1 · capacidad (cuánto por vez).** Lo definen el ingreso (0,84), el cupo (0,84), el **valor medio por transacción (0,91)**, el saldo (0,80) y el pago (0,75): **el tamaño de la billetera del cliente**.
- **F2 · frecuencia de uso (cuántas veces).** Lo define casi solo el **número de transacciones (0,98)**, con la app (0,56) y las compras a cuotas (0,49) en segundo plano.
- **Las siete categorías de gasto cargan en los dos**, por debajo de la diagonal pero cerca de ella (F1 entre 0,50 y 0,68; F2 entre 0,38 y 0,50). **No es un defecto del modelo:** un gasto es *cuántas veces compra el cliente* **por** *cuánto gasta cada vez*, y en logaritmos ese producto se vuelve una suma:

$$\log(\text{gasto}) \approx \log(\text{veces}) + \log(\text{valor por vez}).$$

  **El modelo factorial encontró por su cuenta la forma en que se arma el gasto.**
- Juntos, los dos factores explican **68 de cada 100** partes de la varianza de las 16 variables.
- Las **comunalidades más bajas** son las de viajes (0,40), transacciones internacionales (0,42), entretenimiento (0,46) y cuotas (0,47): tienen bastante variación propia que ningún factor común recoge.

**Señal de cuidado — caso casi Heywood:** `Monthly_Transactions` queda con **unicidad 0,005**, prácticamente cero (comunalidad ≈ 1). Un **caso Heywood** es cuando una comunalidad estimada llega a 1 (o la supera, dando unicidad negativa, imposible). Aquí el modelo pone a la variable entera en el factor, lo que pasa cuando **un factor depende casi de una sola variable**. No invalida el resultado, pero dice que **F2 es, en esencia, el número de transacciones** medido con algo de ruido de las demás.

### 18.5 ¿El modelo reproduce las correlaciones?

**Concepto.** Si el modelo es bueno, $\hat{\mathbf{R}} = \boldsymbol\Lambda \boldsymbol\Lambda^{\top} + \boldsymbol\Psi$ debe parecerse a $\mathbf{R}$. Los **residuos** son la diferencia $\mathbf{R} - \hat{\mathbf{R}}$; fuera de la diagonal deberían ser pequeños (regla usual: $|\text{residuo}| < 0{,}05$).

```r
R_modelo <- cargas %*% t(cargas) + diag(fa2$uniquenesses)
residuos <- R_fa2 - R_modelo
fuera_d  <- residuos[upper.tri(residuos)]
```

**Resultado:**

| Indicador | Valor |
|---|---:|
| Pares de variables (16·15/2) | 120 |
| Residuo máximo $\lvert\cdot\rvert$ | 0,118 |
| Pares con residuo > 0,05 | 10 |
| Par con el peor residuo | `Mobile_App_Login` – `EMI_Count` |
| $r$ observado en ese par | 0,663 |
| $r$ reproducido por el modelo | 0,545 |

**Lectura:** de 120 pares, solo **10** (8 %) tienen un residuo mayor a 0,05. El peor es **0,12**, en el par **`Mobile_App_Login`–`EMI_Count`** (observado 0,66, modelo 0,54): esas dos variables se parecen entre sí un poco más de lo que explican los factores. **Dos factores reproducen bien la estructura de la ficha.**

### 18.6 Varimax o promax: ¿los factores se correlacionan?

**Concepto.**

- **Varimax** es una rotación **ortogonal**: obliga a que los factores sean **independientes** (correlación 0).
- **Promax** es una rotación **oblicua**: parte de varimax, eleva las cargas a una potencia para acentuar el patrón y permite que los factores **se correlacionen**; estima la matriz de correlación entre factores $\boldsymbol\Phi$. En el modelo oblicuo $\mathbf{R} = \boldsymbol\Lambda\boldsymbol\Phi\boldsymbol\Lambda^{\top} + \boldsymbol\Psi$, y las cargas de patrón pueden superar 1 en valor absoluto (no son correlaciones).

En una cartera real la independencia es dudosa: es natural que los clientes con más capacidad también usen más la tarjeta.

```r
fa2_obl <- psych::fa(R_fa2, nfactors = 2, n.obs = n_fa, fm = "ml", rotate = "promax")
round(fa2_obl$Phi, 2); round(max(abs(fa2_obl$loadings)), 2)
```

**Resultado:**

| $\boldsymbol\Phi$ (promax) | ML2 | ML1 |
|---|---:|---:|
| ML2 | 1,00 | **0,75** |
| ML1 | **0,75** | 1,00 |

Carga máxima en valor absoluto en la solución promax: **1,24**.

**Lectura:** con promax los dos factores se correlacionan **0,75**: capacidad y frecuencia **no son independientes**; los clientes que gastan más por vez también compran más veces. Pero la solución oblicua tiene **cargas mayores que 1 (1,24)**, otra señal de que el modelo está **forzado por el número de transacciones** (el mismo problema del casi Heywood).

**Decisión:** para leer los factores **se queda varimax**, sabiendo que la independencia es una simplificación.

### 18.7 Los factores frente a las componentes, y la pregunta del riesgo

**Cómo se aplicó.** Con los puntajes factoriales de cada cliente (`scores_fa`, F1 y F2) se calcularon: (a) sus correlaciones con los scores del PCA (C1, C2, C3) y con tres variables de riesgo (`Credit_Score` y las suplementarias `Payment_Ratio`, `Credit_Utilization`); (b) una regresión lineal de C1 sobre F1 y F2; (c) el mismo ejercicio de costo del Módulo 16 (el 20 % más alto de cada factor frente al 20 % de peor puntaje).

**Resultado — correlaciones de los factores:**

| | C1 | C2 | C3 | `Credit_Score` | `Payment_Ratio` | `Credit_Utilization` |
|---|---:|---:|---:|---:|---:|---:|
| F1 | **0,799** | 0,005 | 0,000 | 0,006 | 0,013 | 0,049 |
| F2 | **0,583** | −0,007 | −0,001 | 0,020 | 0,009 | −0,003 |

**¿C1 es la suma de los dos factores?** $R^2$ de `lm(C1 ~ F1 + F2)` = **0,972**.

**El mismo costo del Módulo 16:**

| Seleccionando el 20 % más alto de… | Clientes en riesgo (20 % peor puntaje) | Los encuentra | % encontrado* |
|---|---:|---:|---:|
| F1 (capacidad) | 10.046 | 1.973 | ≈ 19,6 % |
| F2 (frecuencia) | 10.046 | 1.898 | ≈ 18,9 % |
| *Referencia Módulo 16:* C1 | 10.046 | 1.832 | 18,2 % |
| *Referencia Módulo 16:* C2 | 10.046 | 6.580 | 65,5 % |

\* Porcentajes calculados aquí a partir de los conteos renderizados (el informe da solo los conteos para F1 y F2). Al azar se esperaría ≈ 20 % (≈ 2.009).

**Lectura:**

- **C1 es la suma de los dos factores.** F1 y F2 explican el **97 %** de la C1 del PCA. Lo que el PCA llamó "tamaño", el análisis factorial lo separa en **dos rasgos**: **cuánto gasta el cliente cada vez** y **cuántas veces usa la tarjeta**. Para la Gerencia la distinción es útil: un cliente de cupo alto que casi no usa la tarjeta y uno de cupo medio que la usa a diario **tienen la misma C1, y no son el mismo cliente**.
- **Ningún factor ve el riesgo.** Su correlación con `Credit_Score`, con la proporción pagada y con el uso del cupo es prácticamente cero (todas ≤ 0,05 en valor absoluto), y el 20 % más alto de cada factor encuentra a **1.973 y 1.898** de los **10.046** clientes de peor puntaje: **lo mismo que el azar**, igual que C1 en el Módulo 16.

**Respuesta a la Gerencia:**

- **Sí hay rasgos detrás del dinero** (dos: **capacidad** y **frecuencia**), pero **el riesgo no es un rasgo de ese tipo**.
- Las variables que la C2 del PCA juntaba (puntaje, avances en efectivo, antigüedad) **casi no se correlacionan entre ellas**: las tres correlaciones están entre **−0,07 y 0,05**.
- El puntaje depende de un **contraste entre pago y saldo**, no de un factor común.
- La C2 del PCA tenía un valor propio de **1,11**: el equivalente a **una sola variable**, y esa variable es casi el puntaje (correlación **0,82**).

**Decisión:** el **mapa del Módulo 17 sigue siendo válido**, y su eje de riesgo funciona **porque C2 es, en lo esencial, `Credit_Score`**. Lo que cambia es **cómo se lee**: C2 no mide un rasgo oculto del cliente, **mide el puntaje**.

- Para el **tamaño**, la Gerencia puede usar C1 o, si quiere distinguir clientes, **los dos factores** (capacidad y frecuencia).
- Para el **riesgo**, el eje del mapa se apoya en el **puntaje** y en sus dos componentes observables: la **proporción pagada** y el **uso del cupo**.

#### Cuadro comparativo PCA vs. Análisis Factorial (síntesis del módulo)

| Aspecto | PCA (Módulos 16–17) | Análisis factorial (Módulo 18) |
|---|---|---|
| Objetivo | Mejor resumen (máxima varianza) | Modelo de dónde salen las correlaciones (rasgos latentes) |
| Qué varianza usa | Toda (diagonal de 1) | Solo la común (diagonal = comunalidades) |
| Variables usadas | 21 | 16 (5 excluidas por MSA o $R^2$ bajo) |
| Variables "solitarias" | Pueden formar su propia componente (edad → C3; puntaje → C2) | No forman factor; quedan en la unicidad |
| Resultado sobre el dinero | 1 componente: C1 "tamaño" (50,1 %) | 2 factores: capacidad y frecuencia (68 % de la varianza común de 16 variables); $R^2$ con C1 = 0,972 |
| Resultado sobre el riesgo | C2 (λ = 1,11), dominada por `Credit_Score` | Ningún factor: el riesgo no es un rasgo latente común |
| Unicidad de la solución | Única (salvo signo) | No única (rotación); se eligió varimax |

### 18.8 Qué no es un factor

- **No es una causa demostrada.** El modelo es *compatible* con un rasgo oculto de capacidad; no prueba que exista. El mismo $\mathbf{R}$ podría salir de **una regla del banco que asigna cupos según el ingreso**.
- **No es único.** Cualquier rotación de $\boldsymbol\Lambda$ ajusta igual; los nombres "capacidad" y "frecuencia" dependen de haber escogido varimax, y se discuten con el cliente.
- **No es una componente.** Deja por fuera la varianza propia de cada variable; por eso **no ve a `Credit_Score`**, que es casi toda varianza propia respecto a los factores del dinero.

### 18.9 Conclusión del Módulo 18

1. **Bartlett rechaza**, pero con $n$ grande eso no dice nada; el **KMO global es bueno (0,85)** y el **MSA por variable** deja fuera justamente a las variables del riesgo (`Credit_Score` 0,03, antigüedad 0,03, avances 0,29) y a dos que no comparten nada (edad, puntos redimidos). Con las 16 restantes el KMO sube a 0,91.
2. **`Credit_Score` tiene MSA casi cero y $R^2$ de 0,90 a la vez**: depende de la **diferencia** entre pago y saldo (parciales −0,95 y 0,92), un contraste que ningún factor común puede producir.
3. Con **dos factores** (varimax, máxima verosimilitud) las 16 variables restantes se explican en **68 de cada 100** partes: **F1 = capacidad (cuánto por vez)** y **F2 = frecuencia (cuántas veces)**; el gasto carga en los dos porque es su producto. Con promax se correlacionan **0,75**. Señales de cuidado: unicidad de `Monthly_Transactions` ≈ 0 (casi Heywood) y cargas promax > 1.
4. Los dos factores **reconstruyen la C1 del PCA** ($R^2$ = 0,972) y **no ven el riesgo**. **El riesgo no es un rasgo latente de la cartera:** la C2 del Módulo 16 es, en lo esencial, el propio `Credit_Score`, y así hay que leer el eje de riesgo del mapa del Módulo 17.

---

## Conclusiones generales del informe

> **Fuente:** `Entrega/analisis_synthetic_credit_card.Rmd`, líneas 6902–6934 (capítulo 20 del HTML, "Conclusiones Generales"). Es la sección final del informe.

El informe recorrió la cartera de **50.000 clientes** de lo univariado a lo multivariado, y cada etapa dejó una conclusión que la siguiente usó:

1. **La matriz es confiable** (Módulos 1–2): no tiene faltantes, duplicados ni valores imposibles; las 26 numéricas están bien tipadas y las 4 categóricas tienen los niveles que deben.
2. **Las variables de dinero son asimétricas y redundantes** (Módulos 3–6, 8 y 10): casi todas tienen colas largas a la derecha —por eso `log(x+1)`— y cinco columnas son derivadas o duplicadas de otras, hasta volver singular la matriz de covarianzas.
3. **El riesgo no depende del dinero, sino de la conducta de pago** (Módulos 7, 11 y 12): `Credit_Score` casi no se correlaciona con el ingreso, y queda casi determinado por el uso del cupo y la proporción pagada.
4. **Mirar de a una variable engaña** (Módulos 7, 11, 12 y 13): la relación ingreso–cupo son cinco rectas y no una; transacciones y valor medio invierten su relación según se condicione o no en la tarjeta (Simpson); un monto pagado con $r \approx 0$ cambia la cola de riesgo; y la mayoría de los casos raros no tiene ninguna variable extrema.
5. **Para la Gerencia de Riesgo, la cartera se resume en dos números** (Módulos 16–17): tamaño (C1, la mitad de la información) y riesgo (C2). El primero solo no ve el riesgo; los dos juntos dan un mapa con una lista de seguimiento priorizada.
6. **El tamaño tiene dos rasgos detrás; el riesgo, ninguno** (Módulo 18): el análisis factorial separa la C1 en capacidad (cuánto gasta el cliente por vez) y frecuencia (cuántas veces usa la tarjeta), y muestra que el riesgo no es un factor común: `Credit_Score` depende de un contraste entre pago y saldo, y la C2 del mapa es, en lo esencial, el propio puntaje.

### Síntesis numérica para la Gerencia de Riesgo (Módulos 16–18)

| Pregunta de la Gerencia | Respuesta | Cifra clave |
|---|---|---|
| ¿Puedo ordenar con un solo número? | No: el mejor número (C1) mide tamaño y no ve el riesgo | C1 guarda 50,1 %; encuentra 18 % del 20 % de peor puntaje (azar) |
| ¿Cuál es el resumen mínimo? | Dos números: C1 (exposición) y C2 (riesgo) | C2 encuentra 66 % del 20 % de peor puntaje |
| ¿Los segmentos (tarjeta, ocupación) sirven para elegir a quién seguir? | No: separan en tamaño, no en riesgo | Centros en C2 a menos de 0,2 desviaciones entre sí |
| ¿Cuántos clientes van a seguimiento? | Zonas A + B del mapa (corte C2 > 1 sd, mediana de C1) | 8.195 clientes (16,4 %); A = 4.226, B = 3.969; captura 57,8 % del 20 % de peor puntaje |
| ¿Meto el tipo de tarjeta al mapa? | No como activa; solo para colorear | Sin ponderar, la C2 deja de ser riesgo (r = 0,13 con la original) |
| ¿Hay rasgos ocultos detrás del dinero? | Sí, dos: capacidad y frecuencia | 68 % de varianza común; $R^2$ con C1 = 0,972; correlación entre ellos 0,75 (promax) |
| ¿El riesgo es un rasgo oculto? | No: es esencialmente el propio `Credit_Score` (contraste pago–saldo) | MSA del puntaje 0,025; C2 vs puntaje r = 0,82; factores encuentran 1.973 y 1.898 de 10.046 (azar) |


---

# Parte II — Talleres de Componentes Principales y Análisis Factorial

## Taller de Componentes Principales I: ¿Un número o varios?

**Archivos:** enunciado en `TallerPca/TALLER_Componentes_Principales_I.md`; solución en `TallerPca/taller_componentes_principales_I.Rmd` (tejido a `TallerPca/taller_componentes_principales_I.html`). Autores: Oscar Manuel Contreras Gacha (20221020052), Juan Pablo Sarmiento Ramírez (20221020138), Steven Navarro Parrales (20221020048) y Juan Diego Grajales Castillo (20221020128). Curso Estadística Multidimensional · 26158 · grupo 020-81 · periodo 2026-3 (docente Jhon Alejandro Varón Robayo, Universidad Distrital).

### El encargo del docente

El enunciado parte de un ejemplo de clase: una institución quería asignar tutorías con un solo número (un puntaje global). Ese puntaje guardaba 52,9 de cada 100 partes de la información, y por usarlo se quedaban sin tutoría de escritura 968 de los 2 097 estudiantes que la necesitaban. El taller pide repetir ese razonamiento **para el cliente del caso de negocio** (el definido en la sustentación del primer corte). Se trabaja por equipos, sobre el dataset propio, y se entrega un `.Rmd` y su `.html` tejido.

La regla de fondo: el taller **no se aprueba por correr `prcomp()`**, sino por decirle al cliente **qué gana y qué pierde si resume sus datos**, con números. Cada punto lleva **tres frases**: qué ven, qué significa para el cliente y qué decide él.

Puntos del enunciado y su peso (total 5,0):

| Punto | Qué pide | Puntos |
|---|---|--:|
| 1. El encargo | Un párrafo: quién es el cliente, qué decisión toma y con qué variables numéricas la toma hoy; escoger entre 4 y 10 variables numéricas y decir por qué esas | 0,5 |
| 2. ¿Se repiten? | Matriz de correlaciones en gráfico; qué variables se repiten más, cuál va más sola, si tiene sentido resumirlas (si casi todas las correlaciones están cerca de cero, decirlo) | 0,8 |
| 3. ¿Estandarizar? | Mostrar la desviación de cada variable; **decidir antes de correr** si se estandariza y justificarlo; luego correr el PCA de las dos maneras y mostrar cuánto cambia la información de la primera componente | 0,7 |
| 4. Cuánta información guarda | Gráfica de información por componente con el acumulado; cuánto guarda la primera; cuántas hacen falta para pasar de 80 de cada 100; una frase para el cliente | 1,0 |
| 5. Qué mide cada una | Graficar los pesos de las dos o tres primeras componentes, ponerle nombre a cada una mirando qué variables mandan; recordar que el signo es arbitrario | 1,0 |
| 6. El costo para su cliente | Si el cliente decidiera con un solo número, ¿a quién dejaría por fuera? Definir un grupo que le importe, contar cuántos encuentra la primera componente y cuántos se le escapan, y cerrar con la decisión: ¿uno, dos o tres números? | 1,0 |

**Descuentos** del enunciado: un resultado sin ninguna frase de lectura, −0,2 cada uno; hablar de «autovalores» o «vectores propios» sin decir qué significan para el cliente, −0,2; afirmar que una componente **demuestra** una causa o una habilidad, −0,3. Por esos descuentos todo el documento habla de «partes de información de cada 100», «pesos» y «componentes», y evita los términos técnicos y las afirmaciones causales.

### Convenciones del documento

- Cada resultado se lee con tres frases: 👀 **Qué vemos** (el número o el gráfico, sin interpretar), 💼 **Qué significa para el cliente** (la traducción a la cartera de tarjetas) y ✅ **Qué decide el cliente** (la consecuencia práctica).
- Una **componente** (principal) se define para el cliente como «una suma con pesos de las variables de la ficha». La primera es la que más información guarda; la segunda, lo más que queda, y así.
- Funciones auxiliares de formato: `coma(x, d)` (decimales con coma y miles con espacio) y `miles(x)` (enteros con separador de miles). Paquetes: `ggplot2`, `dplyr`, `tidyr`.
- El taller parte de lo que dejó listo el **Módulo 11** de `Entrega/analisis_synthetic_credit_card.Rmd`: mismas variables retenidas, logaritmo a los montos con asimetría mayor que 1 y todo en la misma escala.

### Punto 1 · El encargo

#### Cliente, decisión y ficha

**El cliente es la Gerencia de Riesgo de Crédito del banco emisor** de las 50 000 tarjetas de la base (rupias indias, ₹). Cada mes **decide qué clientes entran al programa de seguimiento preventivo**: llamada del gestor, congelar los aumentos de cupo y ofrecer refinanciación antes de la mora. Hoy toma esa decisión con una **ficha de 9 variables numéricas por cliente** y quiere saber si puede reemplazarla por **un solo número**.

Comprobación inicial del bloque `datos` (lectura de `data/bronze/synthetic_credit_card_customer_behavior_dataset.csv`):

| clientes | variables activas | celdas vacías |
|--:|--:|--:|
| 50 000 | 9 | 0 |

#### Las 9 variables activas y por qué

Se escogieron 9 de las 21 variables retenidas en el Módulo 11, porque responden las preguntas de un analista de riesgo:

| Pregunta del analista | Variables | Etiqueta en el taller |
|---|---|---|
| ¿Cuánto puede? | `Annual_Income`, `Credit_Limit` | Ingreso anual, Cupo |
| ¿Cuánto debe y paga? | `Statement_Balance`, `Payment_Amount` | Saldo facturado, Monto pagado |
| ¿Cómo usa la tarjeta? | `Monthly_Transactions`, `Avg_Transaction_Value`, `EMI_Count`, `International_Transactions` | Compras al mes, Valor por compra, Compras a cuotas, Compras internacionales |
| ¿Qué dice el buró? | `Credit_Score` | Puntaje crediticio |

**Variables suplementarias** (no construyen el resumen; sirven para entenderlo después): `Payment_Ratio` (Proporción pagada) y `Credit_Utilization` (Uso del cupo).

**Qué se dejó por fuera y por qué:**

- Las **siete categorías de gasto**: dicen *en qué* gasta el cliente y no cambian su riesgo.
- `Cash_Advance_Amount`: tiene al 70 % de los clientes en cero (Módulo 4).
- La **edad**, la **antigüedad de la tarjeta**, la **app** y los **puntos redimidos**: no hacen parte de la decisión.
- No hay celdas vacías (Módulo 2), así que entran los 50 000 clientes.

#### Transformación: logaritmo a las colas largas

**Concepto.** La asimetría (sesgo) muestral se calculó con la misma función del Módulo 11:

$$
g_1 = \frac{1}{n}\sum_{i=1}^{n}\left(\frac{x_i-\bar x}{s}\right)^3
$$

(en R: `skew <- function(x) mean(((x - mean(x)) / sd(x))^3)`). Una asimetría grande y positiva indica cola larga a la derecha: unos pocos clientes con montos enormes. Si esas variables entran crudas, esos pocos clientes «mandan» en las correlaciones y en el resumen. La transformación $\log(x+1)$ (`log1p`) comprime la cola y admite ceros.

**Regla aplicada:** si $|g_1| > 1$ la variable entra como `log1p(x)` y después `scale()`; si no, solo `scale()`.

| Variable | Asimetría | Transformación |
|---|--:|---|
| Ingreso anual | 2,55 | log(x+1) + scale() |
| Cupo | 3,01 | log(x+1) + scale() |
| Saldo facturado | 3,80 | log(x+1) + scale() |
| Monto pagado | 4,20 | log(x+1) + scale() |
| Compras a cuotas | 0,17 | scale() |
| Compras al mes | 0,54 | scale() |
| Valor por compra | 3,90 | log(x+1) + scale() |
| Compras internacionales | 2,11 | log(x+1) + scale() |
| Puntaje crediticio | −0,58 | scale() |

Seis variables entran con logaritmo (ingreso, cupo, saldo, monto pagado, valor por compra y compras internacionales); tres solo se estandarizan (cuotas, compras al mes y puntaje).

### Punto 2 · ¿Se repiten?

#### Concepto: correlación de Pearson

$$
r_{jk} = \frac{\sum_i (x_{ij}-\bar x_j)(x_{ik}-\bar x_k)}{\sqrt{\sum_i (x_{ij}-\bar x_j)^2}\sqrt{\sum_i (x_{ik}-\bar x_k)^2}}, \qquad -1 \le r_{jk} \le 1
$$

Para el cliente: 1 = las dos variables siempre van juntas, 0 = nada que ver, −1 = van en contra. Si muchas variables tienen correlaciones altas entre sí, están «contando la misma historia» y un resumen puede guardar casi todo con menos números.

#### Cómo lo aplicamos

- `R <- cor(X)` sobre las variables ya transformadas (montos en log).
- Mapa de calor con `geom_tile` y etiquetas con dos decimales; escala divergente de naranja (#C05621, −1) a blanco (0) a azul (#2B6CB0, +1), leyenda «Van juntas». Título: «Qué tanto se mueven juntas las variables de la ficha».
- Las variables se **ordenan con un agrupamiento jerárquico** sobre la distancia $1-|r|$: `hclust(as.dist(1 - abs(R)))$order`, para que las que se parecen queden juntas en el gráfico.
- Para cada variable se calculó su **mayor correlación absoluta con otra** (diagonal anulada): `apply(abs(fuera_diag), 1, max)`.
- Se definieron dos bloques: `dinero` = ingreso, cupo, saldo, monto pagado; `uso` = cuotas, compras al mes, valor por compra, compras internacionales.

#### Resultados

Mayor correlación (en valor absoluto) de cada variable con cualquier otra:

| Variable | Su mayor correlación |
|---|--:|
| Puntaje crediticio | 0,17 |
| Compras a cuotas | 0,66 |
| Compras internacionales | 0,66 |
| Compras al mes | 0,68 |
| Valor por compra | 0,78 |
| Monto pagado | 0,93 |
| Saldo facturado | 0,94 |
| Ingreso anual | 0,98 |
| Cupo | 0,98 |

- Dentro del bloque de dinero las correlaciones van de **0,87 a 0,98**.
- Entre uso y dinero van de **0,58 a 0,78**.
- El puntaje con ninguna variable pasa de **0,17** en valor absoluto.

La matriz completa 9×9 solo aparece en el mapa de calor (imagen); sus celdas individuales **no se reportan** en texto en este taller (algunas sí aparecen en el taller de análisis factorial: saldo–monto pagado 0,933; compras a cuotas–compras al mes 0,565; compras al mes–valor por compra 0,201; y las del puntaje: 0,02 con ingreso, 0,03 con cupo, −0,17 con saldo, 0,11 con monto pagado, −0,03 con cuotas, 0,02 con compras al mes, 0,02 con valor por compra y 0,05 con compras internacionales).

#### Lectura para la Gerencia

> 👀 **Qué vemos:** ingreso, cupo, saldo facturado y monto pagado van casi pegados (0,87 a 0,98), las variables de uso de la tarjeta los siguen (0,58 a 0,78) y el puntaje va solo: con ninguna pasa de 0,17.
>
> 💼 **Qué significa para el cliente:** ocho de las nueve variables cuentan la misma historia, el tamaño del cliente, así que **sí tiene sentido resumirlas**; el puntaje, que es lo que la Gerencia más mira para el riesgo, no se parece a ninguna.
>
> ✅ **Qué decide el cliente:** puede resumir la ficha, pero debe comprobar que el resumen no deje por fuera el puntaje.

**Respuestas directas a las preguntas del enunciado:** se repiten más ingreso y cupo (0,98) y, en general, el bloque de dinero; la que va más sola es el puntaje crediticio (0,17); sí tiene sentido resumir, con la advertencia del puntaje.

### Punto 3 · ¿Estandarizar?

#### Concepto

Estandarizar es pasar cada variable a $z_{ij} = (x_{ij} - \bar x_j)/s_j$: media 0 y desviación 1. Hacer PCA sobre datos estandarizados equivale a descomponer la **matriz de correlaciones** en lugar de la de covarianzas. Sin estandarizar, la varianza de cada variable depende de sus unidades, y la primera componente se va detrás de la variable de números más grandes. Para el cliente: «medir cada variable en qué tan lejos está del cliente típico, para que ninguna mande solo por tener números grandes».

#### Las desviaciones (mostradas antes de decidir)

| Variable | Desviación original | Desviación como entra al análisis (tras log si aplica) |
|---|--:|--:|
| Puntaje crediticio | 68,44 | 68,44 |
| Compras al mes | 42,05 | 42,05 |
| Compras a cuotas | 1,67 | 1,67 |
| Monto pagado | 453 396,64 | 1,27 |
| Cupo | 1 009 854,42 | 1,18 |
| Saldo facturado | 559 547,63 | 1,18 |
| Ingreso anual | 1 407 257,48 | 0,80 |
| Compras internacionales | 2,60 | 0,77 |
| Valor por compra | 779,59 | 0,62 |

#### Decisión (tomada antes de correr): estandarizamos

Las unidades no se pueden comparar: en unidades originales la desviación va de **1,67** (compras a cuotas) a **1 407 257** (ingreso, en rupias); aun con el logaritmo va de **0,62** a **68,44** (el puntaje crediticio, que no se transforma). Además es lo que ya había definido el Módulo 11.

#### Cómo lo aplicamos y comparación

```r
pca_sin <- prcomp(X)                 # log, sin estandarizar
pca     <- prcomp(X, scale. = TRUE)  # log + scale (la decisión)
info_c1 <- function(p) 100 * p$sdev[1]^2 / sum(p$sdev^2)
```

| Versión | La C1 guarda (de cada 100) | Variable que más pesa en C1 | Su peso |
|---|--:|---|--:|
| Sin estandarizar | 72,5 | Puntaje crediticio | 1,00 |
| Estandarizando | 64,3 | Cupo | 0,41 |

> 👀 **Qué vemos:** sin estandarizar, la primera componente guarda 72,5 de cada 100 partes de la información, pero es casi solo puntaje crediticio; estandarizando guarda 64,3 y ninguna variable manda sola.
>
> 💼 **Qué significa para el cliente:** la cifra más alta no es la mejor, porque sin estandarizar la componente solo copia la variable de números más grandes.
>
> ✅ **Qué decide el cliente:** debe usar la versión estandarizada, y todo lo que sigue sale de ella.

**Decisión y por qué:** el 72,5 sin estandarizar es engañoso: el puntaje (desviación 68,44 frente a desviaciones cercanas a 1 de los montos en log) acapara la varianza, y la «componente» es el puntaje con otro nombre (peso 1,00). Estandarizando, la C1 reparte pesos entre muchas variables (el máximo, el cupo, apenas 0,41).

### Punto 4 · Cuánta información guarda

#### Concepto

El PCA descompone la matriz de correlaciones $\mathbf R = \mathbf V \boldsymbol\Lambda \mathbf V^\top$. Cada componente $C_k = \mathbf Z \mathbf v_k$ es una suma con pesos de las variables estandarizadas; su varianza es $\lambda_k$ (en R, `pca$sdev[k]^2`). Como con 9 variables estandarizadas $\sum_k \lambda_k = 9$, la información que guarda la componente $k$ es

$$
\text{de cada 100} = 100\cdot\frac{\lambda_k}{\sum_{m=1}^{p}\lambda_m}, \qquad \text{acumulado}_K = \sum_{k=1}^{K}\text{de cada 100}_k .
$$

Al cliente no se le habla de «autovalores»: se le dice «de cada 100 partes de información de la ficha, cuántas guarda cada componente».

#### Cómo lo aplicamos

- Tabla `reparto` con `de_cada_100` y `acumulado`; `k80 <- which(reparto$acumulado > 80)[1]` (primer número de componentes que **pasa** de 80).
- Gráfico de barras por componente (las necesarias para pasar de 80 en azul, el resto en gris), línea naranja con el acumulado (etiquetado de C2 a C5) y línea discontinua en 80.

#### Resultados

| Componente | De cada 100 | Acumulado |
|---|--:|--:|
| C1 | 64,3 | 64,3 |
| C2 | 11,7 | 76,0 |
| C3 | 9,3 | 85,3 |
| C4 | 6,3 | 91,6 |
| C5 | 5,0 | 96,6 |
| C6 | 2,2 | 98,8 |
| C7 | 0,9 | 99,8 |
| C8 | 0,2 | 99,9 |
| C9 | 0,1 | 100,0 |

(Equivalencia técnica, no reportada al cliente: $\lambda_1 \approx 0{,}643 \times 9 \approx 5{,}79$ y $\lambda_2 \approx 0{,}117\times 9\approx 1{,}05$.)

> 👀 **Qué vemos:** la primera componente guarda 64,3 de cada 100 partes de la información; con dos se llega a 76,0 y con **3** se pasa de 80 (85,3).
>
> 💼 **Qué significa para el cliente:** *una sola componente resume 64 de cada 100 partes de la ficha de un cliente, y para no perder más de una quinta parte la Gerencia necesita mirar 3 números.*
>
> ✅ **Qué decide el cliente:** no debe reemplazar la ficha por un solo número sin ver antes qué hay en las otras 36 partes.

### Punto 5 · Qué mide cada una

#### Concepto: pesos y signo arbitrario

El **peso** (carga del vector propio, `pca$rotation`) de la variable $j$ en la componente $k$ dice cuánto manda esa variable en la suma. El vector $\mathbf v_k$ y $-\mathbf v_k$ son igual de válidos: **el signo es arbitrario**, así que se lee qué variables mandan y si van en la misma dirección o en contra, nunca el signo absoluto.

#### Anclaje de signos

Para que la lectura fuera cómoda se fijó el signo de cada componente con una variable ancla:

```r
# C1 positiva = más cupo; C2 positiva = peor puntaje; C3 positiva = compras de mayor valor.
signo <- c(sign(pca$rotation["Credit_Limit", 1]),
           -sign(pca$rotation["Credit_Score", 2]),
            sign(pca$rotation["Avg_Transaction_Value", 3]))
pesos     <- sweep(pca$rotation[, 1:3], 2, signo, `*`)
puntaje_c <- sweep(pca$x[, 1:3], 2, signo, `*`)
```

Es decir: en C1 el cupo pesa positivo; en C2 el puntaje pesa **negativo** (subir en C2 = peor puntaje); en C3 el valor por compra pesa positivo.

#### Resultados: pesos de las tres primeras componentes

| Variable | C1 | C2 | C3 |
|---|--:|--:|--:|
| Ingreso anual | 0,40 | −0,02 | 0,04 |
| Cupo | 0,41 | −0,02 | 0,03 |
| Saldo facturado | 0,40 | 0,17 | 0,05 |
| Monto pagado | 0,38 | −0,10 | 0,02 |
| Compras a cuotas | 0,30 | 0,07 | −0,30 |
| Compras al mes | 0,29 | 0,01 | −0,72 |
| Valor por compra | 0,32 | −0,04 | 0,60 |
| Compras internacionales | 0,29 | −0,09 | 0,18 |
| Puntaje crediticio | 0,00 | −0,97 | −0,07 |

Gráfico: barras horizontales por componente (facetas «C1 · el tamaño del cliente», «C2 · puntaje y hábito de pago», «C3 · estilo de compra»), azul para pesos positivos y naranja para negativos.

#### Validación con suplementarias

Para confirmar los nombres se correlacionaron los puntajes de C1–C3 con dos variables que **no** se usaron para armar las componentes:

| Componente | Proporción pagada (`Payment_Ratio`) | Uso del cupo (`Credit_Utilization`) |
|---|--:|--:|
| C1 | 0,06 | 0,11 |
| C2 | −0,76 | 0,59 |
| C3 | −0,06 | 0,07 |

#### Nombres y lectura

- **C1 · el tamaño del cliente:** todas las variables pesan positivo, y las de rupias mandan (pesos de 0,38 a 0,41); el puntaje pesa 0,00. Sube con todo lo que el cliente gana, tiene y mueve.
- **C2 · puntaje y hábito de pago:** casi solo el puntaje (−0,97); va −0,76 con la proporción pagada y 0,59 con el uso del cupo. Un puntaje bajo va con pagar poco de lo facturado y usar más el cupo.
- **C3 · estilo de compra:** enfrenta el valor por compra (0,60) con las compras al mes (−0,72) y las cuotas (−0,30): pocas compras caras o muchas pequeñas.

> 👀 **Qué vemos:** a la primera componente la mueven las variables en rupias (pesos de 0,38 a 0,41), la segunda casi solo el puntaje (−0,97), que va −0,76 con la proporción pagada, y la tercera enfrenta el valor por compra (0,60) con las compras al mes (−0,72).
>
> 💼 **Qué significa para el cliente:** los llamamos **tamaño del cliente**, **puntaje y hábito de pago** y **estilo de compra**, nombres que ponemos nosotros al ver qué variables mandan, y el signo del peso es arbitrario.
>
> ✅ **Qué decide el cliente:** lo que la primera componente deja por fuera no es ruido sino el puntaje y el pago, así que no debe decidir el seguimiento mirando solo el tamaño.

**Cuidado explícito (por el descuento de −0,3):** los nombres son etiquetas leídas de los pesos; ninguna componente «demuestra» una causa ni una habilidad.

### Punto 6 · El costo para su cliente

#### El grupo que le importa a la Gerencia

Los clientes con **puntaje crediticio bajo**: el 20 % más bajo de la cartera (`Credit_Score <= quantile(Credit_Score, 0.20)`), que el buró señala como más riesgosos. El corte resultó ser **571**: puntaje de 571 o menos, **10 046 clientes** (algo más del 20 % por empates en el corte).

#### Cómo se mide el costo

Si la Gerencia decidiera con un solo número, mandaría a seguimiento al **20 % de clientes en un extremo** de esa componente (`en_el_20_alto <- function(s) s >= quantile(s, 0.80)`). Como el signo es arbitrario, **se prueban los dos extremos** y se queda el que encuentre más (`encuentra(s) = max(sum(riesgo & top20(s)), sum(riesgo & top20(-s)))`): se le da al único número su mejor oportunidad. La referencia es el **azar**: una lista del 20 % al azar encontraría $0{,}2 \times 10\,046 \approx 2\,009$.

#### Resultado con el puntaje bajo

| Decide con | Clientes de riesgo | Los encuentra | Se le escapan | De cada 100 se escapan |
|---|--:|--:|--:|--:|
| Solo C1 (tamaño) | 10 046 | 2 089 | 7 957 | 79,2 |
| C2 (puntaje y pago) | 10 046 | 9 571 | 475 | 4,7 |
| Al azar (referencia) | 10 046 | 2 009 | 8 037 | 80,0 |

> 👀 **Qué vemos:** de los 10 046 clientes con puntaje de 571 o menos, la componente de tamaño encuentra 2 089 y se le escapan 7 957 (79 de cada 100), casi lo mismo que al azar (2 009), mientras que la de puntaje y pago encuentra 9 571.
>
> 💼 **Qué significa para el cliente:** una lista por tamaño es casi sacar nombres de un sombrero y deja sin seguimiento a 79 de cada 100 clientes de puntaje bajo.
>
> ✅ **Qué decide el cliente:** no debe escoger a quién hacer seguimiento con la componente de tamaño.

#### Advertencia y prueba de robustez con `Payment_Ratio`

La C2 casi **es** el puntaje (peso −0,97), así que encontrar con ella a los de puntaje bajo es, en parte, repetir la definición (circularidad). Para comprobarlo con algo distinto se repitió la prueba con el **20 % de clientes que paga la menor parte de lo facturado** (`Payment_Ratio <= quantile(Payment_Ratio, 0.20)`), una medida que no se usó para armar ninguna componente. El corte fue **0,55** (pagan 55 % o menos de lo facturado): **10 311 clientes**.

| Decide con | Clientes que pagan poco | Los encuentra | Se le escapan | De cada 100 se escapan |
|---|--:|--:|--:|--:|
| Solo C1 (tamaño) | 10 311 | 2 401 | 7 910 | 76,7 |
| C2 (puntaje y pago) | 10 311 | 7 090 | 3 221 | 31,2 |
| C3 (estilo de compra) | 10 311 | 2 388 | 7 923 | 76,8 |
| Al azar (referencia) | 10 311 | 2 062 | 8 249 | 80,0 |

> 👀 **Qué vemos:** de los 10 311 clientes que pagan 0,55 o menos de lo facturado, la componente de tamaño encuentra 2 401 (al azar, 2 062), la de puntaje y pago 7 090 y la de estilo de compra 2 388.
>
> 💼 **Qué significa para el cliente:** la conclusión se mantiene sin usar el puntaje, aunque la componente de puntaje y pago deja escapar a 3 221 clientes que pagan poco.
>
> ✅ **Qué decide el cliente:** debe usar la componente de puntaje y pago para priorizar, sabiendo que no encuentra a todos.

#### Un caso concreto: grandes y de riesgo

Se cruzaron el 20 % más grande en C1 con los de puntaje bajo:

| Indicador | Valor |
|---|--:|
| Clientes grandes (20 % superior de C1) y de puntaje bajo | 1 845 |
| Cupo promedio de ellos (₹) | 2 137 005 |
| Cupo promedio de la cartera (₹) | 709 677 |
| Proporción pagada promedio de ellos | 0,47 |
| Proporción pagada promedio de los demás grandes | 0,86 |

> 👀 **Qué vemos:** 1 845 clientes están entre el 20 % más grande y los de puntaje bajo, con un cupo promedio de 2 137 005 rupias (cartera: 709 677) y una proporción pagada de 0,47, contra 0,86 de los demás grandes.
>
> 💼 **Qué significa para el cliente:** para la componente de tamaño son «los mejores clientes» y candidatos a más cupo, aunque tienen puntaje bajo y pagan mucho menos de lo que se les factura.
>
> ✅ **Qué decide el cliente:** un número no le basta, y debe reportar tamaño (cuánto dinero hay en juego) y puntaje y pago (a quién llamar), que juntos guardan 76,0 de cada 100 partes; la tercera componente no le hace falta para riesgo.

**Decisión y por qué:** aunque para pasar de 80 de cada 100 hacen falta 3 componentes (punto 4), la tercera (estilo de compra) no encuentra mejor que el azar a los que pagan poco (2 388 frente a 2 062), así que para la decisión de riesgo bastan **dos números**.

### Lo que le entregamos a la Gerencia (Taller I)

- **Sí se puede resumir la ficha**, porque ocho de sus nueve variables cuentan casi la misma historia: el tamaño del cliente.
- **Pero una sola componente deja por fuera justo el puntaje y el hábito de pago.** Esa información va casi sola en la segunda componente.
- **En clientes, el costo es concreto:** de los 10 046 con puntaje bajo, la componente de tamaño deja por fuera 7 957. A los 1 845 clientes grandes con puntaje bajo los confunde con los mejores clientes.
- **La decisión:** reportar dos números, tamaño y puntaje con hábito de pago (juntos 76,0 de cada 100 partes). El segundo es el que debe decidir la entrada al programa de seguimiento preventivo.

---

## Taller de Componentes Principales II: El mapa de su negocio

**Archivos:** `TallerPca/taller_componentes_principales_II.Rmd` (versión anterior) y `TallerPca/taller_componentes_principales_II_final.Rmd` (versión final, la que se documenta aquí). Mismos autores y curso que el Taller I. Paquetes: `ggplot2`, `dplyr`, `tidyr` y `ggrepel` (se instala si falta).

**Sobre las cifras.** Todas las cifras de esta sección provienen del renderizado `taller_componentes_principales_II.txt` y de las tablas embebidas en `TallerPca/taller_componentes_principales_II.html`. Al revisarlos se comprobó que **ambos renderizados ya contienen el texto y el código de la versión final** (incluyen la bandera `estable`, `comp_tipo`/`info_tipo`, el párrafo «Esta comparación es aparte…» y la redacción «C (grande, no de riesgo)»; no contienen la frase «El docente pidió…» de la versión anterior). Por tanto, todas las cifras de la versión final están disponibles; las diferencias con la versión anterior se describen al final de esta sección.

**Enunciado:** el enunciado de este taller no está en el repositorio. Su estructura se reconstruye desde el propio `.Rmd`, que habla de «los puntos 1 a 5 del taller (mapa, biplot, grupos, grupo del cliente y cortes)»: (1) el mapa de los clientes en las dos primeras componentes y el nombre de sus direcciones; (2) el biplot; (3) ¿hay grupos o un continuo?; (4) ¿los grupos que su cliente conoce se separan en el mapa?; (5) la decisión en el mapa (cortes). A eso el equipo añadió una comparación con y sin *one-hot* del tipo de tarjeta. Mismo formato de tres frases (👀 / 💼 / ✅).

### El encargo

El cliente sigue siendo la **Gerencia de Riesgo de Crédito** del banco emisor de las 50 000 tarjetas (₹), que cada mes decide quién entra al **programa de seguimiento preventivo** (llamada del gestor, congelar aumentos de cupo, refinanciación antes de que la deuda se vuelva mora). En el Taller I se le dijo que un solo número no basta; ahora se le entrega **el mapa de su cartera**: cada cliente es un punto y su posición resume sus 9 variables. «Lo que importa no es el dibujo, sino qué ve la Gerencia en el mapa y qué hace con él».

**Datos y preparación** (idénticos al Taller I «versión corregida», que parte del Módulo 11):

- Las mismas **9 variables activas**: ingreso anual, cupo, saldo facturado, monto pagado, compras a cuotas, compras al mes, valor por compra, compras internacionales y puntaje crediticio. Bloques: `dinero` (las cuatro primeras) y `uso` (las cuatro de uso).
- Misma transformación: `log1p` a las de $|g_1|>1$ y después `scale()`. **6 entran con logaritmo:** ingreso anual, cupo, saldo facturado, monto pagado, valor por compra y compras internacionales.
- Celdas vacías: **0**; entran los **50 000** clientes.
- `Payment_Ratio` y `Credit_Utilization` siguen como **suplementarias**: no construyen el mapa, sirven para nombrar sus direcciones.
- La ruta del CSV se valida (`file.exists`) y si no existe el bloque se detiene con un mensaje.

### Punto 1 · El mapa y sus direcciones

#### Concepto

El mapa es el **plano factorial** de las dos primeras componentes: cada cliente $i$ se dibuja en $(C_{1i}, C_{2i})$, sus puntajes en C1 y C2. Las direcciones se nombran con la correlación de cada variable con cada eje; para una variable activa estandarizada esa correlación vale

$$
\operatorname{cor}(x_j, C_k) = v_{jk}\sqrt{\lambda_k},
$$

y para una suplementaria se calcula directamente.

#### Cómo lo aplicamos

- `pca <- prcomp(X, scale. = TRUE)` (log + scale, la decisión del Taller I).
- **Anclaje de signos** (el signo de `prcomp()` es arbitrario; invertirlo solo refleja el mapa):
  - C1: el **cupo** debe pesar positivo → ir a la derecha = más cupo.
  - C2: el **puntaje** debe pesar **negativo** → ir hacia arriba = peor puntaje.

| Componente | Variable ancla | Regla | Peso después | ¿Hubo que invertir? |
|---|---|---|--:|---|
| C1 | Cupo | el cupo debe pesar positivo | 0,41 | No |
| C2 | Puntaje crediticio | el puntaje debe pesar negativo | −0,97 | **Sí** |

- Correlación de C1 y C2 con cada variable (`cor(puntaje_c, X)` y con las suplementarias):

| Variable | Tipo | Con C1 | Con C2 |
|---|---|--:|--:|
| Ingreso anual | activa | 0,97 | −0,02 |
| Cupo | activa | 0,98 | −0,02 |
| Saldo facturado | activa | 0,96 | 0,17 |
| Monto pagado | activa | 0,92 | −0,10 |
| Compras a cuotas | activa | 0,73 | 0,08 |
| Compras al mes | activa | 0,70 | 0,01 |
| Valor por compra | activa | 0,78 | −0,04 |
| Compras internacionales | activa | 0,71 | −0,10 |
| Puntaje crediticio | activa | 0,01 | −1,00 |
| Proporción pagada | suplementaria | 0,06 | −0,76 |
| Uso del cupo | suplementaria | 0,11 | 0,59 |

- Gráfico «El mapa de los 50 000 clientes»: los 50 000 puntos con transparencia 0,06, ejes en cero; eje x «← cliente más pequeño · C1: el tamaño del cliente · cliente más grande →», eje y «← mejor puntaje · C2: el riesgo · peor puntaje →».

#### Resultados y lectura

C1 guarda **64,3** de cada 100 partes y C2 **11,7**: **juntas 76,0**; quedan por fuera **24,0**.

> 👀 **Qué vemos:** ir a la derecha va con más cupo (0,98) y más saldo facturado (0,96), y casi no tiene que ver con el puntaje (0,01). Ir hacia arriba va con peor puntaje (correlación −1,00, negativa por cómo fijamos el signo). Entre las suplementarias, C2 va −0,76 con la proporción pagada y 0,59 con el uso del cupo.
>
> 💼 **Qué significa para el cliente:** **Derecha · el tamaño del cliente**: más cupo, más saldo y más rupias en juego; no dice cómo paga. **Arriba · el riesgo**: peor puntaje, que va con una proporción pagada menor y con más uso del cupo. Los nombres son nuestros: el mapa muestra qué variables se mueven juntas, **no que el tamaño cause un buen o mal pago**.
>
> ✅ **Qué decide el cliente:** leer cada cliente con dos preguntas: *¿qué tan a la derecha está?* (cuánto dinero hay en juego) y *¿qué tan arriba?* (cuánto riesgo). Al mirar solo este plano quedan por fuera 24,0 de cada 100 partes de la información de la ficha: eso es lo que se sacrifica por tener un mapa de dos dimensiones.

Nota: en este taller C2 se rebautiza de «puntaje y hábito de pago» (Taller I) a **«el riesgo»**.

### Punto 2 · El biplot

#### Concepto

Un **biplot** superpone en el mismo plano los individuos (puntos) y las variables (flechas). Aquí cada flecha es la correlación de la variable con C1 y C2: `flechas <- carga × sdev`. Propiedades que se usan:

- **Largo** de la flecha $\ell_j = \sqrt{r_{j1}^2 + r_{j2}^2}\le 1$; $100\,\ell_j^2$ es la parte de la variable que «se ve» en el plano. Una flecha que llega a la circunferencia unitaria se ve entera.
- **Ángulo** entre dos flechas $\mathbf a,\mathbf b$: $\theta = \arccos\!\big(\mathbf a\cdot\mathbf b / (\|\mathbf a\|\|\mathbf b\|)\big)$. Cerca de 0° = se mueven juntas; cerca de 90° = casi no tienen que ver; cerca de 180° = se mueven en contra. Solo es confiable si las flechas son largas.
- **Ángulo desde C1**: `atan2(C2, C1)` en grados (0° = derecha, 90° = arriba).

#### Cómo lo aplicamos

- Bloques de color: Dinero (azul #2B6CB0), Uso de la tarjeta (gris #718096), Puntaje (naranja #C05621).
- Nube de fondo: muestra de **6 000 clientes** (`set.seed(2026)`), solo para aligerar; los puntos se **reescalan** con `esc = 1,1 / percentil 99 de |puntajes|` para que quepan junto a las flechas. Circunferencia unitaria discontinua; etiquetas con `geom_text_repel`.
- Matriz de ángulos entre todos los pares (`acos` acotado a [−1, 1]).
- Reglas de lectura automáticas: `juntas` = máximo ángulo dentro del dinero < 30°; `pun_aparte` = mínimo ángulo puntaje–dinero > 45°; pares «en contra» = ángulo > 120°; flechas «pobres» = largo < 0,7; variable «sola» = la de mayor ángulo a su vecina más cercana.

#### Resultados

| Variable | Bloque | Ángulo desde C1 (°) | Largo de la flecha | De cada 100 que se ve en el mapa |
|---|---|--:|--:|--:|
| Ingreso anual | Dinero | −1 | 0,97 | 94 |
| Cupo | Dinero | −1 | 0,98 | 96 |
| Saldo facturado | Dinero | 10 | 0,98 | 95 |
| Monto pagado | Dinero | −6 | 0,92 | 85 |
| Compras a cuotas | Uso de la tarjeta | 6 | 0,73 | 54 |
| Compras al mes | Uso de la tarjeta | 1 | 0,70 | 49 |
| Valor por compra | Uso de la tarjeta | −3 | 0,78 | 60 |
| Compras internacionales | Uso de la tarjeta | −8 | 0,71 | 51 |
| Puntaje crediticio | Puntaje | −90 | 1,00 | 99 |

Ángulos entre flechas (grados, redondeados):

| | Ingreso | Cupo | Saldo | Pago | Cuotas | Compras/mes | Valor/compra | Internac. | Puntaje |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Ingreso anual | 0 | 0 | 11 | 5 | 7 | 2 | 2 | 7 | 89 |
| Cupo | 0 | 0 | 11 | 5 | 7 | 2 | 2 | 7 | 88 |
| Saldo facturado | 11 | 11 | 0 | 17 | 4 | 9 | 13 | 18 | 100 |
| Monto pagado | 5 | 5 | 17 | 0 | 12 | 7 | 4 | 1 | 83 |
| Compras a cuotas | 7 | 7 | 4 | 12 | 0 | 5 | 9 | 14 | 96 |
| Compras al mes | 2 | 2 | 9 | 7 | 5 | 0 | 4 | 9 | 91 |
| Valor por compra | 2 | 2 | 13 | 4 | 9 | 4 | 0 | 5 | 87 |
| Compras internacionales | 7 | 7 | 18 | 1 | 14 | 9 | 5 | 0 | 82 |
| Puntaje crediticio | 89 | 88 | 100 | 83 | 96 | 91 | 87 | 82 | 0 |

> 👀 **Qué vemos:**
> - **Van juntas:** las cuatro flechas de dinero salen casi en la misma dirección; entre ellas forman ángulos de **0° a 17°**.
> - **Va sola:** la flecha más aislada es la del **puntaje crediticio**, con **82°** hasta su vecina más cercana. El puntaje forma entre **83° y 100°** con las de dinero (con el cupo, **88°**).
> - **Uso de la tarjeta:** las flechas de uso forman entre **1° y 18°** con las de dinero.
> - **En contra:** ningún par pasa de 120°; la pareja más abierta es puntaje crediticio con saldo facturado (**100°**).
> - **Cuánto se ve:** todas las flechas llegan cerca de la circunferencia (ninguna bajo 0,7 de largo; la más corta, compras al mes, 0,70), así que sus ángulos son confiables.
>
> 💼 **Qué significa para el cliente:** ingreso, cupo, saldo y monto pagado **cuentan casi la misma historia**, el tamaño del cliente: mirar las cuatro a la vez no le da cuatro señales, le da una repetida. Las de uso acompañan ese bloque en mayor o menor grado. El puntaje apunta a otro lado: **el riesgo no se lee en las variables de dinero**, y ninguna lo reemplaza.
>
> ✅ **Qué decide el cliente:** para el seguimiento le basta **una** variable de tamaño (la que prefiera por costo de obtenerla) y **no puede prescindir del puntaje**. La ficha de 9 variables se puede acortar sin perder lo que distingue a los clientes, pero quitarle el puntaje sí le quitaría el riesgo.

(Las condiciones `juntas` = 17° < 30° y `pun_aparte` = 83° > 45° se cumplieron, por eso se imprimieron esas frases.)

### Punto 3 · ¿Hay grupos o hay un continuo?

#### Concepto

Si la cartera tuviera «tipos» de cliente separados, la densidad de los puntajes en cada eje tendría **varias cumbres separadas por un valle profundo**, y las curvas de nivel de la nube mostrarían más de un centro. Si no, es un **continuo**. La densidad se estima con un núcleo (kernel) gaussiano:

$$
\hat f(x) = \frac{1}{nh}\sum_{i=1}^{n} K\!\left(\frac{x - x_i}{h}\right).
$$

#### Cómo lo aplicamos

Función propia `forma(x, prom = 0.10)` sobre `density(x)`:

1. **Picos:** máximos locales de la densidad (`diff(sign(diff(y))) == -2`), ignorando bultos menores al **10 %** del pico más alto.
2. **Valle sobre pico:** entre los dos picos más altos, la densidad mínima dividida por la del menor de los dos picos.
3. **Central sobre pico:** la densidad más baja dentro del **80 % central** de los datos (percentiles 10 a 90) dividida por la máxima.
4. Se considera que **hay valle** si hay ≥ 2 picos y el valle baja a **menos del 50 %** del pico. `continuo` = no hay valle ni en C1 ni en C2.
5. **Referencia con islas:** el PCA estandarizado de `iris` (4 medidas), el caso de clase en que *setosa* queda separada.

Gráficos: nube con curvas de nivel (`geom_density_2d`, 10 niveles), densidades de C1 y C2 por separado, y el mapa de iris coloreado por especie.

#### Resultados

| Mapa | Picos | Densidad en el valle / la del pico | Densidad más baja del 80 % central / pico |
|---|--:|---|--:|
| Clientes · C1 | 3 | 95 % | 28 % |
| Clientes · C2 | 1 | no hay valle | 35 % |
| Iris · C1 | 2 | 22 % | 19 % |
| Iris · C2 | 1 | no hay valle | 41 % |

> 👀 **Qué vemos:** en el mapa de clientes la curva de C1 tiene 3 picos y la de C2 tiene 1. En C1 no hay un valle que separe dos cumbres (el valle entre los dos picos mayores se queda en el 95 % de la altura: son ondulaciones, no islas). En C2 tampoco. Dentro del 80 % central, la densidad más baja de C1 es 28 % de la más alta (en C2, 35 %). Con el mismo cálculo, iris tiene 2 picos en C1 y su valle baja a 22 % del pico: así se ve una isla de verdad. Las curvas de nivel de los clientes forman una sola mancha, sin un segundo centro.
>
> 💼 **Qué significa para el cliente:** la cartera es un **continuo**: no hay «tipos» de cliente separados por un hueco. El riesgo y el tamaño son gradientes; no existe un punto del mapa donde termine un grupo y empiece otro, como sí lo hay entre setosa y las demás.
>
> ✅ **Qué decide el cliente:** no diseñar la política por «tipos» de cliente que el mapa no muestra. Cualquier corte será una decisión suya, según cuántos clientes puede atender, y no un borde que el mapa haya encontrado.

**Decisión y por qué:** se usó un criterio numérico (umbral del 50 % para el valle, 10 % para ignorar bultos) y una referencia conocida (iris) para no depender de la impresión visual; los tres picos de C1 se descartan como grupos porque el valle entre ellos es muy poco profundo (95 %).

### Punto 4 · ¿Los grupos que su cliente conoce se separan?

#### El grupo del cliente

La Gerencia ya decide con el **tipo de tarjeta** (`Card_Type`): de él dependen el cupo, los beneficios y la política de aumentos. Es **ordinal**: Basic < Silver < Gold < Platinum < Signature (Módulo 1 de la entrega). Aquí se usa como **grupo externo**: no entra a construir el mapa.

#### Conceptos y cómo lo aplicamos

1. **Distancia entre promedios en desviaciones del eje:** $d = (\bar C_{k,\text{Signature}} - \bar C_{k,\text{Basic}})/s_{C_k}$, calculada por separado en C1 y C2 (`dist_medias`).
2. **Proporción de varianza explicada por el tipo** ($\eta^2$ de un ANOVA de una vía, `summary(aov(y ~ g))`):
$$
\eta^2 = \frac{SC_{\text{entre}}}{SC_{\text{total}}}.
$$
3. **Traslape con elipses del 90 %:** para cada tipo «en» se estima media $\boldsymbol\mu$ y covarianza $\mathbf S$ de sus puntos en (C1, C2), y se cuenta qué fracción de los clientes del tipo «de» cae dentro de su elipse, es decir con distancia de Mahalanobis
$$
d^2 = (\mathbf x - \boldsymbol\mu)^\top \mathbf S^{-1} (\mathbf x - \boldsymbol\mu) \le \chi^2_{2;\,0{,}90} \approx 4{,}61
$$
(`mahalanobis(B_, colMeans(A_), cov(A_)) <= qchisq(0.90, 2)`), suponiendo forma normal (`stat_ellipse(level = 0.90, type = "norm")` en el gráfico).
4. Gráficos: mapa coloreado por tipo (paleta viridis) con una muestra de **12 000 clientes** (`set.seed(2026)`) y elipses calculadas con **todos**; y diagramas de caja de C1 y C2 por tipo.

#### Resultados

Promedios por tipo:

| Tipo | Clientes | Promedio C1 | Promedio C2 |
|---|--:|--:|--:|
| Basic | 10 261 | −3,20 | −0,04 |
| Silver | 12 056 | −0,99 | 0,04 |
| Gold | 16 895 | 0,62 | 0,09 |
| Platinum | 8 284 | 2,67 | −0,12 |
| Signature | 2 504 | 4,87 | −0,23 |

Separación de los extremos y peso del tipo en cada eje:

| Eje | Basic → Signature (en desviaciones) | De cada 100 de la varianza que explica el tipo |
|---|--:|--:|
| C1 · tamaño | 3,36 | 83,6 |
| C2 · riesgo | −0,18 | 0,8 |

Traslape (de cada 100 clientes de la fila, cuántos caen dentro de la elipse del 90 % de la columna):

| De… / en la elipse de… | Basic | Silver | Gold | Platinum | Signature |
|---|--:|--:|--:|--:|--:|
| Basic | 91 | 39 | 2 | 0 | 0 |
| Silver | 46 | 92 | 51 | 5 | 0 |
| Gold | 2 | 59 | 91 | 46 | 0 |
| Platinum | 0 | 1 | 41 | 89 | 19 |
| Signature | 0 | 0 | 0 | 38 | 92 |

> 👀 **Qué vemos:** en **C1**, Basic y Signature están a 3,36 desviaciones y el tipo explica 83,6 de cada 100 partes de la variación de C1. En **C2** esa distancia es de 0,18 desviaciones y el tipo explica 0,8 de cada 100. De cada 100 Basic, 0 caen en la elipse de Signature, y de cada 100 Signature, 0 caen en la de Basic. Entre vecinos es distinto: de cada 100 Gold, 46 caen en la elipse de Platinum, y de cada 100 Platinum, 41 en la de Gold.
>
> 💼 **Qué significa para el cliente:** los tipos **se desplazan** a lo largo del tamaño: cuanto más alto el tipo, más a la derecha, y los extremos casi no se pisan. Los vecinos sí se traslapan bastante, así que el tipo no separa a los clientes uno a uno. En el riesgo los grupos casi coinciden: un Signature está tan arriba o tan abajo como un Basic. El tipo **va con** la posición en el mapa; no decimos que la cause.
>
> ✅ **Qué decide el cliente:** el tipo de tarjeta le sirve para saber **cuánto dinero hay en juego**, pero **no para escoger a quién mandar a seguimiento**: dentro de cada tipo hay clientes de riesgo y sanos en proporciones parecidas. Para el seguimiento necesita el eje C2.

(Condiciones de redacción que se cumplieron: |d en C1| = 3,36 ≥ 1; Basic→Signature y Signature→Basic < 10; Gold→Platinum 46 > 20; |d en C2| = 0,18 < 0,3.)

### Punto 5 · La decisión en el mapa

#### Los cortes y por qué el 20 %

Dos cortes, uno por eje, que son **decisión de la Gerencia y no bordes del mapa** (el punto 3 mostró que no hay huecos):

- **Corte de riesgo (C2):** el 20 % de clientes más arriba (`C2 >= quantile(C2, 0.80)`).
- **Corte de tamaño (C1):** el 20 % más a la derecha (`C1 >= quantile(C1, 0.80)`).

Se eligió el 20 % por coherencia con el Taller I, donde el riesgo se definió como el 20 % con peor puntaje (`Credit_Score <= quantile(Credit_Score, 0.20)`, 10 046 clientes). Los dos cortes parten el mapa en **cuatro zonas**: A (grande y de riesgo: arriba y a la derecha), B (de riesgo, no grande), C (grande, no de riesgo) y D (el resto).

#### Resultados por zona

| Zona | Nombre | Clientes | De cada 100 de la cartera | Con peor puntaje | Puntaje promedio | Proporción pagada | Uso del cupo | Saldo facturado (millones ₹) |
|---|---|--:|--:|--:|--:|--:|--:|--:|
| A | grande y de riesgo | 1 766 | 3,5 | 1 704 | 524 | 0,47 | 0,63 | 2 497 |
| B | de riesgo, no grande | 8 234 | 16,5 | 7 867 | 525 | 0,44 | 0,56 | 1 908 |
| C | grande, no de riesgo | 8 234 | 16,5 | 141 | 654 | 0,85 | 0,42 | 8 716 |
| D | el resto | 31 766 | 63,5 | 334 | 655 | 0,84 | 0,38 | 5 188 |

(B y C tienen exactamente el mismo tamaño porque cada corte deja 10 000 clientes y A, su intersección, tiene 1 766: 10 000 − 1 766 = 8 234.)

Cifras derivadas: A + B = **10 000** clientes llamados; alcanzan **9 571** de los 10 046 de peor puntaje (**95** de cada 100); A es **18** de cada 100 llamados pero concentra **57** de cada 100 rupias facturadas del grupo llamado (2 497 de 4 405 millones).

#### Sensibilidad del corte de riesgo

| Corte de C2 | Clientes a seguimiento | De ellos con peor puntaje | De cada 100 con peor puntaje que encuentra | De cada 100 llamados que son de riesgo |
|---|--:|--:|--:|--:|
| percentil 70 | 15 000 | 10 046 | 100,0 | 67,0 |
| percentil 80 | 10 000 | 9 571 | 95,3 | 95,7 |
| percentil 90 | 5 000 | 5 000 | 49,8 | 100,0 |

Clientes en la zona A al mover ambos cortes:

| Zona A | C2 desde el percentil 70 | C2 desde el percentil 80 | C2 desde el percentil 90 |
|---|--:|--:|--:|
| C1 desde el percentil 70 | 4 328 | 2 775 | 1 336 |
| C1 desde el percentil 80 | 2 764 | 1 766 | 833 |
| C1 desde el percentil 90 | 1 299 | 848 | 389 |

Gráfico: el mapa coloreado por zona (A naranja, B ocre, C azul, D gris), cortes punteados y etiquetas con el número de clientes; ejes recortados a los percentiles 0,2 y 99,8.

#### Lectura

> 👀 **Qué vemos:** 1 766 clientes en A, 8 234 en B, 8 234 en C y 31 766 en D. De los 10 046 con peor puntaje, A tiene 1 704 y B 7 867. La proporción pagada es 0,47 en A, 0,44 en B, 0,85 en C y 0,84 en D; el uso del cupo, 0,63, 0,56, 0,42 y 0,38. El saldo facturado de A es 2 497 millones de ₹ contra 1 908 de B.
>
> 💼 **Qué significa para el cliente, zona por zona:**
> - **A · grande y de riesgo (1 766):** el grupo que el índice único del Taller I confundía con los mejores clientes. Son 18 de cada 100 llamados pero concentran 57 de cada 100 rupias facturadas del grupo. **Gestor senior, congelar aumentos de cupo y oferta de refinanciación.**
> - **B · de riesgo, no grande (8 234):** también en el 20 % de mayor riesgo, con menos dinero en juego por cliente. **Llamada estándar o mensaje automatizado con oferta de refinanciación**, sin gestor dedicado.
> - **C · grande, no de riesgo (8 234):** mucho dinero, fuera del 20 % de mayor riesgo. **No entran al seguimiento**; pueden considerarse para aumento de cupo.
> - **D · el resto (31 766):** **sin acción**.
>
> **Si se mueve el corte de riesgo:** en el percentil 70 se llama a 15 000 y se encuentran 100 de cada 100 de peor puntaje; en el 90, a 5 000 y se encuentran 50. De cada 100 llamados, 67 son de riesgo con el corte en 70 y 100 con el corte en 90: subir el corte hace la lista más corta y más precisa, pero deja más riesgo sin visitar. La zona A va de 389 clientes (ambos cortes en 90) a 4 328 (ambos en 70).
>
> ✅ **Qué decide el cliente:** empezar con **A** (1 766), donde cada llamada protege más dinero, y sumar **B** si la capacidad del equipo lo permite: con A y B se llama a 10 000 y se alcanzan 9 571 de los 10 046 de peor puntaje (95 de cada 100). El corte se mueve según cuántas llamadas pueda hacer el equipo; no hay un valor «correcto» que el mapa indique. **Un cuidado:** C2 se construyó en parte con el puntaje, que es lo que define el riesgo; la comprobación honesta son la proporción pagada y el uso del cupo, que **no entraron al mapa**, y en ellas las zonas A y B se separan de C y D (proporción pagada 0,47 y 0,44 frente a 0,85 y 0,84).

### Punto adicional · Con y sin one-hot: el tipo de tarjeta como variable activa

#### Concepto

**One-hot encoding** convierte una variable categórica de $m$ niveles en $m$ columnas 0/1, con un único 1 por cliente. Problemas al meterla a un PCA:

- Las $m$ columnas suman siempre 1 → son **linealmente dependientes**, y la última componente guarda ≈ 0.
- Cada columna estandarizada aporta varianza 1, así que el tipo **pesa como $m$ variables**.
- Pierde el **orden** de una ordinal.

**Ponderación:** tras estandarizar, dividir cada una de las $m=5$ columnas por $\sqrt{5}$ hace que su varianza conjunta sea $5 \times (1/\sqrt5)^2 = 1$: el tipo pesa como **una** variable.

#### Por qué se hizo y en qué condición (versión final)

En la versión final se presenta como una prueba propia: «Probamos también qué pasa si el tipo de tarjeta entra al PCA como variable activa». Y se aclara que la comparación es **aparte** del mapa principal: los puntos 1 a 5 se hicieron con las 9 numéricas, porque si el tipo entrara como variable activa **dejaría de ser un grupo externo** que se compara con el mapa (punto 4), ya que ayudaría a construirlo.

#### Cómo lo aplicamos

```r
tipo_f <- factor(credit$Card_Type, levels = orden_tipo)
D <- model.matrix(~ tipo_f - 1)               # 5 columnas Card_Basic ... Card_Signature
stopifnot(all(rowSums(D) == 1), all(colSums(D) == as.vector(table(tipo_f))))
X_oh   <- cbind(X, D)                          # 9 numéricas (con log1p) + 5 dummies
pca_oh <- prcomp(X_oh, scale. = TRUE)          # con one-hot (14 columnas)
Z <- scale(X_oh); Z[, dum] <- Z[, dum] / sqrt(5)
pca_ob <- prcomp(Z, scale. = FALSE)            # con one-hot ponderado
```

- Comprobación (`stopifnot`): cada cliente tiene un solo 1 y los conteos coinciden con la tabla original. Ejemplo de las 6 primeras filas: Silver, Basic, Platinum, Silver, Gold, Gold.
- **Alineación de ejes** (`alinear`, entre las primeras 6 componentes): el eje de «tamaño» es la componente más correlacionada (en valor absoluto) con el cupo; el de «riesgo», la más correlacionada con el puntaje, excluyendo la de tamaño; signos fijados como arriba (más cupo a la derecha, peor puntaje arriba).
- Comparación: correlación de los ejes nuevos con los originales; **lista de seguimiento** = 20 % superior en el eje de riesgo y cuántos de la lista original se mantienen; cuántos de peor puntaje encuentra; precisión; tamaño de la zona A; $\eta^2$ del tipo en cada eje.
- **Bandera `estable`** (solo versión final): `estable <- cor_c2["con"] > 0.95 && mantienen["con"] >= 85`; una sola condición para todo el texto.
- **`comp_tipo` / `info_tipo`** (solo versión final): componentes del PCA con one-hot que tienen más del 50 % de su peso (suma de pesos al cuadrado de las 5 dummies) en el tipo, y cuánta información guardan juntas.
- Gráficos: barras de información de las 8 primeras componentes de cada versión; biplot del mapa con one-hot con las 14 variables (los cinco niveles en verde #2F855A); y mapas por tipo con elipses del 90 %, sin y con one-hot lado a lado (muestra de 12 000).

#### Resultados

Clientes por nivel:

| Nivel | Clientes | De cada 100 de la cartera |
|---|--:|--:|
| Basic | 10 261 | 20,5 |
| Silver | 12 056 | 24,1 |
| Gold | 16 895 | 33,8 |
| Platinum | 8 284 | 16,6 |
| Signature | 2 504 | 5,0 |

Información de cada versión:

| Versión | Columnas | Primera componente | Segunda | Las dos primeras | Componentes para pasar de 80 |
|---|--:|--:|--:|--:|--:|
| Sin one-hot | 9 | 64,3 | 11,7 | 76,0 | 3 |
| Con one-hot | 14 | 48,8 | 11,4 | 60,2 | 5 |
| Con one-hot ponderado | 14 | 59,9 | 10,5 | 70,4 | 4 |

La última componente guarda **0,0000** de cada 100 con one-hot y **0,0000** con el ponderado (la redundancia esperada de las dummies).

Qué componente hace de tamaño y de riesgo:

| Versión | Componente de tamaño | Componente de riesgo | Correlación con el tamaño original | Correlación con el riesgo original |
|---|---|---|--:|--:|
| Sin one-hot | C1 | C2 | 1 | 1,00 |
| Con one-hot | C1 | **C5** | 1 | 0,98 |
| Con one-hot ponderado | C1 | C2 | 1 | 1,00 |

Efecto sobre la decisión:

| Versión | De cada 100 de peor puntaje que encuentra | De cada 100 llamados que son de riesgo | De cada 100 de la lista original que se mantienen | Clientes en la zona A | De cada 100 de C1 que explica el tipo | De cada 100 de C2 que explica el tipo |
|---|--:|--:|--:|--:|--:|--:|
| Sin one-hot | 95,3 | 95,7 | 100,0 | 1 766 | 83,6 | 0,8 |
| Con one-hot | 92,0 | 92,4 | 89,6 | 2 174 | 88,3 | 1,2 |
| Con one-hot ponderado | 92,7 | 93,1 | 97,0 | 1 656 | 84,7 | 1,8 |

Dónde se concentra el tipo en el PCA con one-hot:

| Componente | De cada 100 de información | De cada 100 del peso en el tipo | Hace de |
|---|--:|--:|---|
| C1 | 48,8 | 16 | tamaño |
| C2 | 11,4 | 79 | |
| C3 | 9,6 | 96 | |
| C4 | 8,6 | 84 | |
| C5 | 7,4 | 1 | riesgo |

`comp_tipo` = C2, C3 y C4; `info_tipo` = **29,7** de cada 100 (cifra que solo existe en la versión final).

#### Lectura (versión final)

> 👀 **Qué vemos:** sin one-hot, la primera componente guarda 64,3 y las dos primeras 76,0. Con one-hot (14 columnas) pasan a 48,8 y 60,2, y con el tipo ponderado a 59,9 y 70,4. Para pasar de 80 hacen falta 3, 5 y 4 componentes. Con one-hot, el tamaño es C1 y el riesgo la C5; se parecen a los originales con correlación 1,00 y 0,98. La lista de seguimiento conserva 90 de cada 100 clientes y encuentra 92 de cada 100 de peor puntaje, contra 95 sin one-hot. El tipo explica 83,6 de C1 sin one-hot y 88,3 con él; en C2, 0,8 y 1,2. C2, C3 y C4 tienen más de la mitad de su peso en el tipo y guardan juntas 29,7 de cada 100.
>
> 💼 **Qué significa para el cliente:** el eje de riesgo casi no se mueve (0,98), pero la lista de seguimiento sí cambia en 10 de cada 100 clientes. Las componentes que se llenan con el tipo describen el tipo, no el riesgo, y por eso el riesgo se corre a la C5. El eje de tamaño también se conserva. Tres cuidados: **el one-hot no conoce el orden** (Basic < … < Signature se pierde: gana una flecha por nivel); **las cinco columnas son redundantes** (siempre suman 1, la última componente guarda 0,0000; es lo esperado, no un error); **sin ponderar, el tipo pesa como cinco variables**, por eso las cifras de información con y sin one-hot no se comparan una a una. El tipo **va con** la posición; no decimos que la cause.
>
> ✅ **Qué decide el cliente:** el mapa casi no cambia, así que no hace falta meter el tipo de tarjeta: la lista cambia en 10 de cada 100 y el eje de riesgo encuentra 92 de cada 100 de peor puntaje contra 95 sin one-hot. **Recomendación: quedarse con el mapa sin one-hot**: es más simple y el tipo ya se lee como grupo externo. Si la Gerencia quiere que el tipo intervenga en quién entra al seguimiento, **la versión ponderada es la más prudente**: conserva 97 de cada 100 clientes de la lista.

### Lo que le entregamos a la Gerencia (Taller II)

- **El mapa guarda 76,0 de cada 100 partes de la información de la ficha** y se lee con dos preguntas: qué tan a la derecha (tamaño) y qué tan arriba (riesgo).
- **Ingreso, cupo, saldo y monto pagado van juntas; el puntaje va solo.** La ficha puede acortarse a una variable de tamaño más el puntaje.
- **Los clientes forman un continuo, no grupos.** Los cortes son decisión de la Gerencia, no hallazgo del mapa.
- **El tipo de tarjeta se desplaza en tamaño (3,36 desviaciones entre Basic y Signature) pero casi no se desplaza en riesgo (0,18):** sirve para saber cuánto dinero hay en juego, no para escoger a quién llamar.
- **Con one-hot, el mapa casi no cambia:** el eje de riesgo se parece 0,98 al original, la lista de seguimiento conserva 90 de cada 100 clientes y el one-hot no recupera el orden Basic < Silver < Gold < Platinum < Signature.
- **La decisión:** dos cortes del 20 %, cuatro zonas. A recibe gestor senior y refinanciación (1 766 clientes), B una llamada estándar (8 234), C una oferta de aumento de cupo (8 234) y D nada (31 766).

### Diferencias entre la versión anterior y la versión final del Taller II

Las secciones 1 a 6 (encargo, mapa, biplot, continuo, tipo de tarjeta, cortes) son idénticas salvo una palabra; los cambios se concentran en la sección one-hot:

| Aspecto | Versión anterior (`taller_componentes_principales_II.Rmd`) | Versión final (`..._II_final.Rmd`) |
|---|---|---|
| Nombre de la zona C en el párrafo de lectura | «C (grande, **sin** riesgo)» | «C (grande, **no de** riesgo)», coherente con la tabla |
| Justificación del one-hot | «**El docente pidió** que el tipo de tarjeta entrara también al PCA» | «**Probamos también** qué pasa si el tipo de tarjeta entra al PCA como variable activa»: decisión metodológica propia |
| Alcance de la comparación | No se aclaraba | Párrafo nuevo: la comparación es **aparte**; los puntos 1–5 usan las 9 numéricas, porque meter el tipo lo convertiría de grupo externo en constructor del mapa |
| Criterio de estabilidad | Cada frase usaba su propio umbral: `cor_c2 > 0.95` para el 💼 y el resumen, `mantienen >= 90` para el ✅ | Una sola bandera `estable <- cor_c2["con"] > 0.95 && mantienen["con"] >= 85` para todo el texto |
| `comp_tipo` / `info_tipo` | No existían | Nuevas: C2, C3 y C4 tienen > 50 % del peso en el tipo y guardan 29,7 de cada 100; se citan en el 👀 |
| 💼 del one-hot | «el eje de riesgo casi no se mueve…: el tipo no cambia **a quién** ve la Gerencia como de riesgo» | «el eje de riesgo casi no se mueve (0,98), **pero la lista sí cambia en 10 de cada 100**…; el riesgo se corre a la C5» |
| ✅ / recomendación | Con `mantienen` = 89,6 < 90, la versión anterior habría impreso la rama «la lista de seguimiento **cambia bastante** (se conservan 90 de cada 100)… la Gerencia debe decidir…», que contradecía al 💼 («casi no se mueve») | Rama `estable` (0,98 > 0,95 y 89,6 ≥ 85): «el mapa casi no cambia… encuentra 92 de cada 100 contra 95… quedarse **sin one-hot**; si quiere que el tipo intervenga, la **ponderada es la más prudente** (conserva 97 de cada 100)» |
| Resumen final, viñeta one-hot | Condicionada a `cor_c2 > 0.95` | Condicionada a `estable` (mismo resultado: «casi no cambia») |

La reformulación corrige, por tanto, una incoherencia interna: con los mismos números, la versión anterior decía a la vez que el riesgo «casi no se mueve» y que la lista «cambia bastante». La salida concreta de la versión anterior no está renderizada en el repositorio; lo dicho sobre ella se deduce aplicando sus condiciones a las cifras reales.

---

## Taller de Análisis Factorial: Lo que las variables comparten

**Archivos:** `tallerAnalisisFactorial/taller_analisis_factorial.Rmd` (tejido a `taller_analisis_factorial.html`; hay también un `.zip`) y la guía `tallerAnalisisFactorial/explicacion_taller_analisis_factorial.md`. Subtítulo: «Análisis factorial para la Gerencia de Riesgo de Crédito». Mismos autores y curso. Paquetes: `psych`, `GPArotation` (para la rotación oblicua), `ggplot2` y `ggrepel` (se instalan si faltan).

**Enunciado:** el enunciado no está en el repositorio; las preguntas conceptuales se reconstruyen desde el `.Rmd` (hablan de «módulos» de una prueba —lectura, escritura— y de «habilidades», el ejemplo de clase; «la sesión 3» es la de PCA).

### El encargo y el enfoque

El taller continúa los dos de componentes principales (que a su vez parten, según este `.Rmd`, de los **Módulos 15 a 17** de `Entrega/analisis_synthetic_credit_card.Rmd`; los de PCA citaban el Módulo 11 como origen de las variables). La diferencia está en la pregunta:

- El **PCA** buscaba **el mejor resumen** de las variables (retener la mayor varianza total).
- El **análisis factorial** busca **lo que las variables comparten**: una «habilidad» común que no se mide directamente, y separa en cada variable la **parte común** (lo que viene de esa habilidad) de la **parte propia** (lo que la variable dice por su cuenta).

El **Módulo 18** del informe hace un análisis factorial más amplio (16 variables, sin el puntaje) y llega a lo mismo: detrás del dinero hay capacidad y frecuencia de uso, y el riesgo va aparte. Este taller responde con la ficha de la Gerencia y **con el puntaje adentro**.

**La pregunta de la Gerencia:**

> *«Mis analistas dicen que ingreso, cupo, saldo, pagos y número de compras son "lo mismo": la capacidad económica del cliente. ¿Es cierto que hay una sola capacidad detrás de todas? ¿Y el puntaje crediticio, también es parte de esa capacidad?»*

### Datos y variables

- Las **mismas 9 variables** de los talleres de PCA: ingreso anual, cupo, saldo facturado, monto pagado (dinero); compras al mes, valor por compra, compras a cuotas, compras internacionales (uso); y el **puntaje crediticio**, metido **a propósito** porque es lo que le importa a la Gerencia, para comprobar si comparte algo con las demás o va solo.
- Misma transformación: `log1p` a las de $|g_1|>1$; **6 entran con logaritmo** (ingreso anual, cupo, saldo facturado, monto pagado, valor por compra y compras internacionales). Las columnas se renombran en español.
- **No se estandariza a mano:** el análisis factorial trabaja sobre la matriz de correlaciones `R <- cor(X)`, lo que equivale a estandarizar.
- 50 000 clientes. La ruta del CSV se busca en `../data/bronze/…` y en `data/bronze/…`.

### Concepto: el modelo factorial de un factor

Con variables estandarizadas, el modelo de un factor dice que cada variable es

$$
x_i = \ell_i\,F + u_i, \qquad \operatorname{Var}(F)=1,\ \operatorname{Cov}(F,u_i)=0,\ \operatorname{Cov}(u_i,u_j)=0 .
$$

- **Carga** $\ell_i$: la correlación de la variable con la habilidad común.
- **Parte común (comunalidad)** $h_i^2 = \ell_i^2$: de cada 100 partes de las diferencias entre clientes en esa variable, cuántas vienen de la habilidad.
- **Parte propia (unicidad)** $u_i^2 = 1 - h_i^2$: lo que la variable mide y ninguna otra, más su error de medición.
- Implicación clave: $r_{ij} = \ell_i\ell_j$ para $i\ne j$; en forma matricial $\mathbf R \approx \mathbf L\mathbf L^\top + \boldsymbol\Psi$.
- Información total que reúne el factor: $\sum_i h_i^2 / p$.

Con $k$ factores: $\mathbf R \approx \mathbf L \boldsymbol\Phi \mathbf L^\top + \boldsymbol\Psi$, donde $\boldsymbol\Phi$ es la correlación entre factores (identidad si son ortogonales).

### Sección 1.2 · ¿Comparten lo suficiente? El KMO

#### Concepto

El índice **Kaiser-Meyer-Olkin** compara las correlaciones simples con las **parciales** (lo que queda entre dos variables descontando todas las demás). Las parciales salen de la inversa de $\mathbf R$: si $\mathbf R^{-1} = (r^{ij})$,

$$
p_{ij} = -\frac{r^{ij}}{\sqrt{r^{ii}r^{jj}}}, \qquad
\text{KMO}_j = \frac{\sum_{i\ne j} r_{ij}^2}{\sum_{i\ne j} r_{ij}^2 + \sum_{i\ne j} p_{ij}^2}, \qquad
\text{KMO} = \frac{\sum\sum_{i\ne j} r_{ij}^2}{\sum\sum_{i\ne j} r_{ij}^2 + \sum\sum_{i\ne j} p_{ij}^2}.
$$

Si lo que comparten dos variables también lo comparten con las demás, la parcial es pequeña y el KMO se acerca a 1. Por debajo de 0,5 la variable no comparte lo suficiente con el grupo.

#### Cómo lo aplicamos

`kmo <- KMO(R)` (paquete `psych`); clasificación con `cut` en (0, 0,5] inaceptable, (0,5, 0,6] miserable, (0,6, 0,7] mediocre, (0,7, 0,8] aceptable, (0,8, 0,9] meritorio, (0,9, 1] maravilloso.

#### Resultados

| Variable | KMO | Lectura |
|---|--:|---|
| Ingreso anual | 0,86 | meritorio |
| Cupo | 0,77 | aceptable |
| Saldo facturado | 0,66 | mediocre |
| Monto pagado | 0,65 | mediocre |
| Compras a cuotas | 0,92 | maravilloso |
| Compras al mes | 0,73 | aceptable |
| Valor por compra | 0,76 | aceptable |
| Compras internacionales | 0,92 | maravilloso |
| Puntaje crediticio | 0,02 | inaceptable |
| **KMO global** | **0,71** | aceptable |

#### Por qué el puntaje tiene KMO tan bajo

Se compararon sus correlaciones simples con las parciales (`P <- -cov2cor(solve(R))`) y se midió cuánto de él predicen las demás:

| Puntaje con… | Ingreso | Cupo | Saldo | Monto pagado | Cuotas | Compras/mes | Valor/compra | Internac. |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| Correlación simple | 0,02 | 0,03 | −0,17 | 0,11 | −0,03 | 0,02 | 0,02 | 0,05 |
| Correlación parcial | 0,04 | 0,52 | −0,94 | 0,91 | −0,15 | 0,24 | 0,25 | 0,11 |

- $R^2$ del puntaje con las otras 8 (correlación múltiple al cuadrado, `smc(R)`, $R^2_j = 1 - 1/r^{jj}$): **0,890**.
- $R^2$ de una regresión del puntaje sobre ingreso, cupo, compras al mes, valor por compra, cuotas e internacionales (es decir, **sin saldo ni pago**): **0,006**.

> 👀 **Qué vemos:** el KMO global es 0,71 (aceptable) y todas las variables pasan de 0,6 salvo el puntaje, con 0,02; por separado el puntaje casi no se correlaciona con nada (−0,17 a 0,11), pero descontando las demás va −0,94 con el saldo y 0,91 con el pago (y 0,52 con el cupo).
>
> 💼 **Qué significa para el cliente:** el puntaje no sigue al tamaño del cliente sino a la **diferencia entre lo que paga y lo que debe** (la proporción pagada, y el saldo frente al cupo): combinando pago, saldo y cupo, las otras variables predicen 89 de cada 100 del puntaje, y sin saldo ni pago apenas 0,6; un factor común no puede producir ese contraste, porque empuja a las variables en la misma dirección, y eso es lo que delata su KMO bajo.
>
> ✅ **Qué decide el cliente:** tiene sentido buscar una habilidad común en la ficha, y el puntaje se queda adentro para mostrar con números que no pertenece a ella.

**Decisión y por qué:** no se elimina el puntaje pese a su KMO inaceptable, porque la pregunta de la Gerencia es justamente si pertenece a la capacidad; dejarlo es la forma de responderla con números. (Precisión: la guía `explicacion_…md` dice «sin ellos [pago, saldo y cupo], menos de 1»; la regresión del `.Rmd` excluye solo saldo y pago y **sí incluye el cupo**.)

### Sección 2 · Una sola habilidad

#### Cómo lo aplicamos

```r
fa1 <- fa(R, nfactors = 1, fm = "ml", n.obs = nrow(X))   # máxima verosimilitud
carga1 <- fa1$loadings[, 1]
if (sum(carga1) < 0) carga1 <- -carga1                   # signo: más capacidad = positivo
```

Estimación por **máxima verosimilitud** (`fm = "ml"`), con `n.obs = 50 000`. Parte común $= 100\,\ell_i^2$; parte propia $= 100 \times$ `fa1$uniquenesses`. Gráfico de barras horizontales apiladas «Parte común y parte propia de cada variable (un factor)» (común en azul, propia en gris, línea de referencia en 50).

#### Resultados

| Variable | Carga $\ell_i$ | Parte común (de cada 100) | Parte propia (de cada 100) |
|---|--:|--:|--:|
| Cupo | 0,996 | 99,1 | 0,9 |
| Ingreso anual | 0,987 | 97,5 | 2,5 |
| Saldo facturado | 0,946 | 89,6 | 10,4 |
| Monto pagado | 0,886 | 78,5 | 21,5 |
| Valor por compra | 0,772 | 59,7 | 40,3 |
| Compras al mes | 0,676 | 45,7 | 54,3 |
| Compras a cuotas | 0,666 | 44,3 | 55,7 |
| Compras internacionales | 0,654 | 42,7 | 57,3 |
| Puntaje crediticio | 0,018 | 0,0 | 100,0 |

En total el factor reúne **61,9 de cada 100** partes de las 9 variables.

> 👀 **Qué vemos:** la habilidad común explica casi todo del cupo (99 de cada 100) y del ingreso (98), buena parte del saldo y del pago, y entre 43 y 60 de cada 100 de las de uso; en total reúne 61,9 de cada 100 partes de la ficha.
>
> 💼 **Qué significa para el cliente:** llamamos a esa habilidad **capacidad económica** (un nombre nuestro, leído de las cargas); los analistas tienen razón para el dinero, porque ingreso y cupo son casi pura capacidad, pero solo a medias para el uso, donde más de la mitad de lo que mueve cada variable es otra cosa.
>
> ✅ **Qué decide el cliente:** para medir capacidad le bastan ingreso y cupo, y las variables de uso conviene mirarlas aparte.

#### 2.1 · ¿Qué variable es casi toda propia?

`mas_propia <- partes$variable[which.max(partes$propia)]` → **Puntaje crediticio**: carga 0,018, parte común 0,0, parte propia 100,0.

> 👀 **Qué vemos:** el puntaje crediticio es 100,0 de cada 100 propio (carga 0,018), coherente con el KMO: no tiene nada en común con la capacidad.
>
> 💼 **Qué significa para el cliente:** **el riesgo no es parte de la capacidad económica**: saber cuánto gana, cuánto cupo tiene o cuánto compra un cliente predice apenas 0,6 de cada 100 de su puntaje; y esa parte propia **no es error de medición**, porque la combinación de pago, saldo y cupo predice 89 de cada 100.
>
> ✅ **Qué decide el cliente:** no puede usar la capacidad, ni el tipo de tarjeta (que se asigna por ingreso), como sustituto del riesgo, y el puntaje debe entrar **por su cuenta** a la decisión de seguimiento.

#### 2.2 · ¿Alcanza una habilidad?

**Concepto.** Si una sola habilidad explica lo que comparten las variables, cada correlación debe ser el producto de las cargas, $r_{ij}\approx \ell_i\ell_j$: dos variables se parecen solo porque las dos se parecen a la habilidad. La diferencia $r_{ij}-\ell_i\ell_j$ es el **residuo** del modelo.

**Cómo.** Se evaluaron los $\binom{9}{2}=36$ pares; se contaron los de diferencia absoluta < 0,05 y > 0,1; gráfico de dispersión «¿Una habilidad explica las correlaciones?» (eje x: producto de cargas; eje y: correlación observada; diagonal = la habilidad lo explica todo), con los pares de diferencia > 0,08 resaltados en rojo y etiquetados.

| Pares | Diferencia < 0,05 | Diferencia > 0,08 | Diferencia > 0,1 |
|--:|--:|--:|--:|
| 36 | 31 | 5 | 3 |

Los seis pares más lejanos:

| Par | Correlación | Producto de cargas | Diferencia |
|---|--:|--:|--:|
| Compras al mes – Valor por compra | 0,201 | 0,522 | −0,321 |
| Saldo facturado – Puntaje crediticio | −0,169 | 0,017 | −0,186 |
| Compras a cuotas – Compras al mes | 0,565 | 0,450 | 0,116 |
| Saldo facturado – Monto pagado | 0,933 | 0,839 | 0,095 |
| Monto pagado – Puntaje crediticio | 0,108 | 0,016 | 0,093 |
| Compras a cuotas – Puntaje crediticio | −0,028 | 0,012 | −0,040 |

> 👀 **Qué vemos:** 31 de los 36 pares quedan a menos de 0,05 de la diagonal y se apartan 5: el más lejano es **compras al mes – valor por compra** (la habilidad predice 0,52 y la correlación real es 0,20), seguido de **saldo** y **pago** con el **puntaje**, y de cuotas – compras al mes y saldo – pago.
>
> 💼 **Qué significa para el cliente:** una habilidad reproduce casi toda la ficha, y lo que no explica son dos cosas: **cómo se gasta** (a igual capacidad, muchas compras pequeñas o pocas grandes: la paradoja de Simpson del informe de entrega, que la guía ubica dentro de cada nivel de tarjeta) y que **el saldo baja el puntaje y el pago lo sube** más de lo que predice la capacidad, que es conducta de pago y no tamaño.
>
> ✅ **Qué decide el cliente:** una habilidad alcanza para casi toda la ficha pero no para todo, así que vale la pena probar con dos.

### Sección 3 · Dos habilidades

#### Concepto: rotación oblicua

Con dos factores la solución no es única (cualquier rotación reproduce igual $\mathbf R$). La rotación **oblimin** es **oblicua**: busca cargas simples y permite que los factores se correlacionen ($\boldsymbol\Phi \ne \mathbf I$).

#### Cómo lo aplicamos

```r
fa2 <- fa(R, nfactors = 2, fm = "ml", rotate = "oblimin", n.obs = nrow(X))
```

Se identifica como **capacidad** el factor que más carga en el cupo; se pone primero y con signo positivo; el segundo se orienta para que su carga dominante sea positiva; $\boldsymbol\Phi$ se reordena y se corrigen sus signos. Además se compara la reproducción de correlaciones: residuo $\mathbf E = \mathbf R - \hat{\mathbf R}$ (`modelo$model`) con diagonal anulada.

#### Resultados

| Variable | F1 capacidad | F2 segundo | Común con 1 factor | Común con 2 factores |
|---|--:|--:|--:|--:|
| Ingreso anual | 0,987 | 0,025 | 97,5 | 97,5 |
| Cupo | 0,994 | 0,026 | 99,1 | 98,9 |
| Saldo facturado | 0,952 | −0,170 | 89,6 | 93,7 |
| Monto pagado | 0,891 | 0,107 | 78,5 | 80,4 |
| Compras a cuotas | 0,666 | −0,028 | 44,3 | 44,5 |
| Compras al mes | 0,676 | 0,021 | 45,7 | 45,7 |
| Valor por compra | 0,773 | 0,022 | 59,7 | 59,8 |
| Compras internacionales | 0,652 | 0,047 | 42,7 | 42,7 |
| Puntaje crediticio | 0,003 | 0,998 | 0,0 | 99,5 |

Correlación entre factores: **−0,003**.

| Modelo | Mayor diferencia (residuo) | Par más lejano | De cada 100 común |
|---|--:|---|--:|
| Un factor | 0,321 | Valor por compra – Compras al mes | 61,9 |
| Dos factores | 0,322 | Valor por compra – Compras al mes | 73,6 |

> 👀 **Qué vemos:** la primera habilidad sigue siendo la capacidad, con las mismas cargas, y la segunda carga 0,998 en el **puntaje crediticio** (ninguna otra variable pasa de 0,3); las dos casi no se correlacionan (−0,003) y el par compras al mes – valor por compra sigue sin explicarse.
>
> 💼 **Qué significa para el cliente:** **la segunda no es una habilidad con sentido, es una sola variable**, el puntaje con otro nombre, y que su parte común pase de 0 a casi 100 solo quiere decir que el modelo le dio un factor para él solo.
>
> ✅ **Qué decide el cliente:** la respuesta no cambia, una capacidad común y el riesgo aparte, y llamar «riesgo financiero» al segundo factor sería inventar una habilidad donde hay una sola variable.

**Decisión y por qué:** el aumento de la parte común total (61,9 → 73,6) es engañoso: viene casi todo del puntaje (0 → 99,5), no de una estructura compartida, y el peor residuo no mejora (0,321 → 0,322).

#### 3.1 · ¿Y si sacamos el puntaje?

Como el puntaje se queda con el segundo factor, se retiró y se volvió a probar con dos sobre las 8 restantes (`R8 <- R[-9, -9]`, `fa(R8, nfactors = 2, fm = "ml", rotate = "oblimin")`), para ver si aparece lo que la capacidad no explicaba (cómo se gasta). Orientación: F1 = el factor que más carga en el cupo (positivo); F2 = el que más carga en compras al mes (positivo).

| Variable | F1 capacidad | F2 frecuencia |
|---|--:|--:|
| Ingreso anual | 0,919 | 0,143 |
| Cupo | 0,918 | 0,154 |
| Saldo facturado | 0,873 | 0,150 |
| Monto pagado | 0,818 | 0,141 |
| Compras a cuotas | 0,525 | 0,269 |
| Compras al mes | 0,187 | 0,903 |
| Valor por compra | 0,991 | −0,372 |
| Compras internacionales | 0,615 | 0,076 |

Correlación entre factores: **0,427**. (Las comunalidades y residuos de este modelo **no se reportan**.)

> 👀 **Qué vemos:** sin el puntaje, la segunda habilidad carga 0,90 en compras al mes y −0,37 en valor por compra (sube una y baja la otra), y esta vez las dos habilidades **sí se correlacionan** (0,43).
>
> 💼 **Qué significa para el cliente:** es **frecuencia frente a ticket** (a igual capacidad, hay quien compra mucho y barato y quien compra poco y caro); en estas ocho variables cuelga casi de una sola, compras al mes, pero el Módulo 18 del informe, con 16 variables, también la encuentra como un factor de frecuencia.
>
> ✅ **Qué decide el cliente:** la lista de seguimiento no cambia, y la frecuencia le sirve al área comercial para campañas por frecuencia o por ticket.

#### 3.2 · El factor frente al resumen del PCA

**Concepto.** La primera componente guarda $\lambda_1/p$ de la varianza total; el factor reúne $\sum_i h_i^2/p$. El PCA maximiza la varianza **total** (común + propia); el AF solo cuenta la **compartida**, así que el factor siempre guarda menos.

`lambda <- eigen(R)$values`:

| Método | De cada 100 |
|---|--:|
| PCA: primera componente | 64,3 |
| Análisis factorial: un factor | 61,9 |

> 👀 **Qué vemos:** la primera componente guarda 64,3 de cada 100 partes de las 9 variables y la habilidad común 61,9.
>
> 💼 **Qué significa para el cliente:** el PCA busca el resumen que más guarde y por eso se lleva también parte de lo propio de cada variable, mientras que el factor solo cuenta lo compartido y por eso guarda menos.
>
> ✅ **Qué decide el cliente:** para ordenar la cartera usa el mapa del PCA, y para explicar por qué ingreso, cupo y saldo se mueven juntos usa la capacidad del análisis factorial.

### Sección 4 · Preguntas conceptuales y sus respuestas

**1. ¿Qué diferencia hay entre la parte común y la parte propia de un módulo?**
La **parte común** es la porción de las diferencias entre personas en ese módulo que viene de la habilidad compartida con los demás: la carga al cuadrado. La **parte propia** es lo que queda: lo que el módulo mide y ningún otro mide, más su error de medición. Las dos suman 100 de cada 100. En la cartera, el cupo es **99** de cada 100 común (casi todo lo explica la capacidad) y el puntaje es **100** de cada 100 propio (no lo explica en absoluto).

**2. Escritura tiene 15 de cada 100 partes comunes. ¿Significa que el módulo de escritura está mal hecho? ¿Por qué?**
No. Significa que escritura **comparte poco** con los otros módulos, no que mida mal. Los otros 85 pueden ser una habilidad propia de escribir que los demás no miden —información valiosa que solo ese módulo aporta— y solo una parte será error. El análisis factorial no distingue esas dos cosas dentro de la parte propia; para saber si el módulo es confiable habría que medir su fiabilidad por otro camino (por ejemplo, repetir la prueba). Es lo mismo que el puntaje crediticio: 100 de cada 100 propio, y es la variable más útil de la ficha para la Gerencia. En su caso sí hay ese otro camino: la combinación de pago, saldo y cupo predice **89** de cada 100 del puntaje, así que su parte propia no es error.

**3. Si la correlación entre dos módulos es casi igual al producto de sus cargas, ¿qué nos dice eso sobre cuántas habilidades hay?**
Que **una habilidad alcanza** para explicar lo que esos dos módulos comparten: se parecen entre sí solo porque los dos se parecen a la misma habilidad, y no queda nada en común que necesite una segunda. Si pasa con todos los pares, hay una sola habilidad. En la cartera pasa con **31 de 36** pares; los que se apartan (compras al mes – valor por compra; saldo y pago con el puntaje) son los que piden mirar una segunda.

**4. La segunda habilidad cae casi entera sobre lectura. ¿Por qué no la llamamos «habilidad verbal»?**
Porque una habilidad es algo que **comparten varios módulos**, y esta la tiene uno solo. Un factor que carga en una única variable no es una habilidad nueva: es la parte propia de lectura a la que el modelo le dio un factor. Llamarla «verbal» afirmaría una capacidad que también se ve en otros módulos, y los datos no lo muestran; harían falta al menos dos o tres módulos (por ejemplo, lectura y escritura) cargando fuerte en ella. Es exactamente lo que pasó con el puntaje: el segundo factor es el puntaje solo (0,998), y por eso no se llamó «riesgo financiero».

**5. ¿Por qué el resumen de la sesión 3 guardaba más de cada 100 que la habilidad común de hoy?**
Porque la primera componente principal se construye para **guardar lo máximo posible** de las diferencias totales, sin importar si son comunes o propias: usa también parte de la parte propia de cada variable. La habilidad común solo cuenta lo que las variables **comparten** (la suma de las partes comunes) y deja fuera, por diseño, la parte propia. Por eso el factor siempre guarda menos. En los datos: **64,3** frente a **61,9** de cada 100.

**6. ¿Cuál de estas afirmaciones es correcta?**
La correcta es la **(b)**: *la carga al cuadrado es la parte de las diferencias en un módulo que viene de la habilidad común*. Las otras son falsas:

- **(a)** La habilidad común **no** se mide directamente: es una variable latente que se infiere de lo que los módulos comparten. Nadie les puso a los clientes una nota de «capacidad»; se dedujo de ingreso, cupo, saldo y compras.
- **(c)** La parte propia **no** es siempre error: incluye lo que el módulo mide y los demás no. El puntaje es 100 % propio y no es error: pago, saldo y cupo predicen 89 de cada 100 de él.
- **(d)** Dos habilidades **no** son siempre independientes: con una rotación oblicua (la que usa `fa()` por defecto) pueden correlacionarse. Sin el puntaje, capacidad y frecuencia se correlacionan **0,43**.

### Lo que le entregamos a la Gerencia (Análisis Factorial)

1. **Sí hay una capacidad económica común** detrás de la ficha: explica casi todo del ingreso y el cupo, buena parte del saldo y el pago, y cerca de la mitad de las variables de uso. Reúne **61,9 de cada 100** partes de las 9 variables.
2. **El puntaje crediticio no es parte de esa capacidad**: es 100 % parte propia y su KMO es **0,02**, porque no sigue al tamaño del cliente sino a la diferencia entre lo que paga y lo que debe. Medir el tamaño de un cliente no dice nada de qué tan buen pagador es.
3. **Una habilidad casi alcanza**: reproduce **31 de las 36** correlaciones. Lo que no explica tiene nombre: cómo se gasta (frecuencia frente a ticket) y la relación del puntaje con el saldo y el pago.
4. **La segunda habilidad no es una habilidad**: es el puntaje solo. La recomendación es la misma de los talleres de PCA, ahora desde otro método: la decisión de seguimiento necesita **dos cosas por separado**, la capacidad (cuánto pesa el cliente) y el puntaje (qué tan riesgoso es).

### Cómo encajan los tres talleres

| Taller | Pregunta | Respuesta numérica central | Mensaje común |
|---|---|---|---|
| PCA I | ¿Basta un número? | C1 guarda 64,3; deja escapar 7 957 de 10 046 clientes de puntaje bajo (79 de cada 100, como el azar) | Dos números: tamaño y puntaje/pago |
| PCA II | ¿Qué muestra el mapa y cómo se decide en él? | C1 + C2 = 76,0; continuo sin grupos; tipo de tarjeta explica 83,6 de C1 y 0,8 de C2; zonas A 1 766 / B 8 234 / C 8 234 / D 31 766 | Cortes del 20 %: A y B a seguimiento (95 de cada 100 de peor puntaje) |
| Análisis factorial | ¿Hay una sola capacidad? ¿El puntaje es parte de ella? | Un factor reúne 61,9; puntaje 100 % propio, KMO 0,02; 31 de 36 pares reproducidos | Capacidad y puntaje, por separado |


---

# Parte III — Taller del 31 de octubre, taller del 7 de noviembre y presentación

## Taller del 31 de octubre: resumen y dimensiones para su cliente

**Archivo fuente:** `taller31octubre/TALLER_31oct.Rmd` (tejido en `taller31octubre/TALLER_31oct.html`).
**Subtítulo del informe:** «Gerencia de Riesgo de Crédito · Componentes principales y análisis factorial».
**Autores:** Oscar Manuel Contreras Gacha (20221020052), Juan Pablo Sarmiento Ramírez (20221020138), Steven Navarro Parrales (20221020048) y Juan Diego Grajales Castillo (20221020128). Estadística Multidimensional · 26158 · grupo 020-81 · periodo 2026-3.

**Configuración técnica del documento.** Salida `html_document` con índice flotante (`toc_float`), secciones numeradas, tema `cosmo`, código plegable (`code_folding: show`) y tablas paginadas (`df_print: paged`). Paquetes: `psych` (se carga **antes** que `ggplot2` para que `ggplot2` conserve su función `alpha()`), `GPArotation` (necesario para la rotación oblimin), `ggrepel`, `dplyr`, `tidyr` y `ggplot2`, con `theme_minimal(base_size = 13)`. Se definen tres funciones de formato en español: `coma()` (decimales con coma y miles con espacio), `miles()` (entero con separador de miles) y `unir()` (arma frases del tipo «a, b y c» a partir de listas calculadas). Todos los números del texto son valores en línea de R (`r ...`), por lo que el informe se actualiza solo si cambian los datos.

**Convención de lectura.** Cada resultado se lee con tres frases:

- 👀 **Qué vemos**: el número o el gráfico, sin interpretar.
- 💼 **Qué significa para el cliente**: la traducción a la cartera de tarjetas.
- ✅ **Qué decide el cliente**: la consecuencia práctica.

### 1. El encargo

**El cliente es la Gerencia de Riesgo de Crédito del banco emisor** de las 50 000 tarjetas de la base (rupias indias, ₹). Cada mes **decide qué clientes entran al programa de seguimiento preventivo**: llamada del gestor, congelar los aumentos de cupo y ofrecer refinanciación antes de la mora. Hoy toma esa decisión con una ficha de **9 variables numéricas** por cliente.

La pregunta del taller tiene tres partes:

1. ¿Esa ficha se puede **resumir en pocos indicadores**?
2. ¿**Qué se pierde** al hacerlo?
3. ¿Hay **dimensiones** detrás de las variables que el cliente pueda interpretar y que sean **estables**?

#### Las variables y por qué esas

Las 9 variables son **las mismas durante todo el taller** y las mismas de los talleres anteriores. Responden lo que se pregunta un analista de riesgo: cuánto puede gastar, cuánto debe y paga, cómo usa la tarjeta y qué dice el buró.

| Variable en la base | Etiqueta en español | Bloque | Unidad |
|---|---|---|---|
| `Annual_Income` | Ingreso anual | Dinero | ₹ |
| `Credit_Limit` | Cupo | Dinero | ₹ |
| `Statement_Balance` | Saldo facturado | Dinero | ₹ |
| `Payment_Amount` | Monto pagado | Dinero | ₹ |
| `EMI_Count` | Compras a cuotas | Uso de la tarjeta | número |
| `Monthly_Transactions` | Compras al mes | Uso de la tarjeta | número |
| `Avg_Transaction_Value` | Valor por compra | Uso de la tarjeta | ₹ |
| `International_Transactions` | Compras internacionales | Uso de la tarjeta | número |
| `Credit_Score` | Puntaje crediticio | Puntaje | puntos |

**Variables suplementarias.** `Payment_Ratio` (proporción pagada) y `Credit_Utilization` (uso del cupo) **no entran al análisis**. No construyen ninguna componente ni dimensión; solo sirven para comprobar si los nombres propuestos tienen sentido. La decisión sigue la recomendación del análisis exploratorio: son cocientes de otras columnas (proporción pagada ≈ pago / saldo; uso del cupo ≈ saldo / cupo), y por eso volverían casi singular la matriz si entraran a la construcción.

**Identificador del cliente.** Para citar casos concretos, el código busca una columna de identificación (`Customer_ID`, `CustomerID`, `Customer_Id`, `customer_id`, `Client_ID`, `ID` o `Id`) y la copia en `id_cliente`. Si no la encontrara, usaría el número de fila. En esta base usa `Customer_ID` (códigos del tipo `CC1xxxxx`).

**Carga.** `read.csv()` de `data/bronze/synthetic_credit_card_customer_behavior_dataset.csv`; si no está, busca `../data/bronze/...`, y si tampoco la encuentra se detiene con el mensaje «No se encuentra el CSV: ajuste la ruta en este bloque».

### 2. Los datos que entran

#### 2.1 Qué casos entran y cuáles quedan por fuera

**Concepto.** Antes de cualquier análisis multivariado se audita la calidad de la base: celdas faltantes (`is.na`), filas completas (`complete.cases`), filas duplicadas (`duplicated`), identificadores repetidos y rangos imposibles según las reglas de negocio. La limpieza replica el Módulo 2 del primer corte (`Entrega/analisis_synthetic_credit_card.Rmd`).

**Cómo se aplicó.**

1. Se contaron las celdas vacías y las filas completas de toda la base.
2. Se buscaron filas idénticas en todas las columnas y `Customer_ID` repetidos.
3. Se revisaron los rangos de `Age`, `Payment_Ratio` y `Credit_Utilization`.
4. Para las 9 variables del taller, se contaron por separado las celdas vacías en el archivo (`NA` o texto vacío tras `trimws`). Luego cada variable se forzó a numérica con `as.numeric()`: lo que no fuera numérico quedaría como `NA`. También se contaron los valores negativos.
5. Se conservaron solo los casos completos en las 9 variables (`datos <- credit[completos, ]`).
6. Como verificación adicional, que **se reporta pero no elimina nada**, se contaron las filas idénticas en las 9 variables.

**Resultados.**

| Auditoría general | Valor |
|---|---|
| Celdas vacías | 0 |
| Filas completas | 50 000 |
| Filas duplicadas | 0 |
| `Customer_ID` repetidos | 0 |
| Columnas con algún `NA` | ninguna (`named numeric(0)`) |
| Rango de `Age` | 18 a 70 años |
| Rango de `Payment_Ratio` | 0,1 a 1,00 |
| Rango de `Credit_Utilization` | 0,1 a 0,95 |

| Concepto | Clientes |
|---|---|
| Casos iniciales | 50 000 |
| Casos con información completa en las 9 variables | 50 000 |
| Casos que quedan por fuera | 0 |

En las 9 variables hay 0 celdas vacías en el archivo, 0 valores no numéricos convertidos a vacío y 0 valores negativos. Hay 0 filas repetidas en las 9 variables.

- 👀 **Qué vemos:** la base trae 50 000 clientes, los 50 000 tienen las 9 variables completas y 0 quedan por fuera. **Ninguno se excluye**: no hay celdas vacías ni valores no numéricos en estas variables. La auditoría del primer corte tampoco encontró filas duplicadas (0), identificadores repetidos (0) ni valores imposibles. La edad va de 18 a 70 años, y la proporción pagada y el uso del cupo están entre 0 y 1.
- 💼 **Qué significa para el cliente:** el análisis habla de la cartera completa que la Gerencia tiene en la base (50 000 tarjetas).
- ✅ **Qué decide el cliente:** puede leer los resultados como válidos para esos 50 000 clientes; no hay casos escondidos.

#### 2.2 ¿Debemos estandarizar? Logaritmo y escala

**Concepto: asimetría y transformación log(x+1).** La asimetría muestral se calcula como

$$g_1 = \frac{1}{n}\sum_{i=1}^n\left(\frac{x_i-\bar x}{s}\right)^3 .$$

Si $|g_1| > 1$, la variable tiene cola larga: unos pocos clientes con montos muy altos. Es la regla del Módulo 11. En ese caso se aplica $\log(x+1)$ (`log1p`): comprime la cola y suma 1 para que los ceros no rompan el cálculo.

**Concepto: estandarizar en PCA.** Hacer el PCA sobre la matriz de covarianzas (`prcomp(X)`) deja que mande la variable con la mayor varianza en sus unidades. Hacerlo sobre la matriz de correlaciones (`prcomp(X, scale. = TRUE)`, con cada variable en $z = (x-\bar x)/s$) da a todas el mismo peso de partida.

**Cómo se aplicó.** Se calculó la asimetría de las 9 variables con la función propia `skew()` y se aplicó `log1p` a las que pasan el umbral. Después se compararon dos PCA: sin estandarizar (`pca_sin`, con log) y estandarizando (`pca`, la decisión). Las funciones auxiliares fueron `info_c1()`, que da el porcentaje de varianza de C1, y `manda()`, que da la variable de mayor peso absoluto en C1.

**Resultados (ordenados por desviación original):**

| Variable | Unidad | Asimetría | Entra con log | Desviación original | Desviación después del log |
|---|---|---|---|---|---|
| Ingreso anual | ₹ | 2,55 | sí | 1 407 257,48 | 0,80 |
| Cupo | ₹ | 3,01 | sí | 1 009 854,42 | 1,18 |
| Saldo facturado | ₹ | 3,80 | sí | 559 547,63 | 1,18 |
| Monto pagado | ₹ | 4,20 | sí | 453 396,64 | 1,27 |
| Valor por compra | ₹ | 3,90 | sí | 779,59 | 0,62 |
| Puntaje crediticio | puntos | −0,58 | no | 68,44 | 68,44 |
| Compras al mes | número | 0,54 | no | 42,05 | 42,05 |
| Compras internacionales | número | 2,11 | sí | 2,60 | 0,77 |
| Compras a cuotas | número | 0,17 | no | 1,67 | 1,67 |

Entran con logaritmo **6 variables** (ingreso, cupo, saldo, pago, valor por compra y compras internacionales). Las otras 3 (puntaje, compras al mes y compras a cuotas) entran tal cual.

| Versión | La C1 guarda de cada 100 | Variable que más pesa en C1 | Su peso |
|---|---|---|---|
| Sin estandarizar | 72,5 | Puntaje crediticio | 1,00 |
| Estandarizando | 64,3 | Cupo | 0,41 |

**Decisión: estandarizamos.** Las variables vienen en unidades que no se pueden comparar (rupias, conteos y puntos). En la escala original la desviación va de 1,67 a 1 407 257, y aun con el logaritmo va de 0,62 a 68,44.

- 👀 **Qué vemos:** sin estandarizar, la primera componente guarda 72,5 de cada 100 partes de la información, pero casi todo su peso está en el puntaje crediticio (peso 1,00). Estandarizando guarda 64,3 y ninguna variable manda sola.
- 💼 **Qué significa para el cliente:** si no se estandariza, el resumen copia a la variable de números más grandes, no a lo que distingue a los clientes. Como los montos ya entran en log, la variable de números más grandes es el puntaje crediticio (desviación de 68,44 puntos). El resultado sería ese puntaje presentado como resumen de toda la ficha.
- ✅ **Qué decide el cliente:** todo lo que sigue se hace con las variables en log (las 6 de cola larga) y estandarizadas, para que ninguna mande solo por tener números grandes.

### 3. ¿Se repiten? Correlaciones

**Concepto.** La correlación de Pearson $r = \operatorname{cov}(X,Y)/(s_X s_Y)$ mide cuánto se mueven juntas dos variables: 1 si siempre van juntas, 0 si no tienen nada que ver, −1 si van en contra. Si varias variables se correlacionan mucho, mirarlas todas no da más señales: repite la misma.

**Cómo se aplicó.** Se calculó `R <- cor(X)` sobre las variables ya en log. El mapa de calor ordena las variables con un agrupamiento jerárquico (`hclust(as.dist(1 - abs(R)))`). Está titulado «Qué tanto se mueven juntas las variables de la ficha» y usa una escala de naranja (−1) a blanco (0) a azul (1). Para cada variable se calculó su **mayor correlación absoluta con otra**. También se resumieron tres bloques de correlaciones: dinero con dinero, uso con uso y uso con dinero.

**Resultados.**

| Variable | Su mayor correlación con otra |
|---|---|
| Puntaje crediticio | 0,17 |
| Compras a cuotas | 0,66 |
| Compras internacionales | 0,66 |
| Compras al mes | 0,68 |
| Valor por compra | 0,78 |
| Monto pagado | 0,93 |
| Saldo facturado | 0,94 |
| Ingreso anual | 0,98 |
| Cupo | 0,98 |

- 👀 **Qué vemos:** ingreso, cupo, saldo facturado y monto pagado van muy juntas (correlaciones de 0,87 a 0,98). Las cuatro variables de uso de la tarjeta se parecen entre sí entre 0,20 y 0,57, y a las de dinero entre 0,58 y 0,78. La variable que va por su cuenta es el **puntaje crediticio**: con ninguna pasa de 0,17.
- 💼 **Qué significa para el cliente:** mirar ingreso, cupo, saldo y pago a la vez no le da cuatro señales sino una repetida: **el tamaño del cliente**. Las variables de uso lo acompañan en menor medida. El puntaje crediticio, que es lo que la Gerencia más mira para el riesgo, no se parece a ninguna: dice algo que el tamaño no dice. Por eso **sí tiene sentido resumir** el bloque de dinero y uso en pocos indicadores, y no tiene sentido meter el puntaje en ese mismo resumen sin revisar.
- ✅ **Qué decide el cliente:** puede acortar la ficha en el bloque de dinero (ingreso y cupo bastan para leer el tamaño), pero debe conservar el puntaje como variable aparte.

### 4. El resumen con componentes principales (PCA)

**Concepto.** El análisis de componentes principales busca combinaciones lineales $C_j = \mathbf{a}_j^\top \mathbf{z}$ de las variables estandarizadas. Cada una tiene varianza máxima y no se correlaciona con las anteriores. Los pesos $\mathbf{a}_j$ son los vectores propios de la matriz de correlaciones $R$, y la varianza de cada componente es su valor propio $\lambda_j$. La proporción de información que guarda la componente $j$ es

$$\frac{\lambda_j}{\sum_k \lambda_k}\times 100 \quad\text{(«de cada 100 partes»)} .$$

**Signo de los ejes.** `prcomp()` entrega cada componente con un signo arbitrario. El informe lo fija con una **variable ancla** por componente:

- **C1:** el cupo pesa positivo.
- **C2:** el puntaje pesa **negativo**, así que arriba significa peor puntaje.
- **C3:** el valor por compra pesa positivo.

Pesos y puntajes se multiplican por ese signo (`sweep`).

**El grupo de interés para la Gerencia («riesgo»).** Son los clientes con puntaje crediticio en el 20 % más bajo: `Credit_Score <= quantile(Credit_Score, 0.20)`. Son **10 046 clientes**; el umbral exacto del percentil 20 solo aparece en el subtítulo de un gráfico y en el texto **no se reporta**.

**Cuánto «encuentra» cada componente.** La función `encuentra()` responde: si la Gerencia escogiera el 20 % de clientes con el valor más alto de una componente, ¿cuántos de los 10 046 de riesgo caerían en la lista? Para darle a cada componente su mejor oportunidad, se prueban los dos extremos (la componente y su negativo) y se deja el que más encuentra. Al azar se encontraría el 20 % del grupo, unos 2 009.

#### 4.1 ¿Cuánta información conserva cada componente?

| Componente | De cada 100 | Acumulado |
|---|---|---|
| C1 | 64,3 | 64,3 |
| C2 | 11,7 | 76,0 |
| C3 | 9,3 | 85,3 |
| C4 | 6,3 | 91,6 |
| C5 | 5,0 | 96,6 |
| C6 | 2,2 | 98,8 |
| C7 | 0,9 | 99,8 |
| C8 | 0,2 | 99,9 |
| C9 | 0,1 | 100,0 |

El gráfico «De cada 100 partes de información de la ficha, cuántas guarda cada componente» muestra en barras azules las componentes conservadas (C1 y C2) y en una línea naranja el acumulado.

- 👀 **Qué vemos:** la primera componente guarda 64,3 de cada 100 partes de la información; con dos se llega a 76,0 y con tres a 85,3.
- 💼 **Qué significa para el cliente:** **conservamos dos componentes.** No es una regla de porcentaje sino del problema. La primera es el tamaño del cliente; la segunda concentra el puntaje y el hábito de pago, que es justo lo que el seguimiento necesita. Una tercera sumaría 9,3 partes y es de estilo de compra. Para encontrar a los 10 046 clientes de puntaje bajo, la primera componente encuentra 2 089, la segunda 9 571 y la tercera 2 329, frente a 2 009 al azar. La tercera, por tanto, no le ayuda a decidir.
- ✅ **Qué decide el cliente:** trabajar con dos números, tamaño y puntaje con hábito de pago, que guardan 76,0 de cada 100 partes de la ficha; ni con uno ni con nueve.

**Decisión de cuántas componentes y por qué.** No se usó la regla del 80 % acumulado: el código calcula `k80` (la primera componente que supera 80 es la C3), pero no se usa para decidir. Tampoco se usó el criterio de Kaiser. Se decidió por **utilidad para la pregunta del cliente**, es decir, por cuántos clientes de riesgo encuentra cada componente.

#### 4.2 ¿Qué representan las primeras componentes?

**Pesos (cargas de `prcomp`, con el signo fijado):**

| Variable | C1 | C2 | C3 |
|---|---|---|---|
| Ingreso anual | 0,40 | −0,02 | 0,04 |
| Cupo | 0,41 | −0,02 | 0,03 |
| Saldo facturado | 0,40 | 0,17 | 0,05 |
| Monto pagado | 0,38 | −0,10 | 0,02 |
| Compras a cuotas | 0,30 | 0,07 | −0,30 |
| Compras al mes | 0,29 | 0,01 | −0,72 |
| Valor por compra | 0,32 | −0,04 | 0,60 |
| Compras internacionales | 0,29 | −0,09 | 0,18 |
| Puntaje crediticio | 0,00 | −0,97 | −0,07 |

**Validación con las suplementarias.** Se calculó la correlación de los puntajes C1–C3 con las dos variables que no se usaron para construirlas:

| Componente | Proporción pagada | Uso del cupo |
|---|---|---|
| C1 | 0,06 | 0,11 |
| C2 | −0,76 | 0,59 |
| C3 | −0,06 | 0,07 |

- 👀 **Qué vemos:** a **C1** la mueven sobre todo el cupo (0,41), el ingreso anual (0,40), el saldo facturado (0,40) y el monto pagado (0,38). A **C2**, el puntaje crediticio (−0,97) y el saldo facturado (0,17); C2 se mueve −0,76 con la proporción pagada y 0,59 con el uso del cupo. A **C3**, las compras al mes (−0,72) y el valor por compra (0,60).
- 💼 **Qué significa para el cliente:** se proponen estos nombres, que **son nuestros y no un hallazgo de la estadística**:
  - **C1 · el tamaño del cliente:** los cuatro pesos de dinero van del mismo lado (de 0,38 a 0,41). Sube con todo lo que el cliente gana, tiene y mueve.
  - **C2 · puntaje y hábito de pago:** el puntaje pesa −0,97, y la componente se mueve −0,76 con la proporción pagada, una medida que no la construyó. Arriba quedan los clientes con peor puntaje y que pagan menos de lo facturado.
  - **C3 · estilo de compra:** enfrenta el valor por compra con las compras al mes: pocas compras caras frente a muchas pequeñas.

  El signo de cada eje lo fijamos nosotros, y que dos cosas se muevan juntas no quiere decir que una cause la otra.
- ✅ **Qué decide el cliente:** lo que la primera componente deja por fuera no es ruido sino el puntaje y el pago, así que no debe decidir el seguimiento mirando solo el tamaño.

#### 4.3 ¿Cuál es el costo de resumir en un solo número?

**Concepto.** Lo que C1 conserva de cada variable es $\operatorname{cor}(C_1, x_j)^2 \times 100$. El error de reconstruir a un cliente solo con C1 es

$$\lVert \mathbf z_i - \hat{\mathbf z}_i\rVert^2, \qquad \hat{\mathbf z}_i = c_{i1}\,\mathbf a_1 .$$

Dividido entre $\lVert\mathbf z_i\rVert^2$, da la fracción de lo que distingue al cliente que C1 no muestra (`sin_ver`).

**Qué conserva C1 de cada variable:**

| Variable | De cada 100 que C1 conserva |
|---|---|
| Cupo | 95,6 |
| Ingreso anual | 93,8 |
| Saldo facturado | 92,4 |
| Monto pagado | 84,3 |
| Valor por compra | 60,3 |
| Compras a cuotas | 53,4 |
| Compras internacionales | 49,8 |
| Compras al mes | 49,2 |
| Puntaje crediticio | 0,0 |

**Cobertura de los clientes de riesgo:**

| Decide con | Clientes de riesgo | Los encuentra | Se le escapan | De cada 100 se escapan |
|---|---|---|---|---|
| Solo C1 (tamaño) | 10 046 | 2 089 | 7 957 | 79,2 |
| C2 (puntaje y pago) | 10 046 | 9 571 | 475 | 4,7 |
| Al azar (referencia) | 10 046 | 2 009 | 8 037 | 80,0 |

El gráfico de barras apiladas se titula «Los 10 046 clientes de puntaje bajo: ¿los encuentra cada número?».

**Casos concretos 1: clientes que el índice de tamaño pondría entre los mejores (20 % más grande) pero que tienen puntaje bajo.** Son los cinco más «grandes», ordenados por C1:

| Cliente | Cupo (₹) | Puntaje | Proporción pagada | Uso del cupo | Posición en tamaño |
|---|---|---|---|---|---|
| CC109672 | 6 411 000 | 571 | 0,98 | 0,89 | entre el 0,0 % más grande |
| CC101216 | 5 728 000 | 556 | 0,87 | 0,94 | entre el 0,0 % más grande |
| CC127457 | 5 141 000 | 498 | 0,56 | 0,88 | entre el 0,0 % más grande |
| CC106849 | 4 875 000 | 471 | 0,49 | 0,94 | entre el 0,0 % más grande |
| CC128561 | 5 703 000 | 542 | 0,56 | 0,77 | entre el 0,1 % más grande |

**Casos concretos 2: los cinco clientes de toda la cartera peor representados por C1** (mayor error de reconstrucción):

| Cliente | Cupo (₹) | Puntaje | Proporción pagada | De cada 100 que C1 no muestra |
|---|---|---|---|---|
| CC142116 | 520 000 | 399 | 0,15 | 94 |
| CC109809 | 4 488 000 | 391 | 0,13 | 46 |
| CC142742 | 526 000 | 397 | 0,17 | 94 |
| CC132012 | 986 000 | 390 | 0,16 | 79 |
| CC135653 | 866 000 | 392 | 0,11 | 76 |

En promedio, C1 deja sin mostrar 62 de cada 100 partes de lo que distingue a un cliente de riesgo, frente a 51 en el resto.

- 👀 **Qué vemos:** con una sola componente se conserva 64,3 de cada 100 partes de la ficha. Por variable, C1 conserva 96 de cada 100 del cupo, pero solo 0 de cada 100 del puntaje. De los 10 046 clientes de puntaje bajo, la componente de tamaño encuentra 2 089 y deja escapar 7 957 (79 de cada 100), parecido a elegir al azar (2 009). Hay **1 845 clientes** que están a la vez entre el 20 % más grande y entre los de puntaje bajo. Los cinco de la primera tabla pagan entre 0,49 y 0,98 de lo facturado. Por promedio, 62 de cada 100 partes de lo que distingue a un cliente de puntaje bajo quedan fuera de C1, contra 51 en el resto.
- 💼 **Qué significa para el cliente:** con un solo número **conservaría el tamaño** (cuánto dinero hay en juego) y **perdería el puntaje y el hábito de pago**, que es lo que dice a quién llamar. Los clientes mal representados son justamente los **grandes con puntaje bajo**: el índice único los toma por los mejores clientes y por candidatos a más cupo, aunque pagan mucho menos de lo que se les factura.
- ✅ **Qué decide el cliente:** no usar un solo número para escoger a quién hacer seguimiento. La lista saldría casi tan mal como al azar y dejaría sin llamar a 79 de cada 100 clientes de puntaje bajo.

### 5. Los perfiles en el plano (biplot)

**Concepto: biplot.** El biplot muestra a la vez a los clientes como puntos (sus puntajes en C1 y C2) y a las variables como flechas. Aquí la flecha de cada variable tiene como coordenadas sus correlaciones con C1 y C2: `fl <- t(cor(sc[,1:2], X))`. En consecuencia:

- **Largo de la flecha.** $\sqrt{r_{C1}^2 + r_{C2}^2}$. Si llega a la circunferencia unitaria, la variable se ve entera en el mapa, y su cuadrado × 100 es la parte de la variable que se ve en el plano.
- **Ángulo entre flechas.** Cerca de 0° indica que las variables se mueven juntas; cerca de 90°, que casi no tienen que ver; cerca de 180°, que se mueven en contra.

**Cómo se aplicó.** Para que el gráfico sea liviano se dibujó una muestra de 6 000 puntos (`set.seed(2026)`). Los puntos se reescalaron con el factor 1,1 / percentil 99 de |C1, C2| para que quepan en el círculo. Las flechas se colorean por bloque: Dinero en azul, Uso en gris y Puntaje en naranja. Los ángulos entre flechas se calcularon con la función `ang()` (arcocoseno del producto punto normalizado).

**Resultados:**

| Variable | Bloque | Ángulo desde C1 (°) | Largo de la flecha | De cada 100 que se ve en el mapa |
|---|---|---|---|---|
| Ingreso anual | Dinero | −1 | 0,97 | 94 |
| Cupo | Dinero | −1 | 0,98 | 96 |
| Saldo facturado | Dinero | 10 | 0,98 | 95 |
| Monto pagado | Dinero | −6 | 0,92 | 85 |
| Compras a cuotas | Uso de la tarjeta | 6 | 0,73 | 54 |
| Compras al mes | Uso de la tarjeta | 1 | 0,70 | 49 |
| Valor por compra | Uso de la tarjeta | −3 | 0,78 | 60 |
| Compras internacionales | Uso de la tarjeta | −8 | 0,71 | 51 |
| Puntaje crediticio | Puntaje | −90 | 1,00 | 99 |

- 👀 **Variables:** las cuatro flechas de dinero forman ángulos de 0° a 17° entre sí, es decir, apuntan casi a lo mismo. El puntaje forma con ellas ángulos de 83° a 100°. La flecha más aislada es la del puntaje crediticio, a 82° de la más cercana. La pareja más abierta es puntaje crediticio con saldo facturado (100°). Todas las flechas llegan cerca de la circunferencia: ninguna mide menos de 0,7, aunque compras al mes queda justo en 0,70.
- 💼 **Qué significa para el cliente:** las variables de dinero cuentan casi la misma historia (el tamaño), y el puntaje apunta a otro lado. El riesgo no se lee en las variables de dinero y ninguna de ellas lo reemplaza.

**Casos en el plano.** Con `set.seed(2026)` se tomó un cliente al azar y su vecino más cercano por distancia euclidiana en (C1, C2). Además se calculó la **distancia de Mahalanobis** de cada cliente al centro del plano:

$$d_i^2 = (\mathbf c_i - \bar{\mathbf c})^\top S^{-1}(\mathbf c_i - \bar{\mathbf c}) .$$

Un cliente se marca como «alejado del comportamiento general» si $d_i^2 > \chi^2_{0{,}999;\,2}$.

| Caso | Cliente | Cupo (₹) | Saldo (₹) | Puntaje | Proporción pagada | Uso del cupo | C1 | C2 |
|---|---|---|---|---|---|---|---|---|
| Cliente cualquiera | CC136472 | 556 000 | 123 096 | 659 | 0,72 | 0,13 | 0,67 | −0,48 |
| Su vecino más cercano en el mapa | CC110768 | 463 000 | 219 518 | 666 | 0,96 | 0,36 | 0,66 | −0,47 |
| El más alejado del conjunto | CC106265 | 686 000 | 702 241 | 372 | 0,18 | 0,92 | 1,54 | 4,02 |

**Los cinco más alejados:**

| Orden | Cliente | Cupo (₹) | Saldo (₹) | Puntaje | Proporción pagada | Uso del cupo | C1 | C2 |
|---|---|---|---|---|---|---|---|---|
| 1.º | CC106265 | 686 000 | 702 241 | 372 | 0,18 | 0,92 | 1,54 | 4,02 |
| 2.º | CC118646 | 552 000 | 536 169 | 367 | 0,18 | 0,88 | 0,56 | 4,03 |
| 3.º | CC123061 | 6 335 000 | 5 053 556 | 404 | 0,15 | 0,71 | 5,40 | 3,32 |
| 4.º | CC142865 | 17 000 | 20 115 | 407 | 0,21 | 0,92 | −5,71 | 3,23 |
| 5.º | CC109809 | 4 488 000 | 4 543 151 | 391 | 0,13 | 0,93 | 4,86 | 3,47 |

Hay 22 clientes alejados del comportamiento general (0,04 de cada 100).

- 👀 **Qué vemos:** el cliente CC136472 y su vecino CC110768 están a 0,02 unidades en el mapa. Tienen cupos de 556 000 y 463 000 y puntajes de 659 y 666. Quedan 22 clientes (0,04 de cada 100) muy alejados del comportamiento general. El más alejado es el CC106265, con cupo de 686 000 y puntaje de 372.
- 💼 **Qué significa para el cliente:** los clientes cercanos en el mapa tienen una ficha parecida, y la Gerencia puede tratarlos de forma parecida. Los alejados son extremos (mucho dinero o un puntaje muy fuera de lo normal) y conviene mirarlos uno a uno, sin esperar que se parezcan a nadie.
- ✅ **Qué decide el cliente:** revisar a mano esa lista corta de extremos y usar la posición en el mapa para agrupar al resto.

#### 5.1 Un grupo que le importa al cliente: los grandes y de riesgo (grupo A)

**Cómo se definió.** El grupo A son los clientes con C1 ≥ percentil 80 de C1 **y** C2 ≥ percentil 80 de C2: el cuadrante de arriba a la derecha del mapa, grande y de riesgo. El gráfico usa una muestra de 15 000 clientes (`set.seed(2026)`) con el grupo A en naranja y los cortes en líneas discontinuas.

| Grupo | Clientes | De cada 100 de la cartera | Con puntaje bajo | Cupo promedio (₹) | Puntaje promedio | Proporción pagada | Uso del cupo | Saldo facturado (millones ₹) |
|---|---|---|---|---|---|---|---|---|
| A · grande y de riesgo | 1 766 | 3,5 | 1 704 | 2 074 561 | 524 | 0,47 | 0,63 | 2 497 |
| Resto de la cartera | 48 234 | 96,5 | 8 342 | 659 705 | 633 | 0,77 | 0,42 | 15 812 |

- 👀 **Qué vemos:** el grupo A reúne 1 766 clientes. Tienen un cupo promedio de 2 074 561 ₹ (resto: 659 705). Pagan 0,47 de lo facturado (resto: 0,77) y usan 0,63 del cupo (resto: 0,42). Concentran **14 de cada 100 ₹ facturadas** en toda la cartera.
- 💼 **Qué significa para el cliente:** son clientes **grandes que pagan poco de lo que deben**. El índice de tamaño los trataría como los mejores, pero cada llamada a este grupo protege mucho más dinero que una llamada al resto. La proporción pagada y el uso del cupo no entraron al mapa y aun así confirman que la zona es de riesgo. Esa confirmación es más honesta que mirar el puntaje, que sí ayudó a construir el eje. No se dice que ser grande cause un mal pago, solo que ambas cosas aparecen juntas.
- ✅ **Qué decide el cliente:** empezar el seguimiento preventivo por el grupo A (gestor dedicado, congelar aumentos de cupo y ofrecer refinanciación) y sumar a los de riesgo que no son grandes si la capacidad del equipo lo permite. **El corte del 20 % es una decisión de la Gerencia, no un borde que el mapa haya encontrado.**

### 6. Lo común y lo propio: análisis factorial con una dimensión

**Paso conceptual.** Se pasa del resumen (PCA: qué combinación **guarda más información**) al análisis factorial (AF: qué **comparten** las variables y qué conserva información **propia**). Se trabaja con las mismas 9 variables, en log donde corresponde y con nombres en español (`XE`).

**Concepto: modelo factorial.** Para variables estandarizadas, el modelo es

$$\mathbf z = \Lambda\,\mathbf f + \boldsymbol\varepsilon, \qquad R = \Lambda\Lambda^\top + \Psi .$$

$\Lambda$ son las **cargas**, $\mathbf f$ los factores comunes y $\Psi$ la diagonal de **unicidades**.

- **Carga.** Con un factor, la carga $\lambda_j$ es la correlación de la variable con la dimensión común.
- **Comunalidad (parte común).** $h_j^2 = \sum_k \lambda_{jk}^2$: de cada 100 partes de las diferencias entre clientes en esa variable, cuántas vienen de lo compartido.
- **Parte propia (unicidad).** $\psi_j = 1 - h_j^2$.
- **Común total.** $\sum_j h_j^2 / p \times 100$.

**Cómo se aplicó.** `fa(XE, nfactors = 1, fm = "ml")` del paquete `psych`, estimado por máxima verosimilitud. El signo es arbitrario: si la suma de cargas es negativa se invierte, de modo que más capacidad quede positivo.

| Variable | Carga | Parte común (de 100) | Parte propia (de 100) |
|---|---|---|---|
| Cupo | 0,996 | 99,1 | 0,9 |
| Ingreso anual | 0,987 | 97,5 | 2,5 |
| Saldo facturado | 0,946 | 89,6 | 10,4 |
| Monto pagado | 0,886 | 78,5 | 21,5 |
| Valor por compra | 0,772 | 59,7 | 40,3 |
| Compras al mes | 0,676 | 45,7 | 54,3 |
| Compras a cuotas | 0,666 | 44,3 | 55,7 |
| Compras internacionales | 0,654 | 42,7 | 57,3 |
| Puntaje crediticio | 0,018 | 0,0 | 100,0 |

#### 6.1 ¿Cuánto comparte cada variable?

El gráfico de barras apiladas «Parte común y parte propia de cada variable (una dimensión)» marca con una línea punteada el 50.

- 👀 **Qué vemos:** la dimensión común explica 99 de cada 100 partes del cupo, 98 del ingreso, 90 del saldo, 78 del pago, entre 43 y 60 de las variables de uso y solo 0 del puntaje. En total reúne **61,9 de cada 100** partes de la ficha.
- 💼 **Qué significa para el cliente:** lo que comparten las variables de dinero puede leerse como una **capacidad económica** común. Es un nombre nuestro, leído de las variables que más cargan; el modelo no la mide ni demuestra que exista como tal. En las variables de uso, buena parte de lo que dice cada una es propio, y en el puntaje casi todo lo es.
- ✅ **Qué decide el cliente:** para medir capacidad le bastan el ingreso y el cupo; las variables de uso y el puntaje debe mirarlos aparte.

#### 6.2 ¿Alcanza una sola dimensión?

**Concepto.** Si un solo factor explicara todo lo compartido, la correlación entre dos variables sería el **producto de sus cargas**: $\hat r_{jk} = \lambda_j\lambda_k$. El residuo de cada par es $r_{jk} - \hat r_{jk}$, y la raíz del error cuadrático medio de los residuos (RMSR) resume el ajuste.

**Cómo se aplicó.** Se compararon los 36 pares del triángulo superior. Se contaron los pares con diferencia menor de 0,05 y mayor de 0,10, y se calculó la RMSR. El gráfico enfrenta la correlación reproducida (eje x) con la observada (eje y) y marca en rojo los pares que se apartan más de 0,08.

| Resumen | Valor |
|---|---|
| Pares | 36 |
| Con diferencia menor a 0,05 | 31 |
| Con diferencia mayor a 0,10 | 3 |
| Raíz del error cuadrático medio | 0,070 |

**Los seis pares peor reproducidos:**

| Variable 1 | Variable 2 | Observada | Reproducida | Diferencia |
|---|---|---|---|---|
| Compras al mes | Valor por compra | 0,201 | 0,522 | −0,321 |
| Saldo facturado | Puntaje crediticio | −0,169 | 0,017 | −0,186 |
| Compras a cuotas | Compras al mes | 0,565 | 0,450 | 0,116 |
| Saldo facturado | Monto pagado | 0,933 | 0,839 | 0,095 |
| Monto pagado | Puntaje crediticio | 0,108 | 0,016 | 0,093 |
| Compras a cuotas | Puntaje crediticio | −0,028 | 0,012 | −0,040 |

- 👀 **Qué vemos:** 31 de los 36 pares quedan a menos de 0,05 de lo que reproduce el modelo, y 3 se apartan más de 0,10. El error promedio es 0,070. **El error más grande** está en **compras al mes – valor por compra**: la correlación observada es 0,20 y el modelo reproduce 0,52 (diferencia −0,32).
- 💼 **Qué significa para el cliente:** una sola dimensión reproduce bien la mayoría de las relaciones, pero no todas. Lo que falla está en los pares de la tabla: ahí las variables se parecen o se contraponen más de lo que explica la capacidad común, y eso es conducta (cómo se gasta, cómo se paga), no tamaño.
- ✅ **Qué decide el cliente:** usar la capacidad común para el bloque de dinero, sin suponer que lo explica todo. Conviene probar con dos dimensiones antes de dar la estructura por cerrada.

#### 6.3 ¿Qué variable conserva más información propia?

**Concepto.** La **correlación múltiple al cuadrado** (SMC, `psych::smc`) es el $R^2$ de predecir una variable con todas las demás, y sirve de cota inferior de su comunalidad. Una parte propia alta puede ser error de medición o información específica. Si las otras variables sí predicen a esa variable, su parte propia **no es solo ruido**.

**Cómo se aplicó.** Se identificó la variable de mayor parte propia y se calcularon dos $R^2$: con las otras 8 variables (`smc`), y sin saldo ni pago (regresión `lm` con ingreso, cupo y las cuatro de uso).

| Variable | Carga | Común | Propia |
|---|---|---|---|
| Puntaje crediticio | 0,018 | 0 | 100 |

| $R^2$ | Valor |
|---|---|
| Con las otras 8 | 0,890 |
| Sin saldo ni pago | 0,006 |

- 👀 **Qué vemos:** la variable con más información propia es el **puntaje crediticio**: 100,0 de cada 100 partes son propias (carga 0,018). Las otras ocho variables juntas predicen 89 de cada 100 partes de ella; sin saldo ni pago, apenas 0,6.
- 💼 **Qué significa para el cliente:** esta variable representa **qué tan buen pagador es el cliente y cómo lo ve el buró**, algo que el tamaño no dice. No debería desaparecer dentro de un indicador general. Su parte propia **no es solo error de medición**, porque saldo, pago y cupo combinados sí la predicen en buena parte.
- ✅ **Qué decide el cliente:** si resume la ficha en un índice de capacidad, ignorar esta variable cambiaría la lista de seguimiento: los grandes con puntaje bajo pasarían por buenos clientes. El puntaje debe entrar **por su cuenta** a la decisión.

### 7. ¿Dos dimensiones con nombre?

#### 7.1 ¿Cuántas dimensiones caben?

**Concepto: grados de libertad del modelo factorial.**

$$gl = \frac{(p-k)^2 - (p+k)}{2} \ge 0 .$$

Los grados de libertad son las relaciones entre variables que sobran después de estimar el modelo. Si son negativos, el modelo tendría más cosas por estimar que relaciones con las cuales estimarlas.

| Dimensiones | Grados de libertad | Variables por dimensión | ¿Se puede estimar? |
|---|---|---|---|
| 1 | 27 | 9,0 | sí |
| 2 | 19 | 4,5 | sí |
| 3 | 12 | 3,0 | sí |
| 4 | 6 | 2,2 | sí |
| 5 | 1 | 1,8 | sí |
| 6 | −3 | 1,5 | no |

- 👀 **Qué vemos:** con 9 variables se pueden estimar hasta 5 dimensiones. Con 2 sobran 19 grados de libertad y quedan 4,5 variables por dimensión.
- 💼 **Qué significa para el cliente:** que el modelo se pueda calcular no quiere decir que cada dimensión tenga sentido. Una dimensión necesita varias variables que carguen en ella, idealmente tres o más.
- ✅ **Qué decide el cliente:** dos dimensiones caben con estas variables, así que se estiman y después se juzga si son interpretables.

#### 7.2 Dos dimensiones (rotación oblimin)

**Concepto: rotación oblimin.** Es una rotación **oblicua**: reacomoda las dimensiones para que cada variable cargue sobre todo en una, y les permite estar correlacionadas entre sí, a diferencia de varimax, que las obliga a ser ortogonales. La matriz $\Phi$ da la correlación entre factores.

**Cómo se aplicó.** `fa(XE, nfactors = 2, fm = "ml", rotate = "oblimin")`. Se escribió la función propia `alinear_fa()`, que reordena y fija los signos para poder comparar soluciones:

- pone primero la dimensión que más carga en el cupo (la «capacidad») y con signo positivo;
- pone la segunda con signo positivo en su variable de mayor carga;
- ajusta $\Phi$ con el mismo orden y los mismos signos.

Una variable se asigna a una dimensión si su carga absoluta supera 0,30.

| Variable | F1 | F2 | Parte común con 2 dimensiones (de 100) |
|---|---|---|---|
| Ingreso anual | 0,987 | 0,025 | 97,5 |
| Cupo | 0,994 | 0,026 | 98,9 |
| Saldo facturado | 0,952 | −0,170 | 93,7 |
| Monto pagado | 0,891 | 0,107 | 80,4 |
| Compras a cuotas | 0,666 | −0,028 | 44,5 |
| Compras al mes | 0,676 | 0,021 | 45,7 |
| Valor por compra | 0,773 | 0,022 | 59,8 |
| Compras internacionales | 0,652 | 0,047 | 42,7 |
| Puntaje crediticio | 0,003 | 0,998 | 99,5 |

La correlación entre dimensiones ($\phi$) es −0,003.

- 👀 **Qué vemos:** la primera dimensión la forman el ingreso anual, el cupo, el saldo facturado, el monto pagado, las compras a cuotas, las compras al mes, el valor por compra y las compras internacionales (cargas de más de 0,3). La segunda la forma solo el puntaje crediticio. Las dos dimensiones se correlacionan −0,00.
- 💼 **Qué significa para el cliente:** la segunda dimensión **no es una dimensión con sentido**: es una sola variable (el puntaje crediticio) con otro nombre. Que su parte común suba (de 0,0 a 99,5) solo quiere decir que el modelo le dio una dimensión para ella sola. Una dimensión necesita al menos dos o tres variables que carguen en ella, y por eso **no se le pone nombre**. La primera sí tiene una lectura clara: **capacidad económica** (nombre nuestro, por las variables de dinero que cargan en ella). Las dos dimensiones casi no se relacionan, aunque la rotación oblimin les permitía hacerlo, así que aquí se pueden tratar como casi independientes.
- ✅ **Qué decide el cliente:** mantener la misma recomendación: una capacidad común y el puntaje por separado. Llamar «riesgo financiero» a la segunda dimensión sería inventar una dimensión donde hay una sola variable.

#### 7.3 ¿Son estables?

**Concepto: estabilidad y congruencia de Tucker.** Se repite el análisis cambiando **solo** el método de estimación, de `fm = "ml"` a `fm = "minres"` (residuos mínimos). La congruencia entre las columnas de cargas de los dos métodos es

$$\phi_{\text{cong}} = \frac{\sum_j \lambda^{(ml)}_j\lambda^{(mr)}_j}{\sqrt{\sum_j (\lambda^{(ml)}_j)^2\sum_j(\lambda^{(mr)}_j)^2}} .$$

Vale 1 si el patrón de cargas es idéntico y 0 si no se parecen en nada. Se declaró la estructura **estable** si se cumplen las tres condiciones: congruencia > 0,95 en ambas dimensiones, el 100 % de las variables sigue en la misma dimensión y la mayor diferencia de cargas es menor de 0,10.

| Variable | ml F1 | ml F2 | minres F1 | minres F2 |
|---|---|---|---|---|
| Ingreso anual | 0,987 | 0,025 | 0,982 | 0,029 |
| Cupo | 0,994 | 0,026 | 0,996 | 0,032 |
| Saldo facturado | 0,952 | −0,170 | 0,979 | −0,163 |
| Monto pagado | 0,891 | 0,107 | 0,910 | 0,099 |
| Compras a cuotas | 0,666 | −0,028 | 0,675 | −0,024 |
| Compras al mes | 0,676 | 0,021 | 0,644 | 0,014 |
| Valor por compra | 0,773 | 0,022 | 0,731 | 0,023 |
| Compras internacionales | 0,652 | 0,047 | 0,648 | 0,050 |
| Puntaje crediticio | 0,003 | 0,998 | 0,003 | 0,998 |

| Indicador | Valor |
|---|---|
| Correlación entre dimensiones (ml) | −0,003 |
| Correlación entre dimensiones (minres) | −0,005 |
| Congruencia F1 | 1,000 |
| Congruencia F2 | 1,000 |
| Mayor diferencia de cargas | 0,042 |
| Variables que siguen en la misma dimensión | 1,000 (100 %) |

El gráfico «Las cargas de las dos dimensiones con dos métodos de estimación» compara ml (azul) y minres (naranja) por dimensión.

- 👀 **Qué vemos:** 100 de cada 100 variables siguen en la misma dimensión. La mayor diferencia entre una carga y la otra es 0,042. La congruencia es 1,000 en la primera dimensión y 1,000 en la segunda, y la correlación entre ellas pasa de −0,00 a −0,00.
- 💼 **Qué significa para el cliente:** la estructura es **estable**: con otro método, las mismas variables forman las mismas dimensiones y los pesos principales se mantienen. La lectura de la primera dimensión como capacidad económica se sostiene. Eso sí, que la segunda dimensión sea estable no la convierte en una dimensión con sentido, porque sigue siendo una sola variable.
- ✅ **Qué decide el cliente:** puede apoyarse en la capacidad económica como dimensión estable y dejar el puntaje aparte.

### 8. La recomendación al cliente

1. **¿Puede resumir sus datos en un número? ¿Qué representaría?** Sí. La ficha se resume en un número que representa **el tamaño del cliente** (cuánto gana, tiene y mueve), pero ese número no basta para decidir a quién llamar.
2. **¿Cuánta información conserva y qué deja por fuera?** Un número conserva 64 de cada 100 partes de la ficha y deja por fuera **el puntaje y el hábito de pago**: con él se escapan 7 957 de los 10 046 clientes de puntaje bajo. Dos números conservan 76 de cada 100.
3. **¿Cuántas dimensiones parecen existir y qué debe analizar aparte?** Parece haber **una capacidad económica común** (62 de cada 100 partes de la ficha) y, por separado, el **puntaje crediticio**, con 100 de cada 100 partes propias. Las variables de uso conservan buena parte de información propia y conviene seguirlas viendo aparte. El par que peor explica una sola dimensión es compras al mes – valor por compra: a igual capacidad, unos compran mucho y barato, y otros poco y caro.
4. **¿Qué decisión recomendamos?** Reportar **dos números: el tamaño y el puntaje con hábito de pago**. Para el seguimiento preventivo, escoger primero al grupo de clientes grandes y de riesgo: 1 766 clientes que concentran 14 de cada 100 ₹ facturadas y pagan solo 0,47 de lo facturado. No escoger por tamaño, porque así se escaparían 79 de cada 100 clientes de puntaje bajo.

#### Qué no sabemos todavía

- **No sabemos por qué.** Todo lo que vemos son variables que aparecen juntas. No podemos decir que ser grande cause un mal pago, ni que la capacidad económica cause el puntaje. Los nombres de las componentes y de la dimensión son nuestros, no un hallazgo.
- **No sabemos qué pasará con clientes futuros.** El análisis describe a los 50 000 clientes de esta base en un momento dado. No predice quién caerá en mora ni qué pasará con clientes nuevos.
- **No sabemos si el puntaje bajo es mora.** «Riesgo» se definió como el 20 % de menor puntaje crediticio. La base no trae una variable de mora o incumplimiento con la cual verificarlo, y el corte del 20 % es una decisión nuestra.
- **No sabemos qué variables nos faltan.** Los resultados dependen de las 9 variables escogidas. Otras (historial de mora, producto contratado, canal de venta) podrían cambiar las dimensiones.
- **No sabemos si esto vale para otros bancos o carteras.** La base es sintética, y las conclusiones hablan de ella, no de la población de tarjetas de crédito en general.
- **La segunda dimensión no es una dimensión con sentido** (es una sola variable), y la estabilidad se comprobó solo cambiando el método de estimación, no con otras muestras.

#### Resumen de decisiones del taller del 31 de octubre

| Decisión | Por qué |
|---|---|
| Usar 9 variables fijas (las mismas de talleres previos) | Cubren capacidad, deuda, pago, uso y buró |
| Dejar `Payment_Ratio` y `Credit_Utilization` como suplementarias | Son cocientes derivados; sirven para validar los nombres sin contaminar la construcción |
| No excluir ningún caso | 0 faltantes, 0 duplicados, 0 valores imposibles |
| Aplicar log(x+1) a 6 variables | Asimetría absoluta mayor que 1 (regla del Módulo 11) |
| Estandarizar (PCA sobre correlaciones) | Sin estandarizar, la C1 es solo el puntaje (peso 1,00) |
| Fijar el signo de los ejes con variables ancla | Para que «arriba» en C2 signifique siempre peor puntaje |
| Conservar 2 componentes | La C2 encuentra 9 571 de 10 046 clientes de riesgo; la C3 solo 2 329, cerca del azar (2 009) |
| Definir «riesgo» como el 20 % de menor puntaje | No hay variable de mora en la base; el corte es una convención |
| Grupo A = 20 % superior en C1 y en C2 | Cuadrante de grandes y de riesgo, validado con las suplementarias |
| AF por máxima verosimilitud con 1 y luego 2 factores, rotación oblimin | Permite factores correlacionados; se comprueba si la 2.ª dimensión tiene sentido |
| No nombrar la 2.ª dimensión | Solo carga en ella una variable (el puntaje) |
| Probar la estabilidad con minres | Congruencia 1,000/1,000 y diferencia máxima de 0,042: estable |

---

## Taller del 7 de noviembre: ¿son distintos estos grupos? El informe para su cliente

**Archivo fuente:** `TALLER_7nov_CreditoIndia.Rmd` (tejido en `TALLER_7nov_CreditoIndia.html`; también empaquetado en `TALLER_7nov_CreditoIndia.zip`).
**Título del informe:** «Taller 2: ¿son distintos estos grupos? El informe para su cliente». Subtítulo: «Gerencia de Riesgo de Crédito · Hotelling de una y de dos muestras». Mismos cuatro autores, curso, grupo y periodo que el taller del 31 de octubre.

### Contexto: el enunciado y cómo se adaptó

El enunciado (`TALLER_Hotelling_7nov/TALLER_Hotelling_7nov.md`) es el «Taller 2 — ¿Son distintos estos grupos? El informe para su cliente». Es de la semana del sábado 7 de noviembre de 2026, sin clase en vivo, se hace por equipos sobre el dataset propio y se entrega como un `.Rmd` con su `.html` tejido. La entrega es el lunes 9 de noviembre de 2026 a las 11:59 p. m. en Moodle, con un envío por equipo. El profesor es Jhon Alejandro Varón Robayo (Universidad Distrital).

El enunciado parte de unas notas de clase (`Hotelling_Grupos_Distintos.html`) resueltas con otra base, de una secretaría de educación. De esas notas el informe de crédito toma tres referencias:

- **El Atlántico frente al país** (una muestra): 0,42 desviaciones, real y moderada, y no separa (31,5 de cada 100 estudiantes superan la mediana del país).
- **Hombres frente a mujeres** (dos muestras): mismo nivel y perfil distinto, D = 0,49, con un acierto de 61,8 contra 56,1 adivinando.
- **El estrato** como variable que «viaja» con el grupo, y **los dos estudiantes que sacaron 100 de global** con perfiles opuestos.

El informe de crédito cita estas referencias como analogías, pero **todo el análisis se hace sobre `synthetic_credit_card_customer_behavior_dataset.csv`**. La otra base del enunciado no se usa.

**Rúbrica del enunciado (sobre 5,0):**

| Criterio | Puntos |
|---|---|
| Encargo claro: cliente, dos comparaciones y la referencia justificada | 0,5 |
| Una muestra: diferencias, distancia, si es azar, y cuánto separa con un caso concreto | 1,2 |
| Dos muestras: nivel o perfil con dos casos, distancia comprobada con `manova()`, y acierto contra adivinar | 1,2 |
| Una variable que viaja con el grupo, revisada | 0,8 |
| Tabla de las tres preguntas y decisión para el cliente | 1,3 |

**Descuentos:** −0,5 por concluir solo con el valor p («es significativo, entonces son distintos»); −0,2 por cada resultado sin frase de lectura; −0,3 por afirmar que el grupo **causa** la diferencia. El enunciado pide entre 3 y 6 variables numéricas y tres frases por punto (qué ven, qué significa, qué decide).

**Cómo se mapeó el enunciado al caso de crédito:**

| Pide el enunciado | Se resolvió con |
|---|---|
| Una muestra: grupo frente a referencia (y decir de dónde sale) | Gama alta (Platinum + Signature) frente al **promedio de toda la cartera**, que sale de la misma base |
| Dos muestras: dos grupos entre sí | Tercio más joven (≤ 29 años) frente al tercio más viejo (≥ 40 años) |
| 3 a 6 variables | 6 variables: cupo, saldo facturado, monto pagado, compras al mes, valor por compra y puntaje |
| `hotelling_1()`, `hotelling_2()`, simulación opcional | Funciones copiadas «tal cual» de las notas, más una simulación de 1 000 grupos al azar |
| Comprobación con `manova()` | Wilks → T² |
| `MASS::lda()` contra adivinar el grupo mayor | Acierto con LDA (y con validación cruzada en dos muestras) |
| Variable que viaja | Compras internacionales con la gama alta |
| Tabla de tres preguntas (+ iris opcional) | Tabla con las dos comparaciones y setosa frente a versicolor |

### Configuración técnica

`html_document` con índice flotante, secciones numeradas, tema `cosmo`, código plegable y tablas paginadas. Paquetes: `ggplot2`, `dplyr`, `tidyr` y `MASS`. `MASS` se usa **siempre como `MASS::lda()`** y no se carga con `library()`, para no tapar `dplyr::select`.

**Funciones propias de formato y lectura:**

- `coma()`, `miles()`, `unir()` y `lista()` («ninguna» si la lista está vacía).
- `una_en(p)` traduce un valor p a lenguaje de cliente:
  - «menos de una en un millón» si $p < 10^{-6}$;
  - «una en N» si $p < 0{,}1$;
  - «alrededor de X de cada 100» en otro caso.
- `tam_D(D)` es una **convención propia para nombrar distancias**, no una ley de la estadística:

| D | Palabra |
|---|---|
| < 0,2 | pequeña |
| 0,2 a < 0,5 | moderada |
| 0,5 a < 1 | grande |
| 1 a < 2 | muy grande |
| ≥ 2 | enorme |

- `lee_D(D, sujeto, ref)` arma una frase según el tamaño. Por ejemplo, para «enorme»: «una distancia enorme entre promedios: … queda muy lejos de … (si eso alcanza para separar a cada cliente se ve más abajo)». La función corrige además «de el» → «del» y «a el» → «al».
- `veredicto_separa(acierto, base)` es una **convención propia para decir si un grupo «separa»**:
  - «sí» si el acierto es ≥ 85 % y mejora el de adivinar en ≥ 20 puntos;
  - «en parte» si el acierto es ≥ 70 % y la mejora ≥ 10 puntos;
  - «no» en otro caso.

**Las tres preguntas.** El informe responde siempre tres preguntas por comparación:

- **¿Es real?** ¿Puede ser azar?
- **¿Es grande?** ¿A cuántas desviaciones están los grupos?
- **¿Separa?** Si me dan a un cliente, ¿sé de qué grupo es?

Cada resultado se lee con las mismas tres frases del taller anterior (👀 / 💼 / ✅).

### 1. El encargo

**El cliente es la Gerencia de Riesgo de Crédito del banco emisor**, el mismo de los talleres anteriores. Para el comité de riesgos de fin de año escribe:

> «Vamos a presentar la segmentación de la cartera y necesitamos saber dos cosas. **Primera:** nuestros clientes de gama alta (tarjetas Platinum y Signature), ¿se comportan distinto del resto de la cartera? Si sí, les armamos una política propia de seguimiento y de aumentos de cupo; si no, les basta la política general. **Segunda:** vamos a diseñar campañas de seguimiento preventivo y de educación financiera por grupo de edad. ¿Los clientes jóvenes y los mayores llegan con perfiles distintos, o da igual?»

Son las dos comparaciones del taller:

- **Una muestra.** El grupo de **gama alta** (Platinum y Signature) frente a **la referencia: el promedio de toda la cartera**. La referencia sale de esta misma base (50 000 clientes sintéticos), no de una meta del banco ni de una cifra publicada, y el informe lo dice así. Además, el grupo hace parte de la referencia, igual que el Atlántico hacía parte del país en las notas.
- **Dos muestras.** Los **jóvenes** frente a los **mayores**: el tercio más joven y el tercio más viejo de la base por edad. El tercio del medio queda por fuera para que la comparación sea entre dos grupos claramente distintos en edad.

**Ningún grupo se define con las variables que se comparan.** La gama alta se define con el **tipo de tarjeta** y los grupos de edad con la **edad**, y ninguna de las dos entra entre las variables numéricas comparadas.

#### 1.1 Las variables: seis, y por qué esas

Hay una variable por cada pregunta del analista de riesgo:

| Variable | Nombre en la base | Pregunta que responde |
|---|---|---|
| Cupo | `Credit_Limit` | ¿Cuánto puede gastar? |
| Saldo facturado | `Statement_Balance` | ¿Cuánto debe? |
| Monto pagado | `Payment_Amount` | ¿Cuánto paga? |
| Compras al mes | `Monthly_Transactions` | ¿Con qué frecuencia usa la tarjeta? |
| Valor por compra | `Avg_Transaction_Value` | ¿De cuánto es cada compra? |
| Puntaje crediticio | `Credit_Score` | ¿Qué dice el buró? |

**Quedan fuera de la distancia:**

- **La edad**, porque define uno de los grupos.
- **El ingreso anual, las compras a cuotas y las compras internacionales.** Se guardan como «candidatas» para buscar en la sección 4 qué viaja con el grupo.
- **`Payment_Ratio` y `Credit_Utilization`**, porque son cocientes de variables que sí entran.

Respecto al taller del 31 de octubre, se pasa de 9 a 6 variables: salen el ingreso, las compras a cuotas y las compras internacionales, para respetar el máximo de 6 del enunciado y reservar candidatas para la sección 4.

#### 1.2 Los datos que entran

**Limpieza.** Las 6 variables, las 4 candidatas y `Card_Type` deben estar completas. Las variables numéricas se fuerzan con `as.numeric()` (lo no numérico pasa a `NA`) y `Card_Type` no puede estar vacía tras `trimws`.

| Concepto | Clientes |
|---|---|
| Clientes en la base | 50 000 |
| Con todo completo | 50 000 |
| Quedan por fuera | 0 |

**Transformación log(x+1).** Se usa la misma regla de los talleres anteriores: logaritmo si |asimetría| > 1.

| Variable | Asimetría | Entra con log |
|---|---|---|
| Cupo | 3,01 | sí |
| Saldo facturado | 3,80 | sí |
| Monto pagado | 4,20 | sí |
| Compras al mes | 0,54 | no |
| Valor por compra | 3,90 | sí |
| Puntaje crediticio | −0,58 | no |

Con las variables transformadas se arma la matriz `X`. La **referencia** es `mu <- colMeans(X)`, el promedio de la cartera, y `sd_base` es la desviación de cada variable en toda la cartera.

- 👀 **Qué vemos:** el cupo, el saldo facturado, el monto pagado y el valor por compra tienen cola larga (asimetría mayor que 1: unos pocos clientes con montos muy altos) y entran en logaritmo. Las compras al mes y el puntaje crediticio son casi simétricos y entran tal cual.
- 💼 **Qué significa para el cliente:** sin el logaritmo, los pocos clientes con montos enormes dominarían los promedios y las distancias. Con él, las diferencias se leen como diferencias «proporcionales» (en porcentaje) y no en rupias sueltas.
- ✅ **Qué decide el cliente:** leer las diferencias en montos como diferencias relativas. Los valores en rupias se muestran aparte, en las tablas en unidades originales.

**Grupos.** La gama alta se define con `tolower(trimws(Card_Type)) %in% c("platinum", "signature")`. Si la base no trajera esos niveles, el código imprime la tabla y se detiene. La edad se corta en sus terciles: `quantile(Age, c(1/3, 2/3))`, con jóvenes `Age <= q1` y mayores `Age >= q2`.

| Tarjeta | Clientes |
|---|---|
| Basic | 10 261 |
| Gold | 16 895 |
| Platinum | 8 284 |
| Signature | 2 504 |
| Silver | 12 056 |

| Comparación | Grupo | Regla | Clientes | Se compara con |
|---|---|---|---|---|
| 1 · una muestra | Gama alta (Platinum y Signature) | tarjeta Platinum o Signature | 10 788 | el promedio de toda la cartera |
| 2 · dos muestras | Jóvenes | edad de 29 años o menos | 17 505 | los mayores |
| 2 · dos muestras | Mayores | edad de 40 años o más | 17 624 | los jóvenes |

Quedan fuera de la comparación por edad 50 000 − 17 505 − 17 624 = 14 871 clientes de edad intermedia.

- 👀 **Qué vemos:** la base trae 50 000 clientes, los 50 000 tienen completas las variables usadas y 0 quedan por fuera. La gama alta reúne 10 788 clientes (21,6 de cada 100), los jóvenes 17 505 (hasta 29 años) y los mayores 17 624 (desde 40 años).
- 💼 **Qué significa para el cliente:** los resultados hablan de estos 50 000 clientes. Los grupos son lo bastante grandes para que casi cualquier diferencia salga «real», así que lo que importará es **cuánto** se diferencian y **si separan**.
- ✅ **Qué decide el cliente:** puede leer lo que sigue como válido para la cartera de la base, sin casos escondidos por datos faltantes.

> **Apunte del informe: por qué comparar variable por variable no alcanza.** El cupo, el saldo y el pago suben y bajan juntos. Si se hacen seis comparaciones sueltas, la misma diferencia se cuenta varias veces. La distancia $D$ es **una sola medida** que mira las seis variables al tiempo y descuenta que se mueven juntas. Es la distancia de Mahalanobis, pero aplicada al **promedio de un grupo**, no a un cliente.

### 2. Conceptos de la prueba T² de Hotelling

**Distancia D de Mahalanobis entre promedios.** Con una sola variable, la distancia es

$$D = \frac{\bar y - \mu_0}{s},$$

es decir, cuántas desviaciones separan los dos promedios. Con $p$ variables se descuenta la covarianza entre ellas:

$$D^2 = (\bar{\mathbf y} - \boldsymbol\mu_0)^\top S^{-1} (\bar{\mathbf y} - \boldsymbol\mu_0).$$

Una distancia de 1 es una desviación completa (mucho); una de 0,1 casi no se ve. **D compara promedios**: que el cliente típico esté lejos no dice que cada cliente lo esté. Eso lo responde la pregunta «¿separa?».

**T² de Hotelling de una muestra.** Generaliza la t de Student a varias variables. Contrasta $H_0: \boldsymbol\mu = \boldsymbol\mu_0$:

$$T^2 = n\,(\bar{\mathbf y}-\boldsymbol\mu_0)^\top S^{-1}(\bar{\mathbf y}-\boldsymbol\mu_0) = n D^2,
\qquad F = \frac{n-p}{p(n-1)}\,T^2 \sim F_{p,\;n-p}\ \text{bajo } H_0 .$$

El valor p es $P(F_{p,n-p} > F_{obs})$.

**T² de Hotelling de dos muestras.** Contrasta $H_0: \boldsymbol\mu_1 = \boldsymbol\mu_2$ con la covarianza combinada (*pooled*):

$$S_p = \frac{(n_1-1)S_1 + (n_2-1)S_2}{n_1+n_2-2},\qquad
D^2 = (\bar{\mathbf y}_1-\bar{\mathbf y}_2)^\top S_p^{-1}(\bar{\mathbf y}_1-\bar{\mathbf y}_2),$$

$$T^2 = \frac{n_1 n_2}{n_1+n_2}\,D^2,\qquad
F = \frac{n_1+n_2-p-1}{p\,(n_1+n_2-2)}\,T^2 \sim F_{p,\;n_1+n_2-p-1}.$$

**Supuesto de homogeneidad de covarianzas.** La prueba de dos muestras supone $\Sigma_1 = \Sigma_2$, y por eso puede promediar $S_1$ y $S_2$ en $S_p$. En la prueba de una muestra, `hotelling_1()` mide la distancia con la covarianza **del grupo** $S$, no con la de la referencia. Si el grupo varía distinto que la referencia, la distancia cambia según qué covarianza se use. El informe no aplica una prueba formal de homogeneidad (por ejemplo, la M de Box): **no se reporta**. En cambio, compara las desviaciones del grupo con las de la cartera y recalcula D con la covarianza de toda la cartera (ver 3.2).

**Comprobación con `manova()` y la lambda de Wilks.** Con dos grupos, el MANOVA de un factor equivale exactamente a la T² de dos muestras:

$$\Lambda = \frac{|W|}{|W+B|},\qquad T^2 = (n_1+n_2-2)\left(\frac{1}{\Lambda}-1\right).$$

**Acierto de clasificación frente a adivinar el grupo mayor.** El análisis discriminante lineal (`MASS::lda`) clasifica a cada cliente con las seis variables, y su acierto se compara con la **tasa base**: el porcentaje que se acertaría diciendo siempre el grupo más grande, $\max_g n_g / n$. Si el acierto no supera claramente esa base, los grupos no separan aunque sus promedios difieran. La **validación cruzada** (`CV = TRUE`, dejando uno fuera) mide el acierto sin «hacer trampa»: cada cliente se clasifica con un modelo que no lo vio.

**Diferencia de nivel frente a diferencia de perfil.** Si todas las variables que se apartan van en el mismo sentido, es una diferencia de **nivel**. Si unas suben y otras bajan, es de **perfil**.

**Variable que «viaja con el grupo» y diferencia ajustada por niveles.** Una variable viaja con el grupo cuando el grupo no es una muestra al azar de la cartera en esa variable, como el estrato con el Atlántico. Para ajustar, se divide la cartera en niveles de esa variable y se compara al grupo con la cartera **dentro de cada nivel**. Luego se promedian las diferencias, ponderadas por la fracción del grupo en cada nivel:

$$\mathbf d_{aj} = \sum_k \frac{n_{g,k}}{n_g}\,(\bar{\mathbf y}_{g,k} - \bar{\mathbf y}_{k}),\qquad
D_{aj} = \sqrt{\mathbf d_{aj}^\top S_g^{-1}\mathbf d_{aj}} .$$

**Funciones usadas «tal cual de las notas»:**

```r
hotelling_1 <- function(Y, mu) {
  n <- nrow(Y); p <- ncol(Y); dif <- colMeans(Y) - mu
  D2 <- as.numeric(t(dif) %*% solve(cov(Y)) %*% dif)
  T2 <- n * D2; F <- (n - p) / (p * (n - 1)) * T2
  c(n = n, D = sqrt(D2), T2 = T2, F = F, p = pf(F, p, n - p, lower.tail = FALSE))
}
hotelling_2 <- function(A, B) {
  n1 <- nrow(A); n2 <- nrow(B); p <- ncol(A)
  Sp <- ((n1 - 1) * cov(A) + (n2 - 1) * cov(B)) / (n1 + n2 - 2)
  dif <- colMeans(A) - colMeans(B)
  D2 <- as.numeric(t(dif) %*% solve(Sp) %*% dif)
  T2 <- n1 * n2 / (n1 + n2) * D2
  F  <- (n1 + n2 - p - 1) / (p * (n1 + n2 - 2)) * T2
  c(D = sqrt(D2), T2 = T2, F = F, p = pf(F, p, n1 + n2 - p - 1, lower.tail = FALSE))
}
```

### 3. Una muestra: ¿la gama alta es distinta de la cartera?

#### 3.1 Variable por variable

**Cómo se aplicó.** `dif1 = colMeans(Yg) − mu`, expresada en desviaciones de la cartera: `dif1_std = dif1 / sd_base`. La gráfica de barras se titula «Gama alta frente a la cartera: diferencia en cada variable», en azul las variables por encima y en naranja las por debajo. Una variable cuenta como «por encima» o «por debajo» si se aparta más de 0,05 desviaciones.

**Promedios en unidades originales:**

| | Cupo (₹) | Saldo facturado (₹) | Monto pagado (₹) | Compras al mes | Valor por compra (₹) | Puntaje |
|---|---|---|---|---|---|---|
| Gama alta | 2 072 148,1 | 1 039 084,4 | 791 807,1 | 117,8 | 1 659,1 | 634,9 |
| Cartera | 709 677,2 | 366 172,4 | 279 373,9 | 83,0 | 836,0 | 629,0 |

Las diferencias estandarizadas de cada variable solo aparecen en el gráfico. En el texto se reporta únicamente la mayor, la del cupo, de 1,29 desviaciones; las demás **no se reportan** numéricamente.

- 👀 **Qué vemos:** frente al promedio de la cartera, la gama alta queda por encima en cupo, saldo facturado, monto pagado, compras al mes, valor por compra y puntaje crediticio, y por debajo en ninguna. La diferencia más grande es la del cupo, a 1,29 desviaciones. En rupias, el cupo promedio de la gama alta es 2,9 veces el de la cartera (2 072 148 ₹ frente a 709 677 ₹) y el valor por compra 2,0 veces. El puntaje crediticio, en cambio, apenas se mueve (635 frente a 629 puntos).
- 💼 **Qué significa para el cliente:** es una **diferencia de nivel**: todas las variables que se apartan van en el mismo sentido, hacia arriba. Pero estas barras no son seis hallazgos independientes. El cupo, el saldo y el pago se relacionan (correlaciones de 0,88 a 0,94), así que una brecha en el cupo casi siempre va acompañada de brechas en las otras dos.
- ✅ **Qué decide el cliente:** no presentar seis barras sueltas al comité, sino pedir **una sola medida** de cuánto se aleja la gama alta de la cartera.

#### 3.2 ¿Es grande? La distancia D

**Cómo se aplicó.** `h1 <- hotelling_1(Yg, mu)` da D1 = **2,952**. Además:

- **Índice de parecido a la gama alta.** Es la dirección que mejor distingue al grupo: `w1 = solve(cov(Yg), dif1)` e `idx_ref = X %*% w1`. Da un número por cliente.
- **Percentil del cliente promedio de gama alta** en ese índice.
- **Razón de desviaciones** del grupo frente a la cartera, como chequeo informal de homogeneidad de varianzas.
- **D con la covarianza de toda la cartera**, `D1_cartera`.

**Razón entre la desviación de la gama alta y la de la cartera:**

| Cupo | Saldo facturado | Monto pagado | Compras al mes | Valor por compra | Puntaje |
|---|---|---|---|---|---|
| 0,54 | 0,65 | 0,69 | 0,84 | 1,08 | 1,00 |

| Distancia | Valor |
|---|---|
| D con la variación de la gama alta (`hotelling_1`) | 2,952 |
| D con la variación de la cartera | 1,306 |

- 👀 **Qué vemos:** el promedio de la gama alta está a 2,95 desviaciones del promedio de la cartera, contando las seis variables al tiempo. Si se ordena a toda la cartera por el «índice de parecido a la gama alta», el cliente promedio de gama alta queda por encima de 90 de cada 100 clientes. La gama alta varía menos que la cartera: en el cupo, su desviación es 0,54 veces la de la cartera. Como `hotelling_1()` mide con la variación del grupo, la distancia se ve más grande; medida con la variación de toda la cartera es 1,31.
- 💼 **Qué significa para el cliente:** es una distancia enorme entre promedios: el cliente típico de gama alta queda muy lejos del promedio de la cartera. Si eso alcanza para separar a cada cliente se ve más abajo. Aun con la medida más conservadora (1,31, muy grande), la gama alta se aparta con claridad.
- ✅ **Qué decide el cliente:** en el informe debe decir «la gama alta está entre 1,31 y 2,95 desviaciones de la cartera (muy grande a enorme)», no «es muy distinta» ni «es igual». Falta ver si eso separa a cada cliente.

**Decisión metodológica.** Se reportan **las dos D**: la del enunciado (covarianza del grupo) y la conservadora (covarianza de la cartera). La razón es que las covarianzas no son homogéneas: la gama alta es más compacta en los montos.

#### 3.3 ¿Es real? ¿O puede ser mala suerte?

**Cómo se aplicó.**

- **Simulación de permutación** (`set.seed(711)`): se sacaron 1 000 grupos al azar de la propia cartera, del mismo tamaño que la gama alta (10 788). A cada uno se le midió la misma distancia, con su propia covarianza.
- **Prueba exacta:** T² y F de `hotelling_1()`.

| Resultado de `hotelling_1()` | Valor |
|---|---|
| n | 10 788 |
| D | 2,952 |
| T² | 94 036,992 |
| F | 15 665,567 |
| p | 0,000 (menos de una en un millón) |
| Grados de libertad de F | 6 y 10 782 (p y n − p) |

| Simulación | Valor |
|---|---|
| Distancia típica por azar (mediana) | 0,020 |
| La mayor de 1 000 | 0,043 |
| La de la gama alta | 2,952 |

El histograma se titula «1 000 grupos al azar de 10 788 clientes: ¿qué tan lejos quedan de la cartera?» y marca con una línea naranja «Gama alta: 2,95».

- 👀 **Qué vemos:** un grupo de 10 788 clientes sacado al azar queda típicamente a 0,020 desviaciones, y el más lejano de los 1 000 quedó a 0,043. La gama alta está a 2,95. El cálculo exacto (T² de Hotelling, 94 037,0) da que la probabilidad de ver una distancia así por azar es **menos de una en un millón**.
- 💼 **Qué significa para el cliente:** la diferencia es real: la gama alta no se aparta de la cartera por mala suerte del grupo. La advertencia de «real pero pequeña» no aplica, porque se activa solo con D < 0,2.
- ✅ **Qué decide el cliente:** puede afirmar que la diferencia existe, y debe acompañarla siempre con su tamaño (D) para que nadie la lea como grande por el solo hecho de ser real.

#### 3.4 ¿Separa? ¿Cuántos clientes de gama alta caen del otro lado?

**Cómo se aplicó.**

1. **Del otro lado de la mediana.** En el índice de parecido, ¿qué parte de la gama alta queda por debajo de la mediana de la cartera? Si la gama alta fuera igual a la cartera, serían 50 de cada 100.
2. **Prueba de fuego.** `MASS::lda(X, grp1)` clasifica a cada cliente como «Gama alta» o «Resto», y se compara su acierto con decir siempre «Resto».
3. **Tabla de confusión.**
4. **Mezcla del resto.** El porcentaje del resto que supera el decil 10 de la gama alta en el índice.
5. **Casos concretos.** El cliente de gama alta con el índice más bajo, y el cliente del resto cuyo índice es el más cercano a la mediana de la gama alta.

| Del otro lado de la mediana | Valor |
|---|---|
| Clientes de gama alta por debajo de la mediana de la cartera | 0 |
| De cada 100 | 0,0 |

| Acierto | De cada 100 |
|---|---|
| Con las seis variables (LDA) | 90,5 |
| Diciendo siempre «resto» | 78,4 |

| Real \ Clasificado como | Resto | Gama alta |
|---|---|---|
| Resto | 38 506 | 706 |
| Gama alta | 4 033 | 6 755 |

| Indicador | De cada 100 |
|---|---|
| Gama alta clasificados como resto | 37,4 |
| Resto por encima del decil 10 de la gama alta | 6,7 |

**Casos concretos:**

| Cliente | Tarjeta | Cupo (₹) | Saldo (₹) | Pagado (₹) | Compras al mes | Valor por compra (₹) | Puntaje | % de la cartera con índice mayor |
|---|---|---|---|---|---|---|---|---|
| CC109918 | Platinum | 812 000 | 583 140 | 553 983 | 63 | 2 007 | 658 | 49,6 |
| CC133121 | Gold | 729 000 | 261 458 | 240 541 | 109 | 416 | 670 | 11,1 |

**Mediana de la cartera (referencia):**

| Cupo | Saldo facturado | Monto pagado | Compras al mes | Valor por compra | Puntaje |
|---|---|---|---|---|---|
| 396 000,0 | 192 358,4 | 136 639,8 | 76,0 | 617,2 | 638,0 |

- 👀 **Qué vemos:** 0 clientes de gama alta (0,0 de cada 100) quedan por debajo de la mediana de la cartera en el índice; en el Atlántico, 31,5 de cada 100 quedaban por encima. Pero eso solo dice que la gama alta está en la mitad de arriba, donde también vive la mitad del resto. Con las seis variables se acierta si un cliente es de gama alta o del resto en 90,5 de cada 100, y diciendo siempre «resto» se acierta en 78,4. El error se concentra en la gama alta: 37 de cada 100 de sus clientes quedan clasificados como «resto». Los dos casos lo muestran:
  - El cliente **CC109918** tiene tarjeta Platinum y un cupo de 812 000 ₹ (la mediana de la cartera es 396 000 ₹). Aun así, su índice es más bajo que el de 49,6 de cada 100 clientes de la cartera: está en la mitad, con ficha de cliente corriente.
  - El cliente **CC133121** tiene tarjeta Gold (no es de gama alta), pero su ficha es la del cliente típico de gama alta, con un cupo de 729 000 ₹.
- 💼 **Qué significa para el cliente:** la gama alta **se separa en parte** del resto. Sus clientes están en la mitad alta de la cartera, pero ahí se cruzan con clientes del resto que tienen la misma ficha: 6,7 de cada 100 clientes del resto superan al 10 % más bajo de la gama alta, y como el resto es mucho más numeroso, esa zona común pesa. Por eso la distancia enorme entre promedios no se traduce en grupos que no se tocan.
- ✅ **Qué decide el cliente:** puede usar reglas de segmento, revisando caso a caso a los que quedan en la zona común.

**Veredicto «¿separa?» con la convención propia.** El acierto es 90,5 (≥ 85) pero la mejora es 90,5 − 78,4 = 12,1 puntos (< 20), así que no llega a «sí». Cumple acierto ≥ 70 y mejora ≥ 10: queda en **«en parte»**.

### 4. Dos muestras: ¿los jóvenes y los mayores son distintos?

Se comparan los **jóvenes** (hasta 29 años) con los **mayores** (desde 40 años).

#### 4.1 Variable por variable: ¿nivel o perfil?

**Cómo se aplicó.** `A = X[joven,]` y `B = X[mayor,]`. Se calcula la covarianza combinada $S_p$ y la diferencia jóvenes − mayores en desviaciones de los clientes: `dif2 / sqrt(diag(Sp))`. La gráfica se titula «Jóvenes menos mayores, en cada variable», en morado si los jóvenes tienen más y en azul si los mayores tienen más.

**Promedios en unidades originales:**

| | Cupo (₹) | Saldo facturado (₹) | Monto pagado (₹) | Compras al mes | Valor por compra (₹) | Puntaje |
|---|---|---|---|---|---|---|
| Jóvenes | 718 093,7 | 369 132,0 | 281 909,1 | 83,4 | 838,1 | 629,2 |
| Mayores | 701 424,7 | 362 863,1 | 275 223,5 | 82,8 | 835,2 | 629,1 |

- 👀 **Qué vemos:** ninguna de las seis variables se aparta más de 0,05 desviaciones entre jóvenes y mayores. La diferencia más grande es la de compras al mes, de apenas 0,01 desviaciones (jóvenes menos mayores). En unidades originales pasa lo mismo: el cupo promedio es de 718 094 ₹ en los jóvenes y 701 425 ₹ en los mayores, y el puntaje de 629,2 frente a 629,1.
- 💼 **Qué significa para el cliente:** no es una diferencia de **nivel** (no todo sube en un grupo) ni de **perfil** (no hay variables que suban en uno y bajen en el otro). En las seis variables, jóvenes y mayores tienen en promedio la misma ficha.
- ✅ **Qué decide el cliente:** a simple vista no tiene razón para diseñar campañas distintas por edad. Falta comprobar con una sola medida que las seis diferencias juntas tampoco suman algo.

#### 4.2 ¿Qué tan lejos y qué tan real? Distancia D y comprobación con `manova()`

**Cómo se aplicó.** Se ejecutó `h2 <- hotelling_2(A, B)`. Como comprobación, se ajustó `summary(manova(XY ~ gr), test = "Wilks")` y se convirtió la lambda de Wilks en T² con $T^2 = (n-2)(1/\Lambda - 1)$.

| Resultado de `hotelling_2()` | Valor |
|---|---|
| D | 0,0259 |
| T² | 5,891 |
| F | 0,9818 |
| p | 0,4356 |
| Grados de libertad de F | 6 y 35 122 ($p$ y $n_1+n_2-p-1$, con $n_1+n_2 = 35\,129$) |

| Comprobación | T² |
|---|---|
| `hotelling_2()` | 5,89 |
| `manova()` (Wilks) | 5,89 |

El valor de la lambda de Wilks no se imprime: **no reportado**.

- 👀 **Qué vemos:** los dos grupos están a 0,03 desviaciones, y la probabilidad de que sea azar es de **alrededor de 44 de cada 100**. El T² de Hotelling (5,89) coincide con el que da `manova()` (5,89).
- 💼 **Qué significa para el cliente:** no se puede descartar el azar, y es una distancia pequeña: el joven típico se parece al mayor típico mucho más de lo que se diferencia.
- ✅ **Qué decide el cliente:** no debe hablar de perfiles distintos por edad con estas variables.

#### 4.3 Dos clientes con un resultado parecido y perfiles opuestos

Es el análogo de «los dos estudiantes que sacaron 100 de global» de las notas.

**Cómo se aplicó.**

1. **Índice general.** `nivel = rowMeans(scale(X))`: el promedio de las seis variables, cada una en desviaciones de toda la cartera.
2. **Variables extremas.** Se tomaron las dos variables con la diferencia de grupo más positiva y más negativa: **compras al mes** (`a_var`) y **puntaje crediticio** (`b_var`). La brecha de cada cliente es `Z[, a_var] − Z[, b_var]`.
3. **El joven.** Entre los jóvenes con |índice general| ≤ 0,25, se escogió el de mayor brecha.
4. **El mayor.** Entre los mayores con un índice general a no más de 0,05 del joven (con tolerancias de respaldo de 0,10 y 0,20), se escogió el de menor brecha.

El informe aclara que **la diferencia de grupo en esas dos variables es casi nula**. El caso **no** ilustra una brecha entre jóvenes y mayores, sino que dentro de cada grupo hay fichas opuestas con el mismo resultado general.

| Caso | Cliente | Edad | Cupo (₹) | Saldo (₹) | Pagado (₹) | Compras al mes | Valor por compra (₹) | Puntaje | Índice general |
|---|---|---|---|---|---|---|---|---|---|
| Joven | CC119444 | 28 | 699 000 | 684 339 | 75 277 | 168 | 557 | 401 | −0,06 |
| Mayor | CC134521 | 50 | 256 000 | 75 882 | 73 605 | 27 | 1 069 | 734 | −0,09 |

| En desviaciones frente a toda la cartera | Joven | Mayor |
|---|---|---|
| Compras al mes | 2,02 | −1,33 |
| Puntaje crediticio | −3,33 | 1,53 |

- 👀 **Qué vemos:** el cliente CC119444 (joven, 28 años) y el CC134521 (mayor, 50 años) tienen el mismo índice general (−0,06 y −0,09). En compras al mes el joven está en 2,02 y el mayor en −1,33; en puntaje crediticio, el joven está en −3,33 y el mayor en 1,53.
- 💼 **Qué significa para el cliente:** dos clientes que un resumen único vería como iguales tienen fichas opuestas y necesitan cosas distintas. Es el caso extremo, escogido a propósito: no dice cómo son la mayoría de los jóvenes y de los mayores. En promedio los dos grupos son iguales, y la misma pareja podría haberse encontrado con el joven y el mayor intercambiados.
- ✅ **Qué decide el cliente:** el seguimiento no se diseña con un índice general sino con el perfil, y cada cliente se mira por su propia ficha.

#### 4.4 ¿Separa? El acierto al clasificar, contra adivinar

**Cómo se aplicó.** Se ajustó `MASS::lda(grupo ~ ., data = datos_lda)` y se calcularon su acierto aparente, su acierto con validación cruzada (`CV = TRUE`) y la tasa base de decir siempre el grupo más grande.

| Acierto | De cada 100 |
|---|---|
| Con las seis variables | 50,4 |
| Con validación cruzada | 49,9 |
| Diciendo siempre el grupo más grande («Mayores») | 50,2 |

- 👀 **Qué vemos:** con las seis variables se acierta si un cliente es joven o mayor en 50,4 de cada 100 (49,9 con validación cruzada). Diciendo siempre el grupo más grande («Mayores») se acierta en 50,2, así que las seis variables mejoran el acierto en 0,2 puntos.
- 💼 **Qué significa para el cliente:** conocer las seis variables de un cliente no ayuda a saber si es joven o mayor: es lo mismo que lanzar una moneda. Cuadra con lo anterior: la diferencia no es real y los dos grupos se montan por completo.
- ✅ **Qué decide el cliente:** no diseñar campañas distintas por edad a partir de estas variables. El contenido de las campañas se define por el comportamiento de cada cliente (cupo, saldo, pago, uso y puntaje), no por su edad.

### 5. ¿Qué viaja con el grupo? La gama alta y las compras internacionales

> **Apunte del informe:** una variable «viaja con el grupo» cuando el grupo no es una muestra al azar de la cartera en esa variable. Entonces parte de la diferencia puede deberse a esa variable y no al grupo, como el estrato con el Atlántico en las notas. Se busca entre las variables que **no** entraron a la distancia y se comparan **clientes parecidos** en la que más viaja.

**Paso 1: buscar la candidata.** Para cada candidata (edad, ingreso anual, compras a cuotas y compras internacionales) se aplicó log(x+1) si su |asimetría| > 1. Luego se calculó (promedio de la gama alta − promedio de la cartera) / desviación de la cartera.

| Variable | Gama alta − cartera (desviaciones) |
|---|---|
| Compras internacionales | 1,47 |
| Ingreso anual | 1,21 |
| Compras a cuotas | 0,76 |
| Edad | −0,02 |

- 👀 **Qué vemos:** de las variables que quedaron fuera de la distancia, la que más se aparta en la gama alta es **compras internacionales**, a 1,47 desviaciones de la cartera. La que menos, la edad (−0,02).
- 💼 **Qué significa para el cliente:** la gama alta no es una muestra al azar de la cartera en compras internacionales: quien tiene tarjeta de gama alta suele tener también más compras internacionales, así que parte de su diferencia puede ir con esa variable. Ojo: a diferencia del estrato en las notas, las compras internacionales son un comportamiento con la tarjeta, no algo que el cliente traía antes. Con estos datos no se sabe si van con el tipo de tarjeta o con quién la pide.
- ✅ **Qué decide el cliente:** antes de armar una política «para la gama alta», revisar si la diferencia se mantiene entre clientes parecidos en compras internacionales.

**Decisión: por qué se ajusta por compras internacionales y no por el ingreso.** La regla del código es tomar la candidata que más se aparta (`which.max(abs(d_cand))`). Compras internacionales (1,47) supera al ingreso anual (1,21).

**Paso 2: niveles y diferencia ajustada.** La cartera se dividió en niveles de compras internacionales (en log):

- Si la variable tiene 6 valores distintos o menos, cada valor es un nivel.
- Si no, se intentan tercios con `quantile(c(0, 1/3, 2/3, 1))`. Si muchos clientes tienen el mismo valor, los cortes se repiten y quedan menos niveles.

Aquí quedaron **dos niveles** («bajo» y «alto»). Dentro de cada nivel se aplicó `hotelling_1()` a la gama alta frente al promedio de la cartera de ese nivel, siempre que hubiera más de $5p = 30$ clientes de gama alta en él. Después se calculó la diferencia ajustada, ponderada por la fracción de la gama alta en cada nivel, y su D con la covarianza de toda la gama alta.

| Nivel | Rango de compras internacionales | Clientes de gama alta | De cada 100 de la gama alta | De cada 100 de la cartera | D dentro del nivel | Probabilidad de azar |
|---|---|---|---|---|---|---|
| bajo | 0 a 1 | 1 006 | 9,3 | 69,8 | 4,70 | menos de una en un millón |
| alto | 2 a 14 | 9 782 | 90,7 | 30,2 | 0,86 | menos de una en un millón |

| Distancia | Valor |
|---|---|
| D sin ajustar | 2,952 |
| D entre clientes parecidos | 1,115 |

El gráfico «¿Sigue la diferencia cuando se comparan clientes parecidos?» compara, por variable, la barra «Sin ajustar» (gris) con «Entre clientes con compras internacionales parecido» (azul). Las cifras por variable de ese gráfico **no se reportan** en el texto.

**Clasificación del cambio según las reglas del código:**

| Condición | Lectura |
|---|---|
| D_aj > 1,1 · D | la diferencia crece |
| D_aj ≥ 0,75 · D | casi no cambia |
| D_aj ≥ 0,25 · D | parte de la diferencia viaja con la variable |
| D_aj < 0,25 · D | casi toda la diferencia viaja con la variable |

Aquí 1,115 / 2,952 ≈ 0,38, así que la lectura es «**parte**».

- 👀 **Qué vemos:** en el nivel más alto de compras internacionales está el 91 de cada 100 de la gama alta y el 30 de la cartera. Al comparar dentro del mismo nivel, la distancia pasa de 2,95 a 1,11 desviaciones.
- 💼 **Qué significa para el cliente:** **parte** de la diferencia viaja con las compras internacionales (la distancia baja de 2,95 a 1,11, 62 de cada 100 menos), pero no toda. Esto no demuestra que las compras internacionales sean la causa, solo que la gama alta y esa variable aparecen juntas.
- ✅ **Qué decide el cliente:** no puede atribuir la diferencia solo a la tarjeta ni solo a las compras internacionales. Una política para la gama alta debe revisar las dos cosas.

**Detalle de la tabla.** Dentro del nivel bajo, los pocos clientes de gama alta (1 006) quedan **más lejos** de su nivel (D = 4,70) que la gama alta en conjunto (2,95). En el nivel alto, donde está el 90,7 % de la gama alta, la distancia es menor (0,86). El informe no comenta este contraste por separado.

### 6. Las tres preguntas y la decisión

**Comparación con iris.** Es la regla de comparación de las notas: dos especies que no se tocan. Se tomó `iris` sin virginica, se aplicó `hotelling_2(versicolor, setosa)` sobre sus 4 medidas y se clasificó con `MASS::lda`. Para el «adivinar» de iris se usó 50 (dos grupos de igual tamaño).

| Comparación | ¿Es real? | ¿Es grande? (D) | ¿Separa? |
|---|---|---|---|
| Gama alta frente a la cartera (una muestra) | sí · azar: menos de una en un millón | 2,95 · enorme | en parte · acierta 91 de cada 100; adivinando, 78 |
| Jóvenes frente a mayores (dos muestras) | no · azar: alrededor de 44 de cada 100 | 0,03 · pequeña | no · acierta 50 de cada 100; adivinando, 50 |
| Setosa frente a versicolor (iris, referencia) | sí · azar: menos de una en un millón | 10,16 · enorme | sí · acierta 100 de cada 100; adivinando, 50 |

Los valores de T², F y p de iris no se imprimen: **no reportados**, salvo D = 10,16 y el acierto de 100.

**Qué aporta la comparación con iris.** Muestra cómo se ve una diferencia que **sí separa**: D ≈ 10 y un acierto de 100 contra 50. La gama alta tiene una D «enorme» según la convención (≥ 2), pero queda muy por debajo de iris y solo separa «en parte». Los jóvenes y los mayores están en el otro extremo. La tabla deja ver que **«enorme y real» no implica «separa»**.

**Decisión para el cliente** (texto final del informe):

> La gama alta está a 2,95 desviaciones de la cartera (enorme; 1,31 medida con la variación de toda la cartera) y los jóvenes a 0,03 de los mayores (pequeña). La referencia de una diferencia que sí separa es la de iris, a 10,2 desviaciones y con 100 de cada 100 aciertos. **Gama alta:** la gama alta se separa en parte del resto; eso justifica reglas de segmento propias (alertas y aumentos de cupo), revisando caso a caso a los de la zona común. Parte de la diferencia viaja con las compras internacionales (comparando clientes parecidos, la distancia baja de 2,95 a 1,11), así que la política debe mirar las dos cosas. **Edad:** no hay evidencia de perfiles distintos por edad, así que no se justifica diseñar campañas separadas. En el informe al comité no basta con decir que las diferencias son «significativas»: van siempre las tres respuestas (¿es real?, ¿es grande?, ¿separa?) y lo que se decide con ellas.

**Lógica del árbol de decisión programado** (`dec1`, `dec2`, `dec_viaja`):

- **Gama alta.**
  1. Si no es real → política general.
  2. Si D < 0,2 → la política general basta.
  3. Si no separa → ajustar metas y alertas del segmento como un todo.
  4. Si separa «en parte» → reglas de segmento propias, con revisión caso a caso. **Esta es la rama que salió.**
  5. Si separa «sí» → política propia.
- **Edad.** Si no es real → no se justifican campañas separadas. **Esta es la rama que salió.**
- **Viaja.** Si D_aj ≥ 0,75·D, la diferencia no se explica por la variable. Si no, «parte de la diferencia viaja…». **Salió la segunda opción.**

#### Qué no sabemos todavía

- **No sabemos por qué.** Todo lo que vemos son grupos que se comportan distinto. No decimos que tener tarjeta de gama alta, o tener cierta edad, cause un cupo, un pago o un puntaje: que algo viaje con el grupo no significa que lo cause.
- **La referencia sale de esta misma base.** El promedio de la cartera no es una meta del banco ni una cifra publicada, y el grupo hace parte de él. La base es sintética y sus conclusiones hablan de ella, no de todas las carteras de tarjetas.
- **Los umbrales son nuestros.** Llamar «moderada» a una distancia entre 0,2 y 0,5, o decir que un grupo «separa» cuando se acierta en 85 de cada 100 y se mejora en 20 puntos el adivinar, es una convención para hablar con el cliente, no un resultado de la estadística.
- **El acierto no es mora.** Clasificar a un cliente por su ficha dice si se parece a un grupo, no si va a pagar. La base no trae una variable de incumplimiento con la cual verificarlo.
- **La edad es delicada.** Aquí se usa para diseñar mensajes y prever demanda. Si la política interna o la regulación del banco permiten usarla para decidirle condiciones a un cliente es algo que la Gerencia debe verificar, y esta comparación no lo respalda.
- **Los grupos de edad dejaron fuera a un tercio de la cartera** (los de edad intermedia), y los montos entran en logaritmo. Con otros cortes o sin el logaritmo, las distancias cambiarían de tamaño.

#### Resumen de decisiones del taller del 7 de noviembre

| Decisión | Por qué |
|---|---|
| Referencia = promedio de la propia cartera | No hay meta del banco ni cifra publicada; se declara explícitamente |
| Gama alta = Platinum + Signature (10 788) | Son los dos niveles superiores de la jerarquía ordinal de `Card_Type` |
| Tercios extremos de edad (≤ 29 frente a ≥ 40) | Grupos claramente distintos en edad; se excluyen 14 871 de edad intermedia |
| 6 variables (una por pregunta del analista) | Máximo del enunciado; la edad, el ingreso, las cuotas y las compras internacionales quedan como candidatas |
| log(x+1) a 4 de las 6 variables | |asimetría| > 1 |
| Reportar dos D en una muestra (2,95 y 1,31) | La gama alta tiene covarianza más compacta: varianzas no homogéneas |
| Simulación de 1 000 grupos al azar | Lo sugiere el enunciado (sección 5.3 de las notas) y da intuición del azar |
| Validar T² con `manova()` | Lo exige la rúbrica; T² = 5,89 en ambos casos |
| LDA contra tasa base, y validación cruzada en dos muestras | Para no confundir «real» con «separa» |
| Convenciones de palabras (tam_D, veredicto_separa) | Para hablar con el cliente; se declaran como propias |
| Ajustar por compras internacionales | Es la candidata que más se aparta (1,47) |
| Iris como referencia | Muestra cómo se ve una separación completa (D = 10,16; 100 % de acierto) |

---

## Presentación ejecutiva (PDF)

**Archivo:** `Entrega/Analisis_Exploratorio_Credit_Card_Presentacion.pdf` (38 diapositivas).
**Título:** «Análisis Exploratorio Integral — Comportamiento Crediticio y Riesgo Financiero — Dataset Sintético».
**Encabezado:** «ESTADÍSTICA MULTIDIMENSIONAL · SEMANAS 1 A 6».
**Lema de portada:** «De la importación de los datos a la selección final de variables».
**Autores:** Oscar Manuel Contreras Gacha (20221020052), Juan Pablo Sarmiento Ramírez (20221020138), Steven Navarro Parrales (20221020048) y Juan Diego Grajales Castillo (20221020128).

**Alcance.** La presentación cubre el **primer corte (semanas 1 a 6)**: el análisis exploratorio que va de la importación a la selección de variables para PCA y *clustering*. Precede a los talleres del 31 de octubre y del 7 de noviembre, y su recomendación final (usar `Payment_Ratio` y `Credit_Utilization` como suplementarias) es la que adopta el taller del 31 de octubre. Cada diapositiva tiene un título y un subtítulo separados por «‖», y la mayoría cierra con un recuadro de lectura.

### Estructura general

| Bloque | Diapositivas | Contenido |
|---|---|---|
| Portada y ficha | 1–2 | Título, autores, fuente, contexto |
| Datos y calidad | 3–4 | Lectura en R, dimensiones, auditoría, escalas de medición |
| Diccionario | 5–8 | Las 26 numéricas y las 4 categóricas |
| Transformaciones | 9–11 | log(x+1), `factor()`, `scale()`; regla reproducible |
| Univariado | 12–22 | Sturges, efecto de los cortes, 26 histogramas |
| Categóricas | 23 | Frecuencias relativas |
| Bivariado y selección | 24–32 | Mapa de correlaciones, \|r\| y η², punto imposible, patrones |
| Estandarización | 33–35 | Z-score, cajas antes y después, colas máximas |
| Selección final | 36–37 | 21 retenidas y 5 descartadas |
| Cierre | 38 | Gracias |

### Diapositiva por diapositiva

**1 · Portada.** «ESTADÍSTICA MULTIDIMENSIONAL · SEMANAS 1 A 6». Título «Análisis Exploratorio Integral», subtítulo «Comportamiento Crediticio y Riesgo Financiero — Dataset Sintético», los cuatro autores con sus códigos y el lema «De la importación de los datos a la selección final de variables».

**2 · Ficha técnica y autores** («Quiénes hicimos el análisis y sobre qué datos»).

- **Autores y códigos.**
- **Fuente:** Kaggle — *Credit Card Customer Behavior Analysis & Prediction* (`https://www.kaggle.com/code/devraai/credit-card-customer-behavior-analysis-prediction/input`).
- **Naturaleza:** dataset sintético sobre comportamiento crediticio, capacidad financiera y riesgo de 50 000 clientes simulados de tarjeta de crédito.
- **Contexto económico:** India; todos los valores monetarios están en rupias indias (INR).
- **Cifras destacadas:** 50.000 clientes simulados (filas), 30 variables medidas (columnas) y 11 módulos de análisis.

**3 · Descripción logística de los datos** («Inspección, lectura y calidad de la matriz»).

- Antes de cargar se inspeccionan las primeras líneas en crudo (`readLines`): separador coma, decimal punto y encabezado en la primera fila.
- Código de carga: `credit <- read.csv(file = ruta, header = TRUE, sep = ",", dec = ".", stringsAsFactors = FALSE)`.
- Dimensiones de la matriz $X \in \mathbb R^{n\times p}$: n = 50.000 observaciones (clientes) y p = 30 variables.
- **Auditoría de calidad (Módulo 2):** 0 % de celdas vacías (matriz 100 % completa), 0 filas o identificadores duplicados, sin valores centinela ni niveles mal escritos.
- **Lectura:** la matriz llega limpia y completa, así que no hace falta ninguna estrategia frente a faltantes (casos completos, por pares, imputación).

**4 · Cómo lee R los datos** («Clasificación por escala de medición, no por tipo de almacenamiento»).

`str(credit)` reporta 4 columnas de texto y 26 numéricas, pero el criterio real es si la media o una distancia métrica constante tienen sentido sobre la variable, no cómo la almacena R.

- **Nominales:** `Customer_ID` (50.000 únicos, identificador puro), `Gender` (2 niveles) y `Occupation` (6 niveles laborales).
- **Ordinal:** `Card_Type`, con 5 niveles y jerarquía real Basic < Silver < Gold < Platinum < Signature.
- **Cuantitativas (26):** monetarias (ingreso, cupo, gastos, saldos: 15), ratios (`Payment_Ratio`, `Credit_Utilization`) y conteos (edad, EMI, transacciones: 9).
- **Casos corregidos:** `Card_Type` es texto pero tiene orden real, así que se trata como ordinal y no como nominal. Las variables de rango corto (`Age`, `EMI_Count`) siguen siendo cuantitativas: su media es interpretable pese al rango acotado.

**5 · Diccionario de variables (1/3)** («9 de 26 variables numéricas — perfil y consumo general»).

| Variable | Qué mide |
|---|---|
| `Age` | Edad del titular, en años |
| `Annual_Income` | Ingreso anual declarado (INR) |
| `Credit_Limit` | Cupo total aprobado (INR) |
| `Card_Age_Months` | Antigüedad de la tarjeta, en meses |
| `Monthly_Spending` | Gasto mensual total: suma de las 7 categorías de consumo |
| `Monthly_Transactions` | Número de compras en el mes |
| `Avg_Transaction_Value` | Ticket promedio (gasto mensual / número de transacciones) |
| `Online_Shopping_Spending` | Gasto mensual en compras por internet |
| `Grocery_Spending` | Gasto mensual en supermercado |

**Variables derivadas:** `Monthly_Spending` es la suma exacta de las 7 categorías de gasto, y `Avg_Transaction_Value` = `Monthly_Spending` / `Monthly_Transactions` es un cociente, no una medición directa.

**6 · Diccionario de variables (2/3)** («9 de 26 — categorías de gasto y saldos»).

| Variable | Qué mide |
|---|---|
| `Fuel_Spending` | Gasto mensual en combustible |
| `Dining_Spending` | Gasto mensual en restaurantes |
| `Travel_Spending` | Gasto mensual en viajes |
| `Entertainment_Spending` | Gasto mensual en entretenimiento |
| `Utility_Bill_Spending` | Gasto mensual en servicios públicos pagados con la tarjeta |
| `Outstanding_Balance` | Saldo que el cliente aún debe |
| `Statement_Balance` | Saldo facturado en el último corte |
| `Payment_Amount` | Monto pagado en el mes |
| `Payment_Ratio` | Proporción del saldo facturado efectivamente pagada |

**Otra relación derivada:** `Outstanding_Balance` y `Statement_Balance` miden prácticamente la misma deuda en dos momentos del ciclo (r = 0.997): casi la misma información contada dos veces.

**7 · Diccionario de variables (3/3)** («8 de 26 — comportamiento, uso y riesgo»).

| Variable | Qué mide |
|---|---|
| `Credit_Utilization` | Proporción del cupo usada |
| `Cash_Advance_Amount` | Monto retirado como avance en efectivo |
| `EMI_Count` | Número de compras diferidas a cuotas vigentes |
| `International_Transactions` | Número de compras en el exterior |
| `Reward_Points_Earned` | Puntos de recompensa acumulados, según el gasto |
| `Reward_Points_Redeemed` | Puntos ya redimidos |
| `Mobile_App_Login` | Ingresos a la app móvil en el mes |
| `Credit_Score` | Puntaje crediticio: la variable de riesgo |

**Más cocientes derivados:** `Payment_Ratio` ≈ `Payment_Amount` / `Statement_Balance`; `Credit_Utilization` ≈ `Outstanding_Balance` / `Credit_Limit`; `Reward_Points_Earned` es función del gasto mensual. `Credit_Score` es la variable de riesgo, y el resto del análisis termina relacionándose con ella.

**8 · Diccionario de variables (4/4): categóricas** («Las 4 variables de texto, completas»).

| Variable | Naturaleza | Qué mide |
|---|---|---|
| `Customer_ID` | Nominal (identificador) | Identificador único, 50.000 valores; no mide nada y se excluye de todo cálculo numérico |
| `Gender` | Nominal (2) | F, M, sin jerarquía |
| `Occupation` | Nominal (6) | Retired, Student, Business Owner, Government Employee, Private Employee, Self-Employed |
| `Card_Type` | Ordinal (5) | Basic < Silver < Gold < Platinum < Signature |

Cierre: 26 cuantitativas + 4 cualitativas = las 30 variables de la matriz X.

**9 · Qué significa cada transformación** («Tres herramientas de R, tres efectos distintos»).

- **`log(x+1)`:** comprime las colas largas. Suma 1 para que los ceros no rompan el cálculo y comprime mucho más las distancias entre valores grandes que entre valores pequeños. Ejemplo: `Cash_Advance_Amount` (skew 6.78) queda mucho más manejable.
- **`factor()`:** declara una variable categórica, como paso obligatorio antes de graficar o modelar una nominal. `factor(x, ordered = TRUE)` agrega un orden explícito, que necesita `Card_Type`.
- **`scale()`:** estandariza con $z = (x-\bar x)/s$ (media 0, sd 1). No cambia la forma, solo la escala.
- **Por qué log → scale y no al revés:** estandarizar primero una variable sesgada solo reescala la asimetría, no la corrige. Comprimir la cola con `log()` antes sí acerca la forma a algo simétrico.

**10 · Transformación de variables (1/2)** («Regla reproducible, no a mano»). Resumen: **16** variables con log(x+1) + scale() (|skew| > 1), **5** con solo scale() (simétricas) y **5** excluidas (redundantes o derivadas).

| Variable | Skew | Transformación |
|---|---|---|
| Age | 0.69 | scale() |
| Annual_Income | 2.55 | log+scale |
| Credit_Limit | 3.01 | log+scale |
| Card_Age_Months | 1.14 | log+scale |
| Monthly_Spending | 3.00 | Excluir |
| Monthly_Transactions | 0.54 | scale() |
| Avg_Transaction_Value | 3.90 | log+scale |
| Online_Shopping_Spending | 4.56 | log+scale |
| Grocery_Spending | 4.01 | log+scale |
| Fuel_Spending | 4.69 | log+scale |
| Dining_Spending | 4.64 | log+scale |
| Travel_Spending | 5.71 | log+scale |
| Entertainment_Spending | 5.01 | log+scale |
| Utility_Bill_Spending | 4.35 | log+scale |
| Outstanding_Balance | 4.02 | Excluir |
| Statement_Balance | 3.80 | log+scale |
| Payment_Amount | 4.20 | log+scale |
| Payment_Ratio | −1.04 | Excluir |
| Credit_Utilization | 0.53 | Excluir |
| Cash_Advance_Amount | 6.78 | log+scale |
| EMI_Count | 0.17 | scale() |
| International_Transactions | 2.11 | log+scale |
| Reward_Points_Earned | 3.50 | Excluir |
| Reward_Points_Redeemed | 6.55 | log+scale |
| Mobile_App_Login | 0.33 | scale() |
| Credit_Score | −0.58 | scale() |

**11 · Transformación de variables (2/2)** («Las categóricas necesitan otro tratamiento»). Sobre texto no tienen sentido ni `log()` ni `scale()`:

- `Customer_ID` → se quita (no es variable de análisis).
- `Gender` → `factor()`.
- `Occupation` → `factor()` o codificación *dummy*.
- `Card_Type` → `factor(ordered = TRUE)` o entero 1–5.

**Criterio aplicado (reproducible):** primero, excluir la variable si es redundante o derivada; si no, aplicar log(x+1) antes de estandarizar cuando |asimetría| > 1, y solo `scale()` en caso contrario. 16 de 26 numéricas usan log antes de estandarizar (gasto, saldo y conteos con masa en cero). Las 5 excluidas no se descartan por mala calidad, sino porque vuelven casi singular la matriz de covarianzas.

**12 · Análisis univariado** («Estadísticos clásicos y la regla de Sturges»).

- **Credit_Score como variable de referencia:** media 636.4, mediana 640, desviación estándar 87.3. La media queda por debajo de la mediana: primera señal numérica de una cola hacia la izquierda.
- **Regla de Sturges:** $k = 1 + \log_2 n = 1 + 3.322\log_{10} n$. Con n = 50.000 da k = 17 intervalos.
- **Por qué importa:** el número de cortes de un histograma no es estético; cambia lo que el gráfico dice sobre los mismos datos. k no depende de la variable, porque solo usa n.
- **Inconsistencia detectada al documentar:** estas cifras **no coinciden** con las del análisis actual (`Entrega/analisis_synthetic_credit_card.Rmd`) ni con los talleres, que reportan media 629 (628,98), mediana 638, desviación 68,44 y rango 367–792 para `Credit_Score`. La presentación parece haberse hecho sobre otra versión de los datos o del cálculo; la causa no está documentada.

**13 · El efecto del número de cortes** («Sobre-suavizado, balanceado, ruidoso»). Tres histogramas del puntaje:

- **breaks = 5:** la asimetría a la izquierda desaparece.
- **breaks = 60:** aparecen dientes y huecos de ruido de muestreo.
- **k = 17 (Sturges):** se ve la forma real: unimodal, centrada cerca de 640 y con cola izquierda.

**14–22 · Histogramas de las 26 variables (1/9 a 9/9).** Tres por diapositiva, cada uno con su lectura:

| Diap. | Grupo | Variable (skew): lectura |
|---|---|---|
| 14 | 1/9 — edad, ingreso y cupo | Age (0.69): casi simétrica, leve sesgo derecho, se concentra entre 27 y 44 años · Annual_Income (2.55): cola derecha típica de ingresos, la mayoría cerca de la mediana y pocos ganan mucho más · Credit_Limit (3.01): hereda la cola de Annual_Income y solo toma valores redondeados |
| 15 | 2/9 — antigüedad y actividad mensual | Card_Age_Months (1.14): más tarjetas nuevas que antiguas, masa en los primeros años · Monthly_Spending (3.00): suma de 7 categorías ya sesgadas, acumula todas sus colas · Monthly_Transactions (0.54): conteo acotado (15 a 179 al mes), casi simétrica |
| 16 | 3/9 — ticket y primeras categorías | Avg_Transaction_Value (3.90): cociente gasto/transacciones, dominan los tickets pequeños · Online_Shopping_Spending (4.56): pico pegado al origen, la mayoría gasta poco · Grocery_Spending (4.01): la mediana más alta del grupo, gasto recurrente casi universal |
| 17 | 4/9 — gasto discrecional | Fuel_Spending (4.69): depende de tener vehículo, gasto bajo mayoritario · Dining_Spending (4.64): discrecional, mayoría moderada y minoría con montos altos · Travel_Spending (5.71): el gasto más esporádico, la cola más larga del grupo |
| 18 | 5/9 — entretenimiento y saldos | Entertainment_Spending (5.01): discrecional y ocasional, cola de consumo intensivo · Utility_Bill_Spending (4.35): monto acotado y frecuente, cola de facturas altas · Outstanding_Balance (4.02): sigue la lógica del gasto y el cupo |
| 19 | 6/9 — saldo, pago y ratio | Statement_Balance (3.80): casi idéntica a Outstanding_Balance · Payment_Amount (4.20): proporcional a lo facturado, reproduce la forma del saldo · Payment_Ratio (−1.04): la única cola a la izquierda, acotada en 1, la mayoría paga casi todo |
| 20 | 7/9 — utilización, avances y cuotas | Credit_Utilization (0.53): proporción acotada en [0,1], compacta y sin colas · Cash_Advance_Amount (6.78): inflada en cero, más de la mitad nunca hace avances · EMI_Count (0.17): solo 7 valores enteros (0 a 6), barras separadas |
| 21 | 8/9 — internacional y recompensas | International_Transactions (2.11): típicamente cero, cola discreta · Reward_Points_Earned (3.50): función del gasto, reescala Monthly_Spending · Reward_Points_Redeemed (6.55): acumulación en cero, muchos no redimen |
| 22 | 9/9 — app y puntaje | Mobile_App_Login (0.33): conteo acotado (2 a 71 sesiones), hábito uniforme · Credit_Score (−0.58): acotado por diseño, cola corta de alto riesgo |

**Síntesis (diapositiva 22):** domina la cola derecha con pico en el origen. Las excepciones son `Payment_Ratio` (cola izquierda) y las proporciones o conteos cortos (`Credit_Utilization`, `EMI_Count`, `Mobile_App_Login`), que son compactos y simétricos.

**23 · Distribución de categóricas** («Frecuencia relativa; Card_Type en orden ordinal»).

- **Gender:** 55.2 % M frente a 44.8 % F, una diferencia mínima.
- **Card_Type:** Gold 33.8 % es el nivel más común; Signature es el más raro (5 %).
- **Occupation:** Private 41.9 % es la ocupación dominante, casi 3 veces la siguiente.

Las tres llegan limpias: Gender (2), Card_Type (5) y Occupation (6) niveles, sin niveles «fantasma» ni NA. Estas cifras concuerdan con el taller del 7 de noviembre: Gold 16 895 / 50 000 = 33,8 % y Signature 2 504 / 50 000 = 5,0 %.

**24 · Mapa de calor de correlaciones** («325 pares posibles, reordenados por similitud (hclust)»). Es una diapositiva solo con gráfico: la matriz de correlaciones de las 26 numéricas reordenada por agrupamiento jerárquico. El texto extraído no trae cifras.

**25 · Síntesis de la matriz de correlación** («Qué bloques y qué separaciones deja ver el mapa»).

- **Colinealidad casi perfecta (r > 0.95):** Outstanding_Balance–Statement_Balance 0.997; Monthly_Spending–Reward_Points_Earned 0.980; Credit_Limit–Annual_Income 0.974.
- **Determinantes del riesgo (Credit_Score):** Payment_Ratio r = 0.767; Credit_Utilization r = −0.599; Annual_Income apenas r = 0.032.
- **Ingresos, cupo y gasto forman un solo bloque:** Annual_Income con Credit_Limit (0.974) y con Monthly_Spending (0.945). A mayor ingreso, más cupo y más gasto.
- **Variables «aisladas»:** Payment_Ratio y Credit_Utilization correlacionan casi 0 con las variables de volumen de dinero. El comportamiento de pago es independiente de cuánto gana o gasta el cliente.

**26 · Criterios de selección: |r| y η²** («Dos medidas de asociación, para dos tipos de par distintos»).

- **|r| de Pearson** (numérica ∼ numérica): $r = \operatorname{cov}(X,Y)/(s_Xs_Y)$, entre −1 y 1. Se usa |r| para ordenar los pares por fuerza sin importar el signo.
- **η² (eta al cuadrado)** (numérica ∼ categórica): $\eta^2 = SC_{\text{entre grupos}}/SC_{\text{total}}$, de un ANOVA de un factor, entre 0 y 1. Es la misma clase de medida que $r^2$, para cuando un lado no es numérico.
- **Por qué hace falta un criterio objetivo:** con p = 26 hay $\binom{26}{2} = 325$ pares, y mirarlos uno por uno no es factible.

**27 · Selección objetiva de variables (1/2)** («|r| de Pearson entre las 26 numéricas»).

| v1 | v2 | r |
|---|---|---|
| Outstanding_Balance | Statement_Balance | 0.997 |
| Monthly_Spending | Reward_Points_Earned | 0.980 |
| Annual_Income | Credit_Limit | 0.974 |
| Credit_Limit | Reward_Points_Earned | 0.958 |

- El par numérico más fuerte que **no** es redundancia contable es Annual_Income–Credit_Limit (r = 0.974). Los pares que están por encima son casi la misma cantidad de dinero contada dos veces.
- **Lo que de verdad explica el riesgo:** Payment_Ratio (r = 0.767) y Credit_Utilization (r = −0.599) son, por enorme margen, las correlaciones más fuertes con Credit_Score, no las variables de dinero (r ≈ 0.03).

**28 · Selección objetiva de variables (2/2)** («η²: varianza explicada por la categórica»).

| Comparación | η² |
|---|---|
| Credit_Limit ∼ Card_Type | 0.7997 |
| Annual_Income ∼ Card_Type | 0.6837 |
| Annual_Income ∼ Occupation | 0.6367 |
| Credit_Score ∼ Card_Type | 0.0023 |
| Annual_Income ∼ Gender | 0.0001 |

**Selección final: 4 pares con análisis bivariado profundo.**

| Par | Criterio | Valor | Por qué |
|---|---|---|---|
| Income–Limit | \|r\| | 0.974 | el más fuerte que no es redundante |
| Payment_Ratio–Score | \|r\| | 0.767 | predictor n.º 1 del riesgo |
| Utilization–Score | \|r\| | −0.599 | predictor n.º 2 del riesgo |
| Income–Occupation | η² | 0.637 | el más fuerte entre numérica y categórica |

**Coherencia interna:** Card_Type y Occupation explican bien las variables de dinero, pero casi nada de Credit_Score. El riesgo no depende de cuánto gana el cliente, sino de cómo paga.

**29 · El «punto imposible»** («Normal en cada variable por separado, imposible en conjunto»). Dos casos:

- Un cliente con Payment_Ratio = 0.95 y Credit_Score = 460 (panel izquierdo).
- Un cliente con Annual_Income = 3.000.000 y Credit_Limit = 200 (panel derecho).

Ambos pasan los dos filtros univariados de Tukey, pero caen fuera de la nube conjunta: **la normalidad marginal no garantiza la normalidad conjunta**. Es el argumento para usar métodos multivariados como la distancia de Mahalanobis, que retoman los talleres.

**30 · Confirmando la selección** («Comportamiento de pago vs. uso del cupo»). Matriz de correlación del núcleo bivariado:

| | Income | Limit | Score |
|---|---|---|---|
| Income | 1.00 | 0.97 | 0.03 |
| Limit | 0.97 | 1.00 | 0.04 |
| Payment_Ratio | 0.00 | 0.00 | 0.77 |
| Credit_Util. | 0.00 | 0.00 | −0.60 |

**Lectura:** el cupo lo determina casi exclusivamente el ingreso (r = 0.97). El buen puntaje depende del comportamiento: pagar (r = 0.77) y no sobreusar el cupo (r = −0.60).

**31 · Comparación por grupos: Occupation** («Informativa aquí, ruido en la otra»).

- **Izquierda:** las cajas de Annual_Income por ocupación suben en escalera sin traslaparse; de Student a Business Owner, la razón entre sus medias es de casi 17 a 1 (η² = 0.637).
- **Derecha:** las cajas de Credit_Score por ocupación son indistinguibles (η² = 0.0009).

La misma variable categórica es informativa para una variable y ruido puro para otra.

**32 · Patrones bivariados de la cartera** («Lineal directa, límite físico y grupos ordinales»). Tres gráficos:

1. **Lineal directa:** Income → Limit sube en una banda angosta; usar ambas duplica la misma información.
2. **Efecto cuña:** nadie debe más de lo que su cupo permite. Es un límite físico, no una relación proporcional.
3. **Grupos ordinales:** Card_Type sube en el mismo orden que su jerarquía, sin inversiones.

**33 · Por qué y cómo se estandariza** («z = (x − x̄)/s: mismo idioma para 26 escalas distintas»).

- **El problema de escala:** Annual_Income tiene sd = 1.407.257 y Credit_Utilization sd = 0.206. Entre la variable más dispersa y la menos dispersa hay una razón de **6.835.059 veces**. Graficarlas juntas en escala original es imposible de leer: una sola variable domina el eje.
- **La transformación:** $z_{ij} = (x_{ij}-\bar x_j)/s_j$. Cada variable queda con media 0 y sd 1. No cambia la forma de la distribución, solo la escala.
- **Conexión con PCA:** es la misma decisión que separa un PCA sobre la matriz de covarianzas de uno sobre la matriz de correlaciones, y por eso es indispensable antes de PCA y *clustering*. El taller del 31 de octubre retoma este punto en «¿Debemos estandarizar?».

**34 · Comparación estandarizada** («Las 26 variables, antes y después de scale()»).

- **Izquierda (sin escalar):** 24 de 26 cajas son una línea plana pegada al cero; Annual_Income y Credit_Limit esconden todo lo demás.
- **Derecha (escaladas):** las 26 comparten el mismo eje, y por fin se pueden comparar su dispersión y sus colas.

**35 · Diagnóstico de colas máximas** («A cuántas σ de su media está el máximo»).

| Colas más largas | Zmax | Colas más cortas | Zmax |
|---|---|---|---|
| Travel_Spending | 19.37 | Credit_Utilization | 2.54 |
| Reward_Points_Redeemed | 18.65 | Credit_Score | 2.38 |
| Utility_Bill_Spending | 17.14 | Monthly_Transactions | 2.28 |
| Entertainment_Spending | 16.93 | Mobile_App_Login | 2.25 |
| Dining_Spending | 15.92 | EMI_Count | ∼2.0 |

Travel_Spending tiene el máximo más extremo (19.37σ por encima de su media) porque es el gasto más esporádico: la mayoría viaja poco o nada, y los pocos que viajan lo hacen con montos grandes. El ranking coincide con las variables de cola larga de los histogramas.

**36 · Con cuáles variables nos quedamos** («Tres criterios: clasificación, redundancia, selección»). Se retienen **21 de 26** variables numéricas para PCA y *clustering*, en cuatro bloques:

- **Capacidad y demografía (4):** Age, Annual_Income, Credit_Limit, Card_Age_Months.
- **Gasto por categoría (7):** Online_Shopping, Grocery, Fuel, Dining, Travel, Entertainment, Utility_Bill.
- **Saldos y pagos (4):** Statement_Balance, Payment_Amount, Avg_Transaction_Value, Monthly_Transactions.
- **Comportamiento y riesgo (6):** Cash_Advance, EMI_Count, Intl._Transactions, Reward_Redeemed, Mobile_Login, Credit_Score.

Las 3 categóricas (Gender, Occupation, Card_Type) no entran a un PCA clásico sobre la matriz de correlación, pero se conservan aparte para perfilar los *clusters*. Card_Type es candidata a codificarse como entero ordinal 1–5.

**37 · Variables descartadas y por qué (5)** («Ninguna exclusión es por mala calidad»).

| Variable | Motivo de exclusión |
|---|---|
| Monthly_Spending | Es la suma exacta de las 7 categorías de gasto retenidas: colinealidad garantizada (r = 1) |
| Outstanding_Balance | r = 0.997 con Statement_Balance: la misma información dos veces; se retiene Statement_Balance |
| Reward_Points_Earned | r = 0.980 con Monthly_Spending: función casi lineal del gasto, sin información propia |
| Payment_Ratio | Cociente derivado de columnas ya retenidas; vuelve casi singular la matriz de covarianzas |
| Credit_Utilization | Cociente derivado (Balance/Cupo); misma razón que Payment_Ratio |

**Caso especial:** Payment_Ratio y Credit_Utilization se excluyen de la construcción del PCA y los *clusters* por colinealidad. Pero, precisamente por ser las variables que más predicen Credit_Score, se recomienda **reincorporarlas después como variables suplementarias para interpretar los resultados, no para construirlos**. El taller del 31 de octubre aplica exactamente esta recomendación.

**38 · Gracias.** «De la importación de los datos a la selección final de variables para PCA y clustering». Autores y «Estadística Multidimensional · Semanas 1 a 6».

### Hallazgos principales de la presentación

1. **Calidad:** la matriz de 50 000 × 30 llega completa, sin duplicados ni centinelas. No hace falta tratar faltantes.
2. **Escalas:** `Card_Type` es ordinal; las variables de rango corto siguen siendo cuantitativas.
3. **Formas:** dominan las colas derechas con pico en cero. Se aplica log(x+1) a 16 variables y solo `scale()` a 5.
4. **Redundancias:** Outstanding/Statement (0.997), Monthly_Spending/Reward_Earned (0.980), Income/Limit (0.974).
5. **Riesgo:** el puntaje lo explican el comportamiento de pago (Payment_Ratio 0.767) y el uso del cupo (−0.599), no el dinero (≈ 0.03) ni las categóricas (η² de 0.0023 con Card_Type y 0.0009 con Occupation).
6. **Multivariado:** el «punto imposible» muestra que la normalidad marginal no garantiza la conjunta.
7. **Estandarización:** hay una razón de 6.835.059 entre desviaciones, así que es indispensable estandarizar antes de PCA y *clustering*.
8. **Selección:** se retienen 21 numéricas y se descartan 5 por redundancia o derivación (no por calidad). Las dos razones de pago y uso quedan como suplementarias.

**Conexión con los talleres:**

- El taller del 31 de octubre toma 9 de las 21 retenidas.
- Aplica la misma regla de logaritmo.
- Usa `Payment_Ratio` y `Credit_Utilization` como suplementarias.
- Confirma, con PCA y AF, que el puntaje va por su cuenta respecto al bloque de dinero, como anticipaba la presentación (r ≈ 0.03).
- El taller del 7 de noviembre aprovecha la jerarquía ordinal de `Card_Type` para definir la gama alta (Platinum + Signature).

---

# Anexo A — Glosario de conceptos

Definiciones breves para consulta rápida. La explicación completa, con su aplicación y resultados, está en la sección indicada.

| Concepto | Qué es, en una línea | Dónde se trabaja |
|---|---|---|
| Matriz de datos $\mathbf{X}\in\mathbb{R}^{n\times p}$ | Tabla de $n$ individuos (filas) por $p$ variables (columnas) | Módulo 1, Módulo 9 |
| Cardinalidad | Número de valores distintos de una variable; ayuda a decidir si es cuantitativa o categórica | Módulo 1 |
| Variable nominal / ordinal | Categorías sin orden (Occupation, Gender) o con orden (Card_Type: Basic < Silver < Gold < Platinum < Signature) | Módulo 1 |
| Datos faltantes (NA) | Celdas vacías; `is.na`, `complete.cases` | Módulo 2 |
| Regla de Sturges | Número de clases del histograma: $k = \lceil \log_2 n + 1\rceil$ | Módulo 3 |
| Asimetría (skewness) | Mide hacia qué lado se alarga la cola de una distribución | Módulos 3, 15 |
| Densidad de kernel | Curva suave que estima la densidad sumando «campanitas» centradas en cada dato: $\hat f(x)=\frac{1}{nh}\sum K\!\left(\frac{x-x_i}{h}\right)$ | Módulo 4 |
| Ancho de banda $h$ | Ancho de cada campanita; controla cuánto se suaviza (regla de Silverman) | Módulo 4 |
| Cinco números de Tukey | Mínimo, Q1, mediana, Q3, máximo | Módulo 5 |
| RIC y límites de Tukey | $RIC = Q_3-Q_1$; atípico si queda fuera de $[Q_1-1.5\,RIC,\;Q_3+1.5\,RIC]$ | Módulo 5 |
| Z-score / estandarización | $z=(x-\bar x)/s$: media 0, desviación 1, sin unidades | Módulo 6 |
| Covarianza | $s_{jk}=\frac{1}{n-1}\sum (x_{ij}-\bar x_j)(x_{ik}-\bar x_k)$: cómo varían juntas dos variables, en sus unidades | Módulos 7, 10 |
| Correlación de Pearson $r$ | Covarianza dividida por las dos desviaciones; entre −1 y 1, mide asociación **lineal** | Módulos 7, 8 |
| $\eta^2$ (razón de correlación) | Proporción de la varianza de una numérica explicada por una categórica | Módulo 7 |
| Cuarteto de Anscombe | Cuatro conjuntos con la misma $r$ y gráficos muy distintos: siempre hay que mirar el gráfico | Módulo 7 |
| Atípico multivariante («punto imposible») | Punto normal en cada variable por separado pero imposible en la combinación | Módulos 7, 13 |
| Matriz de correlaciones $\mathbf{R}$ | Simétrica, diagonal de unos, semidefinida positiva | Módulo 8 |
| Coordenadas paralelas | Cada variable es un eje vertical; cada cliente es una línea quebrada | Módulo 8 |
| Vector de medias / centroide | $\bar{\mathbf{x}}=(\bar x_1,\dots,\bar x_p)'$: el «cliente promedio», centro de gravedad de la nube | Módulo 9 |
| Estimadores robustos | Mediana, media recortada: poco sensibles a errores o atípicos | Módulo 9 |
| Distancia euclidiana | $\sqrt{\sum (x_j-y_j)^2}$: ignora unidades y correlaciones | Módulo 9 |
| Matriz de covarianzas $\mathbf{S}$ | $\mathbf{S}=\frac{1}{n-1}(\mathbf{X}-\mathbf{1}\bar{\mathbf{x}}')'(\mathbf{X}-\mathbf{1}\bar{\mathbf{x}}')$ | Módulo 10 |
| Varianza total / generalizada | Traza de $\mathbf{S}$ / determinante de $\mathbf{S}$ | Módulo 10 |
| Matriz singular | Determinante 0, no invertible; ocurre si una variable es combinación exacta de otras (Monthly_Spending = suma de 7 categorías) | Módulos 10, 12, 15 |
| Distribución conjunta / marginal | Comportamiento simultáneo de varias variables / de una sola, sumando o integrando las demás | Módulo 11 |
| Paradoja de Simpson | Una relación que se invierte al agregar o separar grupos | Módulos 11, 12 |
| Distribución condicional | Distribución de una variable fijando el valor de otra: $f(x\mid y)=f(x,y)/f(y)$ | Módulo 12 |
| Independencia | $f(x,y)=f(x)f(y)$; correlación cero **no** la implica | Módulo 12 |
| Ley de la varianza total | $\operatorname{Var}(Y)=E[\operatorname{Var}(Y\mid X)]+\operatorname{Var}(E[Y\mid X])$ | Módulo 12 |
| Normal multivariante | $\mathbf{x}\sim N_p(\boldsymbol\mu,\boldsymbol\Sigma)$; sus condicionales tienen fórmula cerrada | Módulos 12, 13 |
| Distancia de Mahalanobis | $D^2=(\mathbf{x}-\bar{\mathbf{x}})'\mathbf{S}^{-1}(\mathbf{x}-\bar{\mathbf{x}})$: distancia que respeta unidades y correlaciones | Módulo 13, taller 7 nov |
| Corte $\chi^2_p$ | Bajo normalidad, $D^2\sim\chi^2_p$; los que superan el percentil 97,5 o 99 se marcan como raros | Módulo 13 |
| Gráfico Q-Q | Cuantiles observados contra teóricos; si sigue la diagonal, la distribución se ajusta | Módulo 13 |
| Prueba de hipótesis y p-valor | Probabilidad de ver algo tan extremo si $H_0$ fuera cierta; con $n=50\,000$ casi todo resulta «significativo» | Módulo 14 |
| Shapiro-Wilk / Lilliefors | Pruebas de normalidad univariada | Módulo 14 |
| Mardia | Pruebas de normalidad multivariante por asimetría y curtosis | Módulo 14 |
| Transformación $\log(x+1)$ | Comprime colas largas a la derecha; se aplica si \|asimetría\| > 1 | Módulo 15 y talleres |
| One-hot / dummies | Una columna 0/1 por categoría; con $k$ columnas suman 1 (trampa de las dummies) | Módulos 15, 17, PCA II |
| Arquitectura medallion | Bronze (crudo) → Silver (limpio) → Gold (listo para modelar) | Módulo 15 |
| PCA (componentes principales) | Nuevos ejes, combinaciones lineales no correlacionadas que ordenan la información (varianza) de mayor a menor; autovectores de $\mathbf{R}$ | Módulos 16, 17, talleres |
| Autovalor / varianza explicada | Información que guarda cada componente; $\lambda_k/\sum\lambda$ | Módulo 16 |
| Cargas / scores | Peso de cada variable en la componente / coordenada de cada cliente | Módulos 16, 17 |
| Criterio de Kaiser / codo | Retener componentes con $\lambda>1$ / donde la curva de varianza se aplana | Módulo 16 |
| Variable suplementaria | Se proyecta sobre el mapa sin participar en construirlo | Módulos 16, 17 |
| Biplot | Clientes (puntos) y variables (flechas) en el mismo plano | Módulo 17, PCA II |
| Análisis factorial | Modelo $\mathbf{x}=\boldsymbol\Lambda\mathbf{f}+\boldsymbol\varepsilon$: lo común (factores) + lo propio (unicidad) | Módulo 18, talleres |
| Comunalidad / unicidad | Parte de la varianza de una variable compartida con los factores / propia | Módulo 18, talleres |
| KMO y Bartlett | ¿Comparten las variables lo suficiente para hacer factorial? | Módulo 18, talleres |
| Rotación varimax / promax | Ortogonal (factores no correlacionados) / oblicua (se permite correlación) | Módulo 18 |
| $T^2$ de Hotelling | Generalización multivariante de la prueba $t$: compara vectores de medias | Taller 7 nov |
| MANOVA | Análisis de varianza con varias respuestas; para dos grupos equivale a $T^2$ | Taller 7 nov |

---

# Anexo B — Inconsistencias y puntos a revisar detectados al documentar

Al documentar se encontraron estos detalles en los archivos fuente. **No se corrigieron**: se reportan para que el equipo decida.

| # | Dónde | Observación |
|---|---|---|
| 1 | Informe, Módulo 7 | El gráfico de la Tendencia 4 tiene el título «Tendencia 6». |
| 2 | Informe, Módulo 7 | Se anuncian «seis tendencias», pero el Módulo 7 solo grafica cuatro; las otras dos (independencia y embudo) salen de los `pairs` del Módulo 8. |
| 3 | Informe, Módulo 8 | En coordenadas paralelas, los comentarios dicen «2,000 registros» pero el código toma una muestra de 5000 (`set.seed(123)`). |
| 4 | Informe, Módulo 8 | `parcoord()` reescala cada eje a su rango, aunque el eje Y se rotula «z-score». |
| 5 | Informe, Módulo 7 | Se dice que Annual_Income ~ Occupation es «el par numérica-categórica más fuerte», pero Annual_Income ~ Card_Type tiene un η² mayor (0,684 frente a 0,637). |
| 6 | Informe, Módulo 8 | Se dice que Card_Age_Months es «la siguiente más fuerte» con Credit_Score, cuando por \|r\| van antes los saldos (−0,145 y −0,125). |
| 7 | Informe, Módulo 8 | El 9,86 % de Reward_Points_Earned se describe como «muy cercano» al 8,43 % de Monthly_Spending. |
| 8 | Informe, varios módulos | Algunas etiquetas de gráficos usan «$» para montos que están en rupias (₹). |
| 9 | Presentación PDF, diapositiva 12 | Credit_Score aparece con media 636,4, mediana 640 y desviación 87,3; el informe y los talleres dan 628,98, 638 y 68,44. Posible versión anterior de los datos o del cálculo. |
| 10 | `explicacion_taller_analisis_factorial.md` | Dice que sin pago, saldo **y cupo** el puntaje se predice en «menos de 1 de cada 100»; la regresión del Rmd excluye solo saldo y pago e incluye el cupo (R² = 0,006). |
| 11 | Talleres | El taller de factorial dice partir de los Módulos 15–17 del informe; los de PCA citan el «Módulo 11» (numeración anterior del informe). |
| 12 | PCA II (versión previa) | Con `mantienen` = 89,6, el umbral `>= 90` no se cumplía y el texto habría dicho que la lista «cambia bastante» a la vez que el eje de riesgo «casi no se mueve». La versión `_final` lo corrige con la bandera `estable`. |
| 13 | Informe, Módulo 15 | El menor autovalor de la correlación de las 4 dummies k−1 de Card_Type no se calcula (solo el determinante, 0,5154). |
| 14 | Informe, Módulo 1 | Se dice que la edad máxima es 69 años; `summary` y `range` dan 70. |
| 15 | Informe, Módulo 1 | El rango de cardinalidad de las monetarias («40.475–50.000») deja fuera a Cash_Advance_Amount (14.826) y Credit_Limit (4.318); ninguna monetaria llega a 50.000 valores distintos. |
| 16 | Informe, Módulos 3–4 | Varias frases se contradicen sobre cuál variable tiene «la mayor» asimetría (se citan Credit_Limit 3,01 y Travel 5,71, pero Cash_Advance_Amount tiene 6,78). |
| 17 | Informe, Módulo 3 | Se dice que Payment_Ratio es la «única» con asimetría negativa, pero Credit_Score también la tiene. |
| 18 | Informe, Módulo 3 | Según la tabla `Skew`, la variable más simétrica es EMI_Count (0,17), no Monthly_Transactions. |
| 19 | Informe, Módulo 3 | En Online_Shopping_Spending se dice que la mediana es «menos de un tercio de la media», pero el cociente real es 0,55. |
| 20 | Informe, Módulo 3 | La sección de Sturges se refiere a una comparación que aparece después. La conclusión 3 del módulo termina cortada. |
| 21 | Informe, Módulo 4 | Se dice que los picos 43, 64 y 91 de Monthly_Transactions «coinciden» con las medianas por tarjeta (38, 62 y 91); en Basic la diferencia es de 5 transacciones. |
| 22 | Informe, Módulo 9 | Una frase remite a «la misma advertencia del Módulo 14» sobre normalidad; la referencia no es verificable con la numeración actual. |
