"""
Módulo de scraper para dados de processamento de uvas.
"""

from typing import Dict, Optional
import logging

from .base import BaseScraper

logger = logging.getLogger(__name__)

class ProcessingScraper(BaseScraper):
    """Scraper para dados de processamento de uvas."""
    
    def get_processing_data(self, category: str = "viniferas", year: Optional[int] = None) -> Dict:
        """
        Obtém dados de processamento de uvas para uma categoria e ano específicos.

        Args:
            category: A categoria de uva para obter os dados. Opções: "viniferas", "americanas", "mesa", "sem_classificacao"
            year: O ano para obter os dados. Se None, o último ano disponível é usado.

        Returns:
            Dict contendo os dados de processamento com variedades de uvas e quantidades.
        """
        # Mapeia categoria para parâmetro subopcao
        category_map = {
            "viniferas": "subopt_01",
            "americanas": "subopt_02",
            "mesa": "subopt_03",
            "sem_classificacao": "subopt_04"
        }
        
        if category not in category_map:
            raise ValueError(f"Categoria inválida: {category}. Opções válidas são: {', '.join(category_map.keys())}")
            
        url = f"{self.BASE_URL}/index.php?opcao=opt_03&subopcao={category_map[category]}"
        if year:
            url += f"&ano={year}"

        logger.info(f"Buscando dados de processamento para categoria '{category}' e ano: {year if year else 'mais recente'}")
        
        soup = self._fetch_page(url)
        
        # Extrai o ano e título da página
        year_text = soup.select_one(".text_center").text.strip()
        title = year_text.split("[")[0].strip()
        current_year = int(year_text.split("[")[-1].split("]")[0])
        
        # Extrai dados da tabela
        data = {
            "year": current_year,
            "title": title,
            "category": category,
            "varieties": [],
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
            
            variety_name = cells[0].text.strip()
            quantity_text = cells[1].text.strip()
            
            # Converte quantidade para inteiro ou None se for apenas um traço
            quantity = None if quantity_text == "-" else self._parse_number(quantity_text)
            
            if is_main_category:
                data["varieties"].append({
                    "name": variety_name,
                    "quantity": quantity,
                    "subvarieties": []
                })
            else:
                # Adiciona como subvariedade à última categoria principal
                if data["varieties"]:
                    data["varieties"][-1]["subvarieties"].append({
                        "name": variety_name,
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
        
    def get_all_processing_data(self, year: Optional[int] = None) -> Dict:
        """
        Obtém dados de processamento de uvas para todas as categorias em um ano específico.

        Args:
            year: O ano para obter os dados. Se None, o último ano disponível é usado.

        Returns:
            Dict contendo os dados de processamento para todas as categorias.
        """
        categories = ["viniferas", "americanas", "mesa", "sem_classificacao"]
        
        result = {
            "year": year,
            "categories": {}
        }
        
        for category in categories:
            try:
                data = self.get_processing_data(category=category, year=year)
                result["categories"][category] = data
                # Atualiza o ano no resultado principal com base na primeira resposta bem-sucedida
                if result["year"] is None:
                    result["year"] = data["year"]
            except Exception as e:
                logger.error(f"Erro ao buscar dados de processamento para categoria '{category}': {e}")
                result["categories"][category] = {"error": str(e)}
        
        return result 