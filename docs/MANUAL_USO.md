# Manual de JARVIS con Alpha Vantage gratuito
Preparado para **Jorge Valencia** · 18 de octubre de 2026.

## Motivo del cambio

El proyecto usa la clave gratuita. OVERVIEW está marcado Premium; se retiraron P/E, beta, capitalización, sector y rango oficial de 52 semanas. La versión vigente usa solo TIME_SERIES_DAILY compact, hasta 100 sesiones y una consulta por análisis. OpenAI conserva su costo de API. [Motivo, reglas y fórmulas](VERSION_GRATUITA.md).

## Activar una prueba real

1. Guarda en J.A.R.V.I.S. → Settings → Secrets and variables → Actions los mismos cuatro nombres: OPENIA_API_KEY, ALPHAVANTAGE_API_KEY, TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID. No se heredan secretos de otro repositorio. No publiques valores.
2. Abre el bot en Telegram y pulsa Iniciar, en el chat autorizado. Usa un solo consumidor por token.
3. En GitHub abre Actions → mesa-financiera → Run workflow, main, ticker AAPL, simulacion desactivada. Ejecuta una vez.
4. Recibe las entregas y la conclusión técnica. Descarga Artifacts → evidencias y revisa fecha, sesiones, consultas_datos y decision_tecnica.
5. REAL significa datos completos para el contrato gratuito. REAL_PARCIAL indica menos historial y la regla dará INFORMACION_INSUFICIENTE si faltan 50 sesiones. SIN_DATOS significa que no hubo datos válidos; no se inventan precios.

## Enviar órdenes desde Telegram

1. Envía exactamente /analiza AAPL, /analiza MSFT o /analiza IBM. TICKER es un marcador, no una orden para analizar una empresa llamada TICKER.
2. Para atender ahora abre Run workflow y vacía el campo ticker. Desactiva simulacion para datos reales.
3. Cada revisión atiende tres actualizaciones como máximo, incluidos saludos. Repite manualmente si quedan pendientes.
4. El cron corre los lunes 09:00 America/Mexico_City. Telegram conserva pendientes hasta 24 horas; enviar una orden no activa Actions por sí solo. Usa activación manual o envía cerca de la revisión semanal.

## Qué significa la conclusión

Python compara cierre, medias20/50, variación de precio20, volatilidad diaria20 y distancia al máximo de cierre20. Produce EVALUAR_ENTRADA, ESPERAR, OBSERVAR, CAUTELA o INFORMACION_INSUFICIENTE según reglas explícitas. No es una predicción de rentabilidad ni una orden automática. La serie no está ajustada por splits/dividendos. Se necesitan 50 sesiones válidas; un salto absoluto diario mayor a 35 % o huecos relevantes bloquean la conclusión. [Reglas completas y límites](VERSION_GRATUITA.md).

La distancia al máximo reciente no es el máximo drawdown histórico. No se conoce tu patrimonio, cartera, horizonte ni tolerancia personal al riesgo. No se realizó backtesting para afirmar que estas reglas sean rentables.

## Costos y problemas

Una consulta Alpha Vantage por análisis, sin reintentos; el proveedor mantiene su cuota gratuita. GPT-5.1 utiliza hasta dos solicitudes ordinarias, más un reintento por llamada configurado en el SDK si falla. La clave Alpha Vantage no se envía a OpenAI. Los avisos mixtos de cuota/plan se muestran sin diagnosticar como cierta una sola causa.

Si no responde, revisa token, chat, Actions y otros lectores. Si hay webhook, el programa se detiene sin eliminarlo. Si aparece un aviso de cuota, evita repetir hasta restablecerla. Los mensajes fallidos se confirman como en el original: corrige la causa y envía una nueva orden. No hay cola persistente ni reintentos transaccionales.

Para probar sin red con Python 3.12: pip install -r requirements-dev.txt; pytest -q; python analizar.py AAPL --simulacion. Añadir --telegram sí envía mensajes. Colab y Codespaces requieren sus propios secretos.

## Validación de la versión gratuita

62 pruebas locales y prueba real de AAPL completadas: 100 sesiones, cierre 2026-10-16, estado REAL y conclusión EVALUAR_ENTRADA. Telegram aceptó los mensajes. [Registro real](https://github.com/JorgeValba/J.A.R.V.I.S./actions/runs/39186532237/job/117850102455). Las precisiones posteriores de redacción y métricas visibles se verificaron con pruebas locales, sin repetir consultas reales.

Nota educativa, no es recomendación de inversión.
