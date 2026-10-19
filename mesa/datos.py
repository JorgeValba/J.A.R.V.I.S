"""Datos verificables de Alpha Vantage para Jorge Valencia, sin extracción por IA.

Solo TIME_SERIES_DAILY con outputsize=compact, disponible en el plan gratuito.
No registrar respuestas/URLs crudas: podrían incluir credenciales.
"""
import math
from datetime import datetime, date, timezone
import requests

URL_API = "https://www.alphavantage.co/query"
MAX_ANTIGUEDAD_DIAS = 7  # tolerancia explícita para fines de semana y festivos
CAMPOS = ("precio", "cambio_pct", "fecha_dato", "sesiones")
ERRORES = {
    "CUOTA": "Alpha Vantage indicó límite de consultas; espera a que se restablezca tu cuota.",
    "PLAN": "Alpha Vantage exige un plan o permiso adicional para esta consulta.",
    "CLAVE": "Alpha Vantage rechazó la clave; revisa ALPHAVANTAGE_API_KEY.",
    "DEMO": "La clave demo del proveedor no sirve para validar datos actuales de tu ticker.",
    "RED": "No se pudo conectar con Alpha Vantage.",
    "RESTRICCION": "Alpha Vantage devolvió un aviso mixto de cuota o plan; revisa los permisos de la clave. No se confirmó cuota agotada.",
    "SERIE": "La serie diaria contiene datos inválidos o inconsistentes.",
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
    cuota = any(p in m for p in ("rate limit", "call frequency", "requests per day", "api limit", "quota", "25 requests", "higher api call"))
    plan = any(p in m for p in ("premium", "subscription", "entitlement", "subscribe"))
    if cuota and plan:
        return "RESTRICCION"
    if cuota:
        return "CUOTA"
    if plan:
        return "PLAN"
    if "demo" in m:
        return "DEMO"
    if any(p in m for p in ("api key", "apikey", "invalid key")):
        return "CLAVE"
    return "RESPUESTA"


def consultar(funcion, ticker, clave):
    if funcion != "TIME_SERIES_DAILY":
        raise ValueError("Esta versión solo permite TIME_SERIES_DAILY compacto")
    if not clave or clave.strip().lower() == "demo":
        raise ErrorDatos("DEMO" if clave else "CLAVE")
    try:
        r = requests.get(URL_API, params={"function": funcion, "symbol": ticker,
                                         "apikey": clave, "outputsize": "compact"}, timeout=30)
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


def validar_serie(datos, ticker, hoy=None):
    meta = datos.get("Meta Data")
    serie = datos.get("Time Series (Daily)")
    if not isinstance(meta, dict) or not isinstance(serie, dict) or not serie:
        raise ErrorDatos("VACIO")
    if str(meta.get("2. Symbol", "")).upper() != ticker:
        raise ErrorDatos("TICKER")
    hoy = hoy or datetime.now(timezone.utc).date()
    sesiones = []
    for fecha_texto, fila in serie.items():
        try:
            fecha = date.fromisoformat(fecha_texto)
        except (TypeError, ValueError):
            raise ErrorDatos("FECHA") from None
        if fecha > hoy:
            raise ErrorDatos("FECHA")
        if not isinstance(fila, dict):
            raise ErrorDatos("SERIE")
        cierre = numero(fila.get("4. close"))
        if cierre is None or cierre <= 0:
            raise ErrorDatos("PRECIO")
        volumen = numero(fila.get("5. volume"))
        if volumen is not None and (volumen < 0 or not volumen.is_integer()):
            raise ErrorDatos("SERIE")
        sesiones.append({"fecha":fecha.isoformat(), "cierre":cierre,
                         "volumen":int(volumen) if volumen is not None else None})
    sesiones.sort(key=lambda v: v["fecha"])
    sesiones = sesiones[-100:]
    edad = (hoy-date.fromisoformat(sesiones[-1]["fecha"])).days
    if edad > MAX_ANTIGUEDAD_DIAS:
        raise ErrorDatos("ANTIGUO")
    precio = sesiones[-1]["cierre"]
    cambio = (precio/sesiones[-2]["cierre"]-1)*100 if len(sesiones)>1 else None
    return {"precio":precio, "cambio_pct":round(cambio,4) if cambio is not None else None,
            "fecha_dato":sesiones[-1]["fecha"], "antiguedad_dias":edad,
            "sesiones":sesiones, "volumen":sesiones[-1]["volumen"]}


def obtener_ficha(ticker, clave):
    """Una consulta gratuita como máximo. Sin Premium, reintentos ni precios ficticios."""
    ficha = {"ticker":ticker, **dict.fromkeys(CAMPOS), "volumen":None,
             "fuente":"Alpha Vantage API gratuita", "tipo_precio":"cierre diario sin ajustar",
             "estado_datos":"NO_DISPONIBLES", "advertencias":[], "consultas":[]}
    try:
        datos = consultar("TIME_SERIES_DAILY", ticker, clave)
        ficha.update(validar_serie(datos,ticker))
        ficha["consultas"].append({"funcion":"TIME_SERIES_DAILY", "outputsize":"compact", "estado":"OK"})
    except ErrorDatos as error:
        ficha["consultas"].append({"funcion":"TIME_SERIES_DAILY", "estado":error.codigo})
        ficha["advertencias"].append(str(error))
        return ficha
    ficha["estado_datos"] = "COMPLETOS" if len(ficha["sesiones"])>=50 else "PARCIALES"
    if len(ficha["sesiones"])<50:
        ficha["advertencias"].append("Menos de 50 sesiones: conclusión técnica insuficiente.")
    if ficha["volumen"] is None:
        ficha["advertencias"].append("Volumen no disponible; no se usa para decidir.")
    return ficha
