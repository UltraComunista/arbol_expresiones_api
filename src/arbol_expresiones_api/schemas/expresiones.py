# schemas/expresiones.py
# Esquemas Pydantic: validacion de entrada y salida de la API
# ============================================================
# Aqui se definen QUE datos recibe y devuelve la API, con sus
# reglas de validacion. FastAPI los usa automaticamente.

import re

from pydantic import BaseModel, Field, field_validator


# Caracteres permitidos en la expresion: digitos, punto decimal,
# operadores, parentesis y espacios.
PATRON_EXPRESION = re.compile(r"^[0-9+\-*/().\s]+$")


class ExpresionEntrada(BaseModel):
    """Datos que recibe la API: la expresion infija como texto."""

    expresion: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Expresion infija, ej: '3 + 4 * 2' o '(3+4)*2'",
        examples=["3 + 4 * 2"],
    )

    @field_validator("expresion")
    @classmethod
    def validar_caracteres(cls, valor: str) -> str:
        """
        Rechaza la expresion si contiene caracteres no permitidos
        (letras, simbolos raros, etc.).
        """
        if not PATRON_EXPRESION.match(valor):
            raise ValueError(
                "La expresion solo puede contener numeros, "
                "operadores (+ - * /), parentesis y espacios")
        return valor.strip()


class ExpresionSalida(BaseModel):
    """Datos que devuelve la API."""

    infija: str = Field(description="Expresion en notacion infija")
    prefija: str = Field(description="Expresion en notacion prefija")
    posfija: str = Field(description="Expresion en notacion posfija")
    arbol: dict = Field(description="Estructura del arbol (JSON anidado)")


class ErrorSalida(BaseModel):
    """Formato de error de la API."""

    detail: str = Field(description="Descripcion del error")
