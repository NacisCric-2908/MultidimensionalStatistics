# Guía Integral de Sustentación y Resumen Técnico: Análisis Estadístico Multidimensional
**Dataset:** `bronze/synthetic_credit_card_customer_behavior_dataset.csv`  
**Documento base:** `Entrega/analisis_synthetic_credit_card.Rmd` (Semanas 1 a 6 — S01 a S06)  
**Asignatura:** Estadística Multidimensional  
**Autores:**
* Oscar Manuel Contreras Gacha (`20221020052`)
* Juan Pablo Sarmiento Ramírez (`20221020138`)
* Steven Navarro Parrales (`20221020048`)
* Juan Diego Grajales Castillo (`20221020128`)

---

## 1. Ficha Técnica, Dimensiones y Alcance del Estudio

* **Matriz de datos cruda:** $\mathbf{X} \in \mathbb{R}^{n \times p}$ con:
  * $n = 50\,000$ observaciones (clientes simulados / filas).
  * $p = 30$ variables registradas (columnas).
* **Naturaleza del problema:** Análisis del comportamiento de gasto, solvencia económica, hábitos de pago y perfilamiento de riesgo crediticio para una cartera de tarjetas de crédito.
* **Propósito metodológico:** Integrar de forma secuencial los fundamentos teóricos y algebraicos de las **Semanas 1 a 6** (clasificación de escalas, calidad de datos, distribuciones univariadas, estandarización, análisis bivariado objetivo, el concepto de outlier multivariante, estructura de covarianzas, distancia de Mahalanobis, pruebas formales de hipótesis y acondicionamiento matricial para PCA y Clustering).

---

## 2. Taxonomía y Clasificación de Variables (Módulo 1 — S01 y S02)

### 2.1. Criterio Epistemológico: Almacenamiento en R vs. Escala de Medición Real
Uno de los principales errores en analítica de datos es asumir que el tipo de datos asignado por el software (`character`, `numeric`, `integer`) define la naturaleza estadística de la variable. Siguiendo la taxonomía de **Everitt & Hothorn**, la clasificación real depende de si las operaciones aritméticas (promedio, varianza, coeficientes de regresión) poseen interpretación métrica directa y si existe una distancia constante entre niveles.

```
Total de variables (p = 30)
├── Cualitativas / Categóricas (4)
│   ├── Nominales (3): Customer_ID (identificador puro), Gender (2 niveles), Occupation (6 niveles)
│   └── Ordinal (1): Card_Type (5 niveles con jerarquía: Basic < Silver < Gold < Platinum < Signature)
└── Cuantitativas (26)
    ├── Continuas de escala monetaria y gastos (15): Ingreso, cupo, balances y 7 rubros de consumo
    ├── Continuas - Ratios e Índices acotados [0,1] (2): Payment_Ratio, Credit_Utilization
    └── Discretas - Conteos y Puntajes de escala de razón (9): Age, Card_Age_Months, Monthly_Transactions,
        EMI_Count, International_Transactions, Rewards, Mobile_App_Login, Credit_Score
```

### 2.2. Aclaraciones Metodológicas Cruciales para la Sustentación:
1. **Reclasificación de `Card_Type`:** No es nominal. Posee un orden intrínseco de jerarquía y beneficios financieros (`Basic` < `Silver` < `Gold` < `Platinum` < `Signature`). Aunque no haya una distancia métrica idéntica entre escalones, es formalmente **cualitativa ordinal**.
2. **Variables cuantitativas de rango corto (`Age`, `EMI_Count`, `Mobile_App_Login`, `International_Transactions`):** Tienen pocos valores únicos o son conteos discretos acotados por la naturaleza humana o el periodo mensual, pero poseen cero absoluto y distancia constante (la diferencia entre 2 y 3 compras en cuotas es exactamente la misma magnitud que entre 4 y 5). Son tratadas formalmente como **cuantitativas discretas**, no como factores categóricos.
3. **Mecanismo generador y Diccionario de negocio (`por_que`):** Cada distribución atípica tiene una justificación económica:
   * *Variables de gasto y saldo:* Tienen asimetría pronunciada a la derecha ($\text{asimetría} > 2.5$) porque la mayoría de personas gasta montos moderados y una élite financiera concentra transacciones muy elevadas.
   * *Avances en efectivo (`Cash_Advance_Amount`) y transacciones internacionales:* Son **variables infladas en cero** (más del 50% de clientes nunca las utiliza), generando una masa puntual discreta en cero combinada con una cola continua a la derecha.
   * *Ratio de pago (`Payment_Ratio`):* Única variable con **asimetría negativa (hacia la izquierda)**; está acotada superiormente en 1.00 (casi nadie prepaga más del 100% de su saldo) y la mayoría de la cartera paga el total facturado.

---

## 3. Auditoría de Calidad e Integridad de la Matriz (Módulo 2 — S02)

Para garantizar la reproducibilidad antes de cualquier modelado, se aplicó la lista de chequeo de 4 fases sobre la matriz $\mathbf{X}$:

1. **Inspección en Crudo (`readLines`):** Se confirmó delimitador por coma (`,`), separador decimal punto (`.`) y cabecera en primera fila. Carga limpia mediante `read.csv(..., stringsAsFactors = FALSE)`.
2. **Diagnóstico Multivariante de Datos Faltantes:**
   * Celdas vacías (`is.na`): **$0$ de $1\,500\,000$ celdas** ($0.00\%$).
   * Filas completas (`complete.cases`): **$50\,000$ de $50\,000$ filas** ($100.00\%$).
   * *Defensa técnica:* Se evaluó a nivel celda y a nivel vector fila $\mathbf{x}_i \in \mathbb{R}^p$. Al estar $100\%$ completa, no se requirió elegir entre imputación, exclusión por pares (*pairwise*) o eliminación de casos completos (*listwise*).
3. **Verificación de Duplicados e Identificadores:**
   * Duplicados exactos de fila: **$0$**.
   * Identificadores `Customer_ID` repetidos: **$0$** (los $50\,000$ clientes son únicos).
4. **Consistencia de Rangos y Valores Centinela (`summary`):**
   * Ninguna variable de dinero o conteo presentó valores negativos ni códigos centinela (`-99`, `999`).
   * `Age`: rango $[18, 69]$ años (adultos en edad productiva/financiera).
   * `Payment_Ratio`: rango $[0.10, 1.00]$ (conforme a política de pago mínimo vs. pago total).
   * `Credit_Utilization`: rango $[0.10, 0.95]$ (la entidad bancaria bloquea transacciones antes de superar el $95\%-100\%$ del cupo).
5. **Distribución Categórica:**
   * `Gender`: Masculino $50.2\%$, Femenino $49.8\%$ (perfectamente balanceado).
   * `Card_Type`: `Gold` es la moda ($35.8\%$), `Silver` ($27.1\%$), `Platinum` ($18.4\%$), `Basic` ($13.4\%$) y `Signature` es el segmento élite minoritario ($5.3\%$).
   * `Occupation`: Dominada por `Private Employee` ($45.4\%$), seguido de `Government Employee` ($16.2\%$), `Self-Employed` ($14.7\%$), `Business Owner` ($10.3\%$), `Student` ($7.4\%$) y `Retired` ($6.0\%$).

---

## 4. Análisis Univariado y Decisión del Ancho de Clase (Módulos 3 y 8 — S01, S03 y S04)

### 4.1. Calibración de Cortes en Histogramas (`breaks`)
Se demostró cómo la elección del número de intervalos $k$ altera la interpretación visual de la densidad empírica de los datos:
* **Sub-suavizado / Underfitting (`breaks = 5`):** Agrupa en barras demasiado anchas, ocultando la asimetría real y haciendo que distribuciones sesgadas parezcan casi uniformes.
* **Sobre-ajustado / Overfitting (`breaks = 60`):** Cada barra cubre intervalos minúsculos, introduciendo dientes de sierra y vacíos artificiales que responden a ruido muestral.
* **Regla de Sturges ($k = 1 + \log_2(n)$):** Para $n = 50\,000$, arroja $k = 1 + \log_2(50\,000) \approx 16.6 \rightarrow 17$ cortes. Permite captar con precisión la moda, la dispersión central y las colas sin distorsión.

### 4.2. Estimación por Densidad de Kernel (KDE) (Módulo 8)
* **Solución al origen arbitrario:** El histograma depende tanto de $k$ como del punto de inicio del primer intervalo. La densidad de kernel elimina el efecto de las fronteras sumando funciones de densidad locales (kernels gaussianos):
  $$\hat{f}_h(x) = \frac{1}{nh} \sum_{i=1}^n K\left(\frac{x - X_i}{h}\right)$$
* **Selección del ancho de banda ($h$):** Se utilizó la regla óptima de Silverman (`bw.nrd0(x)`), que escala $h$ según la desviación estándar y el rango intercuartílico ($h = 0.9 \min(s, RIC/1.34) n^{-1/5}$).
* **Limitación identificada en variables infladas en cero:** El kernel gaussiano asume soporte continuo suave; al aplicarse sobre variables como `Cash_Advance_Amount` (donde más del $50\%$ de los clientes está exactamente en $0$), la curva derrama densidad sobre valores negativos ficticios y suaviza artificialmente una masa discreta puntual.

---

## 5. Detección Univariada de Atípicos y Cercas de Tukey (Módulo 4 — S03)

### 5.1. Criterio del Rango Intercuartílico (RIC)
Para cada una de las 26 variables numéricas se calcularon los Cinco Números de Tukey y las cercas:
$$\text{Límite Inferior} = Q_1 - 1.5 \cdot RIC \qquad \text{Límite Superior} = Q_3 + 1.5 \cdot RIC$$

### 5.2. Hallazgo Fundamental: Asimetría Estructural vs. Datos Anómalos
La aplicación de la regla de Tukey reveló una clara división dicotómica en la cartera:
1. **Variables de Gasto y Deuda (8% al 19% de "atípicos"):**
   * En `Monthly_Spending` ($Q_1 = \$26\,646$, $Q_3 = \$54\,500$, $RIC = \$27\,854$), los límites de Tukey son $[-\$15\,135, \$96\,281]$.
   * El límite inferior da negativo (imposible para un gasto).
   * Más de $4\,000$ clientes superan los $\$96\,281$ (llegando hasta $\$691\,688$).
   * *Conclusión de defensa:* **Estos valores no son errores de captura ni deben ser eliminados**. Reflejan la cola pesada natural de la distribución del ingreso y gasto (tipo Pareto / Log-Normal). La regla de Tukey asume simetría cercana a la normal; en distribuciones fuertemente asimétricas, rotula incorrectamente valores legítimos como atípicos.
2. **Variables Simétricas o Acotadas (0% al 2% de atípicos):**
   * `Credit_Utilization` ($0\%$), `Age` ($0\%$), `Monthly_Transactions` ($0.5\%$), `Credit_Score` ($0.2\%$). Al estar acotadas por diseño o hábitos biológicos, la regla de Tukey opera según lo teóricamente previsto.

---

## 6. Comparación Multivariada Estandarizada ($Z$-Scores) (Módulo 5 — S03)

### 6.1. La Paradoja de las Escalas Dispares
* La desviación estándar de `Annual_Income` es de aproximadamente $\$1\,248\,000$, mientras que la de `Credit_Utilization` es de apenas $0.19$.
* La razón de dispersión entre la variable más dispersa y la menos dispersa supera las **$6.5 \times 10^6$ veces**.
* Graficar las 26 variables en su escala nativa vuelve el gráfico ilegible: 24 variables se comprimen en una línea invisible sobre el cero.

### 6.2. La Estandarización
Transforma cada valor a desviaciones estándar respecto a su media marginal:
$$z_{ij} = \frac{x_{ij} - \bar{x}_j}{s_j} \implies \bar{z}_j = 0, \quad s^2(z_j) = 1$$
* **Propiedad clave:** La estandarización **no normaliza la forma** (una variable sesgada sigue sesgada en $Z$), pero homogeneiza el eje vertical, permitiendo comparar la longitud relativa de las colas.
* **Ranking de Colas Máximas ($Z_{\max}$):**
  * `Avg_Transaction_Value` alcanza hasta $+12.3\sigma$.
  * `Travel_Spending`, `Fuel_Spending` y `Cash_Advance_Amount` superan $+8\sigma$ a $+10\sigma$.
  * `Monthly_Transactions` y `Credit_Score` tienen su valor máximo acotado a $+2.5\sigma$.

---

## 7. Análisis Bivariado Objetivo, el "Punto Imposible" y las Seis Geometrías (Módulo 6 — S01, S03, S04)

### 7.1. Criterio Objetivo de Selección de Pares
En lugar de inspeccionar arbitrariamente los $\binom{26}{2} = 325$ pares numéricos posibles, se establecieron dos criterios matemáticos de jerarquización:
1. **Pares Numéricos ($|r|$ de Pearson):**
   * El par no contable más fuerte de la cartera es `Annual_Income` y `Credit_Limit` ($r = 0.974$).
   * Las variables determinantes del riesgo (`Credit_Score`): `Payment_Ratio` ($r = 0.767$) y `Credit_Utilization` ($r = -0.599$).
2. **Pares Numérico-Categóricos ($\eta^2$ de ANOVA):**
   $$\eta^2 = \frac{SS_{\text{entre}}}{SS_{\text{total}}}$$
   * `Annual_Income ~ Occupation`: $\eta^2 = 0.637$ (la ocupación explica el **$63.7\%$** de la varianza del ingreso).
   * `Credit_Score ~ Occupation`: $\eta^2 = 0.0006$ (la ocupación explica menos del **$0.06\%$** del puntaje de riesgo).
   * `Annual_Income ~ Gender` y `Credit_Score ~ Gender`: $\eta^2 < 0.0001$ ($0.01\%$, irrelevante).

> **Hallazgo Maestro de Negocio:**  
> **El nivel socioeconómico no define la solvencia moral/crediticia.** Ganar mucho dinero (`Annual_Income`) o tener un cupo alto (`Credit_Limit`) tiene correlación prácticamente nula con el puntaje crediticio ($r \approx 0.03$). Lo que determina el puntaje es exclusivamente el hábito de pago (`Payment_Ratio`) y la disciplina de endeudamiento relativo (`Credit_Utilization`).

### 7.2. Construcción Demostrativa del "Punto Imposible"
Demuestra que **un individuo puede ser perfectamente normal en cada variable por separado y, simultáneamente, ser un valor atípico imposible en el espacio conjunto**.

```
                           Punto Imposible 1: Comportamiento vs. Riesgo
           Credit_Score
                ▲
            800 ┼                                      •••••• (Nube real: r = 0.767)
                │                                ••••••
            650 ┼                          ••••••
                │                    ••••••
            500 ┼              ••••••
            460 ┼───────[X] CLIENTE IMPOSIBLE
                │       (Normal univariado en Score [441, 825] y en Payment [0.11, 1.47],
                │        pero viola por completo la correlación conjunta)
                └───────┼──────────────────────────┼────────────────► Payment_Ratio
                       0.2                        0.95
```

* **Caso 1 (Comportamiento de Pago):** Cliente hipotético con `Payment_Ratio = 0.95` y `Credit_Score = 460`.
  * *Univariado:* $0.95 \in [0.11, 1.47]$ (Normal según Tukey) y $460 \in [441, 825]$ (Normal según Tukey).
  * *Multivariado:* En la práctica, quien paga el $95\%$ de su saldo jamás tiene un score de 460; el punto cae en una región vacía del plano 2D.
* **Caso 2 (Capacidad Financiera):** Cliente hipotético con `Annual_Income = $3\,000\,000` y `Credit_Limit = $200`.
  * *Univariado:* Ambos valores caen dentro de las cercas de Tukey de sus ejes.
  * *Multivariado:* Con $r = 0.974$, la política bancaria jamás asignaría un cupo de $\$200$ a un cliente de $\$3$ millones.

### 7.3. Taxonomía de las Seis Formas Bivariadas
El informe tipifica las relaciones de la cartera en 6 geometrías con consecuencias analíticas:
1. **Lineal directa fuerte ($r = 0.974$):** `Annual_Income` vs. `Credit_Limit` (banda ascendente delgada; duplicidad de información).
2. **Lineal inversa ($r = -0.599$):** `Credit_Utilization` vs. `Credit_Score` (a mayor saturación de cupo, caída continua de calificación).
3. **Independencia en bloque rectangular ($r = 0.032$):** `Annual_Income` vs. `Credit_Score` (nube que llena uniformemente un rectángulo; el dinero no predice el riesgo).
4. **Efecto Cuña / Techo físico:** `Credit_Limit` vs. `Outstanding_Balance` (la nube forma un triángulo inferior; nadie puede deber más de su cupo aprobado).
5. **Efecto Embudo / Heterocedasticidad:** `Monthly_Spending` vs. `Payment_Ratio` ($r \approx 0$, pero la varianza de pago se reduce drásticamente en gastos extremos; a montos gigantescos nadie mantiene ratio 1.0).
6. **Escalón Ordinal:** `Card_Type` vs. `Credit_Limit` (las medianas suben ordenadamente de `Basic` a `Signature`, confirmando la consistencia del orden categórico).

---

## 8. Estructura Multivariada Conjunta (Módulo 7 — S01, S03 y S05)

### 8.1. Matriz de Correlación $\mathbf{R}$ y sus Propiedades Matemáticas
Se verificaron rigurosamente las tres propiedades teóricas exigidas (Everitt & Hothorn):
* Diagonal unitaria: $r_{jj} = 1, \quad \forall j$.
* Simetría exacta: $r_{jk} = r_{kj}$.
* Espectro semidefinido positivo: todos los valores propios $\lambda_j \ge 0$.
  * **Valor propio mínimo hallado:** $\lambda_{\min} \approx 0.0001$.
  * *Defensa técnica:* Un autovalor tan próximo a cero **no es un fallo numérico**; es la prueba irrefutable de que existen relaciones casi linealmente dependientes (redundancia severa entre balances y entre gastos totales y recompensas).

### 8.2. Herramientas Visuales Multivariantes
* **Mapa de Calor con Clustering Jerárquico (`corrplot` + `hclust`):** Agrupa variables en bloques homogéneos, evidenciando el clúster de "Capacidad Financiera y Saldos" separado del clúster de "Riesgo y Cumplimiento".
* **Coordenadas Paralelas Tricolor (12 variables estandarizadas):** Segmentadas por terciles de `Credit_Score` (Verde: Alto, Gris: Medio, Rojo: Bajo). Muestra cómo las trayectorias rojas colapsan en el suelo en `Payment_Ratio`, mientras que en variables de saldo e ingreso los tres colores se cruzan caóticamente (demostrando que el saldo bruto no segrega riesgo).
* **Matriz de Dispersión (`pairs`) en 3 Paneles:** Diagonal con histogramas de distribución, triángulo inferior con nubes de puntos semitransparentes y triángulo superior con correlación cuyo tamaño tipográfico es proporcional a $|r|$.

---

## 9. Geometría Multivariada: Centroide y Distancia de Mahalanobis (Módulo 9 — S06)

### 9.1. Definición y Optimización del Centroide
Se verificó analítica y computacionalmente la identidad del centro de gravedad de la nube:
$$\bar{\mathbf{x}} = \frac{1}{n} \mathbf{X}' \mathbf{1}$$
* **Prueba de minimización cuadrática:** Se comprobó que el vector de medias $\bar{\mathbf{x}}$ satisface:
  $$\bar{\mathbf{x}} = \arg\min_{\mathbf{a}} \sum_{i=1}^n \|\mathbf{x}_i - \mathbf{a}\|^2$$
  Cualquier perturbación en $\pm 0.01\sigma$ sobre $\bar{\mathbf{x}}$ incrementa monótonamente la suma de distancias euclidianas al cuadrado.

### 9.2. Falacia del Centro Único y Fragilidad ante Contaminación
1. **Centros Múltiples por Segmento:** El centroide global de `Credit_Limit` ($\approx \$446\,758$) **no representa a nadie en la realidad**: un cliente `Basic` tiene una media de $\$74\,073$ y un cliente `Signature` promedia $\$4\,114\,793$. La cartera tiene 5 centros locales distintos en el espacio financiero.
2. **Punto de Ruptura y Robustez:**
   * *Error puntual (1 fila corrupta, $0.002\%$):* La media apenas se desplaza un $0.02\%$. El gran tamaño de muestra ($n=50\,000$) absorbe el impacto.
   * *Error sistemático (250 filas con factor $\times 1000$, $0.5\%$ de la muestra):* La media aritmética colapsa y sube un $+50\%$. En contraste, la **mediana marginal** y la **media recortada al 10%** permanecen inmunes, demostrando empíricamente por qué la media clásica tiene un punto de ruptura asintótico nulo ($0\%$).

### 9.3. Distancia Euclidiana vs. Distancia de Mahalanobis
La distancia euclidiana tradicional asume ejes ortogonales con varianzas idénticas (métrica esférica). Si las variables están fuertemente correlacionadas, la métrica esférica falsea la distancia real:
$$d_M(\mathbf{x}_i) = \sqrt{(\mathbf{x}_i - \bar{\mathbf{x}})' \mathbf{S}^{-1} (\mathbf{x}_i - \bar{\mathbf{x}})}$$

* **Experimento demostrativo con clientes $A$ y $B$:**
  * Ambos se ubican exactamente a la misma distancia euclidiana del centroide ($d_E = 628\,000$).
  * Cliente $A$: $+0.5\sigma$ en Ingreso y $+0.5\sigma$ en Cupo (sigue la correlación $r=0.974$).
  * Cliente $B$: $+0.5\sigma$ en Ingreso y $-0.5\sigma$ en Cupo (contradice la correlación).
  * **Resultado:** $d_M(A) = 0.89$ vs. $d_M(B) = 3.32$. La distancia de Mahalanobis cuantifica que el cliente $B$ está casi **4 veces más lejos** de la densidad natural de la cartera que el cliente $A$.

### 9.4. Auditoría de Invertibilidad Matricial (`revisar()`)
Antes de calcular Mahalanobis sobre toda la cartera, se auditó la matriz de covarianzas $\mathbf{S}$. Para evitar que $\mathbf{S}$ fuera casi singular o inestable ($\det(\mathbf{S}) \approx 0$, número de condición explosivo), se excluyeron 5 variables redundantes y derivadas:
1. `Monthly_Spending` (suma algebraica exacta de las 7 categorías de consumo).
2. `Outstanding_Balance` ($r = 0.997$ con `Statement_Balance`).
3. `Reward_Points_Earned` ($r = 0.980$ con `Monthly_Spending`).
4. `Payment_Ratio` (cociente dependiente de pago y balance).
5. `Credit_Utilization` (cociente dependiente de saldo y límite).

### 9.5. Diagnóstico de Mahalanobis sobre las 21 Variables y el QQ-Plot $\chi^2$
* Con $p = 21$ variables no redundantes, bajo el supuesto de Normalidad Multivariante, las distancias al cuadrado se distribuyen teóricamente como:
  $$d_M^2 \sim \chi^2_p$$
* **Punto de corte teórico ($\alpha = 0.025$, cuantil 97.5% de $\chi^2_{21}$):** $35.48$.
* **Valores empíricos observados:** $4\,417$ clientes ($8.83\%$) superan el umbral teórico (más de 3.5 veces lo esperado bajo normalidad).
* **Interpretación del QQ-Plot:** Los cuantiles empíricos de $d_M^2$ se despegan bruscamente hacia arriba respecto a la recta de 45° a partir del percentil 85. Esto demuestra empíricamente que la nube multivariada de clientes posee colas mucho más pesadas que una distribución Gaussiana multidimensional.

---

## 10. Pruebas de Hipótesis e Inferencia Formal (Módulo 10)

### 10.1. Normalidad Univariada (Lilliefors y Shapiro-Wilk)
* **Hipótesis:** $H_0: X \sim \mathcal{N}(\mu, \sigma^2)$ vs. $H_1: X \nsim \mathcal{N}$.
* Se evaluaron `Credit_Score`, `Age`, `Annual_Income` y `Payment_Ratio`.
* **Resultado:** Todas las variables rechazan $H_0$ contundentemente con $p < 2.2 \times 10^{-16}$.
* **Defensa frente al Jurado (El efecto del gran tamaño muestral $n = 50\,000$):**
  La potencia estadística de los tests de bondad de ajuste es función directa de $n$. Con $50\,000$ observaciones, el error estándar es infinitesimal, por lo que el test detecta la más mínima desviación imperceptible (como una curtosis de $-0.1$ en `Credit_Score`) y rechaza $H_0$. Por ello, el criterio rector en grandes volúmenes de datos **no es el $p$-valor**, sino la magnitud de la asimetría y la inspección visual (histograma y QQ-plot).

### 10.2. Normalidad Multivariante de Mardia (Asimetría y Curtosis)
* **Hipótesis:** $H_0: \mathbf{X} \sim \mathcal{N}_p(\boldsymbol{\mu}, \boldsymbol{\Sigma})$.
* Se evaluó sobre una submuestra aleatoria de $m = 1\,500$ clientes (para evitar una matriz de distancias cruzadas $g_{ij}$ de $50\,000 \times 50\,000$ que exigiría 2.500 millones de celdas en RAM) sobre las 21 variables no redundantes:
  * **Asimetría de Mardia ($b_{1,p}$):** Estadístico $\approx 400\,000$, frente a grados de libertad esperados de $\approx 1\,771$. Rechaza $H_0$ con $p < 2.2 \times 10^{-16}$.
  * **Curtosis de Mardia ($b_{2,p}$):** Puntuación estándar $Z \approx 45.8$ desviaciones estándar por encima de lo esperado. Rechaza $H_0$ con $p < 2.2 \times 10^{-16}$.
* **Conclusión:** Se rechaza categóricamente la normalidad multivariante. La cartera crediticia no forma un elipsoide gaussiano puro.

### 10.3. Pruebas $t$ de Correlación Lineal
* Para los pares clave (`Annual_Income` - `Credit_Limit`, `Payment_Ratio` - `Credit_Score`, `Credit_Utilization` - `Credit_Score`), los estadísticos $t$ superan magnitudes de $150$ a $300$ con $p < 2.2 \times 10^{-16}$, confirmando que las asociaciones no provienen del azar del muestreo.

---

## 11. Acondicionamiento Matricial para PCA y Clustering (Módulo 11)

Como cierre del análisis exploratorio, se definió la estrategia matemática para alimentar los algoritmos de reducción de dimensión y segmentación de las siguientes semanas:

### 11.1. Matriz de Decisiones de Transformación
| Grupo de Variables | Variables | Condición Estadística | Transformación Matemática | Justificación |
|---|---|---|---|---|
| **Excluidas Numéricas (5)** | `Monthly_Spending`, `Outstanding_Balance`, `Reward_Points_Earned`, `Payment_Ratio`, `Credit_Utilization` | Colinealidad exacta o dependencia funcional ($r > 0.95$) | Ninguna (Descarte de la matriz activa) | Evitar singularidad en $\mathbf{S}$ e inflación espuria de componentes principales. |
| **Sesgadas / Colas Pesadas (13)** | `Annual_Income`, `Credit_Limit`, `Statement_Balance`, `Payment_Amount`, 7 rubros de consumo, `Avg_Transaction_Value`, `Cash_Advance_Amount` | Asimetría $|\text{Skew}| > 1.0$ (colas pesadas, dinero) | $\log(x + 1) + \text{scale}()$ | El logaritmo contrae la cola derecha y linealiza relaciones; el $+1$ estabiliza los ceros; `scale()` homogeneiza la varianza a 1. |
| **Simétricas / Acotadas (8)** | `Credit_Score`, `Age`, `Card_Age_Months`, `Monthly_Transactions`, `EMI_Count`, `International_Transactions`, `Reward_Points_Redeemed`, `Mobile_App_Login` | Asimetría $|\text{Skew}| \le 1.0$ o conteos acotados | $\text{scale}()$ únicamente | Centrado en media 0 y varianza 1 sin alterar la forma de la distribución. |
| **Cualitativas (4)** | `Customer_ID` (eliminar), `Gender` (dummy/factor), `Occupation` (dummy/factor), `Card_Type` (ordinal 1 a 5) | No numéricas | Codificación especializada / Variables ilustrativas | No entran directamente al PCA numérico clásico; se reservan para cruce con clusters. |

### 11.2. El Papel de las Variables Suplementarias
* `Payment_Ratio` y `Credit_Utilization` se excluyen de la construcción de las componentes de PCA para que la colinealidad no deforme los autovectores.
* Sin embargo, al ser las variables reina que explican el $85\%$ del riesgo crediticio, **se proyectan posteriormente como variables suplementarias / ilustrativas** sobre el plano factorial para interpretar y dar significado financiero a los clusters que se obtengan.

---

## 12. Banco de Preguntas Críticas para la Sustentación Oral

A continuación se presentan las preguntas más probables y difíciles que un profesor o jurado de estadística multidimensional formularía sobre este trabajo, junto con sus respuestas técnicas de defensa:

### P1: ¿Por qué reclasificaron `Card_Type` como ordinal si originalmente venía como texto, y por qué no convirtieron los conteos como `Age` o `EMI_Count` en factores?
> **Respuesta:** En R, `character` es simplemente el tipo de almacenamiento en memoria. Estadísticamente, la jerarquía `Basic` < `Silver` < `Gold` < `Platinum` < `Signature` refleja niveles crecientes de capacidad crediticia, y el Módulo 6 demostró que las medianas de cupo crecen monótonamente en ese mismo orden (Tendencia 6). Por tanto, es una variable cualitativa ordinal. Por otro lado, `Age` o `EMI_Count` son conteos de escala de razón: tienen cero absoluto y la distancia métrica entre unidades es idéntica y constante (pasar de 1 a 2 cuotas diferidas es el mismo incremento de carga financiera que pasar de 4 a 5). Tratarlas como factores destruiría su propiedad métrica y aumentaría artificialmente la dimensionalidad de la matriz.

### P2: Si la regla de Tukey marcó un 15% de atípicos en `Monthly_Spending` y variables de gasto, ¿por qué no los eliminaron antes de calcular medias y correlaciones?
> **Respuesta:** Porque no son errores de captura ni fallos de digitación; son la expresión legítima de la asimetría positiva intrínseca de los datos económicos (distribuciones tipo Log-normal o Pareto). La regla de Tukey ($1.5 \cdot RIC$) fue derivada asumiendo distribuciones simétricas similares a la normal (donde solo marca un $0.7\%$). En distribuciones de colas pesadas, el límite inferior de Tukey da negativo (absurdo para un gasto) y corta artificialmente la cola derecha. Eliminar esos clientes significaría amputar al segmento de clientes más valiosos y de mayor consumo del banco, sesgando todo el análisis posterior.

### P3: ¿Por qué afirman categóricamente que el ingreso y el límite de crédito no predicen el riesgo del cliente?
> **Respuesta:** Porque la evidencia bivariada y multivariada es contundente: la correlación de Pearson entre `Annual_Income` y `Credit_Score` es de apenas $r = 0.032$, y entre `Credit_Limit` y `Credit_Score` es de $r = 0.035$. En el diagrama de dispersión y la matriz `pairs`, la nube forma un bloque rectangular uniforme (independencia). Además, en el ANOVA bivariado, `Occupation` explica el $63.7\%$ de la varianza del ingreso ($\eta^2 = 0.637$), pero apenas el $0.06\%$ del score crediticio. Lo que predice el riesgo no es el volumen de dinero disponible, sino la proporción de deuda que se paga a tiempo (`Payment_Ratio`, $r = 0.767$) y el nivel de apalancamiento relativo (`Credit_Utilization`, $r = -0.599$).

### P4: Explique qué es el "Punto Imposible" y qué demuestra sobre la estadística multivariada frente a la univariada.
> **Respuesta:** El punto imposible demuestra que la normalidad marginal en cada variable por separado no garantiza la normalidad conjunta en el espacio multidimensional. Diseñamos un cliente con `Payment_Ratio = 0.95` y `Credit_Score = 460`. Al verificar variable por variable, ambos valores caen cómodamente dentro de las cercas de Tukey de sus respectivos ejes. Sin embargo, al cruzar ambas variables, con una correlación positiva de $r = 0.767$, ningún cliente en la historia del banco que liquide el $95\%$ de su saldo tiene un puntaje de riesgo tan precario. El punto cae en un vacío absoluto fuera de la elipse de covarianza. Esto prueba que el análisis univariado es ciego a la estructura de interdependencia multivariada.

### P5: ¿Por qué la distancia Euclidiana es insuficiente en este dataset y por qué la distancia de Mahalanobis sí funciona?
> **Respuesta:** La distancia euclidiana asume que las variables son ortogonales (no correlacionadas) y tienen igual dispersión (curvas de nivel esféricas). En nuestro dataset, `Annual_Income` y `Credit_Limit` tienen $r = 0.974$. Si tomamos dos clientes $A$ y $B$ equidistantes del centroide en línea recta ($d_E = 628\,000$), donde $A$ tiene ingreso alto y cupo alto (a favor de la nube) y $B$ tiene ingreso alto pero cupo mínimo (en contra de la nube), la distancia euclidiana los considera exactamente iguales de "raros". La distancia de Mahalanobis, al incorporar la inversa de la matriz de covarianzas $\mathbf{S}^{-1}$, deforma el espacio según los ejes principales de la elipse, revelando que el cliente $B$ tiene un $d_M$ casi 4 veces mayor que $A$. Mahalanobis mide la distancia estadística respetando la correlación real entre variables.

### P6: ¿Por qué tuvieron que excluir 5 variables numéricas antes de calcular Mahalanobis y correr el PCA?
> **Respuesta:** Por problemas de multicolinealidad exacta y singularidad matricial. `Monthly_Spending` es la suma lineal exacta de los 7 rubros de consumo individuales; incluir la suma junto con sus sumandos genera una combinación lineal perfecta ($r=1$). De igual forma, `Outstanding_Balance` tiene $r = 0.997$ con `Statement_Balance`. Mantener estas redundancias hace que la matriz de covarianzas tenga un determinante cercano a cero y un valor propio casi nulo ($\lambda_{\min} \approx 0.0001$), disparando el número de condición a infinito e impidiendo invertir numéricamente $\mathbf{S}$ de forma estable.

### P7: ¿Por qué las pruebas de Lilliefors y Shapiro-Wilk rechazaron la normalidad en todas las variables, incluso en `Credit_Score` que se ve simétrica?
> **Respuesta:** Porque a un tamaño de muestra de $n = 50\,000$ (o $n=5\,000$ en la submuestra de Shapiro-Wilk), el error estándar del estadístico de prueba tiende a cero y la potencia de la prueba tiende a 1. A este nivel de muestra masiva, cualquier desviación infinitesimal de la curtosis teórica (incluso fluctuaciones de orden $10^{-3}$) arroja un $p$-valor inferior a $2.2 \times 10^{-16}$. Rechazar la hipótesis nula no significa que la variable no tenga utilidad práctica o que esté corrupta; significa que la prueba formal es hipersensible al tamaño muestral y que el analista debe priorizar el diagnóstico gráfico (QQ-plots e histogramas con Sturges) y la magnitud de la asimetría por encima del $p$-valor.

### P8: ¿Qué demostró la prueba de normalidad multivariante de Mardia y por qué se usó una submuestra de 1.500 observaciones?
> **Respuesta:** La prueba de Mardia evalúa la asimetría ($b_{1,p}$) y curtosis ($b_{2,p}$) generalizadas. Rechazó contundentemente la normalidad multivariante ($p < 2.2 \times 10^{-16}$), demostrando que la nube conjunta de 21 dimensiones tiene colas mucho más densas que un elipsoide gaussiano, lo cual explica por qué el $8.83\%$ de los clientes supera el cuantil $\chi^2$ del $97.5\%$ en Mahalanobis en lugar del $2.5\%$ teórico. Se usó una submuestra de $m = 1\,500$ porque calcular la matriz de distancias generalizadas $g_{ij} = (\mathbf{x}_i - \bar{\mathbf{x}})' \mathbf{S}^{-1} (\mathbf{x}_j - \bar{\mathbf{x}})$ para los $50\,000$ clientes requeriría una matriz de $50\,000 \times 50\,000$ ($2.5 \times 10^9$ celdas de coma flotante), lo que saturaría la memoria RAM de cualquier servidor convencional.

### P9: ¿Por qué aplicaron $\log(x+1)$ antes de estandarizar en variables como gastos o ingresos para la etapa de PCA?
> **Respuesta:** Porque el PCA clásico está basado en maximizar varianzas y encontrar combinaciones lineales de variables. Cuando una variable tiene una asimetría extrema ($> 2.5$) y observaciones a más de $10\sigma$ de la media, esas pocas observaciones extremas distorsionan y dominan enteramente la primera componente principal, convirtiéndola en un eje de outliers en lugar de un resumen de la estructura general. La transformación logarítmica contrae la cola derecha, simetriza la distribución y estabiliza la varianza. Se añade $+1$ ($\log(x+1)$) porque variables como avances en efectivo o compras internacionales tienen valores legítimos en cero, y $\log(0)$ está indefinido.

### P10: ¿Qué ventajas y desventajas prácticas tiene la estimación de densidad por Kernel frente al Histograma?
> **Respuesta:** La gran ventaja de Kernel es que elimina el problema del origen arbitrario de los intervalos del histograma, produciendo una función de densidad continua $\hat{f}(x)$ óptima para observar modas y densidades suaves. Su desventaja principal, demostrada en el Módulo 8, ocurre cuando los datos son variables infladas en cero (`Cash_Advance_Amount`, `International_Transactions`): el suavizado del kernel gaussiano es ciego a la cota física en cero y derrama densidad hacia el lado negativo ficticio, además de aplanar una masa de probabilidad que en la realidad es un pulso discreto masivo. En esas variables, el histograma con cortes exactos o una tabla de frecuencias discretas resulta más transparente.

---

## 13. Conclusión Ejecutiva Final
El análisis desarrollado demuestra un entendimiento integral de la estructura del dataset:
1. La integridad de los datos es total ($100\%$ completos y sin errores de captura).
2. Las colas largas y "atípicos" observados son de origen económico estructural, no ruido.
3. El riesgo financiero se gobierna por la conducta de pago, no por la magnitud del ingreso.
4. La matriz contiene redundancias funcionales que debieron ser depuradas para garantizar la estabilidad de distancias multidimensionales (Mahalanobis) e inferencias formales (Mardia).
5. La matriz queda rigurosamente condicionada y justificada para abordar con éxito las etapas de **Análisis de Componentes Principales (PCA)** y **Clustering Multidimensional**.
