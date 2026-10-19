> Registro histórico de la primera migración. Para la versión actual consulta VALIDACION_ETAPA2.md.

# Validación de J.A.R.V.I.S.

Elaborado por: **Jorge Valencia**  
Fecha: 18 de octubre de 2026.

## Resultado local

- Python 3.12, SDK OpenAI 2.54.0, pytest 9.1.1.
- **30 pruebas aprobadas en 12.99 segundos**: 20 casos heredados y 10 adicionales.
- `python analizar.py AAPL --simulacion`: cadena completa, entregas 1→2 y 2→3, nota DEMO y evidencia JSON guardada.
- Simulación: precio 150, mínimo 120, máximo 180 → posición 50.0 %; beta 1.25 → volatilidad alta.
- `python verificar_configuracion.py`: cuatro llaves vacías, modelo gpt-6-luna y simulación activa. No se realizaron llamadas externas.
- SDK con transporte HTTP simulado: cuerpo Responses, autenticación ficticia, salida textual, nombres MCP y codificación de URL correctos.
- Respuestas incompletas/vacías, ausencia de llamadas MCP y errores remotos se rechazan sin imprimir credenciales.
- Notebook: celdas Python ejecutadas en simulación (se omite la celda de instalación exclusiva de Colab); nota correcta sin red. No se probó en un kernel alojado de Colab.
- Error de conexión de Telegram simulado: el token ficticio de la URL no aparece en el error público.
- Fórmula y umbrales de `calcular_indicadores` idénticos al original mediante comparación del árbol sintáctico.
- Archivos esenciales de orquestación, comandos, entrada y las dos guías Word conservados byte por byte.
- No se incluye `.env`, respuestas de proveedores, artefactos de ejecución ni entornos virtuales en la publicación.

## Incidencias resueltas durante la preparación

La primera ejecución de pytest no pudo crear su directorio temporal dentro del aislamiento de Windows: nueve pruebas nuevas pasaron y veinte no llegaron a ejecutarse. La repetición con permiso adecuado aprobó 29 casos. Tras añadir el control de errores de Telegram y la revisión del notebook, la ejecución final usó una carpeta temporal del área de trabajo y aprobó los 30 casos. La incidencia era del entorno, no una falla de la fórmula financiera.

## Pendiente externo

Se verificó en GitHub que J.A.R.V.I.S. no tiene Repository Secrets. No es posible transferir sus valores desde el original. Falta configurar OPENIA_API_KEY, ALPHAVANTAGE_API_KEY, TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID en la copia, y hacer una prueba real. No se verificaron saldo, acceso al modelo, cuota MCP, precisión bursátil ni envío/recepción real de Telegram. No se enviaron mensajes.

El workflow de pruebas en GitHub debe revisarse después de la publicación; este registro distingue la evidencia local de una ejecución alojada. La revisión programada conserva el comportamiento original y termina sin atender Telegram mientras no exista token.
