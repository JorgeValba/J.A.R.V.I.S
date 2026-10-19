"""Pruebas en modo simulación: verifican la cadena sin llaves ni internet.  Ejecutar: pytest -q"""
import json
import os

import pytest

os.environ["MODO_SIMULACION"] = "1"

from mesa import agentes, config, pipeline as pl          # noqa: E402
from mesa import comandos                                  # noqa: E402


@pytest.fixture(autouse=True)
def simulacion(monkeypatch, tmp_path):
    monkeypatch.setattr(config, "MODO_SIMULACION", True)
    monkeypatch.setattr(config, "CARPETA_SALIDAS", str(tmp_path))


def test_datos_faltantes_no_rompen_el_calculo():
    ind=agentes.calcular_indicadores({"sesiones":[]})
    assert ind["decision_tecnica"]=="INFORMACION_INSUFICIENTE"


def test_extraer_json_con_texto_alrededor():
    assert agentes.extraer_json('Aquí tienes: {"a": 1} listo')["a"] == 1
    with pytest.raises(ValueError):
        agentes.extraer_json("sin json")


@pytest.mark.parametrize("entrada, esperado", [(" aapl ", "AAPL"), ("brk.b", "BRK.B")])
def test_ticker_valido(entrada, esperado):
    assert pl.normalizar_ticker(entrada) == esperado


@pytest.mark.parametrize("entrada", ["", "AAPL; rm -rf", "ACCIONMUYLARGAXYZ"])
def test_ticker_invalido(entrada):
    with pytest.raises(ValueError):
        pl.normalizar_ticker(entrada)


def test_cadena_completa_output_es_input():
    avisos = []
    r = pl.pipeline("msft", avisar=avisos.append)
    assert r["entrega_2_analisis"]["ficha"] == r["entrega_1_ficha"]       # 1 → 2
    assert r["entrega_1_ficha"]["ticker"] in r["entrega_3_nota"]          # 2 → 3
    assert agentes.DESCARGO in r["entrega_3_nota"]
    assert any("Entrega 1→2" in a for a in avisos) and any("Entrega 2→3" in a for a in avisos)
    with open(r["archivo"], encoding="utf-8") as f:
        assert json.load(f)["ticker"] == "MSFT"


def test_fuente_caida_no_inventa_precios(monkeypatch):
    monkeypatch.setattr(config, "MODO_SIMULACION", False)
    monkeypatch.setattr(agentes, "obtener_ficha", lambda *args: {"ticker":"AAPL", "precio":None, "estado_datos":"NO_DISPONIBLES"})
    ficha, herramientas = agentes.agente_recolector("AAPL")
    assert ficha["precio"] is None and herramientas == []


def test_agentes_reales_encadenan_con_openai_simulado(monkeypatch):
    """Imita las respuestas de OpenAI para revisar el camino 'real' sin gastar llaves."""
    monkeypatch.setattr(config, "MODO_SIMULACION", False)

    def openai_falso(system, mensaje, max_tokens=320):
        if "Analista" in system:
            datos=json.loads(mensaje)
            assert datos["indicadores"]["decision_tecnica"]=="EVALUAR_ENTRADA"
            return '{"lectura_precio":"a","lectura_riesgo":"b","lectura_decision":"c","pregunta_para_investigar":"d"}', []
        assert json.loads(mensaje)["lectura"]["lectura_precio"]=="a"
        return "IBM: lectura técnica breve", []

    ficha=agentes.ficha_demo("IBM","test")
    ficha["fuente"]="Alpha Vantage API gratuita"
    monkeypatch.setattr(agentes,"obtener_ficha",lambda *args:ficha)
    monkeypatch.setattr(agentes, "llamar_openai", openai_falso)
    r = pl.pipeline("IBM", avisar=lambda t: None)
    assert r["herramientas_mcp"] == []
    assert r["entrega_1_ficha"]["fuente"] == "Alpha Vantage API gratuita"
    assert r["entrega_3_nota"].endswith(agentes.DESCARGO)                   # el descargo se garantiza


def test_bot_ignora_chats_ajenos_y_responde_ayuda(monkeypatch):
    enviados = []
    monkeypatch.setattr(comandos, "enviar", lambda chat, texto: enviados.append((chat, texto)))
    monkeypatch.setattr(config, "TELEGRAM_CHAT_ID", "111")
    assert comandos.atender({"chat": {"id": 999}, "text": "/analiza AAPL"}) is None
    assert enviados[-1][1] == "Este bot es privado."
    comandos.atender({"chat": {"id": 111}, "text": "hola"})
    assert "Mesa Financiera" in enviados[-1][1]
    r = comandos.atender({"chat": {"id": 111}, "text": "/analiza aapl"})
    assert r["ticker"] == "AAPL" and agentes.DESCARGO in enviados[-1][1]


def test_revision_de_github_actions_atiende_y_confirma(monkeypatch):
    """Simula la corrida de GitHub Actions: 4 mensajes pendientes, límite de 3 por revisión."""
    import revisar_telegram as rt
    pendientes = [{"update_id": i, "message": {"chat": {"id": 111}, "text": t}}
                  for i, t in enumerate(["/analiza AAPL", "hola", "/analiza MSFT", "/analiza NVDA"], start=10)]
    confirmados, enviados = [], []
    monkeypatch.setattr(config, "TELEGRAM_CHAT_ID", "111")
    monkeypatch.setattr(config, "MAX_ANALISIS_POR_RUN", 3)
    monkeypatch.setattr(config, "TELEGRAM_BOT_TOKEN", "token-de-prueba")
    monkeypatch.setattr(rt, "verificar_bot", lambda: "bot_prueba")
    monkeypatch.setattr(rt, "preparar_polling", lambda: None)
    monkeypatch.setattr(rt, "obtener_mensajes", lambda: pendientes)
    monkeypatch.setattr(rt, "confirmar_leidos", confirmados.append)
    monkeypatch.setattr(comandos, "enviar", lambda chat, texto: enviados.append(texto))
    rt.main()
    assert confirmados == [10, 11, 12]                      # NVDA queda para la siguiente revisión
    assert sum(agentes.DESCARGO in t for t in enviados) == 2  # AAPL y MSFT recibieron su nota


def test_revision_sin_token_termina_sin_error(monkeypatch, capsys):
    """Una copia de la plantilla sin Secrets no debe marcar error en Actions cada 10 minutos."""
    import revisar_telegram as rt
    monkeypatch.setattr(config, "TELEGRAM_BOT_TOKEN", "")
    rt.main()
    assert "nada que revisar" in capsys.readouterr().out


def test_los_agentes_se_presentan_con_su_nombre():
    """Los nombres del mockup (Batuta, Iris, Euler, Vera) aparecen en Telegram."""
    avisos = []
    r = pl.pipeline("AAPL", avisar=avisos.append)
    texto = "\n".join(avisos)
    for nombre in ("Batuta", "Iris", "Euler", "Vera"):
        assert nombre in texto
    assert r["entrega_3_nota"].startswith(agentes.FIRMA_VERA)
