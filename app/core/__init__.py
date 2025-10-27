"""
Core - Lógica de negócio principal
"""

from .generator import DescriptionGenerator
from .ai_client import AIClient
from .models import Product, GenerationResult
from .cache import CacheManager

__all__ = ["DescriptionGenerator", "AIClient", "Product", "GenerationResult", "CacheManager"]