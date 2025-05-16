"""
Processing routes for the API.
"""

from flask import Flask, jsonify, request
from scraper import VitiBrasilScraper

def register_processing_routes(app: Flask):
    """Register processing routes."""
    
    # Initialize the scraper
    scraper = VitiBrasilScraper()
    
    @app.route('/api/processing', methods=['GET'])
    def get_processing():
        """
        Get grape processing data for all categories.
        
        Query Parameters:
            year (optional): The year to get data for.
        """
        year = request.args.get('year')
        
        try:
            if year:
                year = int(year)
            data = scraper.get_all_processing_data(year=year)
            return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/processing/<category>', methods=['GET'])
    def get_processing_by_category(category):
        """
        Get grape processing data for a specific category.
        
        Path Parameters:
            category: The grape category (viniferas, americanas, mesa, sem_classificacao)
            
        Query Parameters:
            year (optional): The year to get data for.
        """
        year = request.args.get('year')
        
        try:
            if year:
                year = int(year)
            data = scraper.get_processing_data(category=category, year=year)
            return jsonify(data)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500 