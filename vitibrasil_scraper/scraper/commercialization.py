"""
Módulo de scraper para dados de comercialização de vinhos.
"""

from typing import Dict, Optional
import logging

from .base import BaseScraper

logger = logging.getLogger(__name__)

class CommercializationScraper(BaseScraper):
    """Scraper para dados de comercialização de vinhos."""
    
    def get_commercialization_data(self, year: Optional[int] = None) -> Dict:
        """
        Obtém dados de comercialização para vinhos e derivados para um ano específico.

        Args:
            year: O ano para obter os dados. Se None, o último ano disponível é usado.

        Returns:
            Dict contendo os dados de comercialização com nomes de produtos e quantidades.
        """
        url = f"{self.BASE_URL}/index.php?opcao=opt_04"
        if year:
            url += f"&ano={year}"

        logger.info(f"Buscando dados de comercialização para o ano: {year if year else 'mais recente'}")
        
        soup = self._fetch_page(url)
        
        # Extrai o ano e título da página
        year_text = soup.select_one(".text_center").text.strip()
        title = year_text.split("[")[0].strip()
        current_year = int(year_text.split("[")[-1].split("]")[0])
        
        # Extrai dados da tabela
        data = {
            "year": current_year,
            "title": title,
            "products": [],
            "total": None
        }
        
        table = soup.select_one(".tb_dados")
        rows = table.select("tbody tr")
        
        for row in rows:
            cells = row.select("td")
            if not cells:
                continue
                
            # Verifica se é uma categoria principal ou subcategoria pela classe CSS
            is_main_category = "tb_item" in cells[0]["class"]
            
            product_name = cells[0].text.strip()
            quantity_text = cells[1].text.strip()
            
            # Converte quantidade para inteiro ou None se for apenas um traço
            quantity = None if quantity_text == "-" else self._parse_number(quantity_text)
            
            if is_main_category:
                data["products"].append({
                    "name": product_name,
                    "quantity": quantity,
                    "subcategories": []
                })
            else:
                # Adiciona como subcategoria à última categoria principal
                if data["products"]:
                    data["products"][-1]["subcategories"].append({
                        "name": product_name,
                        "quantity": quantity
                    })
        
        # Extrai o total do rodapé
        total_row = table.select_one("tfoot tr")
        if total_row:
            total_cells = total_row.select("td")
            if len(total_cells) > 1:
                data["total"] = self._parse_number(total_cells[1].text.strip())
        
        # Extrai as notas de rodapé, se presentes
        footnote_div = soup.select_one(".tb_font")
        if footnote_div:
            footnote_text = footnote_div.get_text(separator="\n").strip()
            data["footnotes"] = footnote_text
        
        return data 