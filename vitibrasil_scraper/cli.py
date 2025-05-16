"""
Command-line interface for VitiBrasil API.

Este módulo fornece a interface de linha de comando para o Scraper VitiBrasil.
É usado tanto para execução direta quanto como ponto de entrada quando instalado como pacote.
"""

import argparse
from api import create_app 


def main():
    """
    Ponto de entrada principal para a API VitiBrasil.
    
    Esta função é usada de duas maneiras:
    1. Chamada diretamente ao executar o arquivo cli.py
    2. Chamada pelo comando 'vitibrasil' quando o pacote é instalado via pip
    
    Parâmetros via linha de comando:
    --host: O endereço IP onde a API será hospedada (padrão: 127.0.0.1)
    --port: A porta onde a API estará disponível (padrão: 5000)
    --debug: Ativa o modo de depuração do Flask
    
    Exemplos:
        # Execução direta
        python vitibrasil_scraper/cli.py
        
        # Execução após instalação como pacote
        vitibrasil --host 0.0.0.0 --port 8080 --debug
    """
    parser = argparse.ArgumentParser(description="Executar a API VitiBrasil")
    parser.add_argument("--host", default="127.0.0.1", help="Host onde a API será executada")
    parser.add_argument("--port", type=int, default=5000, help="Porta onde a API será executada")
    parser.add_argument("--debug", action="store_true", help="Executar no modo de depuração")
    
    args = parser.parse_args()
    
    app = create_app()
    print(f"* Iniciando API VitiBrasil em http://{args.host}:{args.port}")
    print(f"* Modo de depuração: {'Ativado' if args.debug else 'Desativado'}")
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main() 