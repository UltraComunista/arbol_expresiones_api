# services/expresiones_service.py
# Capa de servicio: logica de negocio
# ====================================
# Aqui vive la logica que usa el modelo (arbol de expresiones).
# Los controladores NO hablan directo con el modelo: pasan por
# esta capa.

from arbol_expresiones_api.arbol import ArbolExpresion
from arbol_expresiones_api.schemas import ExpresionSalida


class ExpresionInvalidaError(Exception):
    """Error de negocio: la expresion infija no es valida."""


def convertir_infija_a_posfija(expresion: str) -> ExpresionSalida:
    """
    Construye el arbol de expresion desde la cadena infija y
    devuelve las tres notaciones y la estructura del arbol.

    Args:
        expresion: Cadena infija ya validada por el esquema.

    Returns:
        ExpresionSalida con infija, prefija, posfija y arbol.

    Raises:
        ExpresionInvalidaError: Si la expresion esta mal formada
            (parentesis sin cerrar, operadores sin operandos, etc.).
    """
    arbol = ArbolExpresion()

    try:
        arbol.construir_desde_infija(expresion)
    except ValueError as error:
        raise ExpresionInvalidaError(str(error)) from error

    return ExpresionSalida(
        infija=" ".join(str(d) for d in arbol.InOrden()),
        prefija=" ".join(str(d) for d in arbol.PreOrden()),
        posfija=arbol.a_posfija(),
        arbol=arbol.a_diccionario(),
    )
