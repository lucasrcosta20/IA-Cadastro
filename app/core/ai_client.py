"""
Cliente para comunicação com Ollama
"""

import requests
import json
import time
from typing import List, Dict, Any, Optional
from .models import AIModel, GenerationConfig
from .logger import get_logger

logger = get_logger(__name__)

class AIClient:
    """Cliente para interação com Ollama"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.timeout = 60
    
    def is_available(self) -> bool:
        """Verifica se o Ollama está disponível"""
        try:
            response = self.session.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Ollama não disponível: {e}")
            return False
    
    def get_models(self) -> List[AIModel]:
        """Lista modelos disponíveis"""
        try:
            response = self.session.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                data = response.json()
                models = []
                
                # Modelos conhecidos com metadados
                known_models = {
                    "gemma2:2b": AIModel(
                        id="gemma2:2b",
                        name="Gemma2 2B",
                        size="1.6GB",
                        speed="Média",
                        quality="Boa",
                        description="Modelo equilibrado, recomendado para uso geral"
                    ),
                    "phi3:mini": AIModel(
                        id="phi3:mini",
                        name="Phi3 Mini",
                        size="2.3GB",
                        speed="Lenta",
                        quality="Excelente",
                        description="Alta qualidade, melhor para textos complexos"
                    ),
                    "tinyllama": AIModel(
                        id="tinyllama",
                        name="TinyLlama",
                        size="637MB",
                        speed="Rápida",
                        quality="Básica",
                        description="Muito rápido, qualidade básica"
                    )
                }
                
                # Marcar modelos instalados
                installed_models = [model['name'] for model in data.get('models', [])]
                
                for model_id, model_info in known_models.items():
                    model_info.installed = model_id in installed_models
                    models.append(model_info)
                
                return models
            
        except Exception as e:
            logger.error(f"Erro ao listar modelos: {e}")
        
        return []
    
    def pull_model(self, model_id: str) -> bool:
        """Baixa um modelo"""
        try:
            logger.info(f"Baixando modelo {model_id}...")
            
            payload = {"name": model_id}
            response = self.session.post(
                f"{self.base_url}/api/pull",
                json=payload,
                stream=True,
                timeout=300  # 5 minutos para download
            )
            
            if response.status_code == 200:
                # Processar stream de download
                for line in response.iter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            if data.get('status') == 'success':
                                logger.info(f"Modelo {model_id} baixado com sucesso")
                                return True
                        except json.JSONDecodeError:
                            continue
            
            return False
            
        except Exception as e:
            logger.error(f"Erro ao baixar modelo {model_id}: {e}")
            return False
    
    def generate(self, prompt: str, config: GenerationConfig) -> Optional[str]:
        """Gera texto usando o modelo"""
        try:
            start_time = time.time()
            
            payload = {
                "model": config.model_id,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": config.temperature,
                    "num_predict": config.max_tokens
                }
            }
            
            logger.debug(f"Gerando com modelo {config.model_id}")
            
            response = self.session.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=config.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result.get('response', '').strip()
                
                generation_time = time.time() - start_time
                logger.info(f"Geração concluída em {generation_time:.2f}s")
                
                return generated_text
            else:
                logger.error(f"Erro na geração: Status {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            logger.error("Timeout na geração")
            return None
        except Exception as e:
            logger.error(f"Erro na geração: {e}")
            return None
    
    def chat(self, messages: List[Dict[str, str]], config: GenerationConfig) -> Optional[str]:
        """Chat com o modelo"""
        try:
            payload = {
                "model": config.model_id,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": config.temperature,
                    "num_predict": config.max_tokens
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=config.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('message', {}).get('content', '').strip()
            
            return None
            
        except Exception as e:
            logger.error(f"Erro no chat: {e}")
            return None