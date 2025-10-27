"""
Modelos de dados da aplicação
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime

@dataclass
class Product:
    """Modelo para representar um produto"""
    nome: str
    material: Optional[str] = None
    cor: Optional[str] = None
    descricao_fornecedor: Optional[str] = None
    categoria1: Optional[str] = None
    categoria2: Optional[str] = None
    preco: Optional[float] = None
    marca: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            'nome': self.nome,
            'material': self.material or '',
            'cor': self.cor or '',
            'descricao_fornecedor': self.descricao_fornecedor or '',
            'categoria1': self.categoria1 or '',
            'categoria2': self.categoria2 or '',
            'preco': self.preco,
            'marca': self.marca or ''
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Product':
        """Cria instância a partir de dicionário"""
        return cls(
            nome=data.get('nome', ''),
            material=data.get('material'),
            cor=data.get('cor'),
            descricao_fornecedor=data.get('descricao_fornecedor'),
            categoria1=data.get('categoria1'),
            categoria2=data.get('categoria2'),
            preco=data.get('preco'),
            marca=data.get('marca')
        )

@dataclass
class GenerationResult:
    """Resultado da geração de descrição"""
    product: Product
    description: str
    success: bool
    error_message: Optional[str] = None
    generation_time: Optional[float] = None
    model_used: Optional[str] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

@dataclass
class AIModel:
    """Modelo de IA disponível"""
    id: str
    name: str
    size: str
    speed: str
    quality: str
    description: str
    installed: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'size': self.size,
            'speed': self.speed,
            'quality': self.quality,
            'description': self.description,
            'installed': self.installed
        }

@dataclass
class GenerationConfig:
    """Configuração para geração"""
    model_id: str = "gemma2:2b"
    temperature: float = 0.7
    max_tokens: int = 500
    use_cache: bool = True
    max_workers: int = 2
    timeout: int = 60
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'model_id': self.model_id,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
            'use_cache': self.use_cache,
            'max_workers': self.max_workers,
            'timeout': self.timeout
        }