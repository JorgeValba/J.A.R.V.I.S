# Búsqueda de ejemplo completo
Preparado para **Jorge Valencia** · 18 de octubre de 2026.

Límite autorizado: máximo seis símbolos. Candidatos previstos: IBM, MSFT, GOOGL, AMZN, NVDA y JPM. Se detiene al primer ejemplo completo o ante bloqueo de cuota, plan o clave. No se usan claves demo ni datos simulados para aparentar una respuesta completa.

Resultado observado con la misma clave guardada en Repository Secrets:

| Símbolo probado | Cotización | Fundamentales | Resultado |
|---|---|---|---|
| IBM | GLOBAL_QUOTE OK, cierre 2026-10-16 | OVERVIEW devolvió aviso clasificado CUOTA | Incompleto |

Se probaron **1 de los 6 ejemplos permitidos**, con dos solicitudes Alpha Vantage. No se llamó a OpenAI ni se enviaron mensajes a Telegram. No se probaron los otros cinco símbolos porque el bloqueo encontrado corresponde a la consulta del proveedor y no se resuelve eligiendo otro ticker. Esto no demuestra que dichos símbolos no tengan información.

[Registro de la búsqueda real](https://github.com/JorgeValba/J.A.R.V.I.S./actions/runs/39184757162/job/117844782770). El artefacto de esa ejecución conserva el detalle de campos faltantes y diagnóstico. Se retiró el trabajo temporal de búsqueda; no quedó otro horario automático.

No se encontró un ejemplo completo en esta búsqueda. Primero debe restablecerse la cuota; después podrá comprobarse si la clave tiene acceso a OVERVIEW. No se concluye que exista o falte ese permiso a partir del aviso de cuota actual. El script buscar_ejemplo.py queda disponible para repetir conscientemente la búsqueda con máximo seis candidatos, detenerse al encontrar el primero completo y evitar gastos innecesarios cuando haya un bloqueo global.
