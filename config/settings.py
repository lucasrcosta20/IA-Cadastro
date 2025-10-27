"""
Configurações da aplicação
"""

import os
from pathlib import Path
from typing import Dict, Any

# Diretórios
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
LOGS_DIR = ROOT_DIR / "logs"
CACHE_DIR = ROOT_DIR / "cache"
ASSETS_DIR = ROOT_DIR / "assets"

# Criar diretórios se não existirem
for directory in [DATA_DIR, LOGS_DIR, CACHE_DIR, ASSETS_DIR]:
    directory.mkdir(exist_ok=True)

# Configurações do Ollama
OLLAMA_CONFIG = {
    "base_url": os.getenv("OLLAMA_URL", "http://localhost:11434"),
    "timeout": int(os.getenv("OLLAMA_TIMEOUT", "60")),
    "default_model": os.getenv("DEFAULT_MODEL", "gemma2:2b")
}

# Modelos disponíveis
AVAILABLE_MODELS = {
    "gemma2:2b": {
        "name": "Gemma2 2B",
        "size": "1.6GB",
        "speed": "Média",
        "quality": "Boa",
        "description": "Modelo equilibrado, recomendado para uso geral",
        "recommended": True
    },
    "phi3:mini": {
        "name": "Phi3 Mini", 
        "size": "2.3GB",
        "speed": "Lenta",
        "quality": "Excelente",
        "description": "Alta qualidade, melhor para textos complexos",
        "recommended": False
    },
    "tinyllama": {
        "name": "TinyLlama",
        "size": "637MB", 
        "speed": "Rápida",
        "quality": "Básica",
        "description": "Muito rápido, qualidade básica",
        "recommended": False
    }
}

# Configurações de geração
GENERATION_CONFIG = {
    "temperature": float(os.getenv("TEMPERATURE", "0.7")),
    "max_tokens": int(os.getenv("MAX_TOKENS", "500")),
    "max_workers": int(os.getenv("MAX_WORKERS", "2")),
    "use_cache": os.getenv("USE_CACHE", "true").lower() == "true",
    "cache_ttl": int(os.getenv("CACHE_TTL", "86400"))  # 24 horas
}

# Configurações da interface
UI_CONFIG = {
    "theme": os.getenv("UI_THEME", "dark"),
    "window_size": os.getenv("WINDOW_SIZE", "900x700"),
    "font_family": os.getenv("FONT_FAMILY", "Roboto Mono"),
    "font_size": int(os.getenv("FONT_SIZE", "10"))
}

# Configurações da API
API_CONFIG = {
    "host": os.getenv("API_HOST", "0.0.0.0"),
    "port": int(os.getenv("API_PORT", "8000")),
    "debug": os.getenv("API_DEBUG", "false").lower() == "true",
    "cors_enabled": os.getenv("CORS_ENABLED", "true").lower() == "true"
}

# Configurações de logging
LOGGING_CONFIG = {
    "level": os.getenv("LOG_LEVEL", "INFO"),
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file_rotation": os.getenv("LOG_ROTATION", "daily"),
    "max_files": int(os.getenv("LOG_MAX_FILES", "30"))
}

# Prompt padrão
DEFAULT_PROMPT_TEMPLATE = """Crie uma descrição comercial envolvente para o produto abaixo.
Use apenas as informações fornecidas: Nome, Material, Cor, Descrição do Fornecedor, Categoria 1 e Categoria 2.
Não coloque títulos, listas, cabeçalhos ou markdown.
Não invente medidas, dimensões ou características não mencionadas.
O texto deve ser corrido e persuasivo para venda online.

Nome: {nome}
Material: {material}
Cor: {cor}
Descrição do Fornecedor: {descricao_fornecedor}
Categoria 1: {categoria1}
Categoria 2: {categoria2}

Descrição comercial:"""

DEFAULT_SYSTEM_PROMPT = "Você é um especialista em descrições comerciais para e-commerce. Crie textos persuasivos e profissionais."

# Configurações de performance
PERFORMANCE_CONFIG = {
    "batch_size": int(os.getenv("BATCH_SIZE", "10")),
    "retry_attempts": int(os.getenv("RETRY_ATTEMPTS", "3")),
    "retry_delay": float(os.getenv("RETRY_DELAY", "1.0")),
    "memory_limit": os.getenv("MEMORY_LIMIT", "2GB")
}

def get_config() -> Dict[str, Any]:
    """Retorna todas as configurações"""
    return {
        "ollama": OLLAMA_CONFIG,
        "models": AVAILABLE_MODELS,
        "generation": GENERATION_CONFIG,
        "ui": UI_CONFIG,
        "api": API_CONFIG,
        "logging": LOGGING_CONFIG,
        "performance": PERFORMANCE_CONFIG,
        "prompts": {
            "template": DEFAULT_PROMPT_TEMPLATE,
            "system": DEFAULT_SYSTEM_PROMPT
        }
    }