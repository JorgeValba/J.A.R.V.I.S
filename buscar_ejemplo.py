"""Búsqueda acotada autorizada por Jorge Valencia. No llama a OpenAI ni Telegram."""
import json
import os
from pathlib import Path
from mesa.datos import obtener_ficha, CAMPOS

CANDIDATOS = ("IBM", "MSFT", "GOOGL", "AMZN", "NVDA", "JPM")


def buscar(clave, consultar=obtener_ficha):
    resultado = {"preparado_para":"Jorge Valencia", "maximo_ejemplos":6,
                 "ejemplos":[], "encontrado":None, "motivo_fin":"Límite de seis ejemplos"}
    for ticker in CANDIDATOS[:6]:
        ficha = consultar(ticker, clave)
        faltantes = [c for c in (*CAMPOS, "moneda") if ficha.get(c) is None]
        completo = ficha.get("estado_datos") == "COMPLETOS" and not faltantes
        resultado["ejemplos"].append({"ticker":ticker, "completo":completo,
                                     "faltantes":faltantes, "ficha":ficha})
        if completo:
            resultado["encontrado"] = ticker
            resultado["motivo_fin"] = "Se encontró el primer ejemplo completo y reciente"
            break
        bloqueos = [c["estado"] for c in ficha.get("consultas", [])
                    if c["estado"] in ("CUOTA", "PLAN", "CLAVE", "DEMO")]
        if bloqueos:
            resultado["motivo_fin"] = "Bloqueo del proveedor: " + ", ".join(bloqueos)
            break
    return resultado


def main():
    from mesa import config
    if not config.ALPHAVANTAGE_API_KEY:
        raise SystemExit("Falta ALPHAVANTAGE_API_KEY; no se realizaron consultas.")
    resultado = buscar(config.ALPHAVANTAGE_API_KEY)
    Path(config.CARPETA_SALIDAS).mkdir(exist_ok=True)
    ruta = Path(config.CARPETA_SALIDAS)/"busqueda_ejemplos_Jorge_Valencia.json"
    ruta.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    for ejemplo in resultado["ejemplos"]:
        f = ejemplo["ficha"]
        print(json.dumps({"ticker":ejemplo["ticker"], "completo":ejemplo["completo"],
            "fecha":f.get("fecha_dato"), "consultas":f.get("consultas"),
            "faltantes":ejemplo["faltantes"]}, ensure_ascii=False))
    print("Ejemplos consultados:", len(resultado["ejemplos"]), "/ 6")
    print("Ejemplo completo encontrado:", resultado["encontrado"] or "ninguno")
    print("Fin:", resultado["motivo_fin"])


if __name__ == "__main__":
    main()
