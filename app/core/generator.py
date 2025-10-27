"""
Gerador principal de descrições
"""

import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Callable, Optional
import pandas as pd

from .models import Product, GenerationResult, GenerationConfig
from .ai_client import AIClient
from .cache import CacheManager
from .logger import get_logger
from app.utils.prompt_manager import PromptManager

logger = get_logger(__name__)

class DescriptionGenerator:
    """Gerador principal de descrições comerciais"""
    
    def __init__(self):
        self.ai_client = AIClient()
        self.cache_manager = CacheManager()
        self.prompt_manager = PromptManager()
        self.config = GenerationConfig()
        
    def generate_single(self, product: Product, use_cache: bool = True) -> GenerationResult:
        """Gera descrição para um único produto"""
        start_time = time.time()
        
        try:
            # Verificar cache primeiro
            if use_cache:
                cached_result = self.cache_manager.get(product)
                if cached_result:
                    logger.debug(f"Cache hit para produto: {product.nome}")
                    return cached_result
            
            # Gerar prompt
            prompt = self.prompt_manager.format_prompt(product)
            
            # Gerar descrição
            description = self.ai_client.generate(prompt, self.config)
            
            if description:
                generation_time = time.time() - start_time
                result = GenerationResult(
                    product=product,
                    description=description,
                    success=True,
                    generation_time=generation_time,
                    model_used=self.config.model_id
                )
                
                # Salvar no cache
                if use_cache:
                    self.cache_manager.set(product, result)
                
                logger.info(f"Descrição gerada para '{product.nome}' em {generation_time:.2f}s")
                return result
            else:
                return GenerationResult(
                    product=product,
                    description="",
                    success=False,
                    error_message="Falha na geração da descrição"
                )
                
        except Exception as e:
            logger.error(f"Erro ao gerar descrição para '{product.nome}': {e}")
            return GenerationResult(
                product=product,
                description="",
                success=False,
                error_message=str(e)
            )
    
    def generate_batch(self, 
                      products: List[Product], 
                      progress_callback: Optional[Callable[[int, int], None]] = None,
                      max_workers: Optional[int] = None) -> List[GenerationResult]:
        """Gera descrições em lote com processamento paralelo"""
        
        if max_workers is None:
            max_workers = self.config.max_workers
        
        results = []
        completed = 0
        total = len(products)
        
        logger.info(f"Iniciando geração em lote: {total} produtos, {max_workers} workers")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submeter todas as tarefas
            future_to_product = {
                executor.submit(self.generate_single, product): product 
                for product in products
            }
            
            # Processar resultados conforme completam
            for future in as_completed(future_to_product):
                try:
                    result = future.result()
                    results.append(result)
                    completed += 1
                    
                    # Callback de progresso
                    if progress_callback:
                        progress_callback(completed, total)
                        
                except Exception as e:
                    product = future_to_product[future]
                    logger.error(f"Erro no processamento de '{product.nome}': {e}")
                    
                    # Adicionar resultado de erro
                    error_result = GenerationResult(
                        product=product,
                        description="",
                        success=False,
                        error_message=str(e)
                    )
                    results.append(error_result)
                    completed += 1
                    
                    if progress_callback:
                        progress_callback(completed, total)
        
        # Ordenar resultados pela ordem original
        product_order = {id(p): i for i, p in enumerate(products)}
        results.sort(key=lambda r: product_order.get(id(r.product), float('inf')))
        
        successful = sum(1 for r in results if r.success)
        logger.info(f"Geração em lote concluída: {successful}/{total} sucessos")
        
        return results
    
    def generate_from_dataframe(self, 
                               df: pd.DataFrame,
                               progress_callback: Optional[Callable[[int, int], None]] = None) -> List[str]:
        """Gera descrições a partir de um DataFrame"""
        
        # Converter DataFrame para lista de produtos
        products = []
        for _, row in df.iterrows():
            product = Product(
                nome=str(row.get('Nome', '')),
                material=str(row.get('Material', '')) if pd.notna(row.get('Material')) else None,
                cor=str(row.get('Cor', '')) if pd.notna(row.get('Cor')) else None,
                descricao_fornecedor=str(row.get('Descrição Fornecedor', '')) if pd.notna(row.get('Descrição Fornecedor')) else None,
                categoria1=str(row.get('Categoria 1', '')) if pd.notna(row.get('Categoria 1')) else None,
                categoria2=str(row.get('Categoria 2', '')) if pd.notna(row.get('Categoria 2')) else None,
                preco=row.get('Preço') if pd.notna(row.get('Preço')) else None,
                marca=str(row.get('Marca', '')) if pd.notna(row.get('Marca')) else None
            )
            products.append(product)
        
        # Gerar descrições
        results = self.generate_batch(products, progress_callback)
        
        # Retornar apenas as descrições como lista
        descriptions = []
        for result in results:
            if result.success:
                descriptions.append(result.description)
            else:
                descriptions.append(f"ERRO: {result.error_message}")
        
        return descriptions
    
    def update_config(self, **kwargs):
        """Atualiza configuração do gerador"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
                logger.info(f"Configuração atualizada: {key} = {value}")
    
    def get_stats(self) -> dict:
        """Retorna estatísticas do gerador"""
        return {
            'cache_size': self.cache_manager.size(),
            'cache_hits': self.cache_manager.hits,
            'cache_misses': self.cache_manager.misses,
            'model_available': self.ai_client.is_available(),
            'current_model': self.config.model_id,
            'max_workers': self.config.max_workers
        }
    
    def clear_cache(self):
        """Limpa o cache"""
        self.cache_manager.clear()
        logger.info("Cache limpo")
    
    def test_generation(self) -> GenerationResult:
        """Testa a geração com um produto exemplo"""
        test_product = Product(
            nome="Vaso Decorativo Teste",
            material="Cerâmica",
            cor="Branco",
            descricao_fornecedor="Vaso moderno para decoração",
            categoria1="Decoração",
            categoria2="Casa"
        )
        
        return self.generate_single(test_product, use_cache=False)