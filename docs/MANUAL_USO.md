# Manual de uso y activación de JARVIS
Preparado para **Jorge Valencia** · Actualización del 18 de octubre de 2026.

## Secretos existentes

Se usan OPENIA_API_KEY, ALPHAVANTAGE_API_KEY, TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID. Conserva esos nombres y tus valores; no necesitas otras claves. Deben estar guardados en J.A.R.V.I.S., porque los Repository Secrets de otro repositorio no se heredan. GitHub no permite recuperar sus valores ya guardados. No publiques las claves. Si compartes bot con el original, evita ejecutar dos lectores al mismo tiempo.

## Primera prueba real o comprobación después de actualizar

1. Abre el repositorio J.A.R.V.I.S. → Settings → Secrets and variables → Actions. Guarda los cuatro secretos si aún no existen.
2. En Telegram abre el bot correspondiente al token, pulsa Iniciar y usa el chat autorizado por TELEGRAM_CHAT_ID.
3. En GitHub entra en Actions → mesa-financiera → Run workflow, rama main.
4. Escribe AAPL y deja simulacion desactivada. Ejecuta una vez. Consume hasta dos consultas Alpha Vantage y hasta dos solicitudes OpenAI, además de posibles reintentos del SDK.
5. Espera los avances y la nota de Vera en Telegram.
6. Descarga Artifacts → evidencias y revisa el JSON: REAL indica campos completos; REAL_PARCIAL indica cotización válida con campos faltantes; SIN_DATOS impide interpretar una cotización inválida o antigua. La fecha corresponde al cierre, no necesariamente al día de consulta.
7. Revisa consultas_datos y las advertencias. CUOTA exige esperar al restablecimiento; PLAN exige revisar acceso al endpoint. No repitas muchas veces una consulta bloqueada. Una ejecución verde no confirma fundamentales completos.

La prueba real autorizada de esta actualización ya se realizó: AAPL devolvió cierre 2026-10-16 y estado REAL_PARCIAL porque OVERVIEW indicó límite de consultas. La API de Telegram aceptó los mensajes. Ver [evidencia y diagnóstico](CORRECCION_DATOS.md).

## Enviar instrucciones desde Telegram

1. Envía exactamente /analiza MSFT o /analiza AAPL. No uses la palabra TICKER literalmente: es un marcador de ejemplo.
2. Para atenderlo ahora abre Actions → mesa-financiera → Run workflow y **borra AAPL del campo ticker**. Deja simulacion desactivada y ejecuta.
3. Si hay más de tres actualizaciones, vuelve a activar manualmente con ticker vacío. Saludos y mensajes inválidos también ocupan un lugar del lote.
4. Para usar el horario automático, envía la orden cerca del lunes a las 09:00, Ciudad de México. Telegram solo conserva pendientes hasta 24 horas. Enviar el mensaje no activa Actions por sí mismo.

Evita enviar la misma orden por Telegram y por el campo ticker si solo quieres un análisis. Usa un único consumidor por token. Bot continuo y Colab son alternativas mientras sus procesos estén encendidos.

## Qué hace cada agente

Batuta coordina en Python. Iris consulta GLOBAL_QUOTE y OVERVIEW directamente en la API oficial, lee los campos y verifica fecha y precio; no usa IA para transcribir cotizaciones. Euler conserva los cálculos Python y usa gpt-5.1 para interpretarlos. Vera usa gpt-5.1 para redactar; Python añade fuente, fecha y avisos. Si OpenAI falla, se comunica localmente la información validada. Si la cotización falla, se informa sin inventar precio ni usar DEMO. DEMO queda reservado a simulación.

Alpha Vantage ofrece cierre diario en la consulta configurada. OVERVIEW y el tiempo real están marcados Premium en la documentación actual. Una clave puede devolver precio y bloquear fundamentales; no hay garantía de acceso a todos los campos con un plan gratuito. La tolerancia de fecha es siete días naturales para admitir festivos y fines de semana; no representa un calendario bursátil exacto.

## Seguridad implementada y límites

Chat obligatorio; comando y campos validados; precios finitos, fecha y ticker comprobados; errores de clave, plan y cuota sin texto crudo ni URLs autenticadas; webhook respetado; dependencias y Actions fijadas. No se cambian secretos, accesos ni el original. No se contratan planes de pago.

No se implementaron cola persistente, reintentos transaccionales ni control diario compartido de cuota. Las actualizaciones fallidas se confirman como en el original; corrige la causa y envía una nueva orden. Los artefactos de un repositorio público pueden exponer información de tus consultas: no compartas credenciales ni logs de depuración HTTP.

Si falta respuesta, revisa el estado de Actions, token, chat y otros lectores. Si hay webhook activo, el programa no lo elimina. Si hay SIN_DATOS, lee el motivo en Telegram o en la evidencia. Para comprobar configuración local: python verificar_configuracion.py. La opción --datos consulta Alpha Vantage y consume cuota.

Para simulación local con Python 3.12: pip install -r requirements-dev.txt; pytest -q; python analizar.py AAPL --simulacion. Añadir --telegram sí envía mensajes. Colab y Codespaces requieren sus propios secretos.

[Investigación y cambios detallados](CORRECCION_DATOS.md). Nota educativa, no es recomendación de inversión.
