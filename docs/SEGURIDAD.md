# Seguridad vigente de JARVIS
Preparado para **Jorge Valencia** · Versión gratuita autorizada el 18 de octubre de 2026.

| Implementado | Riesgo reducido | Límite o inconveniente |
|---|---|---|
| Chat obligatorio y comando exacto | Acceso por omisión o instrucciones ambiguas | Hay que guardar TELEGRAM_CHAT_ID; no admite sufijo @bot. |
| Solo TIME_SERIES_DAILY compact | Consultas Premium y selección impredecible de herramientas | Una consulta por análisis no elimina la cuota gratuita. |
| Validación de fechas, ticker y números | Precios viejos, inválidos o de otra acción | Tolerancia de siete días; no es calendario bursátil exacto. |
| Calidad de serie y reglas en Python | Conclusiones sin historial o con saltos sospechosos | Filtros didácticos; no detectan todos los eventos corporativos ni prueban rentabilidad. |
| Webhook respetado y un consumidor recomendado | Interrumpir otro despliegue | Requiere resolver conflictos manualmente. |
| Claves por entorno, errores sin URLs ni texto crudo | Exposición de credenciales | Los artefactos pueden contener consultas; no activar logs HTTP. |
| Versiones y Actions fijadas, contents:read | Cambios inesperados de dependencias | Requiere mantenimiento; no certifica ausencia de vulnerabilidades. |

La clave Alpha Vantage solo se transmite a su API oficial. OpenAI recibe indicadores seleccionados y Telegram recibe avances y nota. store=False no garantiza retención cero del proveedor. No se cambiaron secretos ni accesos administrativos. El original PRUEBA_ELD permanece intacto.

Pendientes: cola persistente (se eligió revisión semanal sencilla), idempotencia y reintentos transaccionales (no incluidos), contador diario compartido de cuota (no implementado), auditoría externa de vulnerabilidades (no realizada), backtesting de la regla financiera (no realizado; no se afirma rentabilidad). No se contrataron planes de pago ni se rotaron claves.

Se reemplazó el respaldo DEMO ante fallas reales por un aviso SIN_DATOS; DEMO solo corresponde a simulación. La retirada de Premium y los cambios de alcance fueron solicitados por Jorge Valencia. [Detalles y reglas](VERSION_GRATUITA.md).
