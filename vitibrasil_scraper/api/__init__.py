"""
API Flask para dados do VitiBrasil.
"""

from flask import Flask

from .production import register_production_routes
from .processing import register_processing_routes
from .commercialization import register_commercialization_routes
from .imports import register_import_routes
from .exports import register_export_routes
from .index import register_index_route

def create_app():
    """Cria e configura a aplicação Flask."""
    app = Flask(__name__)
    
    # Registra todas as rotas
    register_production_routes(app)
    register_processing_routes(app)
    register_commercialization_routes(app)
    register_import_routes(app)
    register_export_routes(app)
    register_index_route(app)
    
    return app 