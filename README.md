# Árbol de Expresiones API

**Autor:** Rodrigo Echeverria Estrada
**Materia:** INF-310 Estructuras de Datos II · Unidad 1

API REST con **FastAPI** que convierte expresiones aritméticas
**infijas → posfijas** usando un árbol binario de expresiones.
Sin base de datos.

## Requisitos

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)

## Ejecutar

```bash
uv sync
uv run fastapi dev main.py
```

Documentación automática: http://127.0.0.1:8000/docs

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Mensaje de bienvenida |
| POST | `/convertir` | Convierte infija → posfija |

## Ejemplo

```bash
curl -X POST http://127.0.0.1:8000/convertir \
     -H "Content-Type: application/json" \
     -d '{"expresion": "3 + 4 * 2"}'
```

Respuesta:

```json
{
  "infija": "3 + 4 * 2",
  "prefija": "+ 3 * 4 2",
  "posfija": "3 4 2 * +",
  "arbol": { "dato": "+", "es_hoja": false, "izquierdo": {}, "derecho": {} }
}
```

Se admiten `+ - * /`, paréntesis y números decimales.

## Estructura

```
├── main.py                          # API FastAPI (endpoints)
└── src/arbol_expresiones_api/
    └── arbol.py                     # Lógica del árbol de expresiones
```
