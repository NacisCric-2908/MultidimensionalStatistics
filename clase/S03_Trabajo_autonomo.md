# Trabajo autónomo — Semana 3

**Estadística Multidimensional · 26158 · grupo 020‑81**
**Del sábado 22 al domingo 30 de agosto de 2026 · HTA ≈ 6 horas**

> Esta semana tuvo **una sola sesión** —el lunes 17 fue festivo—, y dos cierres en 24 horas.
> El orden de abajo es el orden en que hay que hacerlo, no una lista de opciones.

---

## Lo que cierra, con hora

| | Cuándo | Qué | Modalidad |
|---|---|---|---|
| 1 | **sáb 22, al terminar la clase** | **Propuesta de datasets** — candidato 1 verificado | grupal |
| 2 | **dom 23, 11:59 p. m.** | **Taller 1** | **individual** |
| 3 | **dom 23, 11:59 p. m.** | Candidatos 2, 3 y 4 de la propuesta | grupal |
| 4 | **lun 24** | *(el docente publica el dataset asignado a cada grupo)* | — |
| 5 | **dom 30, 11:59 p. m.** | **Taller de la semana 3** — sobre lo visto el sábado 22 | individual |

---

## 1. Sábado en la tarde y domingo — el Taller 1 (≈ 2,5 h)

Es lo primero porque es lo que tiene nota y **cierra mañana**. Enunciado en Moodle desde el 10 de
agosto, sobre `encuesta_sucia.csv`.

Se entregan **los dos archivos**: `[EM][Taller1][sucódigo].Rmd` y `[EM][Taller1][sucódigo].html`.
**Si no teje, no se recibe** — está en la rúbrica, y no es una amenaza sino una consecuencia:
un `.Rmd` que no compila no es reproducible, y la reproducibilidad es la mitad de lo que se
evalúa en esta asignatura.

Antes de subir, tres verificaciones de treinta segundos cada una:

- ¿Todas las rutas son **relativas**? Un `C:/Users/…` cuesta puntos.
- ¿Corre **desde cero** en una sesión limpia? *Session → Restart R and Run All Chunks*.
- ¿Están los dos archivos, y con el nombre exacto?

## 2. Domingo — cerrar la propuesta del grupo (≈ 1,5 h, repartida)

Candidatos 2, 3 y 4, con su ficha y la salida de la verificación pegada. **No es trabajo de una
sola persona**: cuatro candidatos son cuatro búsquedas, y el responsable de entregas sube el PDF
completo.

Recuerden lo que decide todo, y no es el tema:

> Si la **matriz de correlación es casi toda cero**, no hay nada latente que encontrar y el PCA de
> la unidad 6 no va a decir nada. La `|r| máxima` que imprime la función de verificación debería
> pasar de **0,5**. Por debajo de 0,3, ese candidato no sirve aunque cumpla los siete requisitos.

## 3. Entre semana — repasar la sesión (≈ 1 h)

Volver sobre `S03_Clase_Visualizacion.Rmd` y **correrlo entero**, no leerlo. Tres cosas que hay
que poder hacer sin mirar:

1. Sacar los cinco números de una variable y decir dónde termina el bigote.
2. Explicar por qué `boxplot(vino)` no sirve y `boxplot(scale(vino))` sí.
3. Contar de nuevo la historia del punto rojo: **normal en cada variable, imposible en conjunto**.

## 4. Terminar la actividad de clase (≈ 1 h)

`S03_Actividad_en_clase.Rmd`, los cinco puntos. Los puntos 4 y 5 son los que más rinden: el 4
porque van a tener que construir el ejemplo ustedes, y el 5 porque la respuesta es la razón de
ser de la asignatura.

Lo que resuelvan aquí es la base del **taller de la semana 3**, que cierra el domingo 30.

---

## Lectura

**Everitt & Hothorn**, *An Introduction to Applied Multivariate Analysis with R*, capítulo 2
(«Looking at Multivariate Data: Visualisation»), secciones 2.1 y 2.2. Son doce páginas y cubren
exactamente lo del sábado. La sección 2.3, sobre la matriz de dispersión, es la sesión del 29 —
si alcanzan, léanla también y llegan con ventaja.

---

## Cómo pedir ayuda

Sigue rigiendo el protocolo de la asignatura, y no es un formalismo: sin las tres cosas no se
puede diagnosticar nada a distancia.

1. El **código exacto** que corrió.
2. El **error completo, copiado como texto** — no en foto.
3. El `str()` del objeto con el que está trabajando.

Por el grupo de WhatsApp. Los fines de semana se responde, pero no a las 11 de la noche del
domingo: si van a preguntar por el Taller 1, pregunten el sábado.

---

## Lo que viene

- **Lunes 24 · sesión 5** — densidad kernel y diagrama de dispersión. Esa mañana se publica el
  dataset asignado a cada grupo, y la sesión ya se trabaja con él.
- **Sábado 29 · sesión 6** — matriz de dispersión y matriz de correlación visual: los 55 gráficos
  del sábado convertidos en un solo objeto.
