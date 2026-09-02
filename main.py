# main.py
# Proyecto: API REST - Arbol de Expresiones
# ==========================================
# Autor: Rodrigo Echeverria Estrada
# Materia: INF-310 Estructuras de Datos II
#
# Punto de entrada de la API. Solo crea la aplicacion FastAPI
# y registra los controladores (routers).
#
# Arquitectura por capas:
#   main.py                    -> arranque de la app
#   controllers/               -> rutas HTTP (endpoints)
#   services/                  -> logica de negocio
#   arbol.py                   -> modelo (arbol de expresiones)
#   schemas.py                 -> validacion de entrada/salida
#
# Ejecutar con:
#   uv run fastapi dev main.py
#
# Documentacion automatica:
#   http://127.0.0.1:8000/docs

from fastapi import FastAPI

from arbol_expresiones_api.controllers.expresiones_controller import (
    router as expresiones_router,
)

app = FastAPI(
    title="API Arbol de Expresiones",
    description="Convierte expresiones infijas a posfijas "
                "usando un arbol binario de expresiones.",
    version="1.0.0",
)

app.include_router(expresiones_router)
