# Versión basada en Alpha Vantage gratuito
Preparado para **Jorge Valencia** · 18 de octubre de 2026.

## Por qué cambió el análisis

La clave de Alpha Vantage del proyecto es gratuita. La documentación vigente marca OVERVIEW como Premium y el tiempo real exige permisos adicionales. No corresponde seguir pidiendo esos datos ni indicar indefinidamente que faltan P/E o beta. Se retiraron del contrato actual sector, P/E, beta, capitalización, nombre de empresa y rango oficial de 52 semanas. El ticker identifica el instrumento; no se agrega SYMBOL_SEARCH para ahorrar cuota.

Se usa solamente **TIME_SERIES_DAILY con outputsize=compact**, que el proveedor documenta como disponible para claves gratuitas y devuelve hasta 100 observaciones. La implementación bloquea cualquier otra función. No se usa full, DAILY_ADJUSTED, intradía, OVERVIEW ni MCP. `.mcp.json` queda sin servidores para evitar la integración antigua. Los archivos históricos anteriores se conservan como antecedentes.

Esta modificación fue solicitada y autorizada por Jorge Valencia. Se conserva Python para todos los cálculos, GPT-5.1 para explicaciones de Euler y Vera, la cadena Iris → Euler → Vera, Telegram, notebook y los cuatro secretos con sus nombres exactos. No se modificó PRUEBA_ELD.

Fuentes: [serie diaria compact gratuita y precios sin ajustar](https://www.alphavantage.co/documentation/#daily), [OVERVIEW Premium](https://www.alphavantage.co/documentation/#company-overview), [cuota gratuita](https://www.alphavantage.co/support/).

## Qué recibe y calcula el sistema

Iris obtiene ticker, fecha, cierre y volumen cuando existe, y conserva las últimas 100 sesiones disponibles. Calcula el cambio entre los dos últimos cierres. Exige ticker coincidente, precio positivo y finito y fechas válidas, no futuras ni mayores a siete días de antigüedad. La tolerancia no sustituye un calendario exacto de bolsa. No supone USD: la serie no confirma moneda.

Euler calcula en Python:

| Indicador | Definición |
|---|---|
| SMA20 y SMA50 | Promedio de los últimos 20 o 50 cierres. |
| Variación del precio en 20 sesiones | (Último cierre / cierre de 20 intervalos atrás − 1) × 100; necesita 21 cierres. No incluye dividendos. |
| Volatilidad diaria de 20 sesiones | Desviación estándar muestral de los últimos 20 cambios porcentuales diarios. No es anualizada ni beta. |
| Distancia al máximo de cierre de 20 sesiones | (Último cierre / mayor cierre de las últimas 20 observaciones − 1) × 100. No equivale al máximo drawdown histórico. |

Las cantidades 20 y 50 son sesiones bursátiles, no días naturales. Se requieren al menos 50 sesiones válidas para una conclusión distinta de información insuficiente. El volumen se conserva como evidencia y no interviene en la regla.

## Conclusión técnica con reglas transparentes

Se evalúan en este orden y sin redondear los valores usados en comparaciones:

1. **INFORMACION_INSUFICIENTE:** faltan 50 sesiones, hay precios inválidos o alertas de calidad. Un salto diario absoluto mayor a 35 % en los últimos 49 cambios o fechas repetidas/desordenadas/huecos mayores a 10 días bloquean la conclusión. Son comprobaciones heurísticas, no detectores completos de eventos corporativos.
2. **CAUTELA:** volatilidad diaria de 20 sesiones ≥3 % o distancia al máximo de cierre de 20 sesiones ≤−10 %.
3. **EVALUAR_ENTRADA:** cierre > SMA20 > SMA50 y variación de precio en 20 sesiones positiva. Significa revisar una posible entrada, no comprar automáticamente.
4. **ESPERAR:** cierre < SMA20 < SMA50 y variación en 20 sesiones negativa.
5. **OBSERVAR:** señales mixtas o neutrales restantes.

Son reglas educativas de la implementación, no umbrales normativos ni una estrategia con rentabilidad probada. No se realizó backtesting ni se estimaron probabilidades de éxito. El programa no conoce patrimonio, horizonte, cartera o tolerancia personal al riesgo. No evalúa valor intrínseco ni decide cuánto invertir. La decisión y el motivo se añaden a la nota desde Python; los agentes de IA los explican sin sustituirlos.

## Costos y estados

Una consulta Alpha Vantage por análisis, sin reintentos de ese proveedor. El plan gratuito conserva su cuota estándar de 25 solicitudes diarias, compartida por las aplicaciones que usen esa clave. OpenAI sigue siendo de pago: hasta dos solicitudes ordinarias por análisis, más el reintento configurado del SDK si falla. Sin datos suficientes no se llama a IA. La simulación no consume esas API.

REAL significa datos completos para el contrato gratuito, no información fundamental completa ni inversión segura. REAL_PARCIAL indica menos historial del necesario. SIN_DATOS informa una falla sin fabricar precios. Los avisos mixtos de cuota/plan se clasifican RESTRICCION para no presentar una causa única sin evidencia. No se cambiaron secretos ni se contrataron servicios.

## Validación realizada

62 pruebas locales aprobadas y prueba real integrada completada una vez con AAPL. La API devolvió 100 sesiones, cierre 2026-10-16, y el sistema registró estado REAL y conclusión EVALUAR_ENTRADA. La API de Telegram aceptó avances y nota. No se afirma confirmación visual en el dispositivo ni exactitud contra una segunda fuente.

[Ejecución real verificable](https://github.com/JorgeValba/J.A.R.V.I.S./actions/runs/39186532237/job/117850102455). El artefacto conserva serie, indicadores y nota. La explicación de IA de esa ejecución confundió distancia al máximo con caída máxima; se precisó después el prompt para distinguirlas. La regla Python usa distancia, y no cambió por ese ajuste. No se repitió una consulta real para ese cambio editorial.

El trabajo temporal de validación real se retira al terminar. Permanece el único cron financiero: lunes 09:00 America/Mexico_City y ejecución manual. Telegram conserva pendientes hasta 24 horas y se atienden hasta tres actualizaciones por revisión.

## Archivos de esta adaptación

mesa/datos.py, mesa/agentes.py, mesa/pipeline.py, buscar_ejemplo.py, verificar_configuracion.py, notebook, `.mcp.json`, comando de desarrollo, pruebas y documentación. Se reemplazan pruebas de indicadores Premium por pruebas de la serie y las reglas gratuitas. No se cambia la dependencia ni el nombre OPENIA_API_KEY.
