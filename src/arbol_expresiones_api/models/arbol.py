# models/arbol.py
# Proyecto: API REST - Arbol de Expresiones
# ==========================================
# Autor: Rodrigo Echeverria Estrada
# Materia: INF-310 Estructuras de Datos II
#
# Logica del arbol de expresiones (sin entrada por consola):
# recibe una expresion infija como cadena, construye el arbol
# y permite obtener la notacion posfija y la estructura del
# arbol como diccionario (para enviarla como JSON).

from typing import Optional, List, Union, Dict, Any


OPERADORES = "+-*/"


class NodoExpresion:
    """
    Nodo del arbol de expresiones.

    Un nodo puede ser:
        - Operador: tiene hijo izquierdo y derecho.
        - Operando (numero): es una hoja del arbol.
    """

    def __init__(self, dato: Union[str, int, float]):
        """Inicializa el nodo con el operador u operando dado."""
        self._dato = dato
        self._izquierdo = None
        self._derecho = None

    @property
    def dato(self) -> Union[str, int, float]:
        """Retorna el dato almacenado en el nodo."""
        return self._dato

    @dato.setter
    def dato(self, valor: Union[str, int, float]) -> None:
        """Asigna un nuevo dato al nodo."""
        self._dato = valor

    @property
    def izquierdo(self) -> Optional['NodoExpresion']:
        """Retorna el hijo izquierdo del nodo."""
        return self._izquierdo

    @izquierdo.setter
    def izquierdo(self, nodo: Optional['NodoExpresion']) -> None:
        """Asigna el hijo izquierdo del nodo."""
        self._izquierdo = nodo

    @property
    def derecho(self) -> Optional['NodoExpresion']:
        """Retorna el hijo derecho del nodo."""
        return self._derecho

    @derecho.setter
    def derecho(self, nodo: Optional['NodoExpresion']) -> None:
        """Asigna el hijo derecho del nodo."""
        self._derecho = nodo

    def EsHoja(self) -> bool:
        """Retorna True si el nodo es un operando (hoja)."""
        return self._izquierdo is None and self._derecho is None

    def a_diccionario(self) -> Dict[str, Any]:
        """
        Convierte el nodo y sus hijos a un diccionario anidado,
        listo para enviarse como JSON en la API.
        """
        return {
            "dato": self._dato,
            "es_hoja": self.EsHoja(),
            "izquierdo": (self._izquierdo.a_diccionario()
                          if self._izquierdo else None),
            "derecho": (self._derecho.a_diccionario()
                        if self._derecho else None),
        }

    def __repr__(self) -> str:
        """Representacion legible del nodo."""
        return f"NodoExpresion({self._dato})"


class ArbolExpresion:
    """
    Arbol binario que representa una expresion aritmetica.

    Respeta la precedencia de operadores: primero '*' y '/',
    luego '+' y '-'. Se admiten parentesis.

    Ejemplo:
        "3 + 4 * 2" ->      +
                           / \\
                          3   *
                             / \\
                            4   2

        Posfija: 3 4 2 * +
    """

    def __init__(self):
        """Inicializa un arbol de expresion vacio."""
        self._raiz = None

    @property
    def raiz(self) -> Optional[NodoExpresion]:
        """Retorna el nodo raiz del arbol."""
        return self._raiz

    def EsVacio(self) -> bool:
        """Retorna True si el arbol no tiene nodos."""
        return self._raiz is None

    # --------------------------------------------------------------
    # Construccion del arbol desde una expresion infija
    # --------------------------------------------------------------

    def construir_desde_infija(self, expresion: str) -> None:
        """
        Construye el arbol a partir de una cadena infija
        (ej: "3 + 4 * 2" o "(3+4)*2").

        Raises:
            ValueError: Si la expresion es invalida.
        """
        tokens = self._tokenizar(expresion)
        self._pos = 0
        self._raiz = self._parsear_expresion(tokens)
        if self._pos != len(tokens):
            raise ValueError(
                f"Expresion invalida cerca de: '{tokens[self._pos]}'")

    def _tokenizar(self, expresion: str) -> List[str]:
        """Divide la expresion en tokens (numeros, operadores, ( ))."""
        tokens = []
        i = 0
        while i < len(expresion):
            caracter = expresion[i]
            if caracter == " ":
                i += 1
            elif caracter in OPERADORES or caracter in "()":
                tokens.append(caracter)
                i += 1
            elif caracter.isdigit() or caracter == ".":
                numero = ""
                while i < len(expresion) and (expresion[i].isdigit()
                                              or expresion[i] == "."):
                    numero += expresion[i]
                    i += 1
                tokens.append(numero)
            else:
                raise ValueError(f"Caracter no valido: '{caracter}'")

        if not tokens:
            raise ValueError("La expresion esta vacia")
        return tokens

    def _parsear_expresion(self, tokens: List[str]) -> NodoExpresion:
        """Parsea sumas y restas (menor precedencia)."""
        nodo = self._parsear_termino(tokens)
        while (self._pos < len(tokens)
               and tokens[self._pos] in ("+", "-")):
            operador = tokens[self._pos]
            self._pos += 1
            padre = NodoExpresion(operador)
            padre.izquierdo = nodo
            padre.derecho = self._parsear_termino(tokens)
            nodo = padre
        return nodo

    def _parsear_termino(self, tokens: List[str]) -> NodoExpresion:
        """Parsea multiplicaciones y divisiones (mayor precedencia)."""
        nodo = self._parsear_factor(tokens)
        while (self._pos < len(tokens)
               and tokens[self._pos] in ("*", "/")):
            operador = tokens[self._pos]
            self._pos += 1
            padre = NodoExpresion(operador)
            padre.izquierdo = nodo
            padre.derecho = self._parsear_factor(tokens)
            nodo = padre
        return nodo

    def _parsear_factor(self, tokens: List[str]) -> NodoExpresion:
        """Parsea un numero o una subexpresion entre parentesis."""
        if self._pos >= len(tokens):
            raise ValueError("Expresion incompleta")

        token = tokens[self._pos]

        if token == "(":
            self._pos += 1
            nodo = self._parsear_expresion(tokens)
            if (self._pos >= len(tokens)
                    or tokens[self._pos] != ")"):
                raise ValueError("Falta cerrar un parentesis")
            self._pos += 1
            return nodo

        if token in OPERADORES or token == ")":
            raise ValueError(
                f"Se esperaba un numero y se encontro: '{token}'")

        self._pos += 1
        return NodoExpresion(self._a_numero(token))

    @staticmethod
    def _a_numero(token: str) -> Union[int, float]:
        """Convierte un token a int o float."""
        try:
            return int(token)
        except ValueError:
            try:
                return float(token)
            except ValueError:
                raise ValueError(f"Numero invalido: '{token}'")

    # --------------------------------------------------------------
    # Recorridos
    # --------------------------------------------------------------

    def InOrden(self) -> List:
        """Recorrido in-orden: reproduce la expresion infija."""
        resultado = []
        self._in_orden_rec(self._raiz, resultado)
        return resultado

    def _in_orden_rec(self, nodo: Optional[NodoExpresion],
                      resultado: List) -> None:
        if nodo:
            self._in_orden_rec(nodo.izquierdo, resultado)
            resultado.append(nodo.dato)
            self._in_orden_rec(nodo.derecho, resultado)

    def PostOrden(self) -> List:
        """Recorrido post-orden: produce la notacion posfija."""
        resultado = []
        self._post_orden_rec(self._raiz, resultado)
        return resultado

    def _post_orden_rec(self, nodo: Optional[NodoExpresion],
                        resultado: List) -> None:
        if nodo:
            self._post_orden_rec(nodo.izquierdo, resultado)
            self._post_orden_rec(nodo.derecho, resultado)
            resultado.append(nodo.dato)

    def PreOrden(self) -> List:
        """Recorrido pre-orden: produce la notacion prefija."""
        resultado = []
        self._pre_orden_rec(self._raiz, resultado)
        return resultado

    def _pre_orden_rec(self, nodo: Optional[NodoExpresion],
                       resultado: List) -> None:
        if nodo:
            resultado.append(nodo.dato)
            self._pre_orden_rec(nodo.izquierdo, resultado)
            self._pre_orden_rec(nodo.derecho, resultado)

    # --------------------------------------------------------------
    # Conversion y estructura para la API
    # --------------------------------------------------------------

    def a_posfija(self) -> str:
        """Retorna la expresion en notacion posfija."""
        if self.EsVacio():
            return ""
        return " ".join(str(dato) for dato in self.PostOrden())

    def a_diccionario(self) -> Optional[Dict[str, Any]]:
        """Retorna el arbol completo como diccionario anidado."""
        if self.EsVacio():
            return None
        return self._raiz.a_diccionario()
