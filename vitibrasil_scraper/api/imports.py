"""
Import routes for the API.
"""

from flask import Flask, jsonify, request
from scraper import VitiBrasilScraper

def register_import_routes(app: Flask):
    """Register import routes."""
    
    # Initialize the scraper
    scraper = VitiBrasilScraper()
    
    @app.route('/api/import', methods=['GET'])
    def get_import():
        """
        Get import data for all grape product categories.
        
        Query Parameters:
            year (optional): The year to get data for.
        """
        year = request.args.get('year')
        
        try:
            if year:
                year = int(year)
            data = scraper.get_all_import_data(year=year)
            return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/import/<category>', methods=['GET'])
    def get_import_by_category(category):
        """
        Get import data for a specific grape product category.
        
        Path Parameters:
            category: A categoria de importação (em português):
                     - vinhos_mesa (Vinhos de Mesa)
                     - espumantes (Espumantes)
                     - uvas_frescas (Uvas Frescas)
                     - uvas_passas (Uvas Passas)
                     - suco_uva (Suco de Uva)
            
        Query Parameters:
            year (optional): The year to get data for.
        """
        year = request.args.get('year')
        
        try:
            if year:
                year = int(year)
            data = scraper.get_import_data(category=category, year=year)
            return jsonify(data)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500 