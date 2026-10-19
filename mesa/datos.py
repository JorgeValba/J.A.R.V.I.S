"""Datos verificables de Alpha Vantage para Jorge Valencia, sin extracción por IA.

Solo GLOBAL_QUOTE (cierre) y OVERVIEW (fundamentales, según plan).
No registrar respuestas/URLs crudas: podrían incluir credenciales.
"""
import math
from datetime import datetime, date, timezone
import requests

URL_API = "https://www.alphavantage.co/query"
MAX_ANTIGUEDAD_DIAS = 7  # tolerancia explícita para fines de semana y festivos
CAMPOS = ("nombre", "sector", "precio", "cambio_pct", "fecha_dato", "pe_ratio",
          "beta", "max_52s", "min_52s", "cap_mercado_usd")
ERRORES = {
    "CUOTA": "Alpha Vantage indicó límite de consultas; espera a que se restablezca tu cuota.",
    "PLAN": "Alpha Vantage exige un plan o permiso adicional para esta consulta.",
    "CLAVE": "Alpha Vantage rechazó la clave; revisa ALPHAVANTAGE_API_KEY.",
    "DEMO": "La clave demo del proveedor no sirve para validar datos actuales de tu ticker.",
    "RED": "No se pudo conectar con Alpha Vantage.",
    "RESPUESTA": "Alpha Vantage no devolvió una respuesta de datos válida.",
    "VACIO": "Alpha Vantage no devolvió datos para este ticker.",
    "ANTIGUO": "La cotización supera la tolerancia de siete días; no se utilizará como actual.",
    "FECHA": "La cotización no tiene una fecha válida o su fecha está en el futuro.",
    "TICKER": "El ticker devuelto por Alpha Vantage no coincide con el solicitado.",
    "PRECIO": "La cotización no contiene un precio positivo y finito.",
}


class ErrorDatos(RuntimeError):
    def __init__(self, codigo):
        self.codigo = codigo
        super().__init__(ERRORES[codigo])


def numero(valor):
    if valor is None or isinstance(valor, bool):
        return None
    try:
        n = float(str(valor).replace(",", "").replace("%", ""))
        return n if math.isfinite(n) else None
    except (ValueError, TypeError):
        return None


def texto(valor, limite=160):
    if not isinstance(valor, str) or valor.strip().lower() in ("", "none", "null", "n/a"):
        return None
    return " ".join(valor.split())[:limite]


def clasificar_aviso(mensaje):
    m = str(mensaje).lower()
    if any(p in m for p in ("rate limit", "call frequency", "requests per day", "api limit", "quota", "25 requests", "higher api call")):
        return "CUOTA"
    if any(p in m for p in ("premium", "subscription", "entitlement", "subscribe")):
        return "PLAN"
    if "demo" in m:
        return "DEMO"
    if any(p in m for p in ("api key", "apikey", "invalid key")):
        return "CLAVE"
    return "RESPUESTA"


def consultar(funcion, ticker, clave):
    if not clave or clave.strip().lower() == "demo":
        raise ErrorDatos("DEMO" if clave else "CLAVE")
    try:
        r = requests.get(URL_API, params={"function": funcion, "symbol": ticker,
                                         "apikey": clave}, timeout=30)
        if r.status_code == 429:
            raise ErrorDatos("CUOTA")
        if r.status_code in (401, 403):
            raise ErrorDatos("CLAVE")
        r.raise_for_status()
        datos = r.json()
    except requests.RequestException:
        raise ErrorDatos("RED") from None
    except ValueError:
        raise ErrorDatos("RESPUESTA") from None
    if not isinstance(datos, dict):
        raise ErrorDatos("RESPUESTA")
    for campo in ("Information", "Note", "Error Message"):
        if campo in datos:
            raise ErrorDatos(clasificar_aviso(datos[campo]))
    return datos


def validar_cotizacion(datos, ticker, hoy=None):
    q = datos.get("Global Quote")
    if not isinstance(q, dict) or not q:
        raise ErrorDatos("VACIO")
    if str(q.get("01. symbol", "")).upper() != ticker:
        raise ErrorDatos("TICKER")
    precio = numero(q.get("05. price"))
    if precio is None or precio <= 0:
        raise ErrorDatos("PRECIO")
    try:
        fecha = date.fromisoformat(q.get("07. latest trading day", ""))
    except (TypeError, ValueError):
        raise ErrorDatos("FECHA") from None
    hoy = hoy or datetime.now(timezone.utc).date()
    edad = (hoy - fecha).days
    if edad < 0:
        raise ErrorDatos("FECHA")
    if edad > MAX_ANTIGUEDAD_DIAS:
        raise ErrorDatos("ANTIGUO")
    return {"precio": precio, "cambio_pct": numero(q.get("10. change percent")),
            "fecha_dato": fecha.isoformat(), "antiguedad_dias": edad}


def obtener_ficha(ticker, clave):
    """Máximo dos consultas; no se generan precios de respaldo en modo real."""
    ficha = {"ticker": ticker, **dict.fromkeys(CAMPOS), "moneda": None,
             "fuente": "Alpha Vantage API oficial", "tipo_precio": "cierre diario",
             "estado_datos": "NO_DISPONIBLES", "advertencias": [], "consultas": []}
    try:
        cotizacion = consultar("GLOBAL_QUOTE", ticker, clave)
        ficha.update(validar_cotizacion(cotizacion, ticker))
        ficha["consultas"].append({"funcion":"GLOBAL_QUOTE", "estado":"OK"})
    except ErrorDatos as error:
        ficha["consultas"].append({"funcion":"GLOBAL_QUOTE", "estado":error.codigo})
        ficha["advertencias"].append(str(error))
        return ficha
    try:
        overview = consultar("OVERVIEW", ticker, clave)
        if not overview:
            raise ErrorDatos("VACIO")
        if str(overview.get("Symbol", "")).upper() != ticker:
            raise ErrorDatos("TICKER")
        ficha["nombre"] = texto(overview.get("Name"))
        ficha["sector"] = texto(overview.get("Sector"), 80)
        ficha["moneda"] = texto(overview.get("Currency"), 12)
        for campo, externo in (("pe_ratio","PERatio"), ("beta","Beta"),
                                ("max_52s","52WeekHigh"), ("min_52s","52WeekLow")):
            ficha[campo] = numero(overview.get(externo))
        # La capitalización lleva sufijo USD: no etiquetar otra moneda como dólares.
        if ficha["moneda"] == "USD":
            ficha["cap_mercado_usd"] = numero(overview.get("MarketCapitalization"))
        if any(ficha[k] is not None and ficha[k] <= 0 for k in ("max_52s", "min_52s")) or (
            ficha["max_52s"] is not None and ficha["min_52s"] is not None
            and ficha["max_52s"] < ficha["min_52s"]):
            ficha["max_52s"] = ficha["min_52s"] = None
        ficha["consultas"].append({"funcion":"OVERVIEW", "estado":"OK"})
        ficha["fecha_consulta_fundamentales_utc"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        ficha["periodo_fundamentales"] = texto(overview.get("LatestQuarter"), 20)
    except ErrorDatos as error:
        ficha["consultas"].append({"funcion":"OVERVIEW", "estado":error.codigo})
        ficha["advertencias"].append("Fundamentales: " + str(error))
    faltantes = [k for k in ("nombre", "sector", "cambio_pct", "pe_ratio", "beta", "max_52s", "min_52s", "moneda")
                 if ficha[k] is None]
    ficha["estado_datos"] = "PARCIALES" if faltantes else "COMPLETOS"
    if faltantes:
        ficha["advertencias"].append("Datos no disponibles: " + ", ".join(faltantes) + ".")
    return ficha
