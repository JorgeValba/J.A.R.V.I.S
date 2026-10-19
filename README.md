# J.A.R.V.I.S. con Alpha Vantage gratuito
Preparado para **Jorge Valencia**, a partir de la actividad educativa de la Dra. Elda C. Morales. PRUEBA_ELD permanece sin cambios.

Telegram → Batuta → Iris (serie gratuita) → Euler (cálculos y conclusión técnica) → Vera (nota breve).

Iris hace una consulta TIME_SERIES_DAILY compact por análisis y obtiene hasta 100 sesiones. Se retiraron OVERVIEW, MCP, P/E, beta, sector, capitalización y rango oficial de 52 semanas porque el proyecto usa la clave gratuita. Python calcula medias20/50, variación de precio20, volatilidad diaria20 y distancia al máximo de cierre20; aplica reglas educativas EVALUAR_ENTRADA, ESPERAR, OBSERVAR, CAUTELA o INFORMACION_INSUFICIENTE. No hay órdenes bursátiles ni rentabilidad probada.

GPT-5.1 interpreta y comunica mediante OPENIA_API_KEY. Solo Alpha Vantage usa un plan gratuito: OpenAI conserva su costo de API. Se mantienen ALPHAVANTAGE_API_KEY, TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID. No se necesitan otros secretos. La cuota gratuita no desaparece por esta adaptación.

[Motivo, fórmulas, reglas y validación](docs/VERSION_GRATUITA.md) · [Manual de uso](docs/MANUAL_USO.md) · [Seguridad](docs/SEGURIDAD.md) · [Validación](docs/VALIDACION_ETAPA2.md) · [Análisis del original](docs/ANALISIS_ORIGINAL.md).

Ejecuta Actions → mesa-financiera → Run workflow: AAPL, simulacion desactivada, para una prueba real. Para atender solo mensajes enviados al bot, vacía el ticker. Único cron financiero: lunes 09:00 America/Mexico_City. Telegram conserva pendientes hasta 24 horas; cada revisión procesa hasta tres actualizaciones. No uses dos lectores con el mismo token.

Para probar sin red con Python 3.12: pip install -r requirements-dev.txt; pytest -q; python analizar.py AAPL --simulacion. El notebook es autónomo y replica las reglas.

Estados: REAL para el contrato gratuito completo, REAL_PARCIAL si falta historial y SIN_DATOS si la consulta no sirve. Nunca se inventa un precio ante una falla real. Las guías Word originales de la docente y los documentos de etapas anteriores se mantienen como historia; para esta versión prevalece VERSION_GRATUITA.md.

62 pruebas locales y prueba real con AAPL completadas: 100 sesiones, cierre 2026-10-16, estado REAL y nota aceptada por Telegram. Las reglas no fueron sometidas a backtesting para afirmar rentabilidad. Los precios son de cierre sin ajustar splits/dividendos; las medias y variaciones no representan valoración fundamental.

Nota educativa, no es recomendación de inversión.
