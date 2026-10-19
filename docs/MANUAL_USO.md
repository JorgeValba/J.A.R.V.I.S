# C. Manual de uso y activación de J.A.R.V.I.S.
Preparado para: **Jorge Valencia** · 18 de octubre de 2026.

## 1. Preparar el bot y sus secretos

1. Abre [J.A.R.V.I.S. en GitHub](https://github.com/JorgeValba/J.A.R.V.I.S.). Trabaja en este repositorio.
2. Usa un bot diferente del original para que ambos sistemas puedan seguir funcionando. En Telegram, BotFather permite crear uno con `/newbot`. Guarda su token directamente como secreto; no lo publiques ni lo pegues en chats.
3. Abre tu bot y pulsa **Iniciar**; envíale `hola`.
4. Obtén tu identificador de chat. Si lo desconoces, descarga el proyecto, instala dependencias con Python 3.12, copia `.env.example` a `.env`, introduce el token solo en ese archivo local y ejecuta `python obtener_chat_id.py`. El script muestra el identificador; no publiques esa salida. Evita ejecutar otro consumidor mientras lo obtienes.
5. En GitHub abre **Settings → Secrets and variables → Actions → New repository secret** y agrega los cuatro nombres siguientes. Los secretos del original no se copian automáticamente y sus valores no se pueden recuperar desde GitHub.

| Nombre exacto | Valor que debes guardar |
|---|---|
| `OPENIA_API_KEY` | Tu clave de OpenAI, con saldo y acceso a gpt-5.1. Respeta OPENIA. |
| `ALPHAVANTAGE_API_KEY` | Tu clave para los datos financieros. |
| `TELEGRAM_BOT_TOKEN` | Token del bot destinado a J.A.R.V.I.S. |
| `TELEGRAM_CHAT_ID` | Identificador del chat autorizado. |

No necesitas ANTHROPIC_API_KEY. No coloques claves en archivos públicos. No se cambiaron los valores de tus secretos durante la implementación.

## 2. Primera ejecución de prueba

1. Ve a **Actions → mesa-financiera → Run workflow**, rama **main**. Si GitHub solicita habilitar Actions en tu repositorio, habilítalo.
2. Deja **AAPL** en ticker y activa **simulacion**. Pulsa **Run workflow** una sola vez.
3. Abre la ejecución y espera a que termine. El bot debe enviar avances y una nota marcada **DEMO**. Esta prueba no llama a OpenAI ni Alpha Vantage, pero sí envía mensajes por Telegram y también revisa pendientes en simulación.
4. Revisa **Artifacts → evidencias-…** en la ejecución. El JSON identifica fuente, modo, entregas y nota. Una ejecución verde sin token puede significar que no había nada que revisar: verifica que recibiste la nota.
5. Para probar datos reales, repite una vez con **simulacion desactivada**. Consume saldo de OpenAI y cuota Alpha Vantage. Comprueba `modo=REAL`, `fuente=Alpha Vantage vía MCP`, fecha del dato y herramientas MCP en la evidencia. Si aparece DEMO, la consulta real falló o faltan claves; no es validación de datos reales.

## 3. Enviar órdenes desde Telegram

1. En el chat autorizado escribe exactamente `/analiza AAPL`, `/analiza MSFT` o `/analiza IBM`.
2. Para procesar ahora: abre **Actions → mesa-financiera → Run workflow**, **borra AAPL del campo ticker**, desactiva simulacion si quieres datos reales y ejecuta.
3. Si prefieres la revisión automática, envía la orden dentro de las 24 horas anteriores al lunes a las 09:00 de Ciudad de México. GitHub puede iniciar con retraso; para una orden importante, usa la activación manual pronto.
4. Recibirás datos de Iris, interpretación de Euler y nota de Vera. Con MODO_CLASE=1 se muestran las entregas intermedias; el resultado final conserva el descargo educativo.
5. Cada revisión procesa hasta tres actualizaciones, incluyendo saludos o mensajes no válidos. Si hay más, ejecuta otra revisión manual antes de 24 horas. El registro indicará si quedaron pendientes.

**Enviar un mensaje no activa Actions automáticamente.** Telegram elimina pendientes después de como máximo 24 horas; un mensaje del martes no se conserva hasta el lunes siguiente. La opción semanal sencilla fue elegida expresamente y no incluye una cola persistente.

No repitas la misma orden en Telegram y en el campo ticker salvo que quieras dos análisis. No uses `/analiza@nombre_bot`, texto extra ni código adjunto: esta versión acepta `/analiza TICKER` en el chat configurado.

## 4. Horario y otras formas de uso

El único cron financiero ejecuta los lunes a las 09:00, zona America/Mexico_City. También puedes activarlo manualmente cuando lo necesites. Las pruebas automáticas del repositorio no consumen tus API.

En un equipo con Python 3.12: `pip install -r requirements-dev.txt`, luego `pytest -q`; para demostrar: `python analizar.py AAPL --simulacion`. Para una consulta real: `python analizar.py AAPL`; añade `--telegram` para enviarla. `.env` local no se sube a git. En Codespaces y Colab configura sus propios secretos: los de Actions no llegan automáticamente a esos entornos.

El notebook conserva ejecución autónoma y modo simulación por defecto. `python bot_continuo.py` escucha mientras el proceso permanezca abierto. **No lo ejecutes al mismo tiempo que otro lector del mismo bot**, incluidos Colab y el repositorio original.

## 5. Seguridad autorizada e implementada

| Medida | Qué cambia para ti | Ventaja y posible inconveniente |
|---|---|---|
| S1. Chat obligatorio | Debes guardar TELEGRAM_CHAT_ID. | Evita acceso abierto por omisión; detiene atención si falta. |
| S2. Validación | Usa el comando exacto y un ticker; las fichas inválidas se rechazan. | Reduce entradas ambiguas e instrucciones dentro de datos; puede usar DEMO si la fuente devuelve datos mal formados. |
| S3. DEMO explícito | La primera línea avisa y los otros dos agentes usan cálculo/redacción local. | Evita confundir datos ficticios con reales y dos llamadas adicionales; no entrega precio actual. |
| S4. Respeto al webhook | Si hay uno activo, el bot se detiene sin eliminarlo. | Protege otro despliegue; requiere revisar cuál debe atender ese bot. |
| S5. Versiones fijadas | Dependencias y Actions quedan ancladas a versiones verificadas. | Evita cambios inesperados; necesita actualizaciones periódicas con pruebas. |

El detalle de riesgos, límites y medidas pendientes está en [Seguridad](SEGURIDAD.md). No se implementaron cola semanal, reintentos duraderos ni cambios administrativos de acceso. No se rotaron ni trasladaron claves. Las evidencias pueden contener información de tus consultas; en este repositorio público considera su exposición al descargar o compartir artefactos. No compartas logs con credenciales ni actives depuración HTTP.

## 6. Problemas frecuentes

- **No responde:** revisa token, chat, estado de Actions, antigüedad del mensaje y si otro proceso usa el mismo bot. Ejecuta manualmente con ticker vacío.
- **Webhook activo:** el programa no lo borra. Usa un bot independiente o decide conscientemente cómo retirar el despliegue anterior; no cambies el original para resolverlo.
- **Aparece DEMO:** revisa presencia de claves, saldo, cuota, acceso a gpt-5.1 y disponibilidad MCP. No asumas que las cifras son reales.
- **Orden fallida:** el comportamiento original confirma esa actualización; corrige la causa y envía una nueva orden. No existe reintento automático de negocio.
- **Respuestas duplicadas:** no lances varios lectores ni envíes la misma solicitud por ambas rutas. La concurrencia de Actions no garantiza exactamente una vez ante fallos.
- **Programa semanal deshabilitado:** GitHub puede desactivar schedules en repositorios públicos tras 60 días sin actividad. Revisa Actions y reactívalo si corresponde.
- **Modelo no disponible:** la cuenta debe tener acceso. GPT-5.1 tiene retiro anunciado el **1 de abril de 2027**; planifica actualizarlo y volver a probar.

## 7. Alcance de la verificación

48 pruebas locales comprobaron flujo simulado, SDK real con HTTP sustituido, contratos, fórmulas, controles y notebook. No se enviaron mensajes ni se consumieron APIs reales durante estas pruebas. La comprobación integrada final requiere los secretos y los pasos 2–3 anteriores. Ninguna prueba garantiza exactitud financiera ni rentabilidad.

Referencias: [Telegram: retención de actualizaciones](https://core.telegram.org/bots/api#getting-updates), [GitHub: programación de workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule), [OpenAI: retiros de modelos](https://developers.openai.com/api/docs/deprecations).

Nota educativa, no es recomendación de inversión.
