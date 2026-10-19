# Validación vigente de la versión gratuita
Preparado para **Jorge Valencia** · 18 de octubre de 2026.

62 pruebas locales aprobadas y 62 pruebas aprobadas en GitHub antes de la ejecución real. Se cubrieron medias y variaciones, señales alcistas/bajistas/neutrales, volatilidad, caída reciente, datos insuficientes, saltos y huecos, fechas antiguas/futuras, valores inválidos, cuota/plan/mensajes mixtos, falta de IA, secretos explícitos, Telegram y notebook autónomo.

Prueba real autorizada una vez: AAPL, TIME_SERIES_DAILY compact, 100 sesiones, cierre 2026-10-16, estado REAL y conclusión EVALUAR_ENTRADA. La API de Telegram aceptó avances y nota. [Logs](https://github.com/JorgeValba/J.A.R.V.I.S./actions/runs/39186532237/job/117850102455). Se retiró el trabajo temporal real; no quedó otro cron.

Tras esa prueba se precisó el prompt sobre sesiones y distancia al máximo (no es drawdown máximo) y se añadieron cierre y medias visibles desde Python. 62 pruebas locales volvieron a pasar. No se repitió la consulta real para esos ajustes.

No se validó la rentabilidad de las reglas ni se hizo backtesting. No se contrastaron las cifras contra otra fuente ni se confirmó visualmente recepción en el dispositivo. El alcance completo, incidencias y reglas están en VERSION_GRATUITA.md.
