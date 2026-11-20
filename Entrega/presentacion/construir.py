"""Construye presentacion.html (10 láminas 16:9). Las cifras salen del informe
analisis_synthetic_credit_card.html (tabla de decisiones y anexo de comprobación)."""
from pathlib import Path

AQUI = Path(__file__).resolve().parent
TOTAL = 10


def tarjeta4(decidimos, otra, cifra, gerencia):
    filas = [("Decidimos", decidimos), ("La otra opción", otra),
             ("La cifra", cifra), ("Para la Gerencia", gerencia)]
    return '<aside class="c4">' + "".join(
        f'<div class="c4f"><span class="c4l">{l}</span><p>{t}</p></div>' for l, t in filas) + "</aside>"


def lamina(n, kicker, titulo, cuerpo, clase=""):
    return f"""
<section class="slide {clase}">
  <div class="kicker"><span class="num">{n - 1:02d}</span><span>{kicker}</span></div>
  <h1>{titulo}</h1>
  <div class="cuerpo">{cuerpo}</div>
  <footer><span>Equipo 02 · Radar de seguimiento para la Gerencia de Riesgo</span><span>{n} / {TOTAL}</span></footer>
</section>"""


def waffle(encontrados, color, total=100):
    celdas = "".join(f'<i style="background:{color if k < encontrados else "#E3E6EB"}"></i>'
                     for k in range(total))
    return f'<div class="waffle">{celdas}</div>'


def barras_h(datos, maximo, color_pos="#2B6CB0", color_neg="#D7263D", ancho=430):
    filas = []
    for nombre, v, *extra in datos:
        col = extra[0] if extra else (color_pos if v >= 0 else color_neg)
        w = abs(v) / maximo * ancho
        txt = f"{v:+.2f}".replace(".", ",").replace("+", "")
        filas.append(f'<div class="bh"><span class="bhn">{nombre}</span>'
                     f'<span class="bhb" style="width:{w:.0f}px;background:{col}"></span>'
                     f'<span class="bhv">{txt}</span></div>')
    return "".join(filas)


# ---------------------------------------------------------------- 1. Cliente
s1 = f"""
<section class="slide portada">
  <div class="portada-izq">
    <div class="marca">Gerencia de Riesgo de Crédito · 50.000 tarjetas</div>
    <h1 class="gigante">Cada mes hay que escoger a quién llamar <em>antes</em> de que deje de pagar.</h1>
    <p class="lead">Hoy la Gerencia lo decide revisando una ficha de <b>21 columnas por cliente</b>.
       El programa de seguimiento tiene cupos limitados: llamada del gestor, congelar aumentos de cupo,
       refinanciar antes de la mora.</p>
    <p class="pregunta">«¿Puedo ordenar la cartera con un número? ¿Y a quién me pierdo si lo hago?»</p>
    <div class="equipo">Oscar Contreras · Juan Pablo Sarmiento · Steven Navarro · Juan Diego Grajales<br>
      <span>Estadística Multidimensional · Sustentación del corte 2 · Equipo 02</span></div>
  </div>
  <div class="portada-der">
    <div class="producto">
      <div class="prod-tag">Lo que le traemos</div>
      <div class="prod-nombre">El Radar de seguimiento</div>
      <div class="prod-kpi"><b>8.195</b><span>clientes al mes, en vez de 50.000 fichas</span></div>
      <div class="prod-kpi"><b>2</b><span>números por cliente, en vez de 21 columnas</span></div>
      <div class="prod-kpi"><b>85,5 %</b><span>del saldo de la lista, en los primeros 3.939 clientes a llamar</span></div>
      <div class="prod-pie">Así llegamos: nueve decisiones con los datos →</div>
    </div>
  </div>
  <footer><span>Equipo 02 · Radar de seguimiento para la Gerencia de Riesgo</span><span>1 / {TOTAL}</span></footer>
</section>"""

# ---------------------------------------------------------------- 2. Variables
chips = []
fuera = {
    "Monthly_Spending": "= suma exacta de las 7 categorías de gasto",
    "Outstanding_Balance": "r = 0,997 con el saldo facturado",
    "Reward_Points_Earned": "r = 0,98 con el gasto",
    "Payment_Ratio": "cociente de pago ÷ saldo",
    "Credit_Utilization": "cociente de saldo ÷ cupo",
}
dentro = ["Annual_Income", "Credit_Limit", "Statement_Balance", "Payment_Amount", "Grocery_Spending",
          "Utility_Bill_Spending", "Online_Shopping_Spending", "Fuel_Spending", "Dining_Spending",
          "Travel_Spending", "Entertainment_Spending", "Monthly_Transactions", "Avg_Transaction_Value",
          "Mobile_App_Login", "EMI_Count", "International_Transactions", "Reward_Points_Redeemed",
          "Cash_Advance_Amount", "Card_Age_Months", "Age", "Credit_Score"]
chips_in = "".join(f'<span class="chip">{v}</span>' for v in dentro)
chips_out = "".join(f'<div class="fuera"><span class="chip tachado">{v}</span><span class="por">{r}</span></div>'
                    for v, r in fuera.items())
s2 = lamina(2, "¿Qué variables entran?",
            "26 columnas, pero cinco repetían lo que ya decían otras.",
            f"""<div class="visual">
      <div class="etq">Entran · 21 numéricas</div><div class="chips">{chips_in}</div>
      <div class="etq rojo">Salen · 5 repetidas o derivadas</div><div class="fueras">{chips_out}</div>
      <div class="nota">Sexo, ocupación y tipo de tarjeta no construyen el resumen: se usan para colorear el mapa.
      Los dos cocientes explican el <b>95 %</b> del puntaje: no se botan, se usan como lupa para leer el riesgo.</div>
    </div>""" + tarjeta4(
                "Una ficha de 21 columnas sin repetidas.",
                "Meter las 26 numéricas y las categóricas codificadas.",
                "Con las 26, una columna se repite exacta (hay una dirección con varianza cero). El eje de tamaño sale idéntico en las dos versiones: correlación 1,00.",
                "Nada de lo que se quitó era información nueva. Lo que el resumen gana es no contar dos veces lo mismo."))

# ---------------------------------------------------------------- 3. Atípicos
s3 = lamina(3, "¿Qué hacemos con faltantes y atípicos?",
            "Ningún dato malo. 1.641 clientes raros que no había que borrar, sino mirar.",
            f"""<div class="visual">
      <div class="kpis3">
        <div class="kpi"><b>0</b><span>faltantes y duplicados: no sale ningún cliente</span></div>
        <div class="kpi rojo"><b>1.641</b><span>raros en la combinación de sus variables (Mahalanobis, corte del 99 %)</span></div>
        <div class="kpi"><b>64 %</b><span>de ellos no tiene <i>ninguna</i> variable extrema: columna por columna no se ven</span></div>
      </div>
      <div class="etq">¿Quiénes son? Gastan en todo… menos en una cosa (combustible, viajes, entretenimiento)</div>
      <div class="comparar">
        <div class="cmp"><span class="cmpn">Puntaje mediano</span>
          <div class="cmpb"><span style="width:{573/700*560:.0f}px;background:#D7263D">573 · raros</span></div>
          <div class="cmpb"><span style="width:{639/700*560:.0f}px;background:#9AA5B8">639 · resto</span></div></div>
        <div class="cmp"><span class="cmpn">Proporción del saldo que pagan</span>
          <div class="cmpb"><span style="width:{0.57/1*560:.0f}px;background:#D7263D">0,57 · raros</span></div>
          <div class="cmpb"><span style="width:{0.85/1*560:.0f}px;background:#9AA5B8">0,85 · resto</span></div></div>
      </div>
    </div>""" + tarjeta4(
                "Sale 0 casos. Los 1.641 se marcan y se estudian; 0 se corrigen, porque ninguno es un error de captura.",
                "Borrar los atípicos, o revisar solo variable por variable (Tukey).",
                "Quitarlos mueve las correlaciones como mucho 0,02: no están rompiendo nada.",
                "Borrarlos habría escondido a un grupo con más riesgo que el promedio. Ahora es una lista para revisar."))

# ---------------------------------------------------------------- 4. Estandarizar
def barra_c1(etq, v, nota, col):
    return (f'<div class="c1f"><div class="c1e">{etq}</div><div class="c1t">'
            f'<span class="c1b" style="width:{v/100*900:.0f}px;background:{col}"></span>'
            f'<span class="c1v">{str(v).replace(".", ",")}</span></div><div class="c1n">{nota}</div></div>')


s4 = lamina(4, "¿Estandarizamos?",
            "Sin estandarizar, el «resumen» era solo el ingreso con otro nombre.",
            f"""<div class="visual">
      <div class="escala">
        <div><b>1,67</b><span>desviación de las cuotas (EMI)</span></div>
        <div class="flecha">seis órdenes de magnitud →</div>
        <div><b>₹1.410.000</b><span>desviación del ingreso anual</span></div>
      </div>
      <div class="etq">De cada 100 partes de la información, cuántas guarda la primera componente</div>
      {barra_c1("En rupias, sin estandarizar", 95.5, "Una sola variable manda: el ingreso, con peso 0,76. Aporta 56 de cada 100 partes de la varianza total.", "#9AA5B8")}
      {barra_c1("Estandarizado", 48.0, "Ninguna variable manda sola.", "#5DA9E9")}
      {barra_c1("log(x+1) + estandarizado", 50.1, "Además, unos pocos clientes enormes ya no deciden la dirección.", "#2B6CB0")}
    </div>""" + tarjeta4(
                "Sí: logaritmo en las variables con cola larga y después todas a la misma escala.",
                "Trabajar en rupias, o estandarizar sin logaritmo.",
                "En rupias, la primera componente «guarda» 95,5 de cada 100, pero es el ingreso disfrazado. Estandarizada guarda 50,1 y la construyen todas.",
                "El resumen pesa a todas las variables, no solo a las que se miden en números grandes."))

# ---------------------------------------------------------------- 5. Resumir
rep = ["ingreso", "cupo", "saldo", "pagos", "mercado", "servicios", "en línea", "combustible", "restaurantes",
       "viajes", "entretenimiento", "transacciones", "valor por compra", "app", "cuotas", "internacionales"]
solas = [("puntaje", "0,17"), ("edad", "0,01"), ("antigüedad", "0,05"), ("avances", "0,07")]
s5 = lamina(5, "¿Tiene sentido resumir?",
            "El dinero se repite. El puntaje va solo.",
            f"""<div class="visual dos-col">
      <div class="nube">
        <div class="etq">Se repiten · 16 de 21 tienen una compañera con correlación &gt; 0,6</div>
        <div class="racimo">{"".join(f'<span class="bola azul">{v}</span>' for v in rep)}</div>
        <div class="dato">ingreso ↔ cupo: <b>r = 0,98</b></div>
      </div>
      <div class="nube">
        <div class="etq rojo">Van solas · con ninguna pasan de 0,17</div>
        <div class="solas">{"".join(f'<div class="sola"><span class="bola roja">{v}</span><small>máx. |r| = {r}</small></div>' for v, r in solas)}</div>
      </div>
    </div>""" + tarjeta4(
                "Sí se puede resumir: hay mucha información repetida.",
                "No resumir, y seguir mirando las 21 columnas una por una.",
                "16 de 21 variables se repiten con alguna otra (|r| &gt; 0,6). El puntaje, la variable que más le importa a la Gerencia, no pasa de 0,17 con ninguna.",
                "Primera alerta: el tamaño del cliente cabe en un número; el riesgo, no cabe en ese número."))

# ---------------------------------------------------------------- 6. Cuántas
pct = [50.1, 5.3, 4.8, 4.7, 4.5, 4.5, 4.1, 2.9, 2.8, 2.5]
cols = "".join(
    f'<div class="col"><span class="colv">{str(v).replace(".", ",")}</span>'
    f'<span class="colb" style="height:{v/52*330:.0f}px;background:{"#2B6CB0" if k == 0 else "#D7263D" if k == 1 else "#C9CED6"}"></span>'
    f'<span class="colx">C{k+1}</span></div>' for k, v in enumerate(pct))
s6 = lamina(6, "¿Cuántas componentes?",
            "Dos números. No uno, y tampoco ocho.",
            f"""<div class="visual">
      <div class="etq">De cada 100 partes de la información de la ficha, cuántas guarda cada componente</div>
      <div class="cols">{cols}
        <div class="anot a1"><b>C1 · 50,1</b><br>la mitad de la ficha en un número</div>
        <div class="anot a2"><b>C2 · solo 5,3</b><br>…pero es la que ve el riesgo</div>
      </div>
      <div class="vs">
        <div><span class="vsn azul">18 %</span>de los clientes con peor puntaje caen en el 20 % más alto de C1 <small>(al azar sería 20 %)</small></div>
        <div><span class="vsn rojo">66 %</span>caen en el 20 % más alto de C2</div>
      </div>
    </div>""" + tarjeta4(
                "Dos: C1 y C2.",
                "Una (la que más guarda); tres (la regla de «más que una variable»); ocho (para pasar del 80 %).",
                "C2 guarda poco, pero encuentra a 6.580 de los 10.046 clientes con peor puntaje; C1 solo a 1.832.",
                "Nos quedamos con las componentes según lo que necesita la Gerencia, no según una regla: le basta una ficha de dos números."))

# ---------------------------------------------------------------- 7. Qué mide
c1 = [("cupo", .30), ("ingreso", .30), ("saldo", .29), ("pagos", .27), ("mercado", .27), ("app", .25),
      ("… 10 más de dinero y uso", .22), ("puntaje", .01, "#D7263D")]
c2 = [("puntaje", -.78, "#D7263D"), ("avances en efectivo", .49, "#D7263D"),
      ("antigüedad tarjeta", -.34, "#D7263D"), ("cupo", -.01, "#9AA5B8"), ("ingreso", .00, "#9AA5B8")]
s7 = lamina(7, "¿Qué mide cada una?",
            "Un eje mide el tamaño del cliente. El otro, su riesgo.",
            f"""<div class="visual dos-col">
      <div class="pesos"><div class="pt azul">C1 · Tamaño del cliente</div>
        <div class="ps">Todo lo que se mide en rupias o en frecuencia pesa parecido y en la misma dirección.</div>
        {barras_h(c1, 0.8)}</div>
      <div class="pesos"><div class="pt rojo">C2 · Riesgo</div>
        <div class="ps">Hacia arriba: peor puntaje, más avances en efectivo, tarjeta más nueva.</div>
        {barras_h(c2, 0.8)}
        <div class="lupa"><b>Con la lupa</b> (variables que no la construyen): proporción pagada <b>−0,59</b> · uso del cupo <b>+0,47</b>. Confirma el nombre.</div></div>
    </div>""" + tarjeta4(
                "C1 = tamaño; C2 = riesgo (C3 = edad, casi sola).",
                "Ponerles nombre a ojo, sin mirar los pesos.",
                "En C1, 16 variables de dinero y uso pesan entre 0,20 y 0,30; el puntaje, 0,01. En C2 manda el puntaje (−0,78), con los avances en efectivo (+0,49).",
                "El mapa se lee en el idioma del negocio: a la derecha, cuánto pesa el cliente; hacia arriba, cuánto preocupa. Que vayan juntas no quiere decir que una cause a la otra."))

# ---------------------------------------------------------------- 8. Un solo número
s8 = lamina(8, "¿Qué pierde el cliente con un solo número?",
            "Con un solo número se nos escapan 8 de cada 10 clientes en riesgo.",
            f"""<div class="visual dos-col">
      <div class="wbloque"><div class="pt azul">Ordenando solo por C1</div>{waffle(18, "#2B6CB0")}
        <div class="wpie"><b class="rojo">8.214</b> de 10.046 se escapan</div></div>
      <div class="wbloque"><div class="pt rojo">Ordenando por C2</div>{waffle(66, "#D7263D")}
        <div class="wpie"><b>6.580</b> de 10.046 los encuentra</div></div>
      <div class="wley">Cada cuadro = 1 de cada 100 clientes del 20 % con peor puntaje · color = los encuentra el número</div>
    </div>""" + tarjeta4(
                "Un número no basta.",
                "Ordenar toda la cartera solo por C1, el mejor resumen de un número.",
                "De los 10.046 clientes con peor puntaje, C1 deja escapar a 8.214: el 82 %, lo mismo que escoger al azar.",
                "Con un solo número, la Gerencia ordenaría la cartera por tamaño y el riesgo le quedaría fuera."))

# ---------------------------------------------------------------- 9. Mapa
s9 = lamina(9, "¿Qué muestra el mapa?",
            "No hay tribus de riesgo: la cartera es un continuo.",
            f"""<div class="visual dos-col mapa">
      <img src="mapa_tarjetas.png" alt="Mapa de clientes por tipo de tarjeta">
      <div class="lect">
        <div class="lf"><b>En tamaño, la tarjeta ordena</b>De Basic a Signature, los centros van de −2,97 a +4,44 desviaciones.</div>
        <div class="lf"><b>En riesgo, todas se montan</b>Los cinco centros quedan a menos de 0,2 desviaciones. Con la ocupación pasa lo mismo.</div>
        <div class="lf"><b>Un solo pico, sin valle</b>No hay un grupo aparte: el riesgo sube poco a poco.</div>
        <div class="lf corte"><b>El corte lo pone la Gerencia</b>Riesgo &gt; 1 desviación y mitad de tamaño:<br>
          <span class="z za">A · 4.226</span><span class="z zb">B · 3.969</span><span class="z zc">sin seguimiento · 41.805</span></div>
      </div>
    </div>""" + tarjeta4(
                "Es un continuo: el corte se define, no se descubre.",
                "Buscar grupos hechos: escoger por tipo de tarjeta o por ocupación.",
                "La tarjeta explica el tamaño (centros de −2,97 a 4,44) y nada del riesgo (&lt; 0,2). Ojo: C2 se parece −0,82 al puntaje.",
                "Escoger a quién seguir por tipo de tarjeta no sirve. Y como C2 es casi el puntaje, falta una última pregunta…"))

# ---------------------------------------------------------------- 10. Decisión
s10 = f"""
<section class="slide final">
  <div class="kicker"><span class="num">09</span><span>¿Qué decide el cliente?</span></div>
  <h1>El puntaje dice quién entra. El tamaño dice por quién empezar.</h1>
  <div class="cuerpo">
    <div class="visual mapa-final">
      <img src="mapa_clientes.png" alt="Mapa con la lista final">
      <div class="leyenda"><span class="z za">A · 3.939 grandes → llamada del gestor</span>
        <span class="z zb">B · 4.256 pequeños → mensajes</span></div>
    </div>
    <div class="der">
      <div class="kpis-final">
        <div class="kf"><b>8.195</b><span>clientes de peor puntaje al mes (16,4 % de la cartera)</span></div>
        <div class="kf rojo"><b>85,5 %</b><span>del saldo de la lista está en la zona A, que tiene el 48 % de los clientes</span></div>
      </div>
      <div class="duelo"><div class="pt">Con los mismos 8.195 cupos</div>
        <div class="dl"><span>Lista por C2</span><span class="dlb"><i style="width:57.8%"></i></span><b>57,8 %</b></div>
        <div class="dl"><span>Lista por puntaje</span><span class="dlb"><i style="width:81.6%;background:#D7263D"></i></span><b>81,6 %</b></div>
        <small>de los clientes con peor puntaje encontrados · C2 es el puntaje con ruido; lo nuevo que aporta el resumen es C1</small></div>
      <div class="nosabe"><div class="pt">Lo que no sabemos todavía</div>
        <ul><li>No hay datos de mora real: el puntaje es nuestra mejor aproximación.</li>
        <li>Frente al RBI, la cartera simulada gasta ~4 veces y debe ~11 veces lo de una tarjeta real en India: los conteos se recalculan con la cartera propia. Los cortes son relativos y sí se pueden llevar.</li>
        <li>El mapa muestra con qué va el riesgo, no qué lo causa.</li></ul></div>
    </div>
  </div>
  <footer><span>Equipo 02 · Radar de seguimiento para la Gerencia de Riesgo</span><span>10 / {TOTAL}</span></footer>
</section>"""

css = (AQUI / "estilo.css").read_text(encoding="utf-8")
html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Radar de seguimiento</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Fraunces:opsz,wght@9..144,600;9..144,700&display=swap" rel="stylesheet">
<style>{css}</style></head><body>
{s1}{s2}{s3}{s4}{s5}{s6}{s7}{s8}{s9}{s10}
</body></html>"""
(AQUI / "presentacion.html").write_text(html, encoding="utf-8")
print("ok")
