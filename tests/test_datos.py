"""Regresión de datos reales para Jorge Valencia, sin claves ni red."""
from datetime import date, timedelta, datetime, timezone
from types import SimpleNamespace
import pytest
import requests
from mesa import datos, agentes, config


def quote(fecha=None, **kw):
    return {"Global Quote": {"01. symbol":"AAPL", "05. price":"220.50",
        "07. latest trading day":fecha or datetime.now(timezone.utc).date().isoformat(), "10. change percent":"1.25%", **kw}}


def proveedor(monkeypatch, payloads):
    llamadas=[]
    def get(url, params, **kw):
        llamadas.append(params["function"])
        return SimpleNamespace(status_code=200, raise_for_status=lambda:None,
                               json=lambda:payloads[len(llamadas)-1])
    monkeypatch.setattr(datos.requests,"get",get)
    return llamadas


def test_extrae_precio_sin_ia_y_clasifica_plan(monkeypatch):
    llamadas=proveedor(monkeypatch,[quote(),{"Information":"This is a premium endpoint"}])
    f=datos.obtener_ficha("AAPL","ficticia")
    assert llamadas==["GLOBAL_QUOTE","OVERVIEW"]
    assert f["estado_datos"]=="PARCIALES" and f["precio"]==220.5
    assert f["consultas"][1]["estado"]=="PLAN"
    assert f["beta"] is None


def test_campos_completos(monkeypatch):
    proveedor(monkeypatch,[quote(),{"Symbol":"AAPL","Name":"Apple","Sector":"Technology",
        "Currency":"USD","Beta":"1.2","PERatio":"30", "52WeekHigh":"250",
        "52WeekLow":"180","MarketCapitalization":"1000000","LatestQuarter":"2026-06-30"}])
    f=datos.obtener_ficha("AAPL","ficticia")
    assert f["estado_datos"]=="COMPLETOS" and f["cap_mercado_usd"]==1000000
    assert f["periodo_fundamentales"]=="2026-06-30"


@pytest.mark.parametrize("fecha,codigo", [("2024-10-18","ANTIGUO"),("no fecha","FECHA"),
    ((datetime.now(timezone.utc).date()+timedelta(days=1)).isoformat(),"FECHA")])
def test_no_presenta_datos_viejos_como_actuales(monkeypatch,fecha,codigo):
    llamadas=proveedor(monkeypatch,[quote(fecha)])
    f=datos.obtener_ficha("AAPL","ficticia")
    assert f["estado_datos"]=="NO_DISPONIBLES" and f["precio"] is None
    assert f["consultas"][0]["estado"]==codigo
    assert len(llamadas)==1  # sin gastar otra consulta ni llamar a IA


def test_fin_semana_admite_ultimo_cierre():
    f=datos.validar_cotizacion(quote("2026-10-16"),"AAPL",hoy=date(2026,10,18))
    assert f["antiguedad_dias"]==2


@pytest.mark.parametrize("payload,codigo", [({"Note":"25 requests per day"},"CUOTA"),
    ({"Information":"premium subscription"},"PLAN"),({"Error Message":"Invalid API key"},"CLAVE"),
    ({"Global Quote":{}},"VACIO")])
def test_errores_del_proveedor_en_http200(monkeypatch,payload,codigo):
    proveedor(monkeypatch,[payload])
    f=datos.obtener_ficha("AAPL","ficticia")
    assert f["consultas"][0]["estado"]==codigo


def test_clave_demo_no_sale_a_red(monkeypatch):
    monkeypatch.setattr(datos.requests,"get",lambda *a,**kw:pytest.fail("Sin red"))
    assert datos.obtener_ficha("AAPL","demo")["consultas"][0]["estado"]=="DEMO"


def test_error_http_no_revela_clave(monkeypatch):
    def get(*a,**kw):raise requests.ConnectionError("URL privada con clave-ficticia")
    monkeypatch.setattr(datos.requests,"get",get)
    assert "clave-ficticia" not in str(datos.obtener_ficha("AAPL","clave-ficticia"))


@pytest.mark.parametrize("extra,codigo", [({"01. symbol":"IBM"},"TICKER"),
    ({"05. price":"NaN"},"PRECIO"),({"05. price":"-1"},"PRECIO")])
def test_rechaza_ticker_y_precios_invalidos(extra,codigo):
    with pytest.raises(datos.ErrorDatos) as e:datos.validar_cotizacion(quote(**extra),"AAPL")
    assert e.value.codigo==codigo


def test_sin_datos_no_llama_openai_ni_inventa_precios(monkeypatch):
    monkeypatch.setattr(config,"MODO_SIMULACION",False)
    monkeypatch.setattr(config,"ALPHAVANTAGE_API_KEY","ficticia")
    monkeypatch.setattr(agentes,"llamar_openai",lambda *a,**kw:pytest.fail("Sin IA"))
    proveedor(monkeypatch,[quote("2024-10-18")])
    f,_=agentes.agente_recolector("AAPL")
    analisis=agentes.agente_analista(f)
    nota=agentes.agente_comunicador(analisis)
    assert "SIN DATOS VERIFICABLES" in nota and "235" not in nota and "150" not in nota


def test_fallo_openai_conserva_cifras_verificadas(monkeypatch):
    monkeypatch.setattr(config,"MODO_SIMULACION",False)
    monkeypatch.setattr(config,"ALPHAVANTAGE_API_KEY","ficticia")
    def falla(*a,**kw):raise RuntimeError("API no disponible")
    monkeypatch.setattr(agentes,"llamar_openai",falla)
    proveedor(monkeypatch,[quote(),{"Information":"premium"}])
    f,_=agentes.agente_recolector("AAPL")
    nota=agentes.agente_comunicador(agentes.agente_analista(f))
    assert "220.5" in nota and "DATOS PARCIALES" in nota
