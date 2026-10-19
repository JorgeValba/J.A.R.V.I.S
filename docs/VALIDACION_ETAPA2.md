# Validación vigente de JARVIS
Preparado para **Jorge Valencia** · 18 de octubre de 2026.

- 64 pruebas locales aprobadas y 64 pruebas aprobadas en GitHub. Dependencias sin conflictos comprobados en el entorno de trabajo.
- Regresión de fecha 2024, fechas futuras, fin de semana, valores inválidos, cuota y plan en respuestas HTTP 200, errores sin credenciales, datos parciales, fallos OpenAI, Telegram y notebook cubiertos sin red en pruebas unitarias.
- Prueba integrada real de AAPL realizada una vez con los secretos existentes: cierre 2026-10-16, datos de precio presentes, fundamentales bloqueados por aviso de cuota, estado REAL_PARCIAL. OpenAI y envío Telegram completados. No se confirma entrega visual en el dispositivo, sino aceptación de los mensajes por la API de Telegram.
- [Prueba real y logs](https://github.com/JorgeValba/J.A.R.V.I.S./actions/runs/39183844888/job/117842109206).
- [Investigación y alcance de la corrección](CORRECCION_DATOS.md).

Pendiente externo: obtener fundamentales completos cuando haya cuota y acceso a OVERVIEW. No se verificaron contra una segunda fuente las cifras devueltas por Alpha Vantage. No se promete disponibilidad permanente ni ejecución exactamente una vez.
