# Guion de la sustentación — «¿Más rico, más seguro?»

**Equipo 02 · Corte 2 · 8 minutos de presentación + 5 de preguntas**

Cuatro partes de unos 2 minutos. A ritmo tranquilo son unas 130 palabras por minuto: cada parte tiene
alrededor de 250. Los nombres son una propuesta; cámbienlos si quieren, pero cada uno debe poder
responder sobre **todas** las láminas (el profesor pregunta a cualquiera sobre cualquier parte, y «eso lo
hizo otro» baja la nota de todos).

| Persona | Láminas | Qué cuenta | Termina en |
|---|---|---|---|
| Oscar | 1 y 2 | La creencia y el problema | 1:45 |
| Juan Pablo | 3, 4 y 5 | Preparar la ficha para que la prueba sea justa | 3:45 |
| Steven | 6, 7 y 8 | La prueba y su costo | 6:00 |
| Juan Diego | 9 y 10 | La tarjeta, el mapa y la decisión | 8:00 |

**Reglas para el ensayo**

- No lean la lámina: la lámina muestra el número, ustedes lo explican.
- Hablen del negocio, no de R. Si dicen «componente», díganlo una vez como «un resumen de la ficha».
- Nunca digan que el ingreso «causa» o «no causa» el riesgo: digan que **van en direcciones distintas**.
- Si el profesor interrumpe, respondan corto y sigan. Tengan presente en qué minuto termina cada parte.

---

## Oscar · láminas 1 y 2 (0:00 a 1:45)

**Lámina 1 — ¿Más rico, más seguro? (0:45)**

Buenos días. Nuestro cliente es la Gerencia de Riesgo de Crédito de un banco con 50.000 tarjetas. Cada
mes decide a quién subirle el cupo, a quién ascender de tarjeta y a quién vigilar para que no caiga en
mora. Y lo hace, como muchos bancos, con una idea en la cabeza: el cliente que más gana es el más seguro.
Por eso el cupo y la tarjeta suben con el ingreso, como en esta escalera de Basic a Signature, y la
vigilancia se va a los clientes pequeños. Nosotros pusimos esa idea a prueba con los datos. Como no hay datos de mora,
el riesgo lo medimos con el puntaje de crédito.

**Lámina 2 — Su cartera usa el doble del cupo y paga menos que el mercado (1:00)**

¿Por qué importa ahora? Porque comparamos esta cartera con el mercado de tarjetas de India, con cifras
del Banco de la Reserva, de SBI Card y del Banco Mundial. Sus clientes usan el 43 % de su cupo; el
mercado, el 21 %. Solo el 35 % paga su saldo completo, contra el 87 %. La cartera es simulada, así que estas cifras no son el
tamaño exacto del problema, pero sí su dirección: hay más riesgo del normal. Y si el riesgo está
creciendo, hay que saber dónde buscarlo. La creencia dice: en los clientes de menor ingreso.
Juan Pablo les cuenta cómo preparamos los datos para poner eso a prueba.

---

## Juan Pablo · láminas 3, 4 y 5 (1:45 a 3:45)

**Lámina 3 — La ficha suma dos veces el mismo dinero (0:40)**

Antes de probar nada, revisamos la ficha del cliente: 26 columnas numéricas. Cinco no traían información
nueva. El gasto total es la suma exacta de las siete categorías de gasto. El saldo pendiente repite el
saldo facturado. Los puntos ganados salen del gasto. Y la proporción pagada y el uso del cupo son
divisiones entre otras columnas. Nos quedamos con 21. Esas dos últimas no las botamos: explican el 95 %
del puntaje y las usamos al final para leer el riesgo.

**Lámina 4 — No borramos a nadie (0:40)**

No hay faltantes, duplicados ni valores imposibles. Con la distancia de Mahalanobis, que mira todas las
columnas a la vez, encontramos 1.641 clientes raros, el 3,3 %. Los tres más lejanos gastan en todo menos en una cosa: combustible, compras en línea o
viajes casi en cero. Son casos reales, no errores, así que no se corrige ninguno y no se borra ninguno. Y
fue bueno no borrarlos: su puntaje mediano es 573, contra 639 del resto.

**Lámina 5 — En rupias, el ingreso tapa todo (0:40)**

La última decisión antes de la prueba es la escala. El ingreso varía en más de un millón de rupias; las
compras a cuotas, en menos de dos. Si resumimos en rupias, el primer resumen guarda 95,5 de cada 100
partes de la información, pero es el ingreso con otro nombre: la prueba estaría amañada a favor del
ingreso. Por eso pasamos los montos a logaritmo y medimos todo con la misma regla. Así el primer
resumen guarda 50,1 de cada 100 partes, y lo construyen las 21 columnas.
Steven les muestra qué pasó con la creencia.

---

## Steven · láminas 6, 7 y 8 (3:45 a 6:00)

**Lámina 6 — Ganen lo que ganen, 20 de cada 100 tienen el peor puntaje (0:45)**

Primera evidencia. Dividimos a los clientes en cinco grupos por ingreso y contamos cuántos de cada grupo
están en el 20 % de peor puntaje. Si la creencia fuera cierta, los de menor ingreso tendrían muchos más.
No es así: son unos 20 de cada 100 en todos los grupos, desde el de menor ingreso hasta el de mayor. El
ingreso y el cupo van juntos (0,98), pero el puntaje no se parece a ninguna columna: como mucho, 0,17.

**Lámina 7 — La ficha dice dos cosas que no tienen que ver entre sí (0:45)**

El análisis de componentes principales resume la ficha en pocos números. Nos quedamos con dos, porque
son los que necesita la Gerencia. El primero es el tamaño: cuánto dinero hay en juego. Guarda la mitad de
la información de la ficha, 50,1 de cada 100 partes, y lo forman el cupo, el ingreso y el saldo. El
segundo es el riesgo: guarda poco, 5,3, pero es el único que ve el riesgo, y lo forman el puntaje, los
avances en efectivo y las tarjetas nuevas. Fíjense en los pesos: el ingreso pesa cero en el riesgo, y el
puntaje casi cero en el tamaño. Son dos cosas distintas.

**Lámina 8 — Si vigila por tamaño, 8 de cada 10 en riesgo se escapan (0:45)**

¿Cuánto le cuesta al banco la creencia? Si escoge a quién vigilar por tamaño, es decir, por ingreso,
cupo y gasto, y toma al 20 % más grande, de los 10.046 clientes con peor puntaje encuentra a menos de dos
de cada diez. Se le escapan 8.214. Es lo mismo que escoger al azar. Con el resumen de riesgo, en cambio,
encuentra a 6.580.
Juan Diego les cuenta qué pasa con la tarjeta y qué recomendamos.

---

## Juan Diego · láminas 9 y 10 (6:00 a 8:00)

**Lámina 9 — Signature ordena el cupo, no el riesgo (0:55)**

Lo mismo pasa con la tarjeta. La categoría ordena
perfecto el cupo: de 66 mil rupias en Basic a más de cuatro millones en Signature. Pero en cada categoría
hay entre 17 y 21 de cada 100 clientes con el peor puntaje: Signature no es más segura que Basic. A la
derecha está el mapa de la ficha, el biplot: las flechas de dinero van todas juntas hacia la derecha, y
el puntaje va solo, en ángulo recto, a 88 grados. Y cuando miramos a los clientes en ese mapa no aparecen
grupos: el riesgo sube poco a poco, sin un punto natural de corte. Por eso el corte lo tiene que poner la
Gerencia.

**Lámina 10 — El ingreso dice cuánto está en juego, no quién va a pagar (1:05)**

Esa es nuestra respuesta. Proponemos un corte: 560 puntos o menos, una desviación por debajo del
promedio. Ahí hay 8.301 clientes, que deben el 21,6 % de todo el saldo de la cartera. Dentro de ellos, el tamaño decide el orden: 3.998 son clientes grandes y concentran el 85,6 % de
ese saldo. Son justo los que la creencia daba por seguros, y a ellos va primero la llamada del gestor. Los
4.303 pequeños reciben mensajes y oferta de refinanciación. Lo que cambia para el banco: no subir el cupo
ni ascender de tarjeta sin mirar el puntaje, y vigilar por puntaje, no por ingreso ni por categoría. Lo
que no sabemos: no hay mora real, la cartera es simulada, y vemos con qué va el riesgo, no qué lo causa. En una frase: el ingreso dice cuánto está en juego,
no quién va a pagar. Gracias.

---

## Preguntas probables

Cualquiera de los cuatro puede recibir cualquiera de estas. Respondan corto y con la cifra.

**Las variables (decisión 1)**

- **¿Por qué sacaron la proporción pagada y el uso del cupo, si son las que más explican el riesgo?**
  Porque son divisiones entre columnas que ya están (pago entre saldo, saldo entre cupo). Juntas
  explican el 95 % del puntaje (R² = 0,95): son sus ingredientes. Las usamos como variables
  suplementarias: el eje de riesgo se correlaciona −0,59 con la proporción pagada y +0,47 con el uso del cupo.
- **¿Qué pasa si usan las 26?** Una columna se repite exacta (la matriz tiene una dirección con varianza
  prácticamente cero). El eje de tamaño sale idéntico (correlación 1,00, Módulo 19).

**Atípicos (decisión 2)**

- **¿Cómo definieron «raro»?** Distancia de Mahalanobis, con logaritmo, por encima del percentil 99 de
  una chi-cuadrado. Son 1.641.
- **¿Por qué no borrarlos?** Porque no son errores (0 valores imposibles) y tienen más riesgo: puntaje
  mediano 573 contra 639, y pagan el 57 % de su saldo contra el 85 %. Quitarlos mueve las correlaciones
  como mucho 0,02. Además, 64 de cada 100 no tienen ningún dato extremo por separado: revisando columna
  por columna no se ven.
- **¿Qué hacen con ellos?** 760 ya están en la lista de seguimiento. Los otros 881 van a revisión de la cuenta.

**Estandarizar (decisión 3)**

- **¿Qué cambia si no estandarizan?** El primer resumen guarda 95,5 de cada 100, pero es el ingreso solo
  (peso 0,76). Estandarizando sin logaritmo guarda 48,0; con logaritmo, 50,1.
- **¿Por qué logaritmo?** Los montos tienen colas largas: unos pocos clientes enormes mandarían el resumen.

**¿Tiene sentido resumir? (decisión 4)**

- **¿Qué se repite y qué va solo?** 16 de las 21 columnas tienen una compañera con correlación mayor que
  0,6 (ingreso y cupo, 0,98). Van solos el puntaje, la edad, la antigüedad de la tarjeta y los avances
  (ninguno pasa de 0,17).

**Cuántas componentes (decisión 5)**

- **¿Por qué dos y no tres, si hay tres con autovalor mayor que 1?** El autovalor dice cuánta información
  guarda cada resumen, medida en columnas: mayor que 1 quiere decir que guarda más que una sola columna.
  El tercero es la edad, y no cambia ninguna decisión de la Gerencia. Elegimos por lo que necesita el
  cliente, no por la regla.
- **¿Por qué no ocho, para pasar del 80 %?** Porque nadie lee ocho números por cliente.
- **Si el segundo guarda solo 5,3, ¿para qué sirve?** Es el único que ve el riesgo: encuentra 6.580 de
  los 10.046 de peor puntaje; el primero, 1.832.

**Qué mide cada una (decisión 6)**

- **¿Cómo le pusieron nombre?** Por sus pesos. Tamaño: cupo e ingreso 0,30, saldo 0,29, y las 16 columnas
  de dinero entre 0,20 y 0,30; el puntaje, 0,01. Riesgo: puntaje −0,78, avances 0,49, antigüedad −0,34;
  el ingreso, 0,00.
- **¿El segundo eje demuestra que los avances causan riesgo?** No. Muestra que van juntos.

**Un solo número (decisión 7)**

- **¿Qué se pierde?** De los 10.046 clientes de peor puntaje, el resumen de tamaño deja escapar a 8.214
  (82 %), lo mismo que el azar.

**El mapa (decisión 8)**

- **¿Hay grupos o un continuo?** Un continuo: en el eje de riesgo hay un solo pico y ningún valle.
- **¿Y las tarjetas?** Se separan en tamaño (sus centros van de −2,97 a 4,44) y casi nada en riesgo
  (menos de 0,2). En cada tarjeta, ocupación o nivel de ingreso hay entre 17 y 21 de cada 100 en el peor 20 %.
- **¿Por qué 560?** Es una desviación por debajo del promedio del puntaje (629). Si hay menos gestores,
  se baja el corte. Zonas: A = 3.998, B = 4.303, sin seguimiento = 41.699.

**La decisión (decisión 9)**

- **Si al final usan el puntaje, ¿para qué el PCA?** Para dos cosas que el puntaje solo no da: mostrar
  que el riesgo no está en el tamaño (que es lo que contradice la creencia) y dar el eje de tamaño para
  ordenar la lista. La zona A tiene el 48 % de los clientes de la lista y el 85,6 % de su saldo.
- **¿Por qué no cortar en el eje de riesgo en vez del puntaje?** El eje de riesgo se parece al puntaje
  (−0,82), pero no es igual: con el mismo criterio, 2.384 de sus 8.195 cupos irían a clientes fuera del
  peor 20 %.
- **¿El riesgo que encuentra el eje de riesgo no es circular, si el puntaje está adentro?** En parte sí,
  y por eso la lista usa el puntaje directamente. El hallazgo no es «el eje de riesgo encuentra el
  riesgo», sino que el riesgo va en una dirección distinta del tamaño.
- **¿Cómo comparan una cartera simulada con datos reales?** La comparación da la dirección: esta cartera
  usa más cupo y paga menos que el mercado. Los montos exactos no se trasladan; por eso los conteos se
  recalculan con la cartera real.
- **¿Qué no saben todavía?** No hay datos de mora; proponemos un piloto de tres meses que la mida. Los
  conteos son de esta cartera. Y mostramos con qué va el riesgo, no qué lo causa.
