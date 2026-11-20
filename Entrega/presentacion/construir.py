"""Construye presentacion.html (10 láminas 16:9) en formato de informe de consultoría.

Las cifras salen del informe analisis_synthetic_credit_card.html (tabla de decisiones, Módulos 13-17 y
Módulo 20) y de perfiles calculados sobre data/bronze. "La competencia" son las cifras reales del
mercado indio de tarjetas (RBI, SBI Card y Banco Mundial) del Módulo 20.
"""
from pathlib import Path

AQUI = Path(__file__).resolve().parent
TOTAL = 10
FUENTE_COMP = "Competencia: mercado de tarjetas de India · RBI (abr-2025 a mar-2026; BSR 2023), SBI Card (mar-2026), Banco Mundial Findex 2024"


def franja(decidimos, otra, dato, negocio):
    filas = [("Lo que decidimos", decidimos), ("La otra opción", otra),
             ("El dato que lo sostiene", dato), ("Qué significa para ustedes", negocio)]
    return '<div class="franja">' + "".join(
        f'<div class="ff"><span class="fl">{l}</span><p>{t}</p></div>' for l, t in filas) + "</div>"


def lamina(n, tema, titulo, cuerpo, pie_fuente=""):
    fuente = f'<span class="fuente">{pie_fuente}</span>' if pie_fuente else "<span></span>"
    return f"""
<section class="slide">
  <div class="kicker"><span class="num">Decisión {n - 1} de 9</span><span>{tema}</span></div>
  <h1>{titulo}</h1>
  <div class="cuerpo">{cuerpo}</div>
  <footer>{fuente}<span>{n} / {TOTAL}</span></footer>
</section>"""


def persona(color, relleno=True):
    fill = color if relleno else "none"
    return (f'<svg viewBox="0 0 40 80" class="persona"><circle cx="20" cy="13" r="11" fill="{fill}" stroke="{color}" stroke-width="3"/>'
            f'<path d="M4 76 V44 Q4 29 20 29 Q36 29 36 44 V76 Z" fill="{fill}" stroke="{color}" stroke-width="3"/></svg>')


def barras(datos, maximo, fmt, ancho=520, color="#1F4E79"):
    out = []
    for etq, v, *c in datos:
        col = c[0] if c else color
        out.append(f'<div class="br"><span class="brn">{etq}</span><span class="brt">'
                   f'<span class="brb" style="width:{v / maximo * ancho:.0f}px;background:{col}"></span>'
                   f'<span class="brv">{fmt(v)}</span></span></div>')
    return "".join(out)


def es(x, d=1):
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ------------------------------------------------------------------ 1. El cliente
def bench(titulo, nos, comp, nota):
    return (f'<div class="bench"><div class="bt">{titulo}</div>'
            f'<div class="bv"><div><b class="rojo">{nos}</b><small>su cartera</small></div>'
            f'<div><b>{comp}</b><small>competencia</small></div></div><div class="bn">{nota}</div></div>')


s1 = f"""
<section class="slide portada">
  <div class="marca">Informe para la Gerencia de Riesgo de Crédito · Cartera de 50.000 tarjetas</div>
  <h1 class="gigante">Sus clientes deben más y pagan peor que los de la competencia. ¿A quién llamar primero?</h1>
  <div class="encargo">
    <div><span class="et">Su decisión de cada mes</span>Qué clientes entran al programa de seguimiento preventivo:
      llamada del gestor, congelar aumentos de cupo, refinanciar antes de la mora. Los cupos son limitados.</div>
    <div><span class="et">Cómo lo hacen hoy</span>Revisan una ficha de <b>26 columnas por cliente</b>, y se preguntan si basta
      con mirar el ingreso, la categoría de la tarjeta o la ocupación.</div>
    <div><span class="et">Lo que les entregamos</span>Una <b>lista mensual de 8.301 clientes</b>, ordenada por el dinero en juego,
      y tres fallas de procedimiento que conviene corregir.</div>
  </div>
  <div class="benchs">
    {bench("Saldo pendiente por tarjeta", "₹303 mil", "₹28 mil", "11 veces lo de la competencia")}
    {bench("Uso del cupo", "43 %", "21 %", "el doble")}
    {bench("Pagan su saldo completo", "35 %", "87 %", "menos de la mitad")}
    {bench("Usan avances en efectivo", "30 %", "0,6 %", "50 veces más")}
  </div>
  <div class="equipo">Equipo 02 · Oscar Contreras · Juan Pablo Sarmiento · Steven Navarro · Juan Diego Grajales
    <span>Estadística Multidimensional · Sustentación del corte 2</span></div>
  <footer><span class="fuente">{FUENTE_COMP}. «Pagan completo»: en su cartera, pagan el 95 % o más.</span><span>1 / {TOTAL}</span></footer>
</section>"""

# ------------------------------------------------------------------ 2. Variables
sobran = [("Gasto mensual total", "Es la suma exacta de las 7 categorías de gasto que ya están en la ficha."),
          ("Saldo pendiente", "Repite el saldo facturado: van juntos en 99,7 de cada 100 casos."),
          ("Puntos ganados", "Se calculan del gasto: van juntos en 98 de cada 100."),
          ("Proporción pagada", "Es pago ÷ saldo, dos columnas que ya están."),
          ("Uso del cupo", "Es saldo ÷ cupo, otras dos columnas que ya están.")]
filas = "".join(f'<div class="sob"><span class="sobn">{a}</span><span class="sobr">{b}</span></div>' for a, b in sobran)
s2 = lamina(2, "¿Qué variables entran?",
            "Hallazgo 1: su ficha de cliente cuenta dos veces lo mismo.",
            f"""<div class="fila">
      <div class="col-g">
        <div class="etq">5 de sus 26 columnas no traen información nueva</div>{filas}
      </div>
      <div class="col-p">
        <div class="grande"><b>21</b><span>columnas bastan para describir a cada cliente</span></div>
        <div class="aviso"><b>Ojo:</b> la proporción pagada y el uso del cupo explican el <b>95 %</b> del puntaje de crédito.
          No se botan: quedan como <b>alertas</b> para leer el riesgo (lámina 7).</div>
        <div class="mini">Sexo, ocupación y categoría de tarjeta se usan para describir a los grupos, no para construir los indicadores.</div>
      </div>
    </div>""" + franja(
                "Trabajar con 21 columnas: 5 repetidas salen de los indicadores.",
                "Usar las 26 columnas y además las categorías de cliente.",
                "Con las 26, una columna se repite exacta. El indicador de tamaño sale idéntico en las dos versiones (coinciden en 1,00).",
                "Sus reportes mensuales pueden ser más cortos sin perder nada, y dejar de sumar dos veces el mismo gasto."))

# ------------------------------------------------------------------ 3. Atípicos
s3 = lamina(3, "¿Qué hacemos con faltantes y atípicos?",
            "Hallazgo 2: sus datos están sanos, pero hay 1.641 clientes con un perfil que nadie estaba mirando.",
            f"""<div class="fila">
      <div class="col-p">
        <div class="sano"><b>0</b> datos faltantes &nbsp;·&nbsp; <b>0</b> clientes duplicados &nbsp;·&nbsp; <b>0</b> valores imposibles</div>
        <div class="grande rojo"><b>1.641</b><span>clientes «raros»: cada dato por separado es normal, pero la combinación no lo es (3,3 % de la cartera)</span></div>
        <div class="mini"><b>64 de cada 100</b> de ellos no tienen ningún dato extremo: una revisión columna por columna no los encuentra.</div>
      </div>
      <div class="col-g perfil">
        <div class="ptag">Perfil de riesgo · «El cliente disparejo»</div>
        <div class="pdesc">Gasta en todo, menos en una cosa: combustible, viajes, entretenimiento o compras en línea casi en cero.</div>
        <div class="comp"><span>Puntaje de crédito mediano</span><b class="rojo">573</b><em>frente a 639 del resto</em></div>
        <div class="comp"><span>Parte del saldo que paga cada mes</span><b class="rojo">57 %</b><em>frente a 85 % del resto</em></div>
        <div class="comp"><span>Con tarjeta Platinum o Signature</span><b class="rojo">38 %</b><em>frente a 21 % del resto</em></div>
      </div>
    </div>""" + franja(
                "No sale ningún cliente. Los 1.641 se marcan y se estudian; no hubo errores que corregir.",
                "Borrarlos como «datos raros», o revisar solo dato por dato.",
                "Quitarlos no cambia la estructura de la cartera (las relaciones se mueven como mucho 0,02).",
                "Borrarlos habría escondido a un grupo con más riesgo que el promedio. Ahora tienen nombre, y en la lámina 10 les decimos qué hacer con ellos."))

# ------------------------------------------------------------------ 4. Estandarizar
s4 = lamina(4, "¿Estandarizamos?",
            "Medidos en rupias, los clientes ricos tapan todo lo demás.",
            f"""<div class="fila">
      <div class="col-g">
        <div class="etq">Si los clientes se comparan en rupias…</div>
        <div class="pila"><span style="width:56%;background:#1F4E79">el ingreso: 56 %</span><span style="width:44%;background:#C9CED6;color:#14213D">las otras 20 columnas: 44 %</span></div>
        <div class="mini">…el ingreso explica 56 de cada 100 diferencias entre clientes, solo porque se mide en millones. Un resumen hecho así es <b>el ingreso con otro nombre</b>: «guarda» 95,5 de cada 100 partes, pero no ve nada más.</div>
        <div class="etq" style="margin-top:34px">…y si se miden con la misma regla</div>
        <div class="pila"><span style="width:100%;background:linear-gradient(90deg,#1F4E79,#2E86AB,#5DA9E9,#1F4E79,#2E86AB,#5DA9E9)">las 21 columnas aportan · ninguna pesa más de 0,30</span></div>
        <div class="mini">El primer indicador guarda 50,1 de cada 100 partes de la información de la ficha, y lo construyen todas.</div>
      </div>
      <div class="col-p">
        <div class="cita">«Si su modelo de seguimiento usa montos en rupias, termina vigilando a los clientes más ricos, no a los más riesgosos.»</div>
        <div class="mini">De la columna más chica (cuotas, 1,67) a la más grande (ingreso, ₹1.410.000) hay seis órdenes de magnitud.</div>
      </div>
    </div>""" + franja(
                "Sí: pasar todo a la misma escala, con logaritmo en los montos con colas largas.",
                "Trabajar en rupias, o igualar escalas sin logaritmo (guarda 48,0).",
                "En rupias, el resumen «guarda» 95,5 de cada 100, pero es el ingreso disfrazado (peso 0,76). En la misma escala, 50,1, y aportan todas.",
                "Los indicadores pesan a todos los clientes por lo que hacen, no por cuánto ganan."))

# ------------------------------------------------------------------ 5. Resumir
quint = [("20 % de menor ingreso", 20.4), ("Siguiente 20 %", 21.0), ("20 % del medio", 20.6),
         ("Siguiente 20 %", 20.1), ("20 % de mayor ingreso", 18.4)]
s5 = lamina(5, "¿Tiene sentido resumir?",
            "Hallazgo 3: ingreso, cupo y gasto cuentan la misma historia, y no dicen nada del riesgo.",
            f"""<div class="fila">
      <div class="col-p">
        <div class="grande"><b>16 de 21</b><span>columnas se mueven juntas: ingreso, cupo, saldo, pagos, las 7 categorías de gasto, transacciones y uso de la app. Cuentan <b>cuánto pesa el cliente</b>.</span></div>
        <div class="mini">Ingreso y cupo van juntos casi siempre (0,98). El puntaje de crédito no pasa de 0,17 con ninguna otra columna: <b>va solo</b>.</div>
      </div>
      <div class="col-g">
        <div class="etq">De cada 100 clientes de cada nivel de ingreso, ¿cuántos están en el 20 % de peor puntaje?</div>
        {barras(quint, 25, lambda v: es(v), ancho=560)}
        <div class="aviso">Ganen lo que ganen, son unos 20 de cada 100. <b>El ingreso no sirve como filtro de riesgo.</b></div>
      </div>
    </div>""" + franja(
                "Sí se puede resumir: hay mucha información repetida.",
                "Seguir mirando las columnas una por una.",
                "16 de 21 columnas tienen una compañera con relación mayor que 0,6. El puntaje no pasa de 0,17 con ninguna.",
                "El tamaño del cliente cabe en un indicador. El riesgo no cabe en ese indicador: necesita el suyo."))

# ------------------------------------------------------------------ 6. Cuántas
s6 = lamina(6, "¿Cuántas componentes?",
            "Dos indicadores reemplazan la ficha de 21 columnas.",
            f"""<div class="fila">
      <div class="col-g">
        <div class="ficha">
          <div class="fhead"><span>Ficha mensual del cliente</span><small>antes: 21 columnas</small></div>
          <div class="find"><div><b>Índice de Tamaño</b><small>Resume 16 columnas de dinero y uso. Guarda la mitad de la información de la ficha: 50,1 de cada 100 partes.</small></div>
            <div class="medidor"><i style="width:72%;background:#1F4E79"></i></div></div>
          <div class="find"><div><b>Índice de Riesgo</b><small>Guarda solo 5,3 de cada 100 partes, pero es el que encuentra a los clientes en riesgo. Y resultó ser, en esencia, <b>su propio puntaje de crédito</b> (se parecen 0,82).</small></div>
            <div class="medidor"><i style="width:38%;background:#C8102E"></i></div></div>
        </div>
      </div>
      <div class="col-p">
        <div class="etq">¿Por qué no uno, tres u ocho?</div>
        <div class="opt"><b>1</b> El de tamaño solo no ve el riesgo (lámina 8).</div>
        <div class="opt"><b>3</b> La regla de «guardar más que una columna» agrega la edad, que no cambia la decisión.</div>
        <div class="opt"><b>8</b> Hacen falta para guardar 80 de cada 100 partes, pero nadie lee 8 números por cliente.</div>
      </div>
    </div>""" + franja(
                "Dos indicadores: Tamaño y Riesgo.",
                "Uno, tres (la regla) u ocho (para guardar el 80 %).",
                "El Índice de Riesgo encuentra a 6.580 de los 10.046 clientes de peor puntaje (66 %). El de Tamaño, solo a 1.832.",
                "Buena noticia: su puntaje ya medía bien el riesgo. Lo que le faltaba a la ficha es el tamaño, y eso es lo nuevo que les entregamos."))

# ------------------------------------------------------------------ 7. Qué mide
def semaforo(titulo, filas, nota):
    f = "".join(f'<div class="sf"><span>{a}</span><span class="sfb"><i style="width:{v}%;background:{c}"></i></span><b>{v:.0f}</b></div>'
                for a, v, c in filas)
    return f'<div class="sem"><div class="st">{titulo}</div>{f}<div class="sn">{nota}</div></div>'


rojo, nar, amar, verde = "#C8102E", "#E8833A", "#E9B44C", "#3A9D5D"
s7 = lamina(7, "¿Qué mide cada una?",
            "Hallazgo 4: el riesgo de sus clientes está en cómo pagan y cuánto cupo usan, no en cuánto ganan.",
            f"""<div class="fila">
      <div class="col-g"><div class="etq">De cada 100 clientes de cada franja, cuántos están en el 20 % de peor puntaje</div><div class="dos">
        {semaforo("Parte del saldo que pagan cada mes", [("30 % o menos", 94.1, rojo), ("30 a 60 %", 51.4, nar), ("60 a 90 %", 11.8, amar), ("más de 90 %", 1.6, verde)],
                  "Ustedes: solo 35 de cada 100 pagan casi todo. Competencia: 87.")}
        {semaforo("Parte del cupo que usan", [("menos de 30 %", 7.0, verde), ("30 a 50 %", 16.0, amar), ("50 a 70 %", 29.7, nar), ("más de 70 %", 53.0, rojo)],
                  "Ustedes: 43 % de uso promedio. Competencia: 21 %.")}
      </div></div>
      <div class="col-p">
        <div class="etq">Qué mide cada indicador (según sus pesos)</div>
        <div class="nombre"><b class="azul">Índice de Tamaño</b> = cupo (0,30) + ingreso (0,30) + saldo (0,29) + pagos y gasto (0,22 a 0,27). El puntaje pesa 0,01.</div>
        <div class="nombre"><b class="rojo">Índice de Riesgo</b> = peor puntaje (0,78) + más avances en efectivo (0,49) + tarjeta más nueva (0,34). Es su puntaje con dos señales más: por eso, para escoger clientes, basta con el puntaje.</div>
        <div class="mini">Que vayan juntos no prueba que uno cause el otro: son señales para mirar, no explicaciones.</div>
      </div>
    </div>""" + franja(
                "Llamar a los indicadores por lo que miden, según sus pesos: Tamaño y Riesgo.",
                "Ponerles nombre a ojo.",
                "En el de Tamaño, 16 columnas de dinero y uso pesan entre 0,20 y 0,30. El de Riesgo lo manda el puntaje (0,78). Proporción pagada: −0,59; uso del cupo: +0,47.",
                "Sus clientes viven más en las franjas rojas que los de la competencia. Ahí está el trabajo de cobranza preventiva."),
            FUENTE_COMP)

# ------------------------------------------------------------------ 8. Un solo número
gente = "".join(persona("#1F4E79") if k < 2 else persona("#C8102E", relleno=False) for k in range(10))
s8 = lamina(8, "¿Qué pierde el cliente con un solo número?",
            "Si ordenan a sus clientes solo por tamaño, 8 de cada 10 clientes en riesgo pasan desapercibidos.",
            f"""<div class="fila centro">
      <div class="col-g">
        <div class="gente">{gente}</div>
        <div class="gpie"><span><i class="cuad azul-f"></i>los encuentra</span><span><i class="cuad rojo-o"></i>se escapan</span></div>
      </div>
      <div class="col-p">
        <div class="grande rojo"><b>8.214</b><span>de los 10.046 clientes de peor puntaje se escapan si se escoge al 20 % más «grande»</span></div>
        <div class="mini">Es lo mismo que escoger al azar. Con el Índice de Riesgo, en cambio, se encuentran 6.580.</div>
      </div>
    </div>""" + franja(
                "Un solo indicador no basta.",
                "Ordenar la cartera solo por tamaño, el mejor resumen en un número.",
                "Escogiendo por tamaño se escapan 8.214 de 10.046 clientes en riesgo (82 %).",
                "Un seguimiento basado en «los clientes más grandes» deja fuera a casi todos los que van a necesitarlo."))

# ------------------------------------------------------------------ 9. Grupos
tarj = [("Basic", 66000), ("Silver", 227000), ("Gold", 519000), ("Platinum", 1053500), ("Signature", 4094500)]
peor_t = [("Basic", 20.3), ("Silver", 21.1), ("Gold", 20.7), ("Platinum", 18.0), ("Signature", 17.5)]
peor_o = [("Estudiante", 20.2), ("Jubilado", 20.6), ("Empleado privado", 20.5), ("Empleado público", 20.3),
          ("Independiente", 19.3), ("Empresario", 19.2)]
s9 = lamina(9, "¿Qué muestra el mapa?",
            "Hallazgo 5: la categoría de la tarjeta y la ocupación no sirven para escoger a quién vigilar.",
            f"""<div class="fila tres">
      <div><div class="etq">Cupo mediano por categoría</div>{barras(tarj, 4094500, lambda v: "₹" + es(v / 1000, 0) + " mil", ancho=270)}
        <div class="mini">La categoría ordena perfecto el tamaño…</div></div>
      <div><div class="etq rojo">De cada 100, en el 20 % de peor puntaje</div>{barras(peor_t, 25, lambda v: es(v), ancho=270, color="#C8102E")}
        <div class="mini">…pero el riesgo es el mismo en todas.</div></div>
      <div><div class="etq rojo">Lo mismo por ocupación</div>{barras(peor_o, 25, lambda v: es(v), ancho=200, color="#C8102E")}
        <div class="mini">Entre 19 y 21 de cada 100 en todas.</div></div>
    </div>
    <div class="continuo"><b>No hay «tipos» de cliente riesgoso:</b> el riesgo sube poco a poco, sin un punto natural de corte, así que el corte lo pone la Gerencia.
      Proponemos: <b>puntaje de 560 o menos</b> (una desviación por debajo del promedio de 629) y, dentro de ellos, la mitad más grande primero:
      <span class="z za">A · 3.998</span><span class="z zb">B · 4.303</span><span class="z zc">sin seguimiento · 41.699</span></div>""" + franja(
                "Un continuo: el corte se define, no se descubre.",
                "Escoger a quién seguir por categoría de tarjeta u ocupación.",
                "Las categorías se separan en tamaño (de −2,97 a 4,44 desviaciones) y no en riesgo (menos de 0,2). Cortar en el Índice de Riesgo, en vez del puntaje, gastaría 2.384 de 8.195 cupos en clientes que no están en riesgo.",
                "Si hoy asignan seguimiento por categoría de tarjeta, es una falla de procedimiento: cuesta lo mismo y no apunta al riesgo."))

# ------------------------------------------------------------------ 10. Plan
s10 = f"""
<section class="slide plan">
  <div class="kicker"><span class="num">Decisión 9 de 9</span><span>¿Qué decide el cliente?</span></div>
  <h1>Nuestra recomendación: 8.301 clientes al mes, empezando por los 3.998 que concentran el 85,6 % del dinero en juego.</h1>
  <div class="embudo">
    <div class="paso p0"><b>50.000</b><span>clientes en la cartera</span></div>
    <div class="flechita">→</div>
    <div class="paso p1"><b>8.301</b><span>con puntaje de 560 o menos (16,6 %)<br>deben ₹3.278 millones: el 21,6 % de todo el saldo</span></div>
    <div class="flechita">→</div>
    <div class="paso p2"><b>A · 3.998</b><span>los más grandes<br><strong>Llamada del gestor y congelar aumentos de cupo</strong><br>85,6 % del saldo de la lista</span></div>
    <div class="paso p3"><b>B · 4.303</b><span>los más pequeños<br><strong>Mensajes y oferta de refinanciación</strong><br>14,4 % del saldo de la lista</span></div>
  </div>
  <div class="fila abajo cuatro">
    <div class="caja"><div class="ct">Cómo se arma la lista</div>
      <p><b>Quién entra:</b> todo cliente con <b>560 puntos o menos</b>, una desviación por debajo del promedio de su cartera (629). Si tienen menos gestores, bajan el corte.</p>
      <p><b>En qué orden:</b> el Índice de Tamaño, lo nuevo del estudio. El riesgo ya estaba en su puntaje: usar el Índice de Riesgo gastaría 29 de cada 100 cupos en clientes que no están en riesgo.</p></div>
    <div class="caja"><div class="ct">Los 1.641 «disparejos»</div>
      <p><b>760</b> ya están en la lista (404 en la zona A): se atienden con ella.</p>
      <p>Los <b>881</b> restantes todavía no tienen mal puntaje: van a <b>revisión de la cuenta</b>, no a cobranza. Su patrón de gasto es raro y como grupo pagan menos.</p></div>
    <div class="caja"><div class="ct">Frente a la competencia</div>
      <p>Seguir cada mes el <b>uso del cupo</b> (43 % frente a 21 %) y la <b>proporción pagada</b> (35 % paga casi todo, frente a 87 %): son las dos señales que acompañan al puntaje.</p>
      <p>Revisar la política de <b>avances en efectivo</b>: los usa el 30 % de sus clientes; en el mercado, el 0,6 %.</p></div>
    <div class="caja oscura"><div class="ct">Lo que todavía no sabemos</div>
      <ul><li>No hay datos de mora real: el puntaje es nuestra mejor aproximación. Proponemos un piloto de 3 meses que mida la mora.</li>
      <li>Los conteos son de esta cartera; los cortes son relativos y se recalculan cada mes.</li>
      <li>Mostramos con qué va el riesgo, no qué lo causa.</li></ul></div>
  </div>
  <footer><span class="fuente">{FUENTE_COMP}</span><span>10 / {TOTAL}</span></footer>
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
