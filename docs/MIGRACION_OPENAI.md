# Migración y validación de J.A.R.V.I.S.

Elaborado por: **Jorge Valencia**  
Fecha: 18 de octubre de 2026.

## Resultado preparado

Repositorio independiente basado en el commit original `0d594a0424805a26f07b36a13cd91e470e6cc246`. Se conserva la actividad de la Dra. Elda C. Morales y se identifica esta adaptación. El original no recibe commits, cambios de secretos ni de configuración.

## Correspondencia de integración

| Anthropic en el original | OpenAI en esta versión |
|---|---|
| dependencia `anthropic` | dependencia `openai` |
| `ANTHROPIC_API_KEY` | **`OPENIA_API_KEY`** |
| `anthropic.Anthropic(api_key=...)` | `OpenAI(api_key=config.OPENIA_API_KEY)` |
| `messages.create` / `beta.messages.create` | `responses.create` |
| `system` | `instructions` |
| `messages` | `input` con rol user |
| `max_tokens` | `max_output_tokens` (900 Iris/Euler, 600 Vera) |
| bloques `content[type=text]` | propiedad SDK `output_text` |
| bloques `mcp_tool_use` | elementos `output[type=mcp_call]`, nombres `name` |
| `mcp_servers`, `mcp_toolset` y beta | herramienta `mcp` con `server_label`, `server_url`, `require_approval` |
| `claude-haiku-5-5` | `gpt-6-luna`, configurable por `MODELO` |

`reasoning.effort=none` conserva el presupuesto breve de salida sin consumirlo en razonamiento interno. El modelo seleccionado admite este ajuste según su documentación; cambiar a otro modelo requiere revisar compatibilidad. `store=False` evita solicitar almacenamiento de Responses para recuperar la conversación; no equivale a afirmar retención cero en todos los sistemas del proveedor.

Iris mantiene la URL oficial de Alpha Vantage MCP y codifica la llave para incluirla correctamente como parámetro. `require_approval=never` permite el funcionamiento autónomo del bot en el servidor bursátil definido. La llave de Alpha Vantage se transmite a OpenAI dentro de la configuración de MCP y al servidor de Alpha Vantage, como requiere esta arquitectura. No se agregan herramientas de escritura ni servicios adicionales.

El adaptador exige estado `completed`, texto no vacío y, al solicitar MCP, al menos una llamada sin errores. Si falla se aplica el respaldo DEMO de Iris. Esto verifica uso de herramientas, pero no certifica exactitud de cada dato financiero ni impone exactamente dos consultas.

## Archivos cambiados y conservados

- `mesa/agentes.py`: nuevo cliente, solicitud, lectura de salida, rechazo de respuestas incompletas y errores sanitizados; prompts, fórmulas y contratos financieros conservados.
- `mesa/config.py`, `.env.example`, `.devcontainer/devcontainer.json`, `verificar_configuracion.py` y workflow financiero: nombre exacto del secreto y modelo de OpenAI.
- `requirements.txt`: SDK de OpenAI en lugar de Anthropic, con límites de versión mayor para las dependencias.
- Notebook: sustitución completa del adaptador, instalación, configuración, nombres y llamadas. Se mantienen 18 celdas y operación autónoma; sin salidas pregrabadas.
- `tests/test_mesa.py`: mismos casos de regresión, con sustituto OpenAI. `tests/test_openai.py` agrega verificación del SDK, MCP, errores y notebook sin red.
- `mesa/telegram_io.py`, `bot_continuo.py`, `revisar_telegram.py`, `verificar_configuracion.py`: se evita imprimir mensajes HTTP crudos que podrían incluir credenciales. Se conserva polling y comportamiento de comandos.
- `README.md`, `AGENTS.md`, `CLAUDE.md` y documentación nueva: explican configuración y atribución. `.claude/commands/analiza.md` y `.mcp.json` se conservan como ruta opcional de desarrollo, no como dependencia Anthropic de ejecución.
- `mesa/pipeline.py`, `mesa/comandos.py`, scripts de entrada, fórmulas, datos DEMO y guías Word: conservados salvo ajustes de seguridad expresamente indicados. Las guías Word son referencia original; no fueron reescritas ni presentadas como instrucciones actualizadas de OpenAI.

## Verificación y límites

La evidencia de ejecución local se registra en `VALIDACION.md`. Las pruebas usan Python 3.12 y SDK OpenAI 2.54.0 instalado desde el registro. El transporte HTTP simulado recorre la serialización y lectura del SDK real, sin enviar solicitudes externas ni consumir saldo.

Se comprueba la cadena simulada, cálculos originales, autorización del chat, atención de lotes, errores MCP, estado incompleto, texto vacío, codificación de URL, `OPENIA_API_KEY` explícita, separación de herramientas para Iris y ejecución simulada de las celdas del notebook. Eso no sustituye una ejecución con servicios reales.

Las etiquetas `v7` de checkout, setup-python y upload-artifact se consultaron en sus repositorios oficiales y existen; no se cambiaron las versiones originales de Actions.

## Activación pendiente

1. Guardar los cuatro secretos del README en **J.A.R.V.I.S.**. Los cinco nombres del original se verificaron, incluido OPENIA_API_KEY; no se pueden extraer sus valores ni transferir automáticamente.
2. Para que el original siga respondiendo, usar otro bot de Telegram en la copia. No ejecutar dos lectores con el mismo token.
3. Ejecutar una prueba manual con `simulacion=true` y ticker AAPL para validar transporte a Telegram con datos DEMO. Esto sí envía mensajes.
4. Ejecutar una sola prueba real con AAPL. Verificar ficha con `fuente=Alpha Vantage vía MCP`, nombres MCP, fecha de dato, indicadores, nota y artefacto. Consume IA y cuota de datos.
5. Enviar `/analiza MSFT` al nuevo bot y confirmar respuesta por revisión programada. Verificar también chat no autorizado y ticker inválido.

El asistente no envió mensajes a Telegram ni intentó extraer las llaves del original. Mientras no existan credenciales en la copia, el cron termina sin atender Telegram. Esta fase deja el código preparado para las modificaciones posteriores solicitadas por Jorge Valencia.

## Limitaciones heredadas

Se conserva el enfoque educativo: no hay memoria, lectura de archivos, análisis de código, comparativos sectoriales automáticos, control rígido de cuota diaria ni validación financiera exhaustiva. La autorización es abierta si falta CHAT_ID; los mensajes fallidos se confirman y no se reintentan por sí solos. `modo=REAL` puede contener datos DEMO por respaldo. El límite de 900 caracteres y el formato JSON se solicitan por prompt sin esquema estricto. El parser reconoce cualquier texto que empiece por `/analiza` y usa el segundo token. Estas mejoras deben decidirse separadamente para no alterar el alcance de la réplica.

## Referencias oficiales de compatibilidad

- [OpenAI Responses API](https://developers.openai.com/api/reference/python/resources/responses/methods/create): esquema de solicitud y respuesta.
- [OpenAI MCP servers](https://developers.openai.com/api/docs/guides/tools-connectors-mcp): herramientas remotas, aprobación y elementos mcp_call.
- [Modelo GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna): ajuste de razonamiento y Responses.
- [Guía de modelos GPT-6](https://developers.openai.com/api/docs/guides/latest-model): compatibilidad de parámetros.

Se utilizó OpenAI Docs. La página específica de migración Astra no estuvo disponible tras dos intentos y no se utilizó para inferir parámetros de Luna. El modelo y los parámetros se sustentan en su propia página y en la referencia Responses.
