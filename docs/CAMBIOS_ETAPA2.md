# B. Cambios realizados
Preparado para: **Jorge Valencia** · 18 de octubre de 2026.

## Modelo y agentes

Modelo solicitado **gpt-5.1** con Responses API, `reasoning.effort=none`, `store=False` y `OPENIA_API_KEY`. Está configurado en mesa/config.py, .env.example, workflow financiero y notebook. Una variable MODELO local puede sobrescribir el valor; Actions fija gpt-5.1.

| Componente | Función | Personalidad y salida |
|---|---|---|
| Batuta | Orquesta la cadena y guarda evidencia. No es un cuarto agente de IA. | Mantiene su función original. |
| Iris | Consulta cotización y empresa por MCP; entrega ficha JSON. | Conserva curiosidad y meticulosidad. Entrega visible de seis líneas. |
| Euler | Python calcula rango de 52 semanas y semáforo beta; IA interpreta. | Cambiada a auditor escéptico, prudente y preciso; cuatro frases en JSON, cinco líneas visibles con encabezado. |
| Vera | Comunica resultados y límites. | Cambiada a comunicadora ejecutiva, serena y directa; nota de tres a seis líneas con fuente, fecha y descargo. |

Los avisos de progreso pueden ser más breves; los JSON de evidencia conservan datos completos. Las líneas son saltos de línea lógicos: Telegram puede envolverlas según la pantalla. No se recortan advertencias para cumplir un conteo visual.

Prompts compactos y entradas sin duplicar la ficha completa. Presupuestos de salida por solicitud: Iris 600, Euler 320, Vera 280; total máximo configurado 1,200 frente a 2,400 en la primera migración. Esto **no equivale a 50 % de ahorro real**: no se midieron tokens facturados, reintentos ni consumo MCP. Si falla Iris, Euler y Vera se ejecutan localmente. Las fórmulas de calcular_indicadores permanecen iguales.

## Programación

`.github/workflows/mesa-financiera.yml`: único cron `0 9 * * 1` con `timezone: America/Mexico_City`, lunes 09:00 CDMX (actualmente 15:00 UTC). Se conserva workflow_dispatch, concurrencia, permisos contents:read, límite de ocho minutos y artefactos de catorce días. GitHub puede retrasar o descartar ejecuciones programadas bajo carga; en repositorios públicos puede deshabilitarlas tras 60 días sin actividad.

La ruta manual analiza el ticker indicado y luego revisa Telegram. Vacía el campo ticker si solo quieres procesar mensajes. La otra automatización, pruebas.yml, corre por push o manualmente en simulación; no hay otro cron versionado. Bot continuo y Colab se conservan como alternativas manuales. No se puede certificar desde el repositorio que no exista otro proceso externo usando el bot.

Se conservan tres actualizaciones por revisión y confirmación por offset. Se eliminan update_id repetidos dentro del lote recibido. La concurrencia evita simultaneidad dentro del workflow, no garantiza ejecución exactamente una vez ni impide lectores externos.

## Inventario de cambios de esta etapa

- `mesa/config.py`, `.env.example`: modelo predeterminado.
- `mesa/agentes.py`: prompts, presupuestos, validación, respaldo y notas breves.
- `mesa/pipeline.py`: resúmenes visibles, modo efectivo y atribución de evidencia.
- `mesa/comandos.py`, `mesa/telegram_io.py`, `bot_continuo.py`, `revisar_telegram.py`: S1–S4 y revisión semanal/manual.
- `.github/workflows/mesa-financiera.yml`, `.github/workflows/pruebas.yml`: horario/modelo y Actions fijadas.
- `requirements.txt`, `requirements.lock.txt`, `requirements-dev.txt`, `.devcontainer/devcontainer.json`: versiones verificadas e instalación reproducible.
- `notebook/Mesa_Financiera_Telegram.ipynb`: mismas funciones y controles, 18 celdas, ejecución autónoma, sin salidas guardadas.
- `tests/test_mesa.py`, `tests/test_openai.py`, `tests/test_seguridad.py`: regresión y controles nuevos.
- `README.md`, `AGENTS.md` y documentos de esta etapa: instrucciones actualizadas. Análisis del original y validación inicial quedan identificados como históricos.

## Limitaciones pendientes

Prueba integrada real pendiente de secretos y acceso al modelo. Telegram conserva mensajes hasta 24 horas, no una semana. Los mensajes fallidos se confirman como en el original y no se reintentan automáticamente. Los datos de Alpha Vantage pueden ser retrasados o incompletos; no se verifica cada cifra contra otra fuente. El semáforo beta es didáctico, no una medida de riesgo total; P/E exige contexto sectorial. No se ejecuta código adjunto, no se leen archivos ni se realizan operaciones bursátiles.

[OpenAI anuncia retiro de GPT-5.1 el 1 de abril de 2027](https://developers.openai.com/api/docs/deprecations). Antes de esa fecha será necesario autorizar y probar otra migración.
