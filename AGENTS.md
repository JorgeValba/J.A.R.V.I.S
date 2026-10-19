# Instrucciones para agentes de programación (Codex, Claude Code y otros)

Este repositorio es una **actividad educativa para principiantes** del diplomado de la Dra. Elda C. Morales:
un ecosistema de **3 agentes financieros** que se pasan el trabajo en cadena y se controlan desde Telegram.

```
Telegram /analiza AAPL ─► Batuta · Orquestador (mesa/pipeline.py)
   ├─ Iris  · Recolectora  (Agente 1: API oficial Alpha Vantage) ─► ficha JSON
   ├─ Euler · Analista     (Agente 2: Python calcula, OpenAI interpreta) ─► análisis JSON
   └─ Vera  · Comunicadora (Agente 3: OpenAI redacta) ─► nota final en Telegram
```

Usa siempre estos nombres (Batuta, Iris, Euler, Vera) al explicar el sistema: coinciden con el mockup y con las guías.

## Cómo hablar con la persona usuaria
- Responde en **español**, con lenguaje sencillo: la persona está aprendiendo.
- Antes de cada comando di en una línea qué va a hacer y qué debe ver al terminar.
- Si algo falla, explica la causa probable y el siguiente paso; no pegues trazas largas sin explicarlas.

## Reglas de seguridad (obligatorias)
1. **Nunca** imprimas, copies ni subas el valor de una llave. Para revisar llaves usa `python verificar_configuracion.py`, que solo dice si existen.
2. **Nunca** agregues `.env` a git ni escribas llaves dentro del código.
3. El modo real gasta cuota (Alpha Vantage gratuito: 25 consultas al día) y saldo de la API de OpenAI.
   **Pregunta antes** de ejecutar sin `--simulacion` más de una vez.
4. No cambies la regla de oro: los cálculos se hacen en Python (`calcular_indicadores`), no en el prompt.
5. Toda nota final debe terminar con: "Nota educativa, no es recomendación de inversión."

## Comandos
| Para qué | Comando |
|---|---|
| Instalar | `pip install -r requirements-dev.txt` |
| Pruebas (sin llaves) | `pytest -q` → debe decir `20 passed` o más |
| Cadena en simulación | `python analizar.py AAPL --simulacion` |
| Revisar configuración | `python verificar_configuracion.py` (`--datos` hace una consulta gratuita) |
| Cadena real | `python analizar.py AAPL` |
| Cadena real + Telegram | `python analizar.py AAPL --telegram` |
| Saber el chat_id | `python obtener_chat_id.py` (antes escribe "hola" al bot) |
| Bot en vivo | `python bot_continuo.py` (Ctrl + C para detener) |

Las llaves se leen de variables de entorno o del archivo `.env` (plantilla: `.env.example`).
Si faltan `OPENIA_API_KEY` o `ALPHAVANTAGE_API_KEY`, el sistema entra solo en **modo simulación**.

## Rutina "ejecuta la actividad"
Cuando te pidan ejecutar o probar la actividad, sigue este orden y reporta cada resultado:
1. Instala dependencias y corre `pytest -q`.
2. Corre `python analizar.py AAPL --simulacion` y muestra las entregas 1→2 y 2→3.
3. Corre `python verificar_configuracion.py`. Si hay llaves, pregunta si desea el modo real.
4. En modo real, corre `python analizar.py <TICKER>` y confirma que la modo sea REAL o REAL_PARCIAL y el cierre sea reciente.
5. Indica dónde quedó la evidencia (`salidas/*.json`) y qué capturas tomar para la rúbrica.

## Estructura
- `mesa/config.py` llaves y modos · `mesa/agentes.py` los 3 agentes · `mesa/pipeline.py` el orquestador
- `mesa/telegram_io.py` Bot API · `mesa/comandos.py` interpreta `/analiza`
- `revisar_telegram.py` lo usa GitHub Actions los lunes a las 09:00 de Ciudad de México o manualmente (funciona con la computadora apagada)
- `.github/workflows/` automatizaciones · `tests/` pruebas en simulación

## Adaptación vigente — Jorge Valencia
Modelo gpt-5.1; secreto OPENIA_API_KEY. Respetar S1–S5 en docs/SEGURIDAD.md. Consultar docs/MANUAL_USO.md para retención de Telegram (24 h), activación y límites. No modificar PRUEBA_ELD.

## Corrección de datos vigente
Iris usa mesa/datos.py exclusivamente con TIME_SERIES_DAILY outputsize=compact; no depende de IA para leer cifras. No emitir datos ficticios ante fallas reales. Consultar docs/CORRECCION_DATOS.md. Mantener las claves y los errores del proveedor fuera de logs crudos.

Versión gratuita autorizada por Jorge Valencia: medias20/50, variación20, volatilidad diaria20 y conclusión técnica en Python. Los indicadores Premium y sus fórmulas anteriores se retiraron a solicitud expresa. Ver docs/VERSION_GRATUITA.md.
