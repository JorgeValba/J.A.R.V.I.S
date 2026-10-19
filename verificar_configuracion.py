"""Revisa que todo esté listo, sin mostrar el valor de ninguna llave.

  python verificar_configuracion.py           → revisa llaves y el token de Telegram
  python verificar_configuracion.py --datos   → prueba TIME_SERIES_DAILY compact (una consulta gratuita)
"""
import sys

from mesa import config


def main():
    print("🔎 Estado de la configuración")
    for nombre, estado in config.resumen().items():
        print(f"  {nombre:<22} {estado}")

    errores = 0
    if config.TELEGRAM_BOT_TOKEN:
        try:
            from mesa.telegram_io import verificar_bot
            print(f"  Telegram                ✅ bot @{verificar_bot()} responde")
        except Exception as error:
            errores += 1
            print(f"  Telegram                ❌ {type(error).__name__}; revisa configuración y conexión")

    if "--mcp" in sys.argv or "--datos" in sys.argv:
        if config.MODO_SIMULACION:
            print("  API Alpha Vantage       ⬜ omitido: faltan OPENIA_API_KEY o ALPHAVANTAGE_API_KEY")
        else:
            from mesa.agentes import agente_recolector
            ficha, herramientas = agente_recolector("IBM")
            if ficha.get("estado_datos") in ("COMPLETOS", "PARCIALES"):
                print(f"  API Alpha Vantage       ✅ respondió (herramientas: {', '.join(x['funcion'] + ':' + x['estado'] for x in ficha.get('consultas', []))})")
            else:
                errores += 1
                print(f"  API Alpha Vantage       ❌ {' '.join(ficha.get('advertencias', []))}")

    if config.MODO_SIMULACION:
        print("\nℹ️  Estás en MODO SIMULACIÓN: todo funciona, pero con datos ficticios.")
    sys.exit(1 if errores else 0)


if __name__ == "__main__":
    main()
