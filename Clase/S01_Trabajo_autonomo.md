# Trabajo autónomo — Semana 1

**Estadística Multidimensional · 26158 · grupo 020‑81**
**Semana del 3 al 8 de agosto de 2026 · HTA ≈ 6 horas**
**Entrega: antes de la sesión del lunes 10 de agosto, 6 a. m.**

---

## Por qué esta semana pesa más de lo que parece

La semana 2 abre con datos faltantes, mensajes de error e importación de archivos, y **cierra con
el Taller 1, que vale el 10 %**. Todo eso da por sabido lo de esta semana. Si llega el lunes sin
R instalado y sin haber escrito un `data.frame`, la semana 2 se pierde y el taller se entrega mal.

---

## 1. Instalación (≈ 1 h, obligatorio)

Antes de la próxima sesión hay que tener funcionando:

1. **R** — <https://cran.r-project.org/> (instalar primero R, después RStudio).
2. **RStudio Desktop** — <https://posit.co/download/rstudio-desktop/>
3. Crear un **proyecto** para la asignatura: `File → New Project… → New Directory → New Project`,
   con el nombre `EstadisticaMultidimensional_2026-3`.
4. Instalar los paquetes del semestre, una sola vez:

```r
install.packages(c("MVA", "ggplot2", "GGally", "mvtnorm", "psych"))
```

5. Verificar que quedó bien. Este bloque debe correr sin errores:

```r
library(MVA)
data(iris)
dim(iris)
```

**Si no tiene computador propio o la instalación falla:** cree una cuenta gratuita en
<https://posit.cloud> y trabaje ahí. Funciona en el navegador y sirve para toda la asignatura.
Avísele al docente por correo antes del domingo si no logró ninguna de las dos cosas.

---

## 2. Lectura (≈ 1,5 h)

**Everitt, B. & Hothorn, T. (2011).** *An Introduction to Applied Multivariate Analysis with R*.

- **Capítulo 1, secciones 1.1 a 1.3** — qué es un dato multivariante y cómo se organiza.

Al leer, buscar respuesta a tres preguntas concretas:

1. ¿Qué es la matriz de datos $\mathbf{X}$ y qué representan sus filas y columnas?
2. ¿Qué diferencia hay entre una variable **continua**, una **ordinal** y una **nominal**?
   ¿Por qué importa esa distinción a la hora de analizar?
3. ¿Por qué el libro insiste en que los datos faltantes son un problema *multivariante*
   y no sólo un hueco en una columna?

*(La pregunta 3 es exactamente el tema con el que abre la clase del lunes.)*

---

## 3. Práctica (≈ 2,5 h)

### 3.1 Repaso guiado

Vuelva a escribir —**escribir, no copiar y pegar**— los ejemplos de
`S01_Clase_Objetos_R.Rmd`, secciones «Vectores» y «El `data.frame`».
Copiar y pegar no sirve: la sintaxis se aprende con los dedos.

### 3.2 Su propia matriz de datos

Construya un `data.frame` con **al menos 10 observaciones y 4 variables numéricas**, de un tema
que le interese: jugadores de un equipo, canciones de una lista, municipios, computadores en
venta, lo que sea. Los datos pueden ser reales o inventados, pero **coherentes**.

Sobre él:

1. `dim()`, `str()`, `summary()`, `head()`.
2. La media y la desviación estándar de cada variable.
3. La matriz de correlación completa.
4. Un histograma de una variable y un diagrama de dispersión de dos.
5. `pairs()` de las cuatro.

Y escriba **tres conclusiones**, una de cada tipo:

- una **univariada** (sobre cómo se distribuye una variable),
- una **bivariada** (sobre la relación entre dos),
- una **multivariada** (algo que sólo se ve mirando la matriz de correlación o el `pairs()`,
  y que no se vería mirando las variables de a una).

> La tercera es la que importa. Es la que separa esta asignatura de Estadística I.

### 3.3 Provocar dos errores a propósito

Ejecute estas dos líneas, lea el mensaje **completo** y escriba con sus palabras qué está diciendo:

```r
mean(c(1, 2, "tres"))
library(estePaqueteNoExiste)
```

Leer errores es una habilidad del curso, no un accidente. Se retoma el lunes.

---

## Entrega

Un archivo `.R` o `.Rmd` llamado
`[EM][S01][código].R` — por ejemplo `[EM][S01][20221020056].R` —
con el código, las conclusiones como comentarios y su nombre y código al inicio.

**Por Moodle**, en la tarea «Semana 1 — Trabajo autónomo», **antes del lunes 10 de agosto a las 6 a. m.**
Nada de correo ni de WhatsApp: si no está subido a Moodle, no está entregado.

**No es calificable.** Se revisa y se devuelve con comentarios: es la última entrega sin nota
antes del Taller 1.

---

## Lo que viene

| | |
|---|---|
| **Lunes 10 ago, 6–8** | Datos faltantes. Sistema de ayuda. Errores y advertencias. |
| **Sábado 15 ago, 6–8** | Importación y exportación de archivos. **Taller 1 (10 %)**. |
| **Lunes 17 ago** | **Festivo** — no hay clase. |
