"""Construye presentacion.html (10 láminas 16:9) para la sustentación del corte 2.

La historia, con el estilo de la exposición de correspondencias: se parte de una creencia común del
banco y se pone a prueba con los datos.

  Creencia: «más rico, más seguro». El banco sube cupos y asciende tarjetas (hasta Signature) según
  el ingreso, y vigila sobre todo a los clientes pequeños.
  Respuesta: no. El tamaño del cliente y su riesgo van en direcciones distintas. El ingreso dice
  cuánto está en juego, no quién va a pagar.

Orden: 1 portada · 2 su cartera frente al mercado · 3 a 5 preparar la ficha (variables, atípicos,
escala) · 6 primera evidencia · 7 los dos ejes · 8 el costo de la creencia · 9 la tarjeta y el mapa ·
10 la decisión. Cubre las nueve decisiones de la guía en el mismo orden; la tabla completa está en el .Rmd.

Las cifras salen del informe analisis_synthetic_credit_card.html (tabla de decisiones, Módulos 13 a 17
y Módulo 20 para el mercado).

Para el PDF:
  brave-browser --headless --disable-gpu --no-pdf-header-footer \
      --print-to-pdf=presentacion.pdf presentacion.html
"""
import math
from pathlib import Path

AQUI = Path(__file__).resolve().parent
TOTAL = 10
AZUL, NARANJA, GRIS = "#2E6FA8", "#E8833A", "#C3CAD4"


def lamina(n, titulo, cuerpo, oscura=False, antetitulo=""):
    clase = "slide oscura" if oscura else "slide"
    ante = f'<div class="tag">{antetitulo}</div>' if antetitulo else ""
    return f"""
<section class="{clase}">
  {ante}<h1>{titulo}</h1>
  <div class="cuerpo">{cuerpo}</div>
  <div class="pag">{n} / {TOTAL}</div>
</section>"""


def persona(color, relleno=True):
    fill = color if relleno else "none"
    return (f'<svg viewBox="0 0 40 80" class="persona"><circle cx="20" cy="13" r="11" fill="{fill}" stroke="{color}" stroke-width="3"/>'
            f'<path d="M4 76 V44 Q4 29 20 29 Q36 29 36 44 V76 Z" fill="{fill}" stroke="{color}" stroke-width="3"/></svg>')


def barras(datos, maximo, fmt, ancho=520, color=AZUL):
    out = []
    for etq, v, *c in datos:
        col = c[0] if c else color
        out.append(f'<div class="br"><span class="brn">{etq}</span><span class="brt">'
                   f'<span class="brb" style="width:{max(abs(v) / maximo * ancho, 4):.0f}px;background:{col}"></span>'
                   f'<span class="brv">{fmt(v)}</span></span></div>')
    return "".join(out)


def es(x, d=1):
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def icono(nombre):
    trazos = {
        "banco": '<path d="M4 20h16M5 17V10M9 17V10M15 17V10M19 17V10M3 9l9-5 9 5z"/>',
        "lista": '<path d="M9 6h11M9 12h11M9 18h11"/><circle cx="4.5" cy="6" r="1.3"/><circle cx="4.5" cy="12" r="1.3"/><circle cx="4.5" cy="18" r="1.3"/>',
        "lupa": '<circle cx="10.5" cy="10.5" r="6"/><path d="M15 15l5 5"/>',
    }
    return f'<svg viewBox="0 0 24 24" class="ico">{trazos[nombre]}</svg>'


TARJETAS = [("Basic", 66, 20.3), ("Silver", 227, 21.1), ("Gold", 519, 20.7), ("Platinum", 1054, 18.0), ("Signature", 4094, 17.5)]

# ------------------------------------------------------------------ 1. Portada: la creencia
escalera = "".join(
    f'<div class="esc"><i style="height:{70 + k * 62}px"></i><span>{t}</span></div>' for k, (t, _, _) in enumerate(TARJETAS))
s1 = f"""
<section class="slide oscura portada">
  <div class="izq">
    <div class="marca">Componentes principales · Gerencia de Riesgo de Crédito</div>
    <h1 class="gigante">¿Más rico,<br>más seguro?</h1>
    <p class="sub">El banco sube cupos y asciende tarjetas según el ingreso, y vigila sobre todo a los clientes pequeños. ¿El cliente que más gana es de verdad el que menos riesgo tiene?</p>
    <div class="items">
      <div>{icono("banco")}<div><b>El cliente</b><span>La Gerencia de Riesgo de Crédito del banco emisor.</span></div></div>
      <div>{icono("lista")}<div><b>La decisión</b><span>A quién subir el cupo, a quién ascender de tarjeta y a quién vigilar cada mes.</span></div></div>
      <div>{icono("lupa")}<div><b>Los datos</b><span>50.000 tarjetas. No hay datos de mora: el riesgo se mide con el puntaje de crédito.</span></div></div>
    </div>
    <div class="equipo">Equipo 02 · Oscar Contreras · Juan Pablo Sarmiento · Steven Navarro · Juan Diego Grajales</div>
  </div>
  <div class="der"><div class="escalera">{escalera}</div><div class="leyenda">Cada categoría de tarjeta, más cupo que la anterior</div></div>
  <div class="pag">1 / {TOTAL}</div>
</section>"""

# ------------------------------------------------------------------ 2. Su cartera frente al mercado
def comp(titulo, nos, mercado, w_nos, w_mer, nota):
    return (f'<div class="cmp"><div class="cmpt">{titulo}</div>'
            f'<div class="cmpb"><span class="cl">su cartera</span><span class="ct2"><i style="width:{w_nos}%;background:{NARANJA}"></i></span><b class="naranja">{nos}</b></div>'
            f'<div class="cmpb"><span class="cl">mercado</span><span class="ct2"><i style="width:{w_mer}%;background:{GRIS}"></i></span><b class="gr">{mercado}</b></div>'
            f'<div class="cmpn">{nota}</div></div>')


s2 = lamina(2, "Su cartera usa el doble del cupo y paga menos que el mercado",
            f"""<div class="rejilla-cmp">
      {comp("Uso del cupo", "43 %", "21 %", 86, 42, "el doble")}
      {comp("Pagan su saldo completo", "35 %", "87 %", 35, 87, "menos de la mitad")}
      {comp("Usan avances en efectivo", "30 %", "0,6 %", 60, 1.5, "50 veces más")}
      {comp("Saldo pendiente por tarjeta", "₹303 mil", "₹28 mil", 100, 9, "11 veces más")}
    </div>
    <p class="frase">Si el riesgo está creciendo, importa saber dónde buscarlo. La creencia del banco dice: en los clientes de menor ingreso.</p>
    <p class="fuente-claro">Mercado de tarjetas de India: RBI (2025-2026), SBI Card (2026) y Banco Mundial (Findex 2024). La cartera es simulada: las cifras muestran la dirección del problema, no su tamaño exacto.</p>""",
            antetitulo="El problema")

# ------------------------------------------------------------------ 3. Variables
cuadros = "".join(f'<i class="{"fuera" if k in (3, 9, 14, 19, 24) else ""}"></i>' for k in range(26))
s3 = lamina(3, "Antes de probarlo, la ficha suma dos veces el mismo dinero",
            f"""<div class="fila centro">
      <div class="waffle26">{cuadros}</div>
      <div class="dato"><b>21</b><span>de las 26 columnas bastan para describir a cada cliente</span>
        <p class="nota">Salen el gasto total, el saldo pendiente, los puntos ganados, la proporción pagada y el uso del cupo:
        son sumas, copias o cocientes de otras columnas. Las dos últimas se guardan para leer el riesgo al final.</p></div>
    </div>""", antetitulo="Preparar la ficha")

# ------------------------------------------------------------------ 4. Atípicos
cuadros100 = "".join(f'<i class="{"raro" if k in (7, 41, 73) else ""}"></i>' for k in range(100))
s4 = lamina(4, "No borramos a nadie: los clientes «raros» tienen peor puntaje",
            f"""<div class="fila centro">
      <div class="waffle100">{cuadros100}<p class="pie">Cada cuadro, 500 clientes. 1.641 son «raros» (3,3 %): lejos del resto en la combinación de sus datos.</p></div>
      <div class="col">
        <div class="dato"><b class="naranja">573</b><span>puntaje mediano de los raros, contra 639 del resto</span></div>
        <div class="casos"><div class="ct">Los tres más lejanos</div>
          <div><b>CC145327</b> combustible casi en cero <em>real</em></div>
          <div><b>CC107443</b> compras en línea casi en cero <em>real</em></div>
          <div><b>CC139311</b> viajes casi en cero <em>real</em></div>
          <p class="nota">0 faltantes y 0 errores: se marcan y se estudian.</p></div>
      </div>
    </div>""", antetitulo="Preparar la ficha")

# ------------------------------------------------------------------ 5. Estandarizar
sds = [("ingreso", 1410000), ("cupo", 1010000), ("saldo facturado", 560000), ("pagos", 453000), ("avances", 78000),
       ("mercado", 23700), ("servicios", 16800), ("en línea", 16600), ("combustible", 15500), ("restaurantes", 13700),
       ("entretenimiento", 12300), ("viajes", 10700), ("puntos redimidos", 2360), ("valor por compra", 780),
       ("puntaje", 68.4), ("transacciones", 42.0), ("antigüedad", 31.2), ("app", 16.8), ("edad", 12.2),
       ("internacionales", 2.60), ("cuotas", 1.67)]
filas_sd = "".join(f'<div class="sd"><span>{a}</span><i style="width:{(math.log10(v) + 0.5) / 6.8 * 260:.0f}px"></i></div>' for a, v in sds)
s5 = lamina(5, "En rupias, el ingreso tapa todo: hay que medir con la misma regla",
            f"""<div class="fila">
      <div class="col ancha">
        <div class="ct">Cuánto guarda el primer resumen, de cada 100 partes</div>
        <div class="gb"><span class="gl">En rupias</span><span class="gt"><i style="width:95.5%;background:{GRIS}"></i></span><b>95,5</b></div>
        <p class="gn">pero es el ingreso con otro nombre</p>
        <div class="gb"><span class="gl">Misma escala</span><span class="gt"><i style="width:50.1%;background:{AZUL}"></i></span><b class="azul">50,1</b></div>
        <p class="gn">y lo construyen las 21 columnas</p>
        <p class="frase">En rupias, la prueba estaría amañada: el ingreso ganaría solo por medirse en millones.</p>
      </div>
      <div class="col"><div class="ct">Cuánto varía cada columna (escala log)</div><div class="sds">{filas_sd}</div>
        <p class="pie">De 1,67 cuotas a ₹1.410.000 de ingreso.</p></div>
    </div>""", antetitulo="Preparar la ficha")

# ------------------------------------------------------------------ 6. Primera evidencia
quint = [("menor ingreso", 20.4), ("", 21.0), ("", 20.6), ("", 20.1), ("mayor ingreso", 18.4)]
cols_q = "".join(f'<div class="cq"><b>{es(v)}</b><i style="height:{v * 9:.0f}px"></i><span>{e}</span></div>' for e, v in quint)
s6 = lamina(6, "Ganen lo que ganen, 20 de cada 100 tienen el peor puntaje",
            f"""<div class="fila centro">
      <div class="col ancha"><div class="ct">De cada 100 clientes de cada nivel de ingreso, cuántos están en el 20 % de peor puntaje</div>
        <div class="columnas">{cols_q}</div></div>
      <div class="col">
        <div class="dato"><b class="azul">0,98</b><span>ingreso y cupo se mueven juntos: el dinero se repite en la ficha.</span></div>
        <div class="dato"><b class="naranja">0,17</b><span>es lo más que el puntaje se parece a cualquier otra columna.</span></div>
      </div>
    </div>""", oscura=True, antetitulo="La prueba")

# ------------------------------------------------------------------ 7. Dos ejes
def mini_pesos(datos, color):
    return "".join(f'<div class="mp"><span>{a}</span><i style="width:{v / 0.8 * 100:.0f}%;background:{color}"></i><b>{es(v, 2)}</b></div>' for a, v in datos)


s7 = lamina(7, "La ficha dice dos cosas que no tienen que ver entre sí",
            f"""<div class="dos-tarjetas">
      <div class="tarjeta"><span class="tt azul">Tamaño · cuánto dinero hay en juego</span><b>50,1</b><span class="tx">de cada 100 partes de la ficha</span>
        <div class="mps">{mini_pesos([("cupo", 0.30), ("ingreso", 0.30), ("saldo", 0.29), ("puntaje", 0.01)], AZUL)}</div></div>
      <div class="tarjeta"><span class="tt naranja">Riesgo · qué tan riesgoso es</span><b>5,3</b><span class="tx">guarda poco, pero es el único que ve el riesgo</span>
        <div class="mps">{mini_pesos([("peor puntaje", 0.78), ("avances", 0.49), ("tarjeta nueva", 0.34), ("ingreso", 0.00)], NARANJA)}</div></div>
    </div>
    <p class="frase centrada">El ingreso no pesa en el riesgo (0,00), y el puntaje casi no pesa en el tamaño (0,01).</p>""",
            antetitulo="La prueba")

# ------------------------------------------------------------------ 8. El costo de la creencia
gente = "".join(persona("#FFFFFF") if k < 2 else persona(NARANJA, relleno=False) for k in range(10))
s8 = lamina(8, "Si vigila a los clientes por su tamaño, 8 de cada 10 en riesgo se escapan",
            f"""<div class="fila centro">
      <div class="gente">{gente}</div>
      <div class="dato"><b class="naranja">8.214</b><span>de los 10.046 clientes de peor puntaje quedan fuera si se escoge a los más «grandes». Es lo mismo que escoger al azar.</span></div>
    </div>""", oscura=True, antetitulo="El costo de la creencia")

# ------------------------------------------------------------------ 9. Signature y el mapa
combo = "".join(
    f'<div class="cb"><span class="cbr">{es(r)}</span><i class="cbbar" style="height:{20 + math.log10(c) / math.log10(4094) * 300:.0f}px"></i>'
    f'<span class="cbt">{t}</span><span class="cbc">₹{es(c, 0)} mil</span></div>' for t, c, r in TARJETAS)
BRUJULA = f'''<svg viewBox="0 0 330 290" class="brujula"><defs>
<marker id="pa" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{AZUL}"/></marker>
<marker id="pn" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{NARANJA}"/></marker></defs>
<line x1="10" y1="150" x2="320" y2="150" stroke="#E2E5EA" stroke-width="2"/><line x1="130" y1="10" x2="130" y2="285" stroke="#E2E5EA" stroke-width="2"/>
''' + "".join(f'<line x1="130" y1="150" x2="{x}" y2="{y}" stroke="{AZUL}" stroke-width="2.5" marker-end="url(#pa)"/>'
              for x, y in [(276, 150), (276, 152), (271, 129), (264, 160), (259, 152), (250, 152), (238, 152)]) + f'''
<line x1="130" y1="150" x2="133" y2="273" stroke="{NARANJA}" stroke-width="4" marker-end="url(#pn)"/>
<line x1="130" y1="150" x2="142" y2="72" stroke="{NARANJA}" stroke-width="4" marker-end="url(#pn)"/>
<path d="M 160 150 A 30 30 0 0 1 131 179" fill="none" stroke="#6B7585" stroke-width="1.5"/><text x="150" y="182" class="b4">88°</text>
<text x="180" y="185" class="b1">dinero y uso</text><text x="180" y="203" class="b2">16 flechas juntas</text>
<text x="140" y="282" class="b3">puntaje</text><text x="150" y="78" class="b3">avances</text></svg>'''
s9 = lamina(9, "Signature ordena el cupo, no el riesgo",
            f"""<div class="fila">
      <div class="col ancha"><div class="ct">Cupo mediano por categoría (barras) y, arriba, de cada 100, cuántos tienen el peor puntaje</div>
        <div class="combo">{combo}</div></div>
      <div class="col">{BRUJULA}<p class="pie">En el mapa, el puntaje va en ángulo recto con el dinero (88°). Los clientes forman un continuo: no hay un «tipo» de cliente riesgoso.</p></div>
    </div>""", antetitulo="La prueba, con la tarjeta")

# ------------------------------------------------------------------ 10. La decisión
s10 = f"""
<section class="slide oscura final">
  <div class="tag">La respuesta</div>
  <h1 class="gigante">El ingreso dice cuánto está en juego,<br>no quién va a pagar</h1>
  <div class="flujo">
    <div class="paso"><b>8.301</b><span>clientes con 560 puntos o menos, en todas las tarjetas. Deben el 21,6 % del saldo de la cartera.</span></div>
    <div class="paso fuerte"><b>3.998</b><span>son grandes y concentran el 85,6 % de ese saldo: los que la creencia daba por seguros. Primero, llamada del gestor.</span></div>
    <div class="paso"><b>4.303</b><span>son pequeños: mensajes y oferta de refinanciación. El resto, 41.699, sin seguimiento.</span></div>
  </div>
  <div class="recom"><b>Qué cambia:</b> no subir el cupo ni ascender de tarjeta sin mirar el puntaje · vigilar por puntaje, no por ingreso ni por categoría · seguir el uso del cupo y la proporción pagada.</div>
  <div class="nosabemos"><b>Lo que todavía no sabemos:</b> no hay datos de mora (el puntaje es la aproximación) · la cartera es simulada y los conteos se recalculan con la real · los datos muestran con qué va el riesgo, no qué lo causa.</div>
  <div class="pag">10 / {TOTAL}</div>
</section>"""

css = (AQUI / "estilo.css").read_text(encoding="utf-8")
html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Más rico, más seguro</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{css}</style></head><body>
{s1}{s2}{s3}{s4}{s5}{s6}{s7}{s8}{s9}{s10}
</body></html>"""
(AQUI / "presentacion.html").write_text(html, encoding="utf-8")
print("ok")
