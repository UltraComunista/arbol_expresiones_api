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

Arquitectura por capas (estilo MVC adaptado a FastAPI):

```
├── main.py                                    # Arranque de la app
└── src/arbol_expresiones_api/
    ├── models/
    │   └── arbol.py                           # Modelo: arbol de expresiones
    ├── schemas/
    │   └── expresiones.py                     # Validaciones (Pydantic)
    ├── controllers/
    │   └── expresiones_controller.py          # Rutas HTTP (endpoints)
    └── services/
        └── expresiones_service.py             # Logica de negocio
```

Las validaciones se hacen en dos niveles: **Pydantic** rechaza
caracteres no permitidos y entradas vacías (422), y el **servicio**
rechaza expresiones mal formadas como `(3+4` (400).
