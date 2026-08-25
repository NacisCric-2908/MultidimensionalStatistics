# Trabajo autónomo — semana del 24 al 29 de agosto

**Estadística Multidimensional · 26158 · grupo 020‑81**
**Entra en el taller de la semana, que cierra el domingo 30 de agosto, 11:59 p. m.**

> **A partir de esta semana todo se hace sobre el dataset que le asignaron.** No hay que buscar más
> datos ni verificar nada: el conjunto está definido y no se cambia.

---

## 1 · Cargarlo bien — 30 min

Antes de graficar nada, el dataset tiene que entrar a R **sin errores y con los tipos correctos**.
Es lo del Taller 1, ahora sobre datos propios.

```r
datos <- read.csv("mi_dataset.csv")     # o read.csv2() si el separador es ";"

dim(datos)
str(datos)
colSums(is.na(datos))
```

**Tres cosas tienen que ser ciertas** antes de seguir: las numéricas son `num` o `int` —no
`chr`—, las categóricas tienen los niveles que deberían, y usted sabe cuántos faltantes hay y dónde.

---

## 2 · Densidad kernel sobre tres variables — 45 min

Escoja **tres variables numéricas** de su conjunto. Para cada una:

```r
h <- bw.nrd0(datos$mi_variable)
plot(density(datos$mi_variable, bw = h), lwd = 2,
     main = paste("mi_variable · h =", round(h, 3)))
rug(datos$mi_variable)
```

Y después **repita con $h/3$ y con $3h$**, los tres en la misma figura o uno al lado del otro.

**Escriba dos frases por variable:**

1. ¿Qué se ve con el $h$ de Silverman que **no** se ve con $3h$?
2. ¿Lo que aparece con $h/3$ es **estructura o ruido**? ¿Cómo lo decide?

> **La segunda pregunta no tiene respuesta automática**, y ése es el punto. Se decide mirando si el
> pico se sostiene al cambiar un poco el $h$, y si tiene sentido en el tema del que hablan los datos.

---

## 3 · Dispersión y correlación — 45 min

1. **Todas las correlaciones**, redondeadas:

   ```r
   num <- datos[, sapply(datos, is.numeric)]
   round(cor(num, use = "pairwise.complete.obs"), 2)
   ```

2. Identifique **el par con la correlación más alta en valor absoluto** y **el par con la más baja**.

3. **Grafique los dos pares.** Uno al lado del otro.

4. Y ahora lo que importa, en un párrafo: **¿el gráfico confirma lo que dice el número?**
   Miren específicamente si en el par de $r$ alto la nube es realmente una recta, o si hay
   un atípico haciendo el trabajo — como en el conjunto 3 de Anscombe.

---

## 4 · La pregunta que se entrega — 20 min

Escriba, en cinco líneas:

> **¿Cuáles dos variables de mi conjunto creo que están midiendo lo mismo, y por qué?**

No se trata de repetir el $r$ más alto. Se trata de decir **qué tienen en común esas dos variables
en el tema del que hablan los datos** — ingreso y gasto, área y precio, temperatura y consumo.

> **Por qué esta pregunta.** En la unidad 6, el PCA va a buscar exactamente eso: variables que
> repiten información. Quien llegue en octubre con una respuesta pensada desde agosto va a entender
> el primer componente principal en cinco minutos. Quien no, va a ver una tabla de números.

---

## Lectura

**Everitt & Hothorn**, capítulo 2 — *Looking at Multivariate Data: Visualisation*.
Las secciones de diagramas de dispersión y estimación de densidad. Son unas quince páginas.

---

## Fechas

| Cuándo | Qué |
|---|---|
| **Sábado 29 de agosto** · 6–8 · Aula 404 | Sesión 6: matriz de dispersión, matriz de correlación visual y coordenadas paralelas. **Traiga su dataset cargado en R.** |
| **Domingo 30 de agosto** · 11:59 p. m. | Cierra el taller de la semana, que incluye los puntos 2, 3 y 4 de arriba. |
