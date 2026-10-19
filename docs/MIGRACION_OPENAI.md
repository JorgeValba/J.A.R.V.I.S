> Actualización posterior: consulta [Corrección de datos](CORRECCION_DATOS.md). La ruta vigente usa la API oficial directa; REAL_PARCIAL identifica datos faltantes y SIN_DATOS rechaza cotizaciones inválidas. El respaldo DEMO descrito abajo quedó limitado a simulación. Este documento registra la etapa anterior donde difiere de esa actualización.

# Migración a OpenAI
Elaborado por: **Jorge Valencia** · Actualizado el 18 de octubre de 2026.

Base original: PRUEBA_ELD, commit `0d594a0424805a26f07b36a13cd91e470e6cc246`, actividad de la Dra. Elda C. Morales. Original conservado sin cambios.

| Original | J.A.R.V.I.S. |
|---|---|
| SDK Anthropic | SDK OpenAI 2.54.0 |
| ANTHROPIC_API_KEY | OPENIA_API_KEY explícita al cliente |
| messages.create / beta.messages.create | responses.create |
| system / messages | instructions / input |
| max_tokens | max_output_tokens: 600 Iris, 320 Euler, 280 Vera |
| bloques content de texto | output_text |
| mcp_tool_use | output de tipo mcp_call |
| mcp_servers y beta | tools de tipo mcp con server_url, server_label, require_approval |
| Claude | gpt-5.1, reasoning none, store false |

Solo Iris recibe herramientas MCP. Su URL Alpha Vantage incluye la clave codificada, que necesariamente se transmite a OpenAI y al proveedor de datos. La aprobación de herramientas se configura como never para permitir ejecución autónoma en el servidor definido. El adaptador exige estado completed, texto y llamadas MCP sin errores. No registra respuestas crudas.

Telegram, tres agentes, orquestación, cálculos, evidencia, terminal, Codespaces y notebook autónomo se conservan. Los cambios autorizados posteriores (personalidades, validación, respaldo, cron y dependencias) están detallados en [Cambios](CAMBIOS_ETAPA2.md), [Seguridad](SEGURIDAD.md) y [Manual](MANUAL_USO.md).

La carpeta .claude y .mcp.json conservan compatibilidad opcional con un asistente de desarrollo; no son una dependencia Anthropic para ejecutar el sistema. Las guías Word son material original histórico. El [análisis original](ANALISIS_ORIGINAL.md) describe el estado anterior, no la configuración vigente.

Validación actual: [48 pruebas locales](VALIDACION_ETAPA2.md); prueba real pendiente de secretos. `store=False` no es garantía de retención cero del proveedor. El límite de dos consultas MCP está en el prompt, no en un contador estricto.

Referencias: [Responses API](https://developers.openai.com/api/reference/python/resources/responses/methods/create), [MCP](https://developers.openai.com/api/docs/guides/tools-connectors-mcp), [GPT-5.1](https://developers.openai.com/api/docs/models/gpt-5.1), [retiro anunciado](https://developers.openai.com/api/docs/deprecations).
