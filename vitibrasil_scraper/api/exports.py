"""
Export routes for the API.
"""

from flask import Flask, jsonify, request
from scraper import VitiBrasilScraper

def register_export_routes(app: Flask):
    """Register export routes."""
    
    # Initialize the scraper
    scraper = VitiBrasilScraper()
    
    @app.route('/api/export', methods=['GET'])
    def get_export():
        """
        Get export data for all grape product categories.
        
        Query Parameters:
            year (optional): The year to get data for.
        """
        year = request.args.get('year')
        
        try:
            if year:
                year = int(year)
            data = scraper.get_all_export_data(year=year)
            return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/export/<category>', methods=['GET'])
    def get_export_by_category(category):
        """
        Get export data for a specific grape product category.
        
        Path Parameters:
            category: A categoria de exportação (em português):
                     - vinhos_mesa (Vinhos de Mesa)
                     - espumantes (Espumantes)
                     - uvas_frescas (Uvas Frescas)
                     - suco_uva (Suco de Uva)
            
        Query Parameters:
            year (optional): The year to get data for.
        """
        year = request.args.get('year')
        
        try:
            if year:
                year = int(year)
            data = scraper.get_export_data(category=category, year=year)
            return jsonify(data)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500 