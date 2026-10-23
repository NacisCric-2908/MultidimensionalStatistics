# Explicación completa del Taller de Análisis Factorial

**Título del taller:** *Lo que las variables comparten — Análisis factorial para la Gerencia de Riesgo de Crédito*  
**Archivo fuente:** `taller_analisis_factorial.Rmd` (y su salida compilada `taller_analisis_factorial.html`)  
**Curso:** Estadística Multidimensional · 26158 · grupo 020-81 · periodo 2026-3  
**Autores:**
- Oscar Manuel Contreras Gacha (20221020052)
- Juan Pablo Sarmiento Ramírez (20221020138)
- Steven Navarro Parrales (20221020048)
- Juan Diego Grajales Castillo (20221020128)

---

## 1. Propósito y enfoque metodológico

Este taller da continuidad a los dos talleres previos de Análisis de Componentes Principales (PCA) sobre la cartera de **50 000 tarjetas de crédito** (`synthetic_credit_card_customer_behavior_dataset.csv`). 

Mientras que el **PCA** respondía a la pregunta de *cómo construir el mejor resumen* de las variables (reteniendo tanta varianza total como fuera posible), el **Análisis Factorial (FA)** responde a una pregunta distinta: **¿qué habilidad o capacidad latente comparten las variables entre sí?** Para ello, el modelo descompone la varianza de cada variable (100 partes) en dos porciones:
1. **Parte común (comunalidad, $h_i^2 = \ell_i^2$):** lo que la variable comparte con las demás debido a la habilidad común subyacente.
2. **Parte propia (unicidad, $u_i^2 = 1 - h_i^2$):** lo que la variable mide por su cuenta y ninguna otra variable del grupo mide, más su error de medición.

Para mantener el rigor comunicativo hacia el negocio, cada bloque de resultados se interpreta con la estructura en tres pasos:
- 👀 **Qué vemos:** lectura objetiva del indicador o gráfico.
- 💼 **Qué significa para el cliente:** traducción al contexto de la cartera de tarjetas de crédito.
- ✅ **Qué decide el cliente:** acción práctica que toma la Gerencia.

---

## 2. El encargo y preparación de los datos (Sección 1)

### 2.1. El cliente y su pregunta de negocio
El cliente es la **Gerencia de Riesgo de Crédito del banco emisor** de las 50 000 tarjetas (valores en rupias indias, ₹), que cada mes define qué tarjetahabientes entran al programa de seguimiento preventivo. Su inquietud es:
> *«Mis analistas dicen que ingreso, cupo, saldo, pagos y número de compras son "lo mismo": la capacidad económica del cliente. ¿Es cierto que hay una sola capacidad detrás de todas? ¿Y el puntaje crediticio, también es parte de esa capacidad?»*

### 2.2. Selección y transformación de las 9 variables numéricas
Se seleccionaron las mismas **9 variables numéricas** trabajadas en los talleres de PCA:
- **Variables de dinero (capacidad financiera):**
  1. `Annual_Income` (*Ingreso anual*)
  2. `Credit_Limit` (*Cupo*)
  3. `Statement_Balance` (*Saldo facturado*)
  4. `Payment_Amount` (*Monto pagado*)
- **Variables de uso de la tarjeta:**
  5. `EMI_Count` (*Compras a cuotas*)
  6. `Monthly_Transactions` (*Compras al mes*)
  7. `Avg_Transaction_Value` (*Valor por compra*)
  8. `International_Transactions` (*Compras internacionales*)
- **Variable de riesgo (incluida a propósito para contrastar la hipótesis de la Gerencia):**
  9. `Credit_Score` (*Puntaje crediticio*)

**Preprocesamiento:**
- Se aplicó la transformación $\log(x + 1)$ (`log1p`) a las **6 variables** con asimetría absoluta mayor que 1 (*Ingreso anual, Cupo, Saldo facturado, Monto pagado, Valor por compra y Compras internacionales*).
- Se calculó la matriz de correlaciones `R <- cor(X)`, sobre la cual opera el análisis factorial (lo que estandariza implícitamente todas las variables a media 0 y varianza 1).

---

## 3. Adecuación muestral: Índice KMO (Sección 1.2)

Se ejecutó `KMO(R)` del paquete `psych` para comparar las correlaciones observadas frente a las correlaciones parciales (lo que queda entre dos variables al descontar las demás):

| Variable | KMO individual (`MSAi`) | Lectura |
| :--- | :---: | :--- |
| Compras a cuotas | 0,92 | Maravilloso |
| Compras internacionales | 0,92 | Maravilloso |
| Ingreso anual | 0,86 | Meritorio |
| Cupo | 0,77 | Aceptable |
| Valor por compra | 0,76 | Aceptable |
| Compras al mes | 0,73 | Aceptable |
| Saldo facturado | 0,66 | Mediocre |
| Monto pagado | 0,65 | Mediocre |
| **Puntaje crediticio** | **0,02** | **Inaceptable** |
| **KMO Global (`MSA`)** | **0,71** | **Aceptable** |

- **Hallazgo y decisión:** El KMO global (0,71) confirma que tiene sentido buscar un factor común en la ficha, ya que las 8 variables de dinero y uso superan 0,60. El **puntaje crediticio (0,02)** no comparte prácticamente nada con el grupo, pero se conserva deliberadamente en el modelo para demostrarle con números a la Gerencia si pertenece o no a la capacidad económica.

---

## 4. Modelo de una sola habilidad (Sección 2)

### 4.1. Ajuste con `fa(R, nfactors = 1, fm = "ml")` y gráfico de parte común vs. propia
Se estimó el modelo factorial de 1 factor por máxima verosimilitud (`fm = "ml"`), orientando el signo para que mayor capacidad sea positiva:

| Variable | Carga ($\ell_i$) | Parte común ($100 \times \ell_i^2$) | Parte propia ($100 \times u_i^2$) |
| :--- | :---: | :---: | :---: |
| **Cupo** | 0,996 | 99,1 | 0,9 |
| **Ingreso anual** | 0,987 | 97,5 | 2,5 |
| **Saldo facturado** | 0,946 | 89,6 | 10,4 |
| **Monto pagado** | 0,886 | 78,5 | 21,5 |
| **Valor por compra** | 0,772 | 59,7 | 40,3 |
| **Compras al mes** | 0,676 | 45,7 | 54,3 |
| **Compras a cuotas** | 0,666 | 44,3 | 55,7 |
| **Compras internacionales** | 0,654 | 42,7 | 57,3 |
| **Puntaje crediticio** | 0,018 | 0,0 | 100,0 |

- **Gráfica generada:** Gráfico de barras horizontales apiladas (`grafico-partes`) que contrasta de cada 100 partes cuánto es común (azul) y cuánto es propio (gris) en cada variable.
- **Interpretación para el cliente:** La habilidad común es la **capacidad económica** y reúne **61,9 de cada 100 partes** de las 9 variables. Explica casi por completo el cupo (99 %) y el ingreso (98 %), buena parte del saldo (90 %) y del pago (79 %), y alrededor de la mitad de las variables de uso (43 % a 60 %).

### 4.2. ¿Qué variable es casi toda propia y qué significa para el cliente? (Sección 2.1)
- **Variable identificada:** El **puntaje crediticio** tiene **100,0 de cada 100 partes propias** (carga de `0,018`, parte común `0,0`).
- **Significado de negocio:** El riesgo crediticio no forma parte de la capacidad económica. Que un cliente gane más, tenga mayor cupo o compre más no dice nada sobre qué tan buen pagador es. No significa que el puntaje esté mal medido, sino que mide otra dimensión (la conducta de pago: utilización del cupo y proporción pagada).
- **Decisión:** La Gerencia no puede usar el tamaño del cliente ni la categoría de su tarjeta como sustituto del riesgo; el puntaje debe entrar **por separado** en la regla de seguimiento preventivo.

### 4.3. ¿Alcanza una habilidad? Comparación $r_{ij}$ vs. $\ell_i \ell_j$ (Sección 2.2)
Si una única habilidad explicara todo lo que comparten las variables, cada correlación observada debería coincidir con el producto de las cargas ($r_{ij} \approx \ell_i \ell_j$). Se evaluaron los $\binom{9}{2} = 36$ pares de variables:
- **31 de los 36 pares** tienen una diferencia absoluta menor a `0,05` respecto al producto de sus cargas.
- Solo **5 pares** se apartan en más de `0,08` (y **3 pares** en más de `0,10`), visualizados en el gráfico de dispersión `grafico-alcanza`:
  1. `Compras al mes – Valor por compra`: $r = 0,201$ vs. $\ell_i \ell_j = 0,522$ (diferencia de `-0,321`). Refleja el estilo de gasto: a igual capacidad, unos clientes hacen muchas compras pequeñas y otros pocas compras grandes (paradoja de Simpson dentro de cada nivel de tarjeta).
  2. `Saldo facturado – Puntaje crediticio`: $r = -0,169$ vs. $\ell_i \ell_j = 0,017$ (diferencia de `-0,186`).
  3. `Compras a cuotas – Compras al mes`: $r = 0,565$ vs. $\ell_i \ell_j = 0,450$ (diferencia de `+0,116`).
  4. `Saldo facturado – Monto pagado`: $r = 0,933$ vs. $\ell_i \ell_j = 0,839$ (diferencia de `+0,095`).
  5. `Monto pagado – Puntaje crediticio`: $r = 0,108$ vs. $\ell_i \ell_j = 0,016$ (diferencia de `+0,093`).

---

## 5. Modelo de dos habilidades y comparación con PCA (Sección 3)

### 5.1. Prueba con 2 factores sobre las 9 variables (`fa2`)
Se ajustó `fa(R, nfactors = 2, fm = "ml", rotate = "oblimin", n.obs = nrow(X))`:
- **Factor 1 (`F1_capacidad`):** Conserva exactamente las mismas cargas de la capacidad económica (Cupo `0,994`, Ingreso `0,987`, Saldo `0,952`, Pago `0,891`).
- **Factor 2 (`F2_segundo`):** Carga **`0,998` en el Puntaje crediticio**, mientras que ninguna otra variable supera `0,30` (solo aparecen ecos leves en Saldo `-0,170` y Pago `0,107`). La correlación entre ambos factores es prácticamente nula (`-0,003`), y el residuo más alto (`Valor por compra – Compras al mes`, `0,322`) queda intacto.
- **Conclusión clave:** **La segunda no es una habilidad con sentido; es una sola variable.** El modelo simplemente le asignó un factor exclusivo a la parte propia del puntaje crediticio. Llamarlo «habilidad de riesgo» sería inventar un factor común donde solo hay una variable aislada.

### 5.2. Prueba adicional con 2 factores retirando el puntaje (`fa2b`, Sección 3.1)
Al quitar el puntaje crediticio y correr 2 factores sobre las 8 variables restantes:
- El segundo factor carga fuerte en `Compras al mes` (`0,903`) y en sentido opuesto en `Valor por compra` (`-0,372`), capturando la tensión **frecuencia vs. ticket**, con una correlación oblicua de **`0,427`** respecto a la capacidad económica.
- Aun así, al depender casi por completo de una sola variable (`Compras al mes`), se interpreta como una pista comercial (para segmentar campañas por frecuencia o por monto de compra) y no como un factor robusto de riesgo.

### 5.3. El factor común frente a la primera componente del PCA (Sección 3.2)
Se comparó la proporción de varianza explicada por ambos métodos sobre las 9 variables:
- **PCA (primera componente):** guarda **64,3 de cada 100 partes** ($\lambda_1 / 9$).
- **Análisis Factorial (un factor):** reúne **61,9 de cada 100 partes** ($\sum h_i^2 / 9$).
- **Explicación:** El PCA busca el resumen que maximice la varianza total e inevitablemente absorbe pedazos de la parte propia de las variables; el análisis factorial aisla únicamente la varianza **compartida** y deja fuera la parte propia.

---

## 6. Síntesis de las 6 preguntas conceptuales (Sección 4)

En el documento se responden todas las preguntas conceptuales del taller conectándolas con la evidencia empírica de la cartera:

1. **Diferencia entre parte común y parte propia:** La parte común ($\ell_i^2$) es la fracción de las diferencias en un módulo explicada por la habilidad compartida con los demás; la parte propia ($1 - \ell_i^2$) es lo específico de ese módulo más el error de medición. Ambas suman 100 (ej.: en nuestra cartera, Cupo es 99 % común y Puntaje es 100 % propio).
2. **¿Un módulo con 15/100 de parte común (Escritura) está mal hecho?:** **No.** Tener poca parte común solo indica que comparte poco con los demás módulos evaluados. El 85 % restante incluye tanto habilidad específica valiosa (propia de escribir) como error, los cuales el análisis factorial no puede separar sin una medición externa de fiabilidad (exactamente igual al puntaje crediticio, que tiene 0 % de parte común pero es indispensable para medir riesgo).
3. **Si $r_{ij} \approx \ell_i \ell_j$, ¿cuántas habilidades hay?:** Indica que **una sola habilidad común basta** para explicar el parecido entre esos dos módulos (en el caso de negocio ocurre en 31 de los 36 pares).
4. **¿Por qué no llamar «habilidad verbal» a un segundo factor que cae casi entero sobre Lectura?:** Porque una habilidad común requiere ser compartida por varios módulos (al menos dos o tres con cargas importantes). Si recae sobre una sola variable, es simplemente su parte propia disfrazada de factor (como ocurrió con el puntaje crediticio en el modelo de 2 factores).
5. **¿Por qué el resumen del PCA (sesión 3) guardaba más de cada 100 que la habilidad común de hoy?:** Porque la CP1 maximiza varianza total (mezclando parte común y parte propia), mientras que el factor común solo contabiliza lo compartido entre variables (`64,3 %` en PCA vs. `61,9 %` en FA).
6. **Pregunta de selección múltiple:** La afirmación correcta es la **(b)** (*la carga al cuadrado es la parte de las diferencias en un módulo que viene de la habilidad común*). Se refutan:
   - **(a)** porque la habilidad común es latente y no se mide directamente;
   - **(c)** porque la parte propia también contiene varianza específica útil y no solo error;
   - **(d)** porque con rotación oblicua (`oblimin`) dos habilidades sí pueden correlacionarse (como el `0,43` entre capacidad y frecuencia al retirar el puntaje).

---

## 7. Recomendación final entregada a la Gerencia (Sección 5)

1. **Existe una única capacidad económica común** detrás de las variables monetarias y transaccionales que explica el **61,9 %** de la variabilidad conjunta (casi el 100 % del ingreso y el cupo).
2. **El puntaje crediticio es 100 % parte propia** (KMO de `0,02` y comunalidad de `0,0 %`): la capacidad económica del cliente no informa sobre su comportamiento de pago.
3. **Una sola habilidad reproduce 31 de las 36 correlaciones**; las discrepancias corresponden al patrón de gasto (*frecuencia vs. ticket*) y al vínculo directo del saldo y pago con el puntaje.
4. **La decisión de seguimiento preventivo requiere dos números por separado:** la **capacidad económica** (cuánto pesa el cliente) y el **puntaje crediticio** (qué tan riesgoso es).
