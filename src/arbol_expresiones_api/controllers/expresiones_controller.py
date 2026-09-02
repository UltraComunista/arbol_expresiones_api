# controllers/expresiones_controller.py
# Capa de controladores: rutas (endpoints) de la API
# ===================================================
# Los controladores solo reciben la peticion HTTP, llaman al
# servicio y devuelven la respuesta. Nada de logica aqui.

from fastapi import APIRouter, HTTPException, status

from arbol_expresiones_api.schemas.expresiones import (
    ErrorSalida,
    ExpresionEntrada,
    ExpresionSalida,
)
from arbol_expresiones_api.services.expresiones_service import (
    ExpresionInvalidaError,
    convertir_infija_a_posfija,
)

router = APIRouter(tags=["Expresiones"])


@router.get("/")
def inicio():
    """Endpoint raiz: mensaje de bienvenida."""
    return {
        "mensaje": "API Arbol de Expresiones - INF310",
        "uso": "POST /convertir con JSON {'expresion': '3 + 4 * 2'}",
        "docs": "/docs",
    }


@router.post(
    "/convertir",
    response_model=ExpresionSalida,
    responses={
        400: {"model": ErrorSalida, "description": "Expresion invalida"},
        422: {"description": "Datos de entrada invalidos"},
    },
)
def convertir(entrada: ExpresionEntrada):
    """
    Convierte una expresion infija a posfija.

    Recibe:   {"expresion": "3 + 4 * 2"}
    Devuelve: infija, prefija, posfija y la estructura del arbol.
    """
    try:
        return convertir_infija_a_posfija(entrada.expresion)
    except ExpresionInvalidaError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error
