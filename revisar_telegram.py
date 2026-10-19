"""Revisión única de mensajes pendientes. Lo ejecuta GitHub Actions los lunes a las 09:00, Ciudad de México, o manualmente.

No necesita tu computadora encendida: lee los /analiza que escribiste en Telegram,
corre la cadena de agentes para cada uno, responde y termina.
"""
import sys

from mesa import config
from mesa.comandos import atender
from mesa.telegram_io import confirmar_leidos, obtener_mensajes, preparar_polling, verificar_bot, exigir_chat_configurado


def main():
    print("Configuración:", config.resumen())
    if not config.TELEGRAM_BOT_TOKEN:
        # Copia de la plantilla sin Secrets: terminar en verde, sin correos de error los lunes a las 09:00, Ciudad de México, o manualmente.
        print("ℹ️ Sin TELEGRAM_BOT_TOKEN: nada que revisar. Agrega tus Secrets para activar el bot.")
        return
    try:
        print(f"Bot: @{verificar_bot()}")
    except RuntimeError as error:
        sys.exit(f"❌ {error}")

    exigir_chat_configurado()
    preparar_polling()
    pendientes = obtener_mensajes()
    if not pendientes:
        print("📭 No hay mensajes nuevos. Fin.")
        return

    # Un update_id es una orden; no deduplicar tickers de órdenes distintas.
    pendientes = list({a["update_id"]: a for a in pendientes}.values())
    lote = pendientes[:config.MAX_ANALISIS_POR_RUN]          # el resto queda para la siguiente revisión
    print(f"📬 {len(pendientes)} mensaje(s) pendiente(s); se atenderán {len(lote)} en esta revisión.")
    if len(pendientes) > len(lote):
        print("Quedan pendientes. Activa otra revisión manual antes de 24 h; no esperes al siguiente lunes.")
    for actualizacion in lote:
        mensaje = actualizacion.get("message")
        try:
            if mensaje:
                resultado = atender(mensaje)
                if resultado:
                    print(f"{resultado['ticker']} · estado {resultado['modo']} · evidencia: {resultado['archivo']}")
        except Exception as error:                           # un error no detiene a los demás
            print(f"⚠️ Error con el mensaje {actualizacion['update_id']}: {type(error).__name__}")
        finally:
            confirmar_leidos(actualizacion["update_id"])      # reduce repetición; no garantiza exactamente una vez


if __name__ == "__main__":
    main()
