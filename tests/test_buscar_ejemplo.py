"""Límites de la búsqueda solicitada por Jorge Valencia, sin red."""
from buscar_ejemplo import buscar
from mesa.datos import CAMPOS


def test_detiene_en_primer_completo():
    llamadas=[]
    def consulta(ticker, clave):
        llamadas.append(ticker)
        return {**dict.fromkeys(CAMPOS,1),"moneda":"USD","estado_datos":"COMPLETOS"}
    assert buscar("ficticia",consulta)["encontrado"]=="IBM"
    assert llamadas==["IBM"]


def test_cuota_no_gasta_los_seis():
    llamadas=[]
    def consulta(ticker, clave):
        llamadas.append(ticker)
        return {"consultas":[{"estado":"CUOTA"}],"estado_datos":"NO_DISPONIBLES"}
    assert buscar("ficticia",consulta)["encontrado"] is None
    assert llamadas==["IBM"]


def test_nunca_mas_de_seis_y_no_acepta_capitalizacion_ausente():
    llamadas=[]
    def consulta(ticker, clave):
        llamadas.append(ticker)
        return {**dict.fromkeys(CAMPOS,1),"cap_mercado_usd":None,
                "moneda":"USD","estado_datos":"COMPLETOS","consultas":[]}
    r=buscar("ficticia",consulta)
    assert len(llamadas)==6 and r["encontrado"] is None
