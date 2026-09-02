# main.py
# Proyecto: API REST - Arbol de Expresiones
# ==========================================
# Autor: Rodrigo Echeverria Estrada
# Materia: INF-310 Estructuras de Datos II
#
# API REST con FastAPI que convierte expresiones infijas
# a posfijas usando un arbol de expresiones (sin base de datos).
#
# Ejecutar con:
#   uv run fastapi dev main.py
#
# Documentacion automatica:
#   http://127.0.0.1:8000/docs

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from arbol_expresiones_api.arbol import ArbolExpresion


app = FastAPI(
    title="API Arbol de Expresiones",
    description="Convierte expresiones infijas a posfijas "
                "usando un arbol binario de expresiones.",
    version="1.0.0",
)


class ExpresionEntrada(BaseModel):
    """Datos que recibe la API: la expresion infija como texto."""

    expresion: str = Field(
        ...,
        description="Expresion infija, ej: '3 + 4 * 2' o '(3+4)*2'",
        examples=["3 + 4 * 2"],
    )


class ExpresionSalida(BaseModel):
    """Datos que devuelve la API."""

    infija: str
    prefija: str
    posfija: str
    arbol: dict


@app.get("/")
def inicio():
    """Endpoint raiz: mensaje de bienvenida."""
    return {
        "mensaje": "API Arbol de Expresiones - INF310",
        "uso": "POST /convertir con JSON {'expresion': '3 + 4 * 2'}",
        "docs": "/docs",
    }


@app.post("/convertir", response_model=ExpresionSalida)
def convertir(entrada: ExpresionEntrada):
    """
    Convierte una expresion infija a posfija.

    Recibe:  {"expresion": "3 + 4 * 2"}
    Devuelve: infija, prefija, posfija y la estructura del arbol.
    """
    arbol = ArbolExpresion()

    try:
        arbol.construir_desde_infija(entrada.expresion)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return ExpresionSalida(
        infija=" ".join(str(d) for d in arbol.InOrden()),
        prefija=" ".join(str(d) for d in arbol.PreOrden()),
        posfija=arbol.a_posfija(),
        arbol=arbol.a_diccionario(),
    )
