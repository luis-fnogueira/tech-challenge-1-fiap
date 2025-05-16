"""
Rota de índice para a API.
"""

from flask import Flask, jsonify

def register_index_route(app: Flask):
    """Registra a rota de índice."""
    
    @app.route('/')
    def index():
        """Retorna informações da API."""
        return jsonify({
            "name": "API VitiBrasil",
            "version": "0.1.0",
            "endpoints": [
                {
                    "path": "/api/production",
                    "methods": ["GET"],
                    "description": "Obter dados de produção de vinho",
                    "parameters": [
                        {"name": "year", "type": "integer", "required": False, "description": "Ano para obter os dados"}
                    ]
                },
                {
                    "path": "/api/processing",
                    "methods": ["GET"],
                    "description": "Obter dados de processamento de uvas para todas as categorias",
                    "parameters": [
                        {"name": "year", "type": "integer", "required": False, "description": "Ano para obter os dados"}
                    ]
                },
                {
                    "path": "/api/processing/<category>",
                    "methods": ["GET"],
                    "description": "Obter dados de processamento de uvas para uma categoria específica",
                    "parameters": [
                        {"name": "category", "type": "string", "required": True, "description": "Categoria de uva (viniferas, americanas, mesa, sem_classificacao)"},
                        {"name": "year", "type": "integer", "required": False, "description": "Ano para obter os dados"}
                    ]
                },
                {
                    "path": "/api/commercialization",
                    "methods": ["GET"],
                    "description": "Obter dados de comercialização para vinhos e derivados",
                    "parameters": [
                        {"name": "year", "type": "integer", "required": False, "description": "Ano para obter os dados"}
                    ]
                },
                {
                    "path": "/api/import",
                    "methods": ["GET"],
                    "description": "Obter dados de importação para todas as categorias de produtos vitivinícolas",
                    "parameters": [
                        {"name": "year", "type": "integer", "required": False, "description": "Ano para obter os dados"}
                    ]
                },
                {
                    "path": "/api/import/<category>",
                    "methods": ["GET"],
                    "description": "Obter dados de importação para uma categoria específica de produtos vitivinícolas",
                    "parameters": [
                        {"name": "category", "type": "string", "required": True, "description": "Categoria de importação (table_wines, sparkling_wines, fresh_grapes, raisins, grape_juice)"},
                        {"name": "year", "type": "integer", "required": False, "description": "Ano para obter os dados"}
                    ]
                },
                {
                    "path": "/api/export",
                    "methods": ["GET"],
                    "description": "Obter dados de exportação para todas as categorias de produtos vitivinícolas",
                    "parameters": [
                        {"name": "year", "type": "integer", "required": False, "description": "Ano para obter os dados"}
                    ]
                },
                {
                    "path": "/api/export/<category>",
                    "methods": ["GET"],
                    "description": "Obter dados de exportação para uma categoria específica de produtos vitivinícolas",
                    "parameters": [
                        {"name": "category", "type": "string", "required": True, "description": "Categoria de exportação (table_wines, sparkling_wines, fresh_grapes, grape_juice)"},
                        {"name": "year", "type": "integer", "required": False, "description": "Ano para obter os dados"}
                    ]
                }
            ]
        }) 