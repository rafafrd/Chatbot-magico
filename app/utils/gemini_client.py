import os
import requests
from dotenv import load_dotenv
from pathlib import Path
import streamlit as st

class GeminiClient:
    def __init__(self):
        self.api_key = self._get_api_key()
        
        if not self.api_key:
            raise ValueError(
                "Chave API não encontrada. Verifique:\n"
                "1. Secrets do Streamlit (para produção)\n"
                "2. Arquivo .env na raiz do projeto (para desenvolvimento local)\n"
                "3. Variáveis de ambiente do sistema"
            )
        
        self.base_url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            "gemini-2.0-flash:generateContent"
        )

    def _get_api_key(self):
        """Hierarquia de fontes para obter a chave API"""
        # 1. Tenta usar Secrets do Streamlit (produção)
        try:
            return st.secrets["GEMINI_API_KEY"]
        except:
            pass
        
        # 2. Tenta variáveis de ambiente do sistema
        if "GEMINI_API_KEY" in os.environ:
            return os.environ["GEMINI_API_KEY"]
        
        # 3. Tenta arquivo .env na raiz do projeto
        env_path = Path(__file__).parent.parent.parent / ".env"
        if env_path.exists():
            load_dotenv(env_path)
            return os.getenv("GEMINI_API_KEY")
        
        # 4. Tenta .env no diretório atual (fallback)
        load_dotenv()  # Tenta carregar .env localmente
        return os.getenv("GEMINI_API_KEY")

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
                timeout=30
            )
            
            # Verificação adicional do status code
            if response.status_code == 503:
                raise Exception("Serviço indisponível. Tente novamente mais tarde ou verifique se o modelo está disponível.")
            
            response.raise_for_status()
            
            try:
                return response.json()["candidates"][0]["content"]["parts"][0]["text"]
            except KeyError:
                print("Resposta completa da API:", response.json())
                raise Exception("Formato de resposta inesperado da API")

        except requests.exceptions.RequestException as e:
            if "503" in str(e):
                raise Exception(
                    "Servidor indisponível (503). Possíveis causas:\n"
                    "- Modelo gemini-2.0-flash não disponível\n"
                    "- Problemas temporários na API\n"
                    "- Tente usar gemini-1.5-flash como alternativa"
                )
            elif "403" in str(e):
                raise Exception(
                    "Acesso negado (403). Verifique:\n"
                    "- Se sua chave API está correta\n"
                    "- Se a API Gemini está ativada no seu projeto"
                )
            else:
                raise Exception(f"Erro na requisição: {str(e)}")