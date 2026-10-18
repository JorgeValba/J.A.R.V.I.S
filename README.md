# J.A.R.V.I.S.

Adaptación OpenAI elaborada por: **Jorge Valencia**.  
Basada en la actividad educativa de la **Dra. Elda C. Morales**, conservada en [PRUEBA_ELD](https://github.com/JorgeValba/PRUEBA_ELD).

Tres agentes financieros en cadena, controlados desde Telegram. Esta versión usa **OpenAI Responses API** con el secreto **`OPENIA_API_KEY`**, escrito exactamente así.

```text
Telegram: /analiza AAPL
          ↓
Batuta · Orquestador (Python)
          ↓
Iris · Recolectora → OpenAI + Alpha Vantage vía MCP → ficha JSON
          ↓
Euler · Analista → Python calcula, OpenAI interpreta → análisis JSON
          ↓
Vera · Comunicadora → OpenAI redacta → nota educativa en Telegram
```

Se conservan los agentes, los cálculos, los comandos, las entregas de clase, las evidencias, el bot continuo, Actions, Codespaces y el notebook autónomo de Colab. Telegram admite `/analiza TICKER`; no ejecuta código ni analiza archivos enviados por el usuario.

## Estado de esta versión

Migración preparada y verificada localmente en simulación y con transporte HTTP simulado del SDK. **La prueba real de OpenAI + Alpha Vantage + Telegram queda pendiente de configurar los secretos en este repositorio.** Los secretos del original no se transfieren y sus valores no pueden recuperarse desde GitHub.

- [Análisis completo del original](docs/ANALISIS_ORIGINAL.md): inventario por archivo, agentes, flujo, cálculos y limitaciones.
- [Migración y validación](docs/MIGRACION_OPENAI.md): cambios de API, pruebas y activación.
- Las dos guías Word en `docs/` son material original de la docente; conservan referencias a Anthropic. Para configurar esta adaptación prevalecen este README y la guía de migración.

## Probar sin llaves

Recomendado: Python 3.12 en un entorno virtual.

```bash
pip install -r requirements.txt pytest
pytest -q
python analizar.py AAPL --simulacion
```

Deberás ver las entregas Iris→Euler y Euler→Vera, una nota con **DATOS DEMO** y un archivo en `salidas/`. Simulación no consulta OpenAI ni Alpha Vantage. Añadir `--telegram` sí envía mensajes a Telegram, incluso en simulación.

## Configurar los secretos

En [Settings → Secrets and variables → Actions de J.A.R.V.I.S.](https://github.com/JorgeValba/J.A.R.V.I.S./settings/secrets/actions), agrega:

| Nombre exacto | Uso |
|---|---|
| `OPENIA_API_KEY` | API de OpenAI con saldo y acceso al modelo |
| `ALPHAVANTAGE_API_KEY` | Servidor MCP de datos bursátiles |
| `TELEGRAM_BOT_TOKEN` | Token del bot de BotFather |
| `TELEGRAM_CHAT_ID` | Chat autorizado; configúralo para restringir el acceso |

No hace falta `ANTHROPIC_API_KEY`. No cambies `OPENIA` por `OPENAI`: el cliente recibe explícitamente el valor de `OPENIA_API_KEY`.

En tu computadora copia `.env.example` a `.env` y completa los valores **solo en ese archivo local**. En Colab usa su panel de secretos; en Codespaces usa secretos de Codespaces. Los secretos de Actions no se inyectan en esos entornos.

`MODELO` usa `gpt-6-luna` por defecto, con razonamiento `none`, adecuado al presupuesto breve de los agentes. Se puede cambiar por otro modelo compatible con Responses, MCP y ese ajuste; no todos aceptan los mismos parámetros. El acceso de tu cuenta se confirma en una prueba real. Opciones conservadas: `MODO_CLASE=1`, `MODO_SIMULACION=1`, `MAX_ANALISIS_POR_RUN=3`, `CARPETA_SALIDAS=salidas`.

## Rutas de ejecución

| Ruta | Cómo se usa |
|---|---|
| Terminal | `python analizar.py AAPL`; agrega `--telegram` para enviar avances y nota |
| Bot continuo | `python bot_continuo.py`; escucha mientras el proceso siga encendido |
| GitHub Actions | Actions → `mesa-financiera` → Run workflow; el cron revisa cada diez minutos, sujeto a retrasos de GitHub |
| Colab | [Abrir notebook de J.A.R.V.I.S.](https://colab.research.google.com/github/JorgeValba/J.A.R.V.I.S./blob/main/notebook/Mesa_Financiera_Telegram.ipynb); conserva simulación por defecto |
| Codespaces | Code → Codespaces; instala dependencias y ejecuta pruebas automáticamente |
| Asistentes de programación | Consultar `AGENTS.md`; se conserva compatibilidad opcional con Claude Code como entorno de desarrollo |

`python verificar_configuracion.py` informa presencia de llaves y consulta Telegram si hay token. `--mcp` consume IA y datos cuando hay llaves. `python obtener_chat_id.py` ayuda a identificar tu chat tras escribir al bot.

**Usa un solo consumidor por token de Telegram.** Si el original y esta copia leen el mismo bot simultáneamente, pueden competir por los mensajes. Configurar un bot separado permite mantener el original operando sin cambios.

## Datos y límites

Alpha Vantage es la fuente prevista; su plan determina actualización y disponibilidad. Iris solicita cotización y datos generales. Python calcula posición en rango de 52 semanas y semáforo de beta. P/E y cambio diario vienen de la fuente; no se calcula un valor intrínseco ni se ejecutan inversiones.

Sin llaves IA/datos se activa simulación. Si falla MCP en modo real, Iris devuelve datos DEMO identificados y los otros agentes aún intentan usar OpenAI. El campo `modo=REAL` describe la configuración: revisa `fuente` para saber si la ficha es real o DEMO. El máximo de dos consultas está en el prompt, no en un contador estricto.

Las evidencias quedan en `salidas/*.json`, excluidas de git. Actions las conserva como artefactos durante 14 días. No actives registros HTTP de depuración: las URLs autenticadas de Telegram y MCP contienen credenciales.

Nota educativa, no es recomendación de inversión.
