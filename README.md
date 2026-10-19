# J.A.R.V.I.S.

Adaptación OpenAI elaborada por **Jorge Valencia**, basada en la actividad educativa de la Dra. Elda C. Morales y en [PRUEBA_ELD](https://github.com/JorgeValba/PRUEBA_ELD), conservado sin cambios.

Telegram → Batuta (orquestador Python) → Iris (API oficial Alpha Vantage) → Euler (cálculos Python e interpretación) → Vera (nota educativa).

Usa **gpt-5.1**, OpenAI Responses API y el secreto **OPENIA_API_KEY** exactamente con ese nombre. Ejecución automática **lunes 09:00, America/Mexico_City**, y manual desde Actions → mesa-financiera → Run workflow. Para revisar solo Telegram, borra el ticker AAPL precargado.

**Telegram conserva pendientes hasta 24 horas:** la ejecución semanal no recupera toda la semana. Envía la orden cerca del lunes o activa una revisión manual antes de 24 h. Cada revisión atiende como máximo tres actualizaciones; repítela si quedan pendientes. Enviar una orden no activa por sí solo GitHub Actions.

## Entregables

- [Manual de uso, activación y seguridad](docs/MANUAL_USO.md).
- [A. Medidas de seguridad implementadas y pendientes](docs/SEGURIDAD.md).
- [B. Cambios, agentes y limitaciones](docs/CAMBIOS_ETAPA2.md).
- [Validación de esta versión](docs/VALIDACION_ETAPA2.md).
- [Análisis exhaustivo del repositorio original](docs/ANALISIS_ORIGINAL.md).
- [Correspondencia de la migración a OpenAI](docs/MIGRACION_OPENAI.md).

Las guías Word originales conservan la autoría y las referencias a Anthropic de la docente. Para esta adaptación usa el manual Markdown actualizado.

## Prueba local sin API

Con Python 3.12 y un entorno virtual:

```bash
pip install -r requirements-dev.txt
pytest -q
python analizar.py AAPL --simulacion
```

La simulación usa datos ficticios etiquetados DEMO y guarda evidencia en `salidas/`. Añadir `--telegram` sí envía mensajes, incluso en simulación.

Se conservan terminal, bot continuo, Codespaces y el [notebook autónomo de Colab](https://colab.research.google.com/github/JorgeValba/J.A.R.V.I.S./blob/main/notebook/Mesa_Financiera_Telegram.ipynb). Usa un solo consumidor por token; un bot independiente evita interferir con el original.

**Actualización de datos:** 64 pruebas locales aprobadas. Iris consulta la API oficial directamente y valida fecha y precio. La cotización es de cierre diario, no tiempo real. Los fundamentales pueden requerir Premium. Consulta la [corrección e investigación](docs/CORRECCION_DATOS.md) y los resultados reales en ese documento. No se cambiaron tus secretos.

GPT-5.1 está marcado como obsoleto y su retiro está anunciado para el 1 de abril de 2027; se conserva por solicitud expresa. [Calendario oficial](https://developers.openai.com/api/docs/deprecations).

Estados actuales: REAL, REAL_PARCIAL y SIN_DATOS. Las fallas reales no generan precios DEMO; la demostración se reserva para simulación.

Nota educativa, no es recomendación de inversión.
