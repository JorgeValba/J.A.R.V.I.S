"""Batuta, el orquestador: decide el orden y pasa el output de cada agente como input del siguiente.

Como un director de orquesta, no toca ningún instrumento: dirige a Iris, Euler y Vera."""
import json
import os
import re
from datetime import datetime, timezone

from . import config
from .agentes import agente_analista, agente_comunicador, agente_recolector, es_demo

PATRON_TICKER = re.compile(r"[A-Z0-9.\-]{1,12}")


def normalizar_ticker(texto):
    """'aapl ' → 'AAPL'. Lanza ValueError si no parece un ticker."""
    ticker = (texto or "").strip().upper()
    if not PATRON_TICKER.fullmatch(ticker):
        raise ValueError(f"Ticker no válido: '{texto}'. Ejemplo correcto: AAPL")
    return ticker


def pipeline(ticker, avisar=print, guardar=True):
    """Batuta ejecuta la cadena Iris → Euler → Vera.

    avisar: función que recibe textos de avance (print en terminal, enviar a Telegram en el bot).
    Devuelve un diccionario con las tres entregas, útil como evidencia.
    """
    ticker = normalizar_ticker(ticker)
    modo = "SIMULACIÓN" if config.MODO_SIMULACION else "REAL"

    avisar(f"🎼 Batuta · Orquestador\nRecibí tu orden. Inicio la cadena para {ticker} (modo {modo}).")
    avisar(f"🛰️ Iris · Recolectora buscando datos de {ticker}…")
    ficha, herramientas = agente_recolector(ticker)
    if es_demo(ficha) and not config.MODO_SIMULACION:
        modo = "DEMO"
    if config.MODO_CLASE:
        avisar("📦 Entrega 1→2 · Iris → Euler\n"
               f"{ticker} · {ficha.get('nombre')} · {ficha.get('sector')}\n"
               f"Precio {ficha.get('precio')} USD · cambio {ficha.get('cambio_pct')} %\n"
               f"Beta {ficha.get('beta')} · P/E {ficha.get('pe_ratio')} · rango {ficha.get('min_52s')}–{ficha.get('max_52s')}\n"
               f"{ficha['fuente']} · {ficha.get('fecha_dato')}\n"
               f"MCP: {', '.join(herramientas) or 'ninguna'}")

    avisar("🧮 Euler · Analista calculando e interpretando…")
    analisis = agente_analista(ficha)
    if config.MODO_CLASE:
        avisar("📦 Entrega 2→3 · Euler → Vera\n" + "\n".join(analisis["lectura"].values()))

    avisar("✍️ Vera · Comunicadora redactando la nota…")
    nota = agente_comunicador(analisis)

    resultado = {
        "ticker": ticker,
        "elaborado_por": "Jorge Valencia",
        "modo_solicitado": "SIMULACIÓN" if config.MODO_SIMULACION else "REAL",
        "modo": modo,
        "fecha_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "entrega_1_ficha": ficha,
        "herramientas_mcp": herramientas,
        "entrega_2_analisis": analisis,
        "entrega_3_nota": nota,
    }
    if guardar:
        resultado["archivo"] = guardar_evidencia(resultado)
    return resultado


def guardar_evidencia(resultado):
    """Guarda la corrida completa en salidas/TICKER_fecha.json (evidencia para la rúbrica)."""
    os.makedirs(config.CARPETA_SALIDAS, exist_ok=True)
    sello = resultado["fecha_utc"].replace(":", "").replace("-", "")[:15]
    ruta = os.path.join(config.CARPETA_SALIDAS, f"{resultado['ticker']}_{sello}.json")
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(resultado, archivo, ensure_ascii=False, indent=2)
    return ruta
