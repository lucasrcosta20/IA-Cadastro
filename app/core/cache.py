"""
Sistema de cache para descrições geradas
"""

import pickle
import hashlib
import time
from pathlib import Path
from typing import Optional, Dict, Any

from .models import Product, GenerationResult
from .logger import get_logger
from config.settings import CACHE_DIR, GENERATION_CONFIG

logger = get_logger(__name__)

class CacheManager:
    """Gerenciador de cache para descrições"""
    
    def __init__(self, cache_file: str = "descriptions_cache.pkl"):
        self.cache_file = CACHE_DIR / cache_file
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.hits = 0
        self.misses = 0
        self.ttl = GENERATION_CONFIG.get('cache_ttl', 86400)  # 24 horas
        
        self._load_cache()
    
    def _generate_key(self, product: Product) -> str:
        """Gera chave única para o produto"""
        # Criar string com dados relevantes do produto
        data_string = f"{product.nome}|{product.material}|{product.cor}|{product.descricao_fornecedor}|{product.categoria1}|{product.categoria2}"
        
        # Gerar hash MD5
        return hashlib.md5(data_string.encode('utf-8')).hexdigest()
    
    def _load_cache(self):
        """Carrega cache do arquivo"""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'rb') as f:
                    self.cache = pickle.load(f)
                
                # Limpar entradas expiradas
                self._cleanup_expired()
                
                logger.info(f"Cache carregado: {len(self.cache)} entradas")
            else:
                logger.info("Arquivo de cache não encontrado, iniciando cache vazio")
                
        except Exception as e:
            logger.error(f"Erro ao carregar cache: {e}")
            self.cache = {}
    
    def _save_cache(self):
        """Salva cache no arquivo"""
        try:
            # Criar diretório se não existir
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.cache_file, 'wb') as f:
                pickle.dump(self.cache, f)
                
            logger.debug(f"Cache salvo: {len(self.cache)} entradas")
            
        except Exception as e:
            logger.error(f"Erro ao salvar cache: {e}")
    
    def _cleanup_expired(self):
        """Remove entradas expiradas do cache"""
        current_time = time.time()
        expired_keys = []
        
        for key, entry in self.cache.items():
            if current_time - entry['timestamp'] > self.ttl:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            logger.info(f"Removidas {len(expired_keys)} entradas expiradas do cache")
    
    def get(self, product: Product) -> Optional[GenerationResult]:
        """Recupera descrição do cache"""
        key = self._generate_key(product)
        
        if key in self.cache:
            entry = self.cache[key]
            
            # Verificar se não expirou
            if time.time() - entry['timestamp'] <= self.ttl:
                self.hits += 1
                logger.debug(f"Cache hit para produto: {product.nome}")
                
                # Reconstruir GenerationResult
                return GenerationResult(
                    product=product,
                    description=entry['description'],
                    success=True,
                    generation_time=entry.get('generation_time'),
                    model_used=entry.get('model_used')
                )
            else:
                # Entrada expirada, remover
                del self.cache[key]
                logger.debug(f"Entrada expirada removida: {product.nome}")
        
        self.misses += 1
        return None
    
    def set(self, product: Product, result: GenerationResult):
        """Armazena descrição no cache"""
        if not result.success:
            return  # Não cachear resultados com erro
        
        key = self._generate_key(product)
        
        entry = {
            'description': result.description,
            'timestamp': time.time(),
            'generation_time': result.generation_time,
            'model_used': result.model_used
        }
        
        self.cache[key] = entry
        
        # Salvar cache periodicamente (a cada 10 entradas)
        if len(self.cache) % 10 == 0:
            self._save_cache()
        
        logger.debug(f"Produto adicionado ao cache: {product.nome}")
    
    def clear(self):
        """Limpa todo o cache"""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
        
        # Remover arquivo de cache
        if self.cache_file.exists():
            self.cache_file.unlink()
        
        logger.info("Cache limpo completamente")
    
    def size(self) -> int:
        """Retorna número de entradas no cache"""
        return len(self.cache)
    
    def hit_rate(self) -> float:
        """Retorna taxa de acerto do cache"""
        total = self.hits + self.misses
        return (self.hits / total * 100) if total > 0 else 0.0
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do cache"""
        return {
            'size': self.size(),
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': self.hit_rate(),
            'ttl_hours': self.ttl / 3600,
            'file_exists': self.cache_file.exists(),
            'file_size_mb': self.cache_file.stat().st_size / 1024 / 1024 if self.cache_file.exists() else 0
        }
    
    def cleanup_old_entries(self, max_age_hours: int = 24):
        """Remove entradas mais antigas que o especificado"""
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        old_keys = []
        for key, entry in self.cache.items():
            if current_time - entry['timestamp'] > max_age_seconds:
                old_keys.append(key)
        
        for key in old_keys:
            del self.cache[key]
        
        if old_keys:
            self._save_cache()
            logger.info(f"Removidas {len(old_keys)} entradas antigas do cache")
        
        return len(old_keys)
    
    def __del__(self):
        """Salva cache ao destruir objeto"""
        try:
            self._save_cache()
        except:
            pass