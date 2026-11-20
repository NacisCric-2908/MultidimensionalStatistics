# Tema adicional 1 — Análisis de correspondencias: ¿qué categorías van juntas?

**Estadística Multidimensional · 26158 · grupo 020‑81**
**Equipo:** Jefferson, Pulido, Steven, Johan
**Entrega:** un `.Rmd` y su `.html` tejido, y una exposición de 15 minutos · **Fecha:** sábado 14 de noviembre de 2026, en clase (el `.Rmd` y el `.html` se suben a Moodle antes de la clase)
**Para qué sirve:** recuperar nota · **Qué nota recupera:** la define el docente

---

## La pregunta

Todo lo que vimos en el semestre trabaja con **variables numéricas**: puntajes, montos, cantidades. Pero
muchas decisiones de un cliente se toman con **categorías**: estrato, tipo de colegio, región, nivel
educativo de los padres, tipo de producto, canal de venta.

El **análisis de correspondencias** responde, para categorías, la misma pregunta que el biplot
respondió para números: **¿qué va con qué?** Produce un mapa donde las categorías que aparecen juntas
más de lo que se esperaría por azar quedan cerca.

Ustedes van a **aprender la técnica por su cuenta y explicársela al curso**, con un cliente y una
decisión, como hemos hecho todo el semestre.

## Los datos

- **Su dataset**, si tiene al menos **dos variables de categorías** con 3 o más niveles cada una, que le
  importen a su cliente.
- Si no las tiene, usen **`PruebaSaber1.csv`**, con un cliente que ustedes definan (una secretaría de
  educación, una institución, una fundación de becas). Por ejemplo: `FAMI_ESTRATOVIVIENDA` con
  `FAMI_EDUCACIONMADRE`, o con `INST_ORIGEN`, o con `ESTU_METODO_PRGM`.

Antes de analizar, limpien: categorías vacías, «No aplica», «No sabe» y errores como la fila corrida
de estrato. **Digan cuántos casos quedan por fuera y por qué.**

## Lo que deben hacer

### 1. El encargo (0,4)
Quién es el cliente, qué decisión toma y por qué le importa saber qué categorías van juntas.

### 2. La tabla cruzada (0,8)
La tabla de conteos de las dos variables y la tabla de **porcentajes por fila**. ¿Qué se ve a simple
vista? Hagan una prueba de independencia (`chisq.test()`) y léanla en palabras: ¿las dos variables
tienen que ver entre sí, o no?

### 3. El mapa (1,2)
```r
library(FactoMineR)
ca <- CA(tabla, graph = FALSE)
ca$eig                       # cuánta información guarda cada dimensión
plot(ca)                     # el mapa de categorías
```
- ¿Cuánta información guarda el mapa de dos dimensiones?
- Pónganle **nombre a cada dirección**, como en el biplot: qué significa ir a la derecha y qué significa
  ir hacia arriba.
- ¿Qué categorías de una variable quedan cerca de qué categorías de la otra?

### 4. Lo que el mapa no dice (0,8)
- La cercanía en el mapa es **asociación**, no causa. Busquen **una variable que viaje** con la
  asociación (como el estrato con el computador en clase) y digan cómo podría explicarla.
- ¿Hay alguna categoría con pocos casos que esté moviendo el mapa? Revisen su contribución
  (`ca$row$contrib`, `ca$col$contrib`).

### 5. Más de dos variables (0,6)
Repitan con **tres o cuatro variables de categorías** usando `MCA()`. ¿Se mantiene lo que vieron con dos?

### 6. La recomendación (0,6)
Cuatro frases para el cliente: qué va con qué, qué tan fuerte es, qué decide con eso y **qué no
sabemos todavía**.

### 7. La exposición (0,6)
Quince minutos para el curso: qué pregunta responde la técnica, en qué se parece al biplot y en qué se
diferencia, y su resultado contado para el cliente. **Sin fórmulas en las diapositivas.**

---

## Rúbrica — sobre 5,0

| Criterio | Puntos |
|---|--:|
| Encargo: cliente, decisión y variables justificadas | 0,4 |
| Tabla cruzada, porcentajes por fila y prueba de independencia leída en palabras | 0,8 |
| Mapa con la información que guarda, direcciones con nombre y cercanías leídas | 1,2 |
| Variable que viaja con la asociación y categorías que mueven el mapa | 0,8 |
| Análisis con tres o cuatro variables (`MCA()`) comparado con el de dos | 0,6 |
| Recomendación en cuatro frases y «qué no sabemos todavía» | 0,6 |
| Exposición clara para el curso, conectada con el biplot | 0,6 |
| **Total** | **5,0** |

**Descuentos:**
- Un resultado sin ninguna frase de lectura: −0,2 cada uno.
- Decir que una categoría **causa** otra porque quedan cerca en el mapa: −0,3.
- Borrar casos o categorías sin decir cuántos ni por qué: −0,5.
- Un `.html` que no abre o no trae las gráficas: −0,5.

**Para empezar a leer:** la ayuda de `FactoMineR::CA` y la del paquete `factoextra`
(`fviz_ca_biplot()`), que ya está instalado.

*Estadística Multidimensional · 26158 · periodo 2026‑3 · Jhon Alejandro Varón Robayo · Universidad Distrital.*
