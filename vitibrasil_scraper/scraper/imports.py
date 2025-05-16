"""
Módulo de scraper para dados de importação.
"""

from typing import Dict, Optional
import logging

from .base import BaseScraper

logger = logging.getLogger(__name__)

class ImportScraper(BaseScraper):
    """Scraper para dados de importação."""
    
    def get_import_data(self, category: str = "vinhos_mesa", year: Optional[int] = None) -> Dict:
        """
        Obtém dados de importação de produtos vitivinícolas para uma categoria e ano específicos.

        Args:
            category: A categoria de importação para obter os dados. 
                     Opções: "vinhos_mesa", "espumantes", "uvas_frescas", "uvas_passas", "suco_uva"
            year: O ano para obter os dados. Se None, o último ano disponível é usado.

        Returns:
            Dict contendo os dados de importação com países, quantidades e valores.
        """
        # Mapeia categoria para parâmetro subopcao
        category_map = {
            "vinhos_mesa": "subopt_01",
            "espumantes": "subopt_02",
            "uvas_frescas": "subopt_03",
            "uvas_passas": "subopt_04",
            "suco_uva": "subopt_05"
        }
        
        # Mapeia categoria para nome de exibição
        category_display_names = {
            "vinhos_mesa": "Vinhos de Mesa",
            "espumantes": "Espumantes",
            "uvas_frescas": "Uvas Frescas",
            "uvas_passas": "Uvas Passas",
            "suco_uva": "Suco de Uva"
        }
        
        if category not in category_map:
            raise ValueError(f"Categoria inválida: {category}. Opções válidas são: vinhos_mesa, espumantes, uvas_frescas, uvas_passas, suco_uva")
            
        url = f"{self.BASE_URL}/index.php?opcao=opt_05&subopcao={category_map[category]}"
        if year:
            url += f"&ano={year}"

        logger.info(f"Buscando dados de importação para categoria '{category}' e ano: {year if year else 'mais recente'}")
        
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
            "display_name": category_display_names[category],
            "countries": [],
            "total_quantity": None,
            "total_value": None
        }
        
        table = soup.select_one(".tb_dados")
        if not table:
            raise Exception(f"Não foi possível encontrar dados de tabela para categoria '{category}'")
            
        # Processa linhas
        rows = table.select("tbody tr")
        
        for row in rows:
            cells = row.select("td")
            if not cells or len(cells) < 3:
                continue
                
            country_name = cells[0].text.strip()
            quantity_text = cells[1].text.strip()
            value_text = cells[2].text.strip()
            
            # Analisa quantidade e valor
            quantity = None if quantity_text == "-" else self._parse_number(quantity_text)
            value = None if value_text == "-" else self._parse_number(value_text)
            
            # Adiciona à lista de países
            data["countries"].append({
                "name": country_name,
                "quantity": quantity,
                "value": value
            })
        
        # Extrai o total do rodapé
        total_row = table.select_one("tfoot tr")
        if total_row:
            total_cells = total_row.select("td")
            if len(total_cells) > 2:  # País, Quantidade, Valor
                data["total_quantity"] = self._parse_number(total_cells[1].text.strip())
                data["total_value"] = self._parse_number(total_cells[2].text.strip())
        
        # Extrai as notas de rodapé, se presentes
        footnote_div = soup.select_one(".tb_font")
        if footnote_div:
            footnote_text = footnote_div.get_text(separator="\n").strip()
            data["footnotes"] = footnote_text
        
        return data
    
    def get_all_import_data(self, year: Optional[int] = None) -> Dict:
        """
        Obtém dados de importação para todas as categorias em um ano específico.

        Args:
            year: O ano para obter os dados. Se None, o último ano disponível é usado.

        Returns:
            Dict contendo os dados de importação para todas as categorias.
        """
        categories = ["vinhos_mesa", "espumantes", "uvas_frescas", "uvas_passas", "suco_uva"]
        
        result = {
            "year": year,
            "categories": {}
        }
        
        for category in categories:
            try:
                data = self.get_import_data(category=category, year=year)
                result["categories"][category] = data
                # Atualiza o ano no resultado principal com base na primeira resposta bem-sucedida
                if result["year"] is None:
                    result["year"] = data["year"]
            except Exception as e:
                logger.error(f"Erro ao buscar dados de importação para categoria '{category}': {e}")
                result["categories"][category] = {"error": str(e)}
        
        return result 