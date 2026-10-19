> Actualización posterior: consulta [Corrección de datos](CORRECCION_DATOS.md). La ruta vigente usa la API oficial directa; REAL_PARCIAL identifica datos faltantes y SIN_DATOS rechaza cotizaciones inválidas. El respaldo DEMO descrito abajo quedó limitado a simulación. Este documento registra la etapa anterior donde difiere de esa actualización.

# A. Seguridad de J.A.R.V.I.S.
Preparado para: **Jorge Valencia** · 18 de octubre de 2026.

S1–S5 fueron recomendadas previamente y autorizadas expresamente por Jorge Valencia. Estas medidas están implementadas en el código y el notebook; no se modificaron secretos, accesos ni reglas administrativas de GitHub.

| Medida implementada | Riesgo reducido y cómo | Ventaja | Inconveniente o límite |
|---|---|---|---|
| S1. Chat obligatorio | Un CHAT_ID vacío antes autorizaba cualquier chat. Ahora se deniega y se detiene la atención si falta. | Evita análisis no autorizados por configuración incompleta. | Hay que configurar TELEGRAM_CHAT_ID antes de atender. Otros chats todavía reciben el aviso de bot privado. |
| S2. Comandos y datos validados | Comando exacto /analiza, un ticker, campos esperados, números finitos, rango coherente y textos acotados. Los prompts tratan datos externos como datos, no órdenes. | Reduce entradas ambiguas, datos inválidos e inyección de instrucciones. | Rechaza variantes como /analiza@bot y fichas incompletas; una validación fallida puede producir DEMO. No elimina toda inyección ni certifica la exactitud financiera. |
| S3. Respaldo DEMO efectivo | Si falla Iris, modo=DEMO, advertencia en la primera línea y Euler/Vera locales. | Evita presentar respaldo como real y evita dos llamadas adicionales. | Se obtiene una demostración educativa, no una cotización actual. |
| S4. Inspección de webhook | Consulta getWebhookInfo y se detiene si existe un webhook. No lo elimina. | Evita interrumpir otro despliegue. | El usuario debe decidir cómo resolver el conflicto; otro lector por polling no se detecta con esta comprobación. |
| S5. Versiones fijadas | Dependencias directas/transitivas fijadas; Actions ancladas a SHA verificado. Se conserva contents:read. | Reduce cambios inesperados de la cadena de suministro. | Las actualizaciones requieren mantenimiento y pruebas. Fijar versiones no demuestra ausencia de vulnerabilidades. |

Se mantienen `.env` y evidencias fuera de git, lectura de secretos por entorno y errores de conexión sin credenciales crudas. `store=False` no implica retención cero en todos los sistemas de OpenAI. La clave Alpha Vantage se transmite a OpenAI para configurar MCP; Telegram recibe las notas y avances.

## Medidas pendientes o fuera del alcance aprobado

- **Cola persistente o receptor continuo:** permitiría conservar mensajes de toda la semana. No implementado porque se eligió la opción semanal más sencilla, con retención Telegram de hasta 24 h.
- **Idempotencia duradera y reintentos transaccionales:** no implementados. La concurrencia serializa Actions y el offset confirma actualizaciones; un fallo entre envío y confirmación puede repetir una respuesta. Una orden nueva con el mismo ticker sigue siendo una orden independiente.
- **Límite diario estricto de cuota y herramientas MCP permitidas:** no implementados. El máximo de dos consultas de Iris es una instrucción al modelo, no un contador obligatorio. Revisar cuotas del proveedor.
- **Rotación de claves, reglas de acceso y cambios administrativos:** no realizados; no fueron necesarios para esta migración. Los secretos del nuevo repositorio deben configurarse por su propietario.
- **Auditoría de vulnerabilidades con un servicio externo:** no realizada. Se verificó compatibilidad del entorno y pruebas, no una certificación de seguridad.

No se cambiaron permisos, secretos ni comportamiento del repositorio PRUEBA_ELD.
