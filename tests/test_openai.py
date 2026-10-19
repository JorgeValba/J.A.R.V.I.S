"""Pruebas de la migración OpenAI. Jorge Valencia. Sin servicios externos."""
import json
from pathlib import Path

import httpx
import pytest
from openai import OpenAI

from mesa import agentes, config


def instalar_transporte(monkeypatch, handler):
    client = OpenAI(api_key="credencial-ficticia", max_retries=0,
                    http_client=httpx.Client(transport=httpx.MockTransport(handler)))
    monkeypatch.setattr(agentes, "_cliente", client)
    monkeypatch.setattr(config, "ALPHAVANTAGE_API_KEY", "valor-ficticio/+?")
    return client


def respuesta(texto="respuesta", estado="completed", calls=None):
    return {"id": "resp_prueba", "object": "response", "created_at": 0,
            "status": estado, "model": "gpt-5.1",
            "output": (calls or []) + [{"type": "message", "id": "msg_prueba",
                       "role": "assistant", "status": "completed",
                       "content": [{"type": "output_text", "text": texto, "annotations": []}]}]}


def test_sdk_envia_texto_sin_herramientas_ni_clave_bursatil(monkeypatch):
    enviados=[]
    def handler(request):
        enviados.append(json.loads(request.content))
        assert request.url.path=="/v1/responses"
        return httpx.Response(200,json=respuesta("lectura técnica"))
    client=instalar_transporte(monkeypatch,handler)
    try:
        assert agentes.llamar_openai("instrucciones","indicadores")==("lectura técnica",[])
        body=enviados[0]
        assert body["model"]=="gpt-5.1" and body["max_output_tokens"]==320
        assert body["reasoning"]=={"effort":"none"} and body["store"] is False
        assert "tools" not in body and "valor-ficticio" not in json.dumps(body)
    finally:client.close()


@pytest.mark.parametrize("estado,texto",[("incomplete","parcial"),("completed","")])
def test_rechaza_respuestas_incompletas(monkeypatch,estado,texto):
    client=instalar_transporte(monkeypatch,lambda req:httpx.Response(200,json=respuesta(texto,estado)))
    try:
        with pytest.raises(RuntimeError):agentes.llamar_openai("Euler","datos")
    finally:client.close()


def test_error_remoto_no_revela_credenciales(monkeypatch):
    client = instalar_transporte(monkeypatch, lambda req: httpx.Response(
        401, json={"error": {"message": "valor-ficticio/+? no debe salir", "type": "auth"}}))
    try:
        with pytest.raises(RuntimeError) as exc:
            agentes.llamar_openai("instrucciones", "AAPL")
        assert "valor-ficticio" not in str(exc.value)
        assert "401" not in str(exc.value)
    finally:
        client.close()


def test_cliente_usa_nombre_exacto_openia(monkeypatch):
    import openai
    recibidos = {}
    def fake(**kwargs):
        recibidos.update(kwargs)
        return object()
    monkeypatch.setattr(openai, "OpenAI", fake)
    monkeypatch.setattr(config, "OPENIA_API_KEY", "solo-prueba-openia")
    monkeypatch.setattr(agentes, "_cliente", None)
    monkeypatch.setenv("OPENAI_API_KEY", "otro-valor-que-no-debe-usarse")
    agentes._cliente_openai()
    assert recibidos["api_key"] == "solo-prueba-openia"


def test_notebook_cadena_simulada_sin_red(monkeypatch):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    nb = json.loads((Path(__file__).parents[1]/"notebook/Mesa_Financiera_Telegram.ipynb").read_text(encoding="utf-8"))
    namespace = {}
    for i, cell in enumerate(nb["cells"]):
        if cell["cell_type"] == "code" and i != 2:  # instalación exclusiva de Colab
            exec(compile("".join(cell["source"]), f"celda_{i}", "exec"), namespace)
    nota = namespace["pipeline"]("MSFT", avisar=lambda texto: None)["entrega_3_nota"]
    assert "MSFT" in nota and "DEMO" in nota and nota.endswith(agentes.DESCARGO)


def test_sin_mcp_euler_y_vera_no_envian_herramientas(monkeypatch):
    enviados = []
    def handler(request):
        enviados.append(json.loads(request.content))
        return httpx.Response(200, json=respuesta("nota"))
    client = instalar_transporte(monkeypatch, handler)
    try:
        assert agentes.llamar_openai("Vera", "análisis", max_tokens=600) == ("nota", [])
        assert "tools" not in enviados[0] and enviados[0]["max_output_tokens"] == 600
    finally:
        client.close()


def test_error_telegram_no_revela_url_con_token(monkeypatch):
    import requests
    from mesa import telegram_io
    def falla(*args, **kwargs):
        raise requests.ConnectionError("https://api.telegram.org/botTOKEN-FICTICIO/getMe")
    monkeypatch.setattr(requests, "request", falla)
    monkeypatch.setattr(config, "TELEGRAM_BOT_TOKEN", "TOKEN-FICTICIO")
    with pytest.raises(RuntimeError) as exc:
        telegram_io.verificar_bot()
    assert "TOKEN-FICTICIO" not in str(exc.value)
    assert "https://" not in str(exc.value)
