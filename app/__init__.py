"""
Gerador de Descrições Comerciais Pro
Sistema profissional para geração automática de descrições usando IA
"""

__version__ = "1.0.0"
__author__ = "Lucas Costa"
__email__ = "lucas@exemplo.com"

from .core.generator import DescriptionGenerator
from .core.ai_client import AIClient
from .ui.main_window import MainWindow

__all__ = ["DescriptionGenerator", "AIClient", "MainWindow"]