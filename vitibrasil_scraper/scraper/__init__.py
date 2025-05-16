"""
Módulo de scraper para o site Vitibrasil.
"""

from .base import BaseScraper
from .production import ProductionScraper
from .processing import ProcessingScraper
from .commercialization import CommercializationScraper
from .imports import ImportScraper
from .exports import ExportScraper

class VitiBrasilScraper(
    ProductionScraper,
    ProcessingScraper,
    CommercializationScraper,
    ImportScraper,
    ExportScraper
):
    """Classe principal de scraper que combina todos os scrapers específicos."""
    pass 