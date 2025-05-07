import os
import requests
from dotenv import load_dotenv
from pathlib import Path

def generate_text(self, prompt):
    try:
        response = requests.post(
            f"{self.base_url}?key={self.api_key}",
            headers={"Content-Type": "application/json"},
            json={
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            },
            timeout=10
        )
        
        # Verificação adicional do status code
        if response.status_code == 503:
            raise Exception("Serviço indisponível. Tente novamente mais tarde ou verifique se o modelo está disponível.")
        
        response.raise_for_status()
        
        try:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except KeyError:
            # Debug adicional para respostas inesperadas
            print("Resposta completa da API:", response.json())
            raise Exception("Formato de resposta inesperado da API")

    except requests.exceptions.RequestException as e:
        # Tratamento específico para diferentes erros HTTP
        if "503" in str(e):
            raise Exception("Servidor indisponível (503). Possíveis causas:\n"
                        "- Modelo gemini-2.0-flash não disponível\n"
                        "- Problemas temporários na API\n"
                        "- Tente usar gemini-1.5-flash como alternativa")
        elif "403" in str(e):
            raise Exception("Acesso negado (403). Verifique:\n"
                        "- Se sua chave API está correta\n"
                        "- Se a API Gemini está ativada no seu projeto")
        else:
            raise Exception(f"Erro na requisição: {str(e)}")
# Solução 100% confiável para encontrar o .env
def find_env_file():
    """Busca o arquivo .env em locais possíveis"""
    possible_locations = [
        # Tentativa 1: Pasta env/ na raiz do projeto
        Path(__file__).resolve().parent.parent.parent / "env" / ".env",
        # Tentativa 2: Pasta env/ no mesmo diretório do script
        Path(__file__).resolve().parent / "env" / ".env",
        # Tentativa 3: Diretório atual de trabalho
        Path.cwd() / "env" / ".env",
    ]
    
    for location in possible_locations:
        if location.exists():
            print(f"Arquivo .env encontrado em: {location}")
            return location
    
    # Se não encontrou, mostra todos os locais verificados
    error_msg = "Arquivo .env não encontrado. Verifique estas localizações:\n"
    error_msg += "\n".join(f"- {loc}" for loc in possible_locations)
    error_msg += "\n\nCrie a pasta 'env' e dentro dela o arquivo '.env' com GEMINI_API_KEY=sua_chave"
    raise FileNotFoundError(error_msg)

# Carrega o arquivo .env
ENV_PATH = find_env_file()
load_dotenv(ENV_PATH)

class GeminiClient:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Chave API não encontrada no arquivo .env\n"
                f"Verifique se o arquivo {ENV_PATH} contém:\n"
                "GEMINI_API_KEY=sua_chave_aqui\n"
                f"Conteúdo atual do arquivo:\n{open(ENV_PATH).read()}"
            )
        
        self.base_url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            "gemini-2.0-flash:generateContent"
        )

    def generate_text(self, prompt):
        try:
            response = requests.post(
                f"{self.base_url}?key={self.api_key}",
                headers={"Content-Type": "application/json"},
                json={"contents": [{"parts": [{"text": prompt}]}]},
                timeout=30
            )
            response.raise_for_status()
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            raise Exception(f"Erro na API Gemini: {str(e)}")