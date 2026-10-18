# Mesa Financiera en Telegram · instrucciones para Claude Code

Las instrucciones completas están en AGENTS.md (compartidas con Codex):
@AGENTS.md

Los agentes de esta versión usan OpenAI y OPENIA_API_KEY. Claude Code es solo una herramienta opcional de desarrollo.

## Extras de Claude Code
- `/analiza AAPL` es un comando de este proyecto (`.claude/commands/analiza.md`): ejecuta la cadena en la terminal.
- `.mcp.json` conecta **también a Claude Code** con el servidor MCP de Alpha Vantage. Así la persona puede
  comparar: "pídele a Claude Code la cotización de AAPL con Alpha Vantage" frente a la ficha que entrega Iris (Agente 1).
  Requiere la variable de entorno `ALPHAVANTAGE_API_KEY` y aprobar el servidor la primera vez.
