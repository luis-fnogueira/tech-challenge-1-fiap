"""
Módulo base do scraper com funcionalidades comuns.
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional
import logging
import time

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class BaseScraper:
    """Scraper base com funcionalidades comuns."""

    BASE_URL = "http://vitibrasil.cnpuv.embrapa.br"

    def __init__(self, max_retries: int = 3, timeout: int = 10):
        """
        Inicializa o scraper.
        
        Args:
            max_retries: Número máximo de tentativas para requisições HTTP
            timeout: Tempo limite para requisições HTTP em segundos
        """
        self.session = requests.Session()
        self.max_retries = max_retries
        self.timeout = timeout
    
    def _fetch_page(self, url: str) -> BeautifulSoup:
        """
        Busca uma página com lógica de retry.
        
        Args:
            url: A URL para buscar
            
        Returns:
            Objeto BeautifulSoup da página analisada
            
        Raises:
            Exception: Se a página não puder ser buscada após as tentativas
        """
        logger.info(f"Buscando página de {url}")
        
        # Tenta obter os dados com retries
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                break
            except requests.RequestException as e:
                logger.error(f"Erro de requisição na tentativa {attempt + 1}/{self.max_retries}: {e}")
                if attempt + 1 < self.max_retries:
                    wait_time = 2 ** attempt  # Backoff exponencial
                    logger.info(f"Tentando novamente em {wait_time} segundos...")
                    time.sleep(wait_time)
                else:
                    raise Exception(f"Falha ao buscar dados após {self.max_retries} tentativas") from e
        
        return BeautifulSoup(response.content, "html.parser")
    
    def _parse_number(self, text: str) -> Optional[int]:
        """
        Analisa um número a partir de texto, tratando vários formatos.
        
        Args:
            text: O texto para analisar um número
            
        Returns:
            O inteiro analisado ou None se a análise falhar
        """
        if not text or text == "-":
            return None
            
        # Remove quaisquer caracteres não numéricos, exceto pontos (que podem ser separadores de milhares)
        cleaned_text = "".join(c for c in text if c.isdigit() or c == ".")
        
        # Se houver pontos, trate-os como separadores de milhares
        cleaned_text = cleaned_text.replace(".", "")
        
        try:
            return int(cleaned_text)
        except ValueError:
            logger.warning(f"Não foi possível analisar número do texto: '{text}'")
            return None 