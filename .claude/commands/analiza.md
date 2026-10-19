---
description: Ejecuta la Mesa Financiera (Batuta dirige a Iris → Euler → Vera) para un ticker
argument-hint: TICKER [--simulacion] [--telegram]
---
Ejecuta la cadena de 3 agentes para: $ARGUMENTS

1. Si no se indicó ticker, usa AAPL.
2. Corre `python verificar_configuracion.py`. Si dice MODO SIMULACIÓN, avísalo y agrega `--simulacion`.
3. Corre `python analizar.py $ARGUMENTS`.
4. Explica en español sencillo, en este orden:
   - Iris entrega hasta 100 sesiones de TIME_SERIES_DAILY compact, función gratuita.
   - Euler calcula medias de 20/50 sesiones, rendimiento de precio de 20 sesiones, volatilidad diaria y caída desde máximo de cierre de 20 sesiones; aplica reglas didácticas documentadas.
   - Vera comunica la conclusión técnica. No es pronóstico ni orden automática de inversión.
5. Indica la ruta del archivo de evidencia en `salidas/`.
Nunca muestres el valor de ninguna llave.
