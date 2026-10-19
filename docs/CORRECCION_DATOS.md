> Documento histórico de una etapa anterior. Para la implementación vigente con funciones gratuitas, consultar [VERSION_GRATUITA.md](VERSION_GRATUITA.md).

# Corrección de datos Alpha Vantage

Preparado para **Jorge Valencia** · 18 de octubre de 2026.

## Investigación del proveedor

Alpha Vantage no tiene un corte general de información en 2024. Su documentación oficial ofrece cotizaciones al cierre de cada sesión y series históricas. Las capturas con fecha 2024 no prueban que el proveedor carezca de información posterior.

| Información solicitada | Endpoint oficial | Disponibilidad y actualización |
|---|---|---|
| Precio, variación, fecha de negociación | GLOBAL_QUOTE | Cierre diario por defecto; no se promete tiempo real. |
| Precio en tiempo real o retrasado 15 minutos | GLOBAL_QUOTE con entitlement o REALTIME_BULK_QUOTES | Exige plan y permisos de mercado adecuados. No es necesario para la revisión semanal. |
| Nombre, sector, P/E, beta, rango de 52 semanas, capitalización y moneda | OVERVIEW | La documentación actual lo marca Premium; se actualiza generalmente al publicar resultados financieros. No hay garantía de acceso con cualquier clave gratuita. |
| Serie diaria | TIME_SERIES_DAILY | Compact devuelve 100 observaciones; no alcanza para deducir de forma fiable un rango de 52 semanas. Full es Premium. No se añade otra consulta para inventar ese rango. |

El plan gratuito tiene una cuota estándar de 25 solicitudes por día. La clave concreta, sus permisos y la cuota restante solo se comprueban con una consulta autenticada; la presencia de un Repository Secret no confirma que el servicio la acepte.

Fuentes oficiales consultadas: [API y campos](https://www.alphavantage.co/documentation/), [planes y cuota](https://www.alphavantage.co/premium/), [soporte](https://www.alphavantage.co/support/).

## Causa confirmada en la implementación anterior

El modelo elegía herramientas MCP y producía un JSON que el programa aceptaba sin contrastar las cifras con la salida de la herramienta, sin exigir precio y fecha y sin comprobar antigüedad. Así podía marcar REAL una ficha vacía o antigua. Una llamada MCP sin error de protocolo no garantiza que su contenido contenga datos utilizables; puede contener avisos de cuota o plan. Los registros anteriores no conservaron respuestas crudas, por lo que no permiten atribuir con certeza el precio de 2024 a una restricción, un ejemplo del proveedor o una extracción del modelo.

## Corrección aplicada

- Iris conserva su función de recolectora y consulta directamente el HTTPS oficial con GLOBAL_QUOTE y OVERVIEW, como máximo dos solicitudes por análisis y sin reintentos automáticos. La ruta normal ya no deja al modelo elegir herramientas ni transcribir cifras. No se cambió de proveedor ni se agregaron secretos.
- Se leen campos concretos de JSON y se exige ticker coincidente, precio positivo y finito, fecha ISO válida y no futura. Una cotización de más de siete días se rechaza; esta tolerancia explícita admite fines de semana y festivos, pero no equivale a un calendario bursátil exacto.
- Los avisos Information, Note y Error Message se clasifican sin publicar su texto crudo: cuota, plan, clave, demo o respuesta inválida. Las URLs autenticadas no se guardan.
- COMPLETOS significa que llegaron los campos esperados; no certifica exactitud financiera ni contemporaneidad de los fundamentales con el cierre. PARCIALES conserva una cotización reciente con advertencias y campos faltantes identificados. NO_DISPONIBLES impide emitir un análisis de precio actual.
- La evidencia usa modo REAL, REAL_PARCIAL o SIN_DATOS, además de SIMULACIÓN al solicitar una demostración. Una falla real no activa precios ficticios. Las notas DEMO solo corresponden a simulación.
- Si falta la cotización válida no se llama a OpenAI. Si OpenAI falla después de obtener datos válidos, Euler y Vera producen una interpretación local con esas mismas cifras. Los cálculos Python se conservan.
- Se reemplaza None por “no disponible” y no se supone USD si la fuente no confirma moneda. La fecha mostrada corresponde al cierre; los fundamentales llevan fecha de consulta y periodo reportado cuando existe, no una fecha de actualización inventada.
- GPT-5.1 sigue disponible para Euler y Vera; Iris hace la recolección determinista sin gastar una llamada de IA. El adaptador MCP anterior se conserva como compatibilidad técnica, pero no participa en el flujo normal.
- No cambian cron semanal, activación manual, chat autorizado ni los cuatro nombres de secretos. La verificación real de corrección se ejecuta una sola vez con AAPL y envío al chat configurado; su trabajo temporal se retira al terminar.

## Validación y alcance

64 pruebas locales aprobadas. Cubren datos completos y parciales, cierre de viernes consultado el domingo, regresión de fecha 2024, fechas futuras, JSON de error con HTTP 200, precios inválidos, cuota, Premium, clave demo y fallos de OpenAI sin inventar cifras. El notebook mantiene las mismas funciones y controles.

El resultado de la prueba autenticada se incorpora en el registro de validación. No se promete eliminar futuras caídas del proveedor, restricciones de plan o falta de saldo. Obtener los fundamentales completos requiere que la clave tenga el permiso correspondiente; ninguna modificación del código puede otorgarlo.

## Uso después de actualizar

Ejecuta Actions → mesa-financiera → Run workflow, ticker AAPL, simulacion desactivada. Para atender solo una orden ya enviada por Telegram, deja ticker vacío. Revisa modo y consultas_datos en el artefacto. Si aparece SIN_DATOS, el comando manual termina con código 2 y explica el motivo; no repitas inmediatamente si se agotó la cuota. Si aparece REAL_PARCIAL, el precio pasó la validación pero no se obtuvieron todos los indicadores. Consulta el aviso de Iris para saber cuáles faltan y por qué.

## Resultado de la prueba real autorizada

El 18 de octubre de 2026, hora de Ciudad de México, se ejecutó una única prueba de AAPL con los secretos existentes, sin cambiarlos. [Ejecución verificable](https://github.com/JorgeValba/J.A.R.V.I.S./actions/runs/39183844888/job/117842109206).

GLOBAL_QUOTE devolvió cierre **2026-10-16**, precio **343.46**, variación **0.4269 %**. Estos son valores observados en esa respuesta del proveedor, no una verificación independiente ni un precio en tiempo real. OVERVIEW devolvió un aviso clasificado CUOTA, por lo que no se obtuvieron fundamentales ni moneda. No se debe inferir de ese aviso si la clave tiene o no acceso Premium después de restablecerse la cuota.

El bot completó Euler y Vera y el envío al chat configurado, con estado **REAL_PARCIAL**, fuente oficial, cierre reciente y advertencia explícita de cuota y campos faltantes. No se afirmó USD al faltar la moneda. Se guardó un artefacto con el diagnóstico. El trabajo temporal de prueba real se retiró del workflow al terminar; se mantiene solamente el cron financiero semanal y la activación manual habitual. No se repitió el análisis ni se consumieron más consultas reales.

Para conseguir también beta, P/E y rango anual será necesario que la cuota permita la siguiente consulta y que OVERVIEW esté habilitado para esa clave. El sistema ya identifica esa condición sin sustituirla por datos inventados. Si la restricción persiste tras restablecerse la cuota, el propietario deberá verificar el plan con Alpha Vantage; no se contrató ni modificó ningún servicio de pago.
