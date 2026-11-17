# Taller 2 — ¿Son distintos estos grupos? El informe para su cliente

**Estadística Multidimensional · 26158 · grupo 020‑81**
**Sábado 7 de noviembre de 2026 · sin clase en vivo · entrega en Moodle**
**Por equipos · sobre el dataset propio · un `.Rmd` y su `.html` tejido**
**Entrega:** lunes 9 de noviembre de 2026, 11:59 p. m., en Moodle. Un envío por equipo.

---

Primero lean las notas `Hotelling_Grupos_Distintos.html`, en orden y con R abierto. Ahí le
respondimos a una secretaría de educación dos preguntas:

- El Atlántico está por debajo del país a 0,42 desviaciones. La diferencia es real y moderada, y no
  separa: 31,5 de cada 100 de sus estudiantes superan la mediana del país.
- Hombres y mujeres tienen el mismo nivel y un perfil distinto: la distancia es de 0,49 desviaciones.
  Pero con los cinco puntajes se acierta el sexo en 61,8 de cada 100 estudiantes, cuando diciendo
  siempre «mujer» se acierta en 56,1.

Ahora hagan lo mismo **para el cliente de su caso de negocio**. El taller no se aprueba por el valor
p. Se aprueba por **responder las tres preguntas —¿es real?, ¿es grande?, ¿separa?— y decirle al
cliente qué decide con eso**. Cada punto lleva **tres frases**: qué ven, qué significa para el
cliente y qué decide él.

---

## 1. El encargo (0,5)

En un párrafo: **quién es su cliente y qué dos comparaciones le sirven**.

- **Una muestra:** un grupo de su base frente a una referencia. La referencia puede ser el promedio
  de toda su base, una meta del cliente o un valor publicado; digan de dónde sale.
- **Dos muestras:** dos grupos de su base entre sí.

Usen entre 3 y 6 variables numéricas y digan por qué esas.

## 2. Una muestra: ¿el grupo es distinto de la referencia? (1,2)

1. La gráfica de diferencias variable por variable.
2. **¿Es grande?** La distancia $D$: a cuántas desviaciones está el grupo de la referencia.
3. **¿Es real?** La probabilidad de que sea azar, con la función `hotelling_1()` de las notas. Si
   quieren, repitan la simulación de los grupos al azar (sección 5.3 de las notas).
4. **¿Separa?** Qué parte del grupo queda del otro lado de la referencia (como el 31,5 del
   Atlántico), y un caso concreto de su base que lo muestre.

## 3. Dos muestras: ¿los dos grupos son distintos? (1,2)

1. La gráfica de diferencias variable por variable. ¿Es diferencia de **nivel** (todo sube) o de
   **perfil** (unas suben y otras bajan)?
2. La distancia $D$ y la probabilidad de que sea azar, con `hotelling_2()`, y la comprobación con
   `manova()`. Muestren **dos casos concretos** con un resultado parecido y perfiles opuestos, como los
   dos estudiantes que sacaron 100 de global.
3. **¿Separa?** El acierto al clasificar con `MASS::lda()`, **comparado con el acierto de adivinar
   siempre el grupo más grande**.

## 4. ¿Qué viaja con el grupo? (0,8)

Escojan una de sus dos comparaciones y busquen **una variable que viaje con el grupo** y pueda
explicar parte de la diferencia, como el estrato con el Atlántico. Muestren si la diferencia sigue
cuando comparan casos parecidos en esa variable.

## 5. Las tres preguntas y la decisión (1,3)

Una tabla con sus dos comparaciones —y, si quieren, iris como referencia— con tres columnas:
**¿es real?, ¿es grande? (D), ¿separa?** Y debajo, **la decisión para el cliente** en tres o cuatro
frases, como la conclusión de las notas.

---

## Rúbrica — sobre 5,0

| Criterio | Puntos |
|---|--:|
| Encargo claro: cliente, dos comparaciones y la referencia justificada | 0,5 |
| Una muestra: diferencias, distancia, si es azar, y cuánto separa con un caso concreto | 1,2 |
| Dos muestras: nivel o perfil con dos casos, distancia comprobada con manova(), y acierto contra adivinar | 1,2 |
| Una variable que viaja con el grupo, revisada | 0,8 |
| Tabla de las tres preguntas y decisión para el cliente | 1,3 |
| **Total** | **5,0** |

**Descuentos:**
- Concluir solo con la probabilidad de azar o el valor p («es significativo, entonces son distintos»), −0,5.
- Un resultado sin ninguna frase de lectura, −0,2 cada uno.
- Afirmar que el grupo **causa** la diferencia, −0,3.

*Estadística Multidimensional · 26158 · periodo 2026‑3 · Jhon Alejandro Varón Robayo · Universidad Distrital.*
