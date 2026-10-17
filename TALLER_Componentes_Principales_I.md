# Taller — ¿Un número o varios? El resumen para su cliente

**Estadística Multidimensional · 26158 · grupo 020‑81**
**Por equipos · sobre el dataset propio · un `.Rmd` y su `.html` tejido**
**Fecha de entrega y peso:** los define el docente al publicarlo.

---

En clase le respondimos a una institución si podía asignar tutorías con un solo número. El puntaje
global guardaba 52,9 de cada 100 partes de la información, y por usarlo se quedaban sin tutoría de
escritura 968 de los 2 097 estudiantes que la necesitaban.

Ahora hagan lo mismo **para el cliente de su caso de negocio**: el que definieron en la sustentación
del primer corte. El taller no se aprueba por correr `prcomp()`. Se aprueba por **decirle al cliente
qué gana y qué pierde si resume sus datos**, y mostrarlo con números. Cada punto lleva **tres
frases**: qué ven, qué significa para el cliente y qué decide él.

---

## 1. El encargo (0,5)

En un párrafo: **quién es su cliente, qué decisión toma y con qué variables numéricas la toma hoy**.
Escojan entre 4 y 10 variables numéricas de su base, y digan por qué esas.

## 2. ¿Se repiten? (0,8)

Hagan la matriz de correlaciones de esas variables, en gráfico. Respondan:

- ¿Qué variables se repiten más?
- ¿Cuál va más sola?
- ¿Tiene sentido resumirlas? Si casi todas las correlaciones están cerca de cero, **díganlo**: ésa
  también es una respuesta para el cliente.

## 3. ¿Estandarizar? (0,7)

Muestren la desviación de cada variable. **Decidan antes de correr** si estandarizan y justifíquenlo.
Después corran el PCA **de las dos maneras** y muestren cuánto cambia la información que guarda la
primera componente.

## 4. Cuánta información guarda (1,0)

Con su decisión del punto 3:

1. La gráfica de cuánta información guarda cada componente, con el acumulado.
2. ¿Cuánta guarda la primera? ¿Cuántas hacen falta para pasar de 80 de cada 100?
3. Escriban, en una frase para el cliente, qué significa esa cifra.

## 5. Qué mide cada una (1,0)

Grafiquen los pesos de las dos o tres primeras componentes. **Pónganle nombre a cada una** mirando
qué variables mandan, y expliquen el nombre. Recuerden que el signo es arbitrario: se lee qué manda y
si las variables van en la misma dirección o en contra.

## 6. El costo para su cliente (1,0)

Ésta es la pregunta de la clase aplicada a su negocio: **si su cliente decidiera con un solo número,
¿a quién o a qué dejaría por fuera?**

- Definan un grupo que al cliente le importe: los peores, los mejores, los de riesgo, los que cumplen
  una condición.
- Cuenten cuántos de ese grupo encuentra la primera componente, y **cuántos se le escapan**.
- Cierren con la decisión: ¿le basta un número, o necesita reportar dos o tres?

---

## Rúbrica — sobre 5,0

| Criterio | Puntos |
|---|--:|
| Encargo claro: cliente, decisión y variables justificadas | 0,5 |
| Matriz de correlaciones leída: qué se repite, qué va sola, si tiene sentido resumir | 0,8 |
| Decisión de estandarizar tomada antes de correr, y comparada después | 0,7 |
| Información por componente, con el acumulado y la frase para el cliente | 1,0 |
| Componentes con nombre, sostenido en sus pesos | 1,0 |
| Costo contado en casos concretos, y la decisión para el cliente | 1,0 |
| **Total** | **5,0** |

**Descuentos:** un resultado sin ninguna frase de lectura, −0,2 cada uno. Hablar de «autovalores» o
«vectores propios» sin decir qué significan para el cliente, −0,2. Afirmar que una componente
**demuestra** una causa o una habilidad, −0,3.

*Estadística Multidimensional · 26158 · periodo 2026‑3 · Jhon Alejandro Varón Robayo · Universidad Distrital.*
