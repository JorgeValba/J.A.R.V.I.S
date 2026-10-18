# Análisis del repositorio PRUEBA_ELD

Elaborado por: **Jorge Valencia**  
Fecha: 18 de octubre de 2026  
Fuente examinada: [JorgeValba/PRUEBA_ELD](https://github.com/JorgeValba/PRUEBA_ELD), rama `main`, commit `0d594a0424805a26f07b36a13cd91e470e6cc246`.

## Conclusión y alcance

El original es una actividad educativa de la Dra. Elda C. Morales. Implementa una cadena secuencial de tres roles con llamadas independientes al mismo modelo de Anthropic. Batuta organiza el flujo; no es una cuarta llamada de IA. Telegram recibe órdenes bursátiles y muestra avances. No hay memoria conversacional, ejecución de código del usuario, lectura de documentos, base de datos, entrenamiento de modelos ni operación de inversiones.

Se inspeccionaron los 27 archivos versionados: código, pruebas, configuraciones, las 18 celdas del notebook y el contenido textual de las dos guías Word. También se verificó en la interfaz de GitHub la existencia de los nombres de Repository Secrets, sin acceder a sus valores. El análisis de código permite explicar el diseño; por sí solo no demuestra que las credenciales, la cuota o los servicios reales funcionen.

## Inventario completo

| Ruta | Contenido y función |
|---|---|
| `.claude/commands/analiza.md` | Comando de desarrollo para Claude Code: verificar configuración, ejecutar la cadena y explicar entregas. No recibe directamente mensajes de Telegram. |
| `.devcontainer/devcontainer.json` | Codespaces con Python 3.12, extensiones Python/Jupyter, sugerencia de cuatro secretos, instalación y pruebas al crear; verificación al conectar. Los secretos de Codespaces son distintos de los de Actions. |
| `.env.example` | Plantilla vacía de cuatro credenciales y opciones `MODELO`, `MODO_CLASE`, `MODO_SIMULACION`. No es una llave ni se carga automáticamente como `.env`. |
| `.github/workflows/mesa-financiera.yml` | Ejecución cada diez minutos o manual; instala dependencias, analiza un ticker manual con Telegram, revisa la bandeja y conserva evidencias durante 14 días. Concurrencia de un workflow y máximo ocho minutos. |
| `.github/workflows/pruebas.yml` | En cada push o ejecución manual instala dependencias y pytest, ejecuta pruebas y análisis AAPL simulado. No inyecta secretos. |
| `.gitignore` | Excluye `.env`, entornos, cachés, evidencias y checkpoints. No protege por sí mismo otros nombres de archivos con secretos. |
| `.mcp.json` | Configura Alpha Vantage para el cliente de desarrollo Claude Code con interpolación de variable. El programa Python configura su conexión por separado. |
| `AGENTS.md` | Instrucciones educativas y de seguridad para asistentes, comandos de ejecución, nombres de agentes y regla de cálculo en Python. |
| `CLAUDE.md` | Remite a AGENTS e indica cómo usar el comando y MCP desde Claude Code. |
| `README.md` | Presentación, arquitectura, rutas Colab/Actions/Claude Code/Codex/Codespaces, instalación y secretos. Contiene enlaces a la plantilla de la docente. |
| `analizar.py` | Entrada de terminal. Recibe ticker, `--simulacion` y `--telegram`; activa simulación antes de importar configuración; muestra avances, nota y ruta de evidencia. |
| `bot_continuo.py` | Bot persistente por polling de 30 s; verifica identidad, elimina webhook, mantiene offset en memoria y atiende mensajes. Reintenta errores de red tras cinco segundos. |
| `docs/01_Guia_del_estudiante.docx` | Guía educativa: roles, fórmulas, rutas de puesta en marcha, secretos, evidencias y resolución de problemas. Se conserva como referencia original. |
| `docs/02_Guia_del_docente_y_rubrica.docx` | Preparación de clase, secuencia didáctica, rúbrica, variantes, problemas y notas técnicas. Declara pruebas simuladas y ausencia de validación real del paquete original. Se conserva como referencia original. |
| `mesa/__init__.py` | Identificación del paquete educativo. |
| `mesa/config.py` | Carga dotenv si está instalado; lee y limpia variables, convierte banderas, establece simulación, límite de lote y directorio de salidas; `resumen` muestra presencia sin valores secretos. |
| `mesa/agentes.py` | Cliente Anthropic diferido, adaptador de mensajes/MCP, extracción JSON, conversión numérica, prompts, datos DEMO, tres agentes, indicadores y nota. Es el núcleo de la integración a migrar. |
| `mesa/comandos.py` | Reconoce `/analiza`, restringe por chat, valida ticker, ejecuta Batuta y envía la nota. Otros textos devuelven ayuda; los adjuntos no se analizan. |
| `mesa/pipeline.py` | Batuta: normaliza ticker, ejecuta Iris→Euler→Vera, publica avisos/entregas y guarda evidencia con fecha UTC. |
| `mesa/telegram_io.py` | Peticiones HTTP a Bot API: `sendMessage`, `getMe`, `deleteWebhook`, `getUpdates`, confirmación por offset y autorización del chat. Trunca mensajes a 4000 caracteres. |
| `notebook/Mesa_Financiera_Telegram.ipynb` | Ruta Colab autónoma con 18 celdas (9 de código): instala, lee secretos, define conexión/agentes/cálculos/orquestador, prueba y escucha Telegram. Duplica lógica de Python y requiere migración separada. No guarda evidencias como el módulo de terminal. |
| `obtener_chat_id.py` | Muestra los chat IDs de mensajes pendientes después de verificar el bot y quitar webhook. No revela el token; sí muestra nombre y chat ID. |
| `requirements.txt` | `anthropic>=1.0`, `requests>=2.31`, `python-dotenv>=1.0`. pytest se instala aparte. No hay lockfile. |
| `revisar_telegram.py` | Revisión de una sola tanda para Actions. Sin token termina correctamente; atiende hasta tres actualizaciones, confirma cada una incluso si falla y termina. |
| `tests/conftest.py` | Añade la raíz del proyecto al path de importación de pytest. |
| `tests/test_mesa.py` | 20 casos contando parametrizaciones: fórmula, umbrales, datos faltantes, JSON, ticker, cadena y evidencias, respaldo DEMO, camino real con modelo sustituido, autorización/ayuda, lote de Actions, falta de token y nombres. No llama a APIs reales. |
| `verificar_configuracion.py` | Muestra presencia de llaves y prueba Telegram si tiene token. `--mcp` invoca Iris para IBM y puede consumir IA y datos. No es una comprobación puramente local si hay credenciales. |

## Variables y secretos

En el original `mesa/config.py` lee `ANTHROPIC_API_KEY`, `ALPHAVANTAGE_API_KEY`, `TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHAT_ID`. `python-dotenv` carga `.env` sin reemplazar variables de entorno existentes. Los espacios exteriores se eliminan. Con alguna de las dos llaves IA/datos ausente, o `MODO_SIMULACION=1`, se activa simulación; las llaves de Telegram no determinan ese modo.

Opciones: `MODELO=claude-haiku-5-5`, `MODO_CLASE=1`, `MAX_ANALISIS_POR_RUN=3` y `CARPETA_SALIDAS=salidas`. Los valores por defecto se observaron en el código; no se verificó disponibilidad del modelo Anthropic.

El workflow conecta expresamente `${{ secrets.NOMBRE }}` con variables del proceso. Un secreto de GitHub no aparece automáticamente en Python, Colab ni Codespaces. El 18 de octubre se verificaron estos nombres en el original: `ALPHAVANTAGE_API_KEY`, `ANTHROPIC_API_KEY`, `OPENIA_API_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`. El código original no utiliza el secreto OpenAI aunque exista. Los valores no se pueden consultar ni copiar desde la interfaz de GitHub.

## Contratos entre agentes

| Componente | Entrada | Proceso | Salida |
|---|---|---|---|
| Batuta | Ticker normalizado, callback de avisos | Secuencia fija y evidencias | Diccionario completo de corrida |
| Iris | Ticker | Solicita al modelo hasta dos consultas MCP de cotización y empresa | Ficha JSON + nombres de herramientas |
| Euler | Ficha completa | `calcular_indicadores` hace aritmética; modelo interpreta | `ficha`, `indicadores`, `lectura` |
| Vera | Análisis completo | Modelo redacta hasta 900 caracteres por instrucción | Texto para Telegram con firma y descargo |

Iris solicita: ticker, nombre, sector, precio, cambio porcentual, fecha del dato, P/E, beta, máximo/mínimo de 52 semanas y capitalización. Añade `fuente`. `extraer_json` toma desde la primera llave hasta la última y usa `json.loads`; no valida un esquema completo.

Euler calcula `(precio − mínimo)/(máximo − mínimo) × 100`, redondeado a un decimal cuando hay números y máximo > mínimo. Beta: menor que 0.8 verde; de 0.8 a 1.2 inclusive amarillo; mayor que 1.2 rojo; sin dato blanco. Convierte P/E y cambio diario a números, pero no los calcula. La lectura solicita precio, riesgo, valuación y pregunta de investigación. Un JSON inválido se sustituye por texto de hasta 300 caracteres; errores de API sí pueden interrumpir la cadena.

Vera recibe todos los datos anteriores. El prompt pide texto plano, español y de tres a cinco emojis. Si el descargo no aparece en el texto, el código lo agrega. La condición original comprueba presencia, no que sea exactamente la última frase. El límite de 900 caracteres se pide al modelo, pero no se valida; Telegram trunca a 4000.

## Flujo desde Telegram

1. El usuario envía `/analiza AAPL` al bot de BotFather.
2. El proceso elimina un webhook previo para poder usar `getUpdates`. Actions hace polling periódico; el bot continuo usa long polling.
3. Se obtiene `message.chat.id` y `message.text`. Si hay chat configurado se compara con su representación textual. Sin chat configurado, se permite cualquier chat.
4. Se comprueba el prefijo `/analiza`; se toma el segundo token, se convierte a mayúsculas y se valida con `[A-Z0-9.\-]{1,12}`. Se permiten puntos y guiones. No se comprueba en ese momento si la acción existe.
5. Batuta informa ticker y modo, anuncia a Iris y recibe su ficha. Con modo clase publica la ficha truncada a 1500 caracteres y nombres MCP.
6. Euler recibe esa misma ficha, Python calcula y el modelo interpreta. Batuta publica los indicadores si está activo modo clase.
7. Vera recibe el análisis y produce la nota. Batuta guarda la corrida; el manejador envía la nota final al chat.
8. Actions confirma la actualización usando `offset=update_id+1`; el bot continuo avanza el offset en memoria. Telegram no mantiene indefinidamente los pendientes.

La ruta manual de Actions puede analizar un ticker y después atender mensajes pendientes en la misma ejecución. El input manual por defecto es AAPL. El límite de tres se aplica a **actualizaciones**, incluyendo ayuda y mensajes no autorizados, no a tres análisis completados. Los fallos también se confirman, por lo que no hay reintento automático del mismo mensaje.

## Integración financiera y Anthropic

El cliente es `anthropic.Anthropic(api_key=...)` y se crea solo cuando se necesita. Euler y Vera usan `messages.create` con `system`, `messages` y `max_tokens`. Iris usa `beta.messages.create`, servidor `https://mcp.alphavantage.co/mcp?apikey=...`, herramienta `mcp_toolset` y beta `mcp-client-2025-11-20`. Se concatenan bloques `text`; los nombres provienen de bloques `mcp_tool_use`.

La fuente de mercado prevista es Alpha Vantage por MCP. No hay CSV, base local de cotizaciones, scraping ni búsqueda web. El modelo decide las herramientas concretas; el código no fija ni verifica dos endpoints específicos. Cotización y datos generales corresponden conceptualmente a GLOBAL_QUOTE y OVERVIEW, pero su invocación efectiva debe observarse en la ejecución real. Fecha, moneda y actualización dependen de los datos y del plan de la fuente; no se debe prometer tiempo real. La pregunta sobre P/E sectorial no implica que el sistema haya descargado comparables del sector.

Si Iris falla por red, cuota, autenticación o JSON, devuelve una empresa ficticia: precio 150, cambio 1.2 %, P/E 28, beta 1.25, máximo 180, mínimo 120 y capitalización null. La posición resultante es 50 % y la beta se clasifica alta. En simulación Euler y Vera también son deterministas; si Iris falla durante modo real, estos dos aún intentan llamadas de IA.

## Hallazgos y límites que pueden cambiar una decisión

| Evidencia en código | Implicación | Tratamiento en esta preparación |
|---|---|---|
| `fuente` se asigna a Alpha Vantage tras extraer JSON, sin exigir llamadas MCP | Una ficha con forma correcta no prueba que se consultó mercado | El adaptador OpenAI exige al menos una llamada MCP sin errores; aún no valida cada cifra contra la respuesta bruta |
| `modo` se calcula antes de recolectar | Puede decir REAL junto a ficha DEMO | Se conserva el contrato y se documenta; para decidir si hay datos reales se inspecciona `fuente` |
| El prompt pide dos consultas; el código no impone contador | No garantiza consumo diario ni dos consultas exactas | Se conserva y se documenta para una mejora futura |
| `chat_autorizado` admite todos si no hay ID | Bot sin esa configuración no es privado | Configurar siempre TELEGRAM_CHAT_ID |
| Offset se confirma en `finally` y concurrencia solo cubre el workflow | Se pueden perder reintentos o competir con otro consumidor del mismo token | No operar original y copia simultáneamente con el mismo bot |
| La guía declara pruebas simuladas, no reales | No es evidencia de funcionamiento de MCP y credenciales | Separar validación local, integración simulada y prueba externa |
| Beta y posición anual son los únicos cálculos principales | No mide riesgo total, rentabilidad esperada ni valor intrínseco | Mantener finalidad educativa, sin convertir el semáforo en señal de inversión |
| No hay esquema estricto, control de antigüedad/moneda o pruebas de cada cifra redactada | Datos y texto pueden requerir revisión humana | No introducir un rediseño en esta migración; registrar limitación |
| Errores de red pueden incluir URLs autenticadas | Riesgo de filtrar tokens en trazas | En la copia se suprimen detalles crudos de errores en rutas de ejecución |

## Requisitos y operación

Python 3.12 según Actions/Codespaces, dependencias de requirements y pytest para pruebas. Internet para OpenAI/Anthropic, Alpha Vantage y Telegram en modo real. Cuota y saldo válidos, acceso al modelo, chat correcto, un único consumidor del bot y Actions habilitado para la ruta programada. No requiere servidor web propio porque usa polling.

Las evidencias de terminal/Actions incluyen ticker, modo, fecha UTC, ficha, nombres MCP, análisis y nota. Se escriben en `salidas/TICKER_fecha.json`, excluidas de git. Actions las sube como artefactos durante 14 días; no se publica la respuesta bruta del proveedor. Los dos Word originales se conservan intactos como material de la docente; para ejecutar OpenAI debe prevalecer el README de esta versión.
