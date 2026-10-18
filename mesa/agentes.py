"""Los tres agentes de la Mesa Financiera.

  Iris  · La Recolectora  (Agente 1) → consulta Alpha Vantage por MCP y entrega una FICHA (JSON)
  Euler · El Analista     (Agente 2) → recibe la ficha, Python calcula y OpenAI interpreta → ANÁLISIS (JSON)
  Vera  · La Comunicadora (Agente 3) → recibe el análisis y redacta la NOTA final para Telegram
  (Batuta, el orquestador que los dirige, vive en mesa/pipeline.py)

Regla de oro: los números los calcula el código; la IA solo interpreta.
"""
import json

from . import config

DESCARGO = "Nota educativa, no es recomendación de inversión."
FIRMA_VERA = "✍️ Vera · Comunicadora"

# ----------------------------------------------------------------------
# Conexión con OpenAI (solo se usa fuera del modo simulación)
# ----------------------------------------------------------------------
_cliente = None


def _cliente_openai():
    global _cliente
    if _cliente is None:
        from openai import OpenAI
        # El nombre personalizado es intencional: no usar OPENAI_API_KEY.
        _cliente = OpenAI(api_key=config.OPENIA_API_KEY, timeout=90.0, max_retries=1)
    return _cliente


def llamar_openai(system, mensaje, usar_mcp=False, max_tokens=900):
    """Responses API: devuelve (texto, nombres de llamadas MCP exitosas).

    No registrar la respuesta cruda: la URL MCP contiene una credencial.
    """
    from urllib.parse import quote
    base = dict(model=config.MODELO, max_output_tokens=max_tokens,
                instructions=system, input=[{"role": "user", "content": mensaje}],
                reasoning={"effort": "none"}, store=False)
    if usar_mcp:
        base["tools"] = [{
            "type": "mcp", "server_label": "alphavantage",
            "server_url": "https://mcp.alphavantage.co/mcp?apikey="
                          + quote(config.ALPHAVANTAGE_API_KEY, safe=""),
            # El bot solo consulta el servidor bursátil definido por el proyecto.
            "require_approval": "never",
        }]
    try:
        respuesta = _cliente_openai().responses.create(**base)
        if respuesta.status != "completed":
            raise ValueError("Respuesta de OpenAI incompleta o fallida")
        texto = (respuesta.output_text or "").strip()
        if not texto:
            raise ValueError("OpenAI no devolvió texto")
        llamadas = [b for b in respuesta.output if b.type == "mcp_call"]
        if usar_mcp and (not llamadas or any(b.error for b in llamadas)):
            raise ValueError("MCP no devolvió llamadas exitosas")
        return texto, [b.name for b in llamadas]
    except Exception as error:
        # Evita que mensajes del SDK/HTTP revelen llaves o URLs autenticadas.
        raise RuntimeError("No se pudo completar la llamada a OpenAI/MCP ("
                           + type(error).__name__ + ")") from None


def extraer_json(texto):
    """Recupera el objeto JSON de un texto (a veces el modelo agrega palabras alrededor)."""
    inicio, fin = texto.find("{"), texto.rfind("}")
    if inicio == -1 or fin <= inicio:
        raise ValueError("El agente no devolvió JSON")
    return json.loads(texto[inicio:fin + 1])


def a_numero(valor):
    """Convierte '123.4', '-0.8%' o '1,234' en número; si no se puede, None."""
    try:
        return float(str(valor).replace("%", "").replace(",", ""))
    except (TypeError, ValueError):
        return None


# ----------------------------------------------------------------------
# IRIS · La Recolectora (Agente 1)
# ----------------------------------------------------------------------
PROMPT_RECOLECTOR = """Eres Iris, la Recolectora (Agente 1) de una mesa financiera educativa.
Tu personalidad: curiosa y meticulosa; jamás inventas un dato.
Tarea: obtener datos REALES de la acción indicada con las herramientas de Alpha Vantage.
Reglas:
- Haz como máximo 2 consultas: cotización actual y datos generales de la empresa.
- NUNCA inventes cifras. Si un dato no está disponible, escribe null.
- Responde SOLO con un JSON con estas claves exactas:
  ticker, nombre, sector, precio, cambio_pct, fecha_dato, pe_ratio, beta,
  max_52s, min_52s, cap_mercado_usd"""

DATOS_DEMO = {
    "nombre": "Empresa ficticia (simulación)", "sector": "Tecnología",
    "precio": 150.0, "cambio_pct": 1.2, "fecha_dato": "dato ficticio",
    "pe_ratio": 28.0, "beta": 1.25, "max_52s": 180.0, "min_52s": 120.0,
    "cap_mercado_usd": None,
}


def ficha_demo(ticker, motivo):
    ficha = {"ticker": ticker, **DATOS_DEMO}
    ficha["fuente"] = f"DATOS DEMO, no son reales ({motivo})"
    return ficha


def agente_recolector(ticker):
    """Devuelve (ficha, herramientas_usadas)."""
    if config.MODO_SIMULACION:
        return ficha_demo(ticker, "modo simulación"), []
    try:
        texto, herramientas = llamar_openai(PROMPT_RECOLECTOR, f"Acción: {ticker}", usar_mcp=True)
        ficha = extraer_json(texto)
        ficha["ticker"] = ticker
        ficha["fuente"] = "Alpha Vantage vía MCP"
        return ficha, herramientas
    except Exception as error:                     # MCP caído, cuota agotada o JSON inválido
        return ficha_demo(ticker, f"MCP no disponible: {type(error).__name__}"), []


# ----------------------------------------------------------------------
# EULER · El Analista (Agente 2)
# ----------------------------------------------------------------------
def calcular_indicadores(ficha):
    """Cálculos deterministas (la IA no hace aritmética)."""
    precio, maximo, minimo = (a_numero(ficha.get(k)) for k in ("precio", "max_52s", "min_52s"))
    beta, pe = a_numero(ficha.get("beta")), a_numero(ficha.get("pe_ratio"))

    # Posición en el rango de 52 semanas: (P - min) / (max - min) × 100
    posicion = None
    if None not in (precio, maximo, minimo) and maximo > minimo:
        posicion = round((precio - minimo) / (maximo - minimo) * 100, 1)

    # Semáforo de beta (umbrales didácticos, no normativos)
    if beta is None:
        semaforo = "⚪ sin dato de beta"
    elif beta < 0.8:
        semaforo = "🟢 volatilidad baja"
    elif beta <= 1.2:
        semaforo = "🟡 volatilidad similar al mercado"
    else:
        semaforo = "🔴 volatilidad alta"

    return {"posicion_rango_52s_pct": posicion, "semaforo_beta": semaforo,
            "beta": beta, "pe_ratio": pe, "cambio_pct": a_numero(ficha.get("cambio_pct"))}


PROMPT_ANALISTA = """Eres Euler, el Analista (Agente 2). Recibes la ficha de Iris y unos indicadores ya calculados.
Tu personalidad: riguroso con los números y paciente para explicarlos.
NO recalcules ni cambies cifras. Interprétalas para un principiante.
Responde SOLO con JSON con las claves:
  lectura_precio (1 frase), lectura_riesgo (1 frase sobre beta),
  lectura_valuacion (1 frase sobre P/E, aclarando que depende del sector),
  pregunta_para_investigar (1 pregunta que el alumno debería investigar)"""


def lectura_simulada(ind):
    pos = ind["posicion_rango_52s_pct"]
    lectura_precio = ("No hay datos suficientes para ubicar el precio en su rango anual." if pos is None else
                      f"El precio está al {pos} % de su rango de 52 semanas (0 % = mínimo, 100 % = máximo).")
    return {
        "lectura_precio": lectura_precio,
        "lectura_riesgo": f"Semáforo de beta: {ind['semaforo_beta']}.",
        "lectura_valuacion": "El P/E solo se interpreta comparándolo con empresas del mismo sector.",
        "pregunta_para_investigar": "¿Cuál es el P/E promedio del sector de esta empresa?",
    }


def agente_analista(ficha):
    indicadores = calcular_indicadores(ficha)
    if config.MODO_SIMULACION:
        lectura = lectura_simulada(indicadores)
    else:
        entrada = json.dumps({"ficha": ficha, "indicadores": indicadores}, ensure_ascii=False)
        texto, _ = llamar_openai(PROMPT_ANALISTA, entrada)
        try:
            lectura = extraer_json(texto)
        except ValueError:
            lectura = {"lectura_precio": texto[:300]}
    return {"ficha": ficha, "indicadores": indicadores, "lectura": lectura}


# ----------------------------------------------------------------------
# VERA · La Comunicadora (Agente 3)
# ----------------------------------------------------------------------
PROMPT_COMUNICADOR = f"""Eres Vera, la Comunicadora (Agente 3). Con el análisis de Euler, redacta una nota para Telegram.
Tu personalidad: clara, breve y honesta sobre los límites del análisis.
- Máximo 900 caracteres, español claro, 3 a 5 emojis como máximo.
- Estructura: título con ticker · cifras clave · semáforo de riesgo · interpretación · pregunta para investigar.
- Usa solo las cifras recibidas; si la fuente dice DEMO, adviértelo en la primera línea.
- Cierra SIEMPRE con: "{DESCARGO}"
Texto plano, sin Markdown."""


def nota_simulada(analisis):
    f, ind, lec = analisis["ficha"], analisis["indicadores"], analisis["lectura"]
    return (f"{FIRMA_VERA}\n⚠️ {f['fuente']}\n"
            f"📊 {f['ticker']} · {f['nombre']}\n"
            f"Precio: {f['precio']} USD ({ind['cambio_pct']} % en el día)\n"
            f"Riesgo: {ind['semaforo_beta']} (beta {ind['beta']})\n"
            f"{lec['lectura_precio']}\n"
            f"{lec['lectura_valuacion']}\n"
            f"🔎 {lec['pregunta_para_investigar']}\n\n{DESCARGO}")


def agente_comunicador(analisis):
    if config.MODO_SIMULACION:
        return nota_simulada(analisis)
    texto, _ = llamar_openai(PROMPT_COMUNICADOR, json.dumps(analisis, ensure_ascii=False), max_tokens=600)
    if DESCARGO not in texto:                      # garantía aunque el modelo lo olvide
        texto += f"\n\n{DESCARGO}"
    return f"{FIRMA_VERA}\n{texto}"
