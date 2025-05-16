"""
Commercialization routes for the API.
"""

from flask import Flask, jsonify, request
from scraper import VitiBrasilScraper

def register_commercialization_routes(app: Flask):
    """Register commercialization routes."""
    
    # Initialize the scraper
    scraper = VitiBrasilScraper()
    
    @app.route('/api/commercialization', methods=['GET'])
    def get_commercialization():
        """
        Get commercialization data for wine and derivatives.
        
        Query Parameters:
            year (optional): The year to get data for.
        """
        year = request.args.get('year')
        
        try:
            if year:
                year = int(year)
            data = scraper.get_commercialization_data(year=year)
            return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500 