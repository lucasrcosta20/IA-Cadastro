"""
Sistema de logging da aplicação
"""

import logging
import sys
from pathlib import Path
from datetime import datetime

def setup_logger(name: str = "gerador_descricoes", level: int = logging.INFO) -> logging.Logger:
    """Configura o sistema de logging"""
    
    # Criar diretório de logs
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Nome do arquivo de log com timestamp
    log_file = log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Configurar logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Evitar duplicação de handlers
    if logger.handlers:
        return logger
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para arquivo
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    
    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)  # Apenas warnings+ no console
    console_handler.setFormatter(formatter)
    
    # Adicionar handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def get_logger(name: str) -> logging.Logger:
    """Obtém logger para um módulo específico"""
    return logging.getLogger(f"gerador_descricoes.{name}")

# Logger principal
main_logger = setup_logger()