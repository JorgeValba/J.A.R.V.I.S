"""Fuente gratuita y reglas técnicas para Jorge Valencia. Datos ficticios, sin red."""
from datetime import date, timedelta, datetime, timezone
from types import SimpleNamespace
import pytest
import requests
from mesa import datos, agentes, config


def fechas(n=100,fin=None):
    fin=fin or datetime.now(timezone.utc).date()
    salida=[]
    while len(salida)<n:
        if fin.weekday()<5:salida.append(fin.isoformat())
        fin-=timedelta(days=1)
    return list(reversed(salida))


def serie(precios=None,fin=None):
    precios=precios or [100+i for i in range(100)]
    return {"Meta Data":{"2. Symbol":"AAPL"},"Time Series (Daily)":{
        fecha:{"4. close":str(precio),"5. volume":"1000"}
        for fecha,precio in zip(fechas(len(precios),fin),precios)}}


def proveedor(monkeypatch,payload):
    llamadas=[]
    def get(url,params,**kw):
        llamadas.append(params.copy())
        return SimpleNamespace(status_code=200,raise_for_status=lambda:None,json=lambda:payload)
    monkeypatch.setattr(datos.requests,"get",get)
    return llamadas


def ficha(precios=None):
    return {"ticker":"AAPL",**datos.validar_serie(serie(precios),"AAPL"),
        "estado_datos":"COMPLETOS","fuente":"Alpha Vantage API gratuita","advertencias":[]}


def test_una_consulta_compact_sin_premium(monkeypatch):
    llamadas=proveedor(monkeypatch,serie())
    f=datos.obtener_ficha("AAPL","ficticia")
    assert llamadas==[{"function":"TIME_SERIES_DAILY","symbol":"AAPL","apikey":"ficticia","outputsize":"compact"}]
    assert f["estado_datos"]=="COMPLETOS" and len(f["sesiones"])==100
    assert not {"beta","pe_ratio","sector","cap_mercado_usd","max_52s","min_52s"}&set(f)


def test_medias_y_rendimiento_calculados():
    ind=agentes.calcular_indicadores(ficha())
    assert ind["sma20"]==189.5 and ind["sma50"]==174.5
    assert ind["rendimiento20_pct"]==round((199/179-1)*100,4)
    assert ind["caida_max_cierre20_pct"]==0
    assert ind["decision_tecnica"]=="EVALUAR_ENTRADA"


@pytest.mark.parametrize("precios,decision",[
    ([200-i*.2 for i in range(100)],"ESPERAR"),
    ([100]*100,"OBSERVAR"),
    ([100*(1.04 if i%2 else 1) for i in range(100)],"CAUTELA"),
    ([100+i for i in range(49)],"INFORMACION_INSUFICIENTE")])
def test_decisiones_didacticas(precios,decision):
    assert agentes.calcular_indicadores(ficha(precios))["decision_tecnica"]==decision


def test_salto_sin_ajustar_impide_concluir():
    ind=agentes.calcular_indicadores(ficha([100]*99+[50]))
    assert ind["decision_tecnica"]=="INFORMACION_INSUFICIENTE" and ind["alertas"]


def test_caida_reciente_activa_cautela():
    ind=agentes.calcular_indicadores(ficha([100]*99+[89]))
    assert ind["decision_tecnica"]=="CAUTELA" and ind["caida_max_cierre20_pct"]==-11


def test_fechas_invertidas_impiden_decidir():
    f=ficha();f["sesiones"]=list(reversed(f["sesiones"]))
    assert agentes.calcular_indicadores(f)["decision_tecnica"]=="INFORMACION_INSUFICIENTE"


@pytest.mark.parametrize("fin,codigo",[(date(2024,10,18),"ANTIGUO"),
    (datetime.now(timezone.utc).date()+timedelta(days=4),"FECHA")])
def test_no_presenta_fecha_vieja_o_futura(monkeypatch,fin,codigo):
    proveedor(monkeypatch,serie(fin=fin))
    f=datos.obtener_ficha("AAPL","ficticia")
    assert f["estado_datos"]=="NO_DISPONIBLES" and f["precio"] is None
    assert f["consultas"][0]["estado"]==codigo


def test_domingo_acepta_cierre_viernes():
    f=datos.validar_serie(serie(fin=date(2026,10,16)),"AAPL",hoy=date(2026,10,18))
    assert f["antiguedad_dias"]==2


@pytest.mark.parametrize("valor",[True,"NaN","Infinity","-1","0"])
def test_rechaza_precio_invalido(valor):
    d=serie();next(iter(d["Time Series (Daily)"].values()))["4. close"]=valor
    with pytest.raises(datos.ErrorDatos,match="precio"):datos.validar_serie(d,"AAPL")


def test_ticker_debe_coincidir():
    with pytest.raises(datos.ErrorDatos) as e:datos.validar_serie(serie(),"IBM")
    assert e.value.codigo=="TICKER"


@pytest.mark.parametrize("mensaje,codigo",[("25 requests per day","CUOTA"),
    ("premium subscription","PLAN"),("25 requests per day. Subscribe to premium","RESTRICCION"),
    ("Invalid API key","CLAVE")])
def test_aviso_http200_y_diagnostico_sin_inventar(monkeypatch,mensaje,codigo):
    proveedor(monkeypatch,{"Information":mensaje})
    assert datos.obtener_ficha("AAPL","ficticia")["consultas"][0]["estado"]==codigo


def test_bloquea_funciones_no_gratuitas_sin_red(monkeypatch):
    monkeypatch.setattr(datos.requests,"get",lambda *a,**kw:pytest.fail("Sin red"))
    with pytest.raises(ValueError):datos.consultar("OVERVIEW","AAPL","ficticia")
    assert datos.obtener_ficha("AAPL","demo")["consultas"][0]["estado"]=="DEMO"


def test_error_sin_credenciales(monkeypatch):
    def get(*a,**kw):raise requests.ConnectionError("URL clave-ficticia")
    monkeypatch.setattr(datos.requests,"get",get)
    assert "clave-ficticia" not in str(datos.obtener_ficha("AAPL","clave-ficticia"))


def test_fallo_fuente_no_inventa_ni_llama_openai(monkeypatch):
    monkeypatch.setattr(config,"MODO_SIMULACION",False)
    monkeypatch.setattr(config,"ALPHAVANTAGE_API_KEY","ficticia")
    monkeypatch.setattr(agentes,"llamar_openai",lambda *a,**kw:pytest.fail("Sin IA"))
    proveedor(monkeypatch,{"Note":"25 requests per day"})
    f,_=agentes.agente_recolector("AAPL")
    nota=agentes.agente_comunicador(agentes.agente_analista(f))
    assert "SIN DATOS VERIFICABLES" in nota and "150" not in nota


def test_fallo_openai_conserva_decision_y_cifras(monkeypatch):
    monkeypatch.setattr(config,"MODO_SIMULACION",False)
    def falla(*a,**kw):raise RuntimeError("Sin API")
    monkeypatch.setattr(agentes,"llamar_openai",falla)
    analisis=agentes.agente_analista(ficha());nota=agentes.agente_comunicador(analisis)
    assert "EVALUAR_ENTRADA" in nota and "199.0" in nota


def test_la_decision_no_la_reescribe_la_ia(monkeypatch):
    monkeypatch.setattr(config,"MODO_SIMULACION",False)
    monkeypatch.setattr(agentes,"llamar_openai",lambda *a,**kw:("lectura sin señal",[]))
    analisis=agentes.agente_analista(ficha());nota=agentes.agente_comunicador(analisis)
    assert "Conclusión técnica: EVALUAR_ENTRADA" in nota
