"""
Production routes for the API.
"""

from flask import Flask, jsonify, request
from scraper import VitiBrasilScraper

def register_production_routes(app: Flask):
    """Register production routes."""
    
    # Initialize the scraper
    scraper = VitiBrasilScraper()
    
    @app.route('/api/production', methods=['GET'])
    def get_production():
        """
        Get wine production data.
        
        Query Parameters:
            year (optional): The year to get data for.
        """
        year = request.args.get('year')
        
        try:
            if year:
                year = int(year)
            data = scraper.get_production_data(year=year)
            return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500 