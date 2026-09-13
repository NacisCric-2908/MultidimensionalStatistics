# Estadística Multidimensional — Análisis Exploratorio Integral y Diagnóstico Multivariado

Repositorio del proyecto de la asignatura **Estadística Multidimensional**, enfocado en el análisis riguroso, diagnóstico de calidad, geometría multivariante, pruebas de hipótesis y preparación matricial sobre el dataset **Synthetic Credit Card Customer Behavior** ($n = 50\,000$ observaciones, $p = 30$ variables).

El proyecto integra de forma secuencial y acumulativa los contenidos desarrollados a lo largo de las **Semanas 1 a 6 (S01 a S06)**.

---

## 👥 Autores

* **Oscar Manuel Contreras Gacha** — `20221020052`
* **Juan Pablo Sarmiento Ramírez** — `20221020138`
* **Steven Navarro Parrales** — `20221020048`
* **Juan Diego Grajales Castillo** — `20221020128`

---

## 📁 Estructura del Repositorio

```
.
├── data/
│   ├── bronze/                                    # Datos crudos e inmutables (fuente única de verdad)
│   │   └── synthetic_credit_card_customer_behavior_dataset.csv
│   ├── silver/                                    # Datos procesados / limpios (regenerables)
│   └── gold/                                      # Matrices finales acondicionadas para PCA/Clustering
│
├── Entrega/
│   ├── analisis_synthetic_credit_card.Rmd         # Documento maestro reproducible en R Markdown (11 módulos)
│   └── analisis_synthetic_credit_card.html        # Render HTML completo del reporte técnico
│
├── Clase/                                         # Material de apoyo, talleres y sesiones de clase (S01 a S06)
│
├── resumen_analisis_synthetic_credit_card.md      # Guía técnica detallada y banco de preguntas de sustentación
├── requerimientos.md                              # Lista de chequeo metodológica por semanas del curso
├── requirements.txt                               # Dependencias de entorno Python
└── README.md                                      # Descripción general del repositorio
```

---

## 🔬 Estructura Metodológica del Análisis (11 Módulos)

El análisis maestro en [`Entrega/analisis_synthetic_credit_card.Rmd`](Entrega/analisis_synthetic_credit_card.Rmd) está estructurado en 11 módulos interdependientes:

1. **Módulo 1 (S02) — Inspección Previa e Importación Reproducible:** Verificación con `readLines`, dimensiones de la matriz $\mathbf{X} \in \mathbb{R}^{50\,000 \times 30}$, taxonomía formal de Everitt & Hothorn (reclasificación de `Card_Type` como ordinal, justificación de conteos como cuantitativos) y diccionario de negocio (`por_que`).
2. **Módulo 2 (S02) — Auditoría y Calidad de la Matriz:** Verificación de completitud ($0\%$ `NA`, $100\%$ casos completos), ausencia de duplicados de fila o identificador, validación de reglas de negocio y distribución de frecuencias.
3. **Módulo 3 (S01 & S03) — Análisis Univariado y Calibración de Histogramas:** Comparación de cortes (`breaks = 5`, `breaks = 17` de Sturges, `breaks = 60`) sobre las 26 variables numéricas de forma individual.
4. **Módulo 4 (S03) — Boxplots y Detección de Atípicos (Tukey):** Cálculo de 5 números de Tukey y cercas ($Q \pm 1.5 \cdot RIC$). Identificación de que el $8\%-19\%$ de outliers en gastos responde a asimetría estructural económica y masa en cero, no a errores de captura.
5. **Módulo 5 (S03) — Comparación Multivariada Estandarizada:** Diagnóstico de la disparidad de escalas ($\Delta \sigma \approx 6.5 \times 10^6$), boxplots comparativos sin estandarizar vs. estandarizados ($Z$-scores) y ranking de colas extremas ($Z_{\max}$).
6. **Módulo 6 (S01, S03 & S04) — Análisis Bivariado Objetivo, el "Punto Imposible" y 6 Geometrías:**
   * Criterio objetivo de selección mediante $|r|$ de Pearson y $\eta^2$ de ANOVA.
   * **Hallazgo clave:** El nivel de ingresos/cupo no predice el riesgo ($r \approx 0.03$, $\eta^2 < 0.001$), mientras que el hábito de pago sí (`Payment_Ratio` $r=0.767$, `Credit_Utilization` $r=-0.599$).
   * Demostración analítica y gráfica de los **2 Clientes Imposibles** (normales univariadamente en Tukey, pero atípicos multivariados).
   * Tipificación de 6 patrones bivariados: lineal directa, lineal inversa, bloque rectangular, cuña/techo, embudo y escalón ordinal.
7. **Módulo 7 (S01, S03 & S05) — Estructura Multivariada Conjunta:** Verificación matemática de la matriz $\mathbf{R}$ (diagonal unitaria, simetría, valores propios $\lambda \ge 0$), mapa de calor jerárquico (`hclust`), coordenadas paralelas tricolor por riesgo y matriz de dispersión `pairs` de 3 paneles.
8. **Módulo 8 (S04) — Estimación por Densidad de Kernel (KDE):** Superación del origen arbitrario de los histogramas, calibración del ancho de banda $h$ con Silverman (`bw.nrd0`) y diagnóstico de limitaciones ante variables infladas en cero.
9. **Módulo 9 (S06) — Vector de Medias, Centroide y Distancia de Mahalanobis:**
   * Formulación matricial $\bar{\mathbf{x}} = \frac{1}{n}\mathbf{X}'\mathbf{1}$ y prueba de minimización cuadrática.
   * Heterogeneidad grupal de centros (el promedio global de cupo no representa a ningún nivel de tarjeta).
   * Robustez ante fallos sistemáticos vs. puntuales (estabilidad de la mediana marginal).
   * Demostración euclidiana vs. Mahalanobis (clientes $A$ y $B$).
   * Auditoría de invertibilidad (`revisar()`), descarte de 5 variables redundantes y cálculo de $d_M^2$ con QQ-plot de $\chi^2_{21}$ (8.83% de atípicos por no-normalidad).
10. **Módulo 10 — Pruebas de Hipótesis Formales:** Normalidad univariada (Lilliefors y Shapiro-Wilk) con discusión crítica sobre la potencia muestral en $n = 50\,000$, normalidad multivariante de Mardia ($b_{1,p}$ y $b_{2,p}$, rechazo contundente con $p < 2.2 \times 10^{-16}$) y significancia de correlaciones lineales.
11. **Módulo 11 — Acondicionamiento para PCA y Clustering:** Matriz de transformaciones ($\log(x+1) + \text{scale}()$ para variables sesgadas, $\text{scale}()$ para simétricas), lista de 21 variables activas retenidas y reserva de ratios clave como variables suplementarias/ilustrativas.

---

## 🚀 Cómo Reproducir el Proyecto

### Opción 1: R / RStudio (Recomendada)

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/NacisCric-2908/MultidimensionalStatistics.git
   cd MultidimensionalStatistics
   ```
2. Abrir R o RStudio.
3. Instalar los paquetes necesarios de R:
   ```R
   paquetes <- c("corrplot", "MASS", "nortest", "knitr", "rmarkdown")
   install.packages(setdiff(paquetes, rownames(installed.packages())))
   ```
4. Renderizar el documento maestro:
   ```R
   rmarkdown::render("Entrega/analisis_synthetic_credit_card.Rmd")
   ```
   *El resultado generado se guardará en `Entrega/analisis_synthetic_credit_card.html`.*

### Opción 2: Entorno Python (Opcional para scripts auxiliares)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 📚 Documentos de Consulta y Sustentación

* **Guía Completa de Sustentación:** [`resumen_analisis_synthetic_credit_card.md`](resumen_analisis_synthetic_credit_card.md)  
  *Contiene el resumen ejecutivo de los 11 módulos, fórmulas matemáticas, estadísticas exactas y un **banco de 10 preguntas críticas de sustentación oral con respuestas técnicas**.*
* **Reporte Maestro R Markdown:** [`Entrega/analisis_synthetic_credit_card.Rmd`](Entrega/analisis_synthetic_credit_card.Rmd)
* **Reporte Compilado (HTML):** [`Entrega/analisis_synthetic_credit_card.html`](Entrega/analisis_synthetic_credit_card.html)
* **Checklist de requerimientos semanales:** [`requerimientos.md`](requerimientos.md)
