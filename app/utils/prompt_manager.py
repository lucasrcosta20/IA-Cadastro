"""
Gerenciador de prompts personalizados
"""

import json
from pathlib import Path
from typing import Dict, Tuple

from ..core.models import Product
from ..core.logger import get_logger
from ...config.settings import DATA_DIR, DEFAULT_PROMPT_TEMPLATE, DEFAULT_SYSTEM_PROMPT

logger = get_logger(__name__)

class PromptManager:
    """Gerenciador de prompts personalizados"""
    
    def __init__(self):
        self.prompts_file = DATA_DIR / "prompts.json"
        self.template = DEFAULT_PROMPT_TEMPLATE
        self.system_prompt = DEFAULT_SYSTEM_PROMPT
        
        self._load_prompts()
    
    def _load_prompts(self):
        """Carrega prompts do arquivo"""
        try:
            if self.prompts_file.exists():
                with open(self.prompts_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                self.template = data.get('template', DEFAULT_PROMPT_TEMPLATE)
                self.system_prompt = data.get('system', DEFAULT_SYSTEM_PROMPT)
                
                logger.info("Prompts personalizados carregados")
            else:
                logger.info("Usando prompts padrão")
                
        except Exception as e:
            logger.error(f"Erro ao carregar prompts: {e}")
            self.template = DEFAULT_PROMPT_TEMPLATE
            self.system_prompt = DEFAULT_SYSTEM_PROMPT
    
    def _save_prompts(self):
        """Salva prompts no arquivo"""
        try:
            # Criar diretório se não existir
            self.prompts_file.parent.mkdir(parents=True, exist_ok=True)
            
            data = {
                'template': self.template,
                'system': self.system_prompt,
                'updated_at': str(Path(__file__).stat().st_mtime)
            }
            
            with open(self.prompts_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            logger.info("Prompts salvos com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao salvar prompts: {e}")
    
    def format_prompt(self, product: Product) -> str:
        """Formata o prompt com os dados do produto"""
        try:
            # Preparar dados do produto
            product_data = {
                'nome': product.nome or '',
                'material': product.material or '',
                'cor': product.cor or '',
                'descricao_fornecedor': product.descricao_fornecedor or '',
                'categoria1': product.categoria1 or '',
                'categoria2': product.categoria2 or '',
                'marca': product.marca or '',
                'preco': f"R$ {product.preco:.2f}" if product.preco else ''
            }
            
            # Formatar template
            formatted_prompt = self.template.format(**product_data)
            
            return formatted_prompt
            
        except Exception as e:
            logger.error(f"Erro ao formatar prompt: {e}")
            # Fallback para prompt simples
            return f"Crie uma descrição comercial para o produto: {product.nome}"
    
    def get_prompts(self) -> Tuple[str, str]:
        """Retorna template e system prompt atuais"""
        return self.template, self.system_prompt
    
    def update_prompts(self, template: str = None, system: str = None):
        """Atualiza os prompts"""
        if template is not None:
            self.template = template
            logger.info("Template de prompt atualizado")
        
        if system is not None:
            self.system_prompt = system
            logger.info("System prompt atualizado")
        
        self._save_prompts()
    
    def reset_to_default(self):
        """Restaura prompts padrão"""
        self.template = DEFAULT_PROMPT_TEMPLATE
        self.system_prompt = DEFAULT_SYSTEM_PROMPT
        self._save_prompts()
        logger.info("Prompts restaurados para padrão")
    
    def validate_template(self, template: str) -> Tuple[bool, str]:
        """Valida se o template está correto"""
        try:
            # Testar com produto exemplo
            test_product = Product(
                nome="Teste",
                material="Material Teste",
                cor="Cor Teste",
                descricao_fornecedor="Descrição Teste",
                categoria1="Categoria 1",
                categoria2="Categoria 2"
            )
            
            # Tentar formatar
            template.format(
                nome=test_product.nome,
                material=test_product.material,
                cor=test_product.cor,
                descricao_fornecedor=test_product.descricao_fornecedor,
                categoria1=test_product.categoria1,
                categoria2=test_product.categoria2,
                marca=test_product.marca or '',
                preco=''
            )
            
            return True, "Template válido"
            
        except KeyError as e:
            return False, f"Variável não encontrada: {e}"
        except Exception as e:
            return False, f"Erro no template: {e}"
    
    def get_available_variables(self) -> Dict[str, str]:
        """Retorna variáveis disponíveis para o template"""
        return {
            '{nome}': 'Nome do produto',
            '{material}': 'Material do produto',
            '{cor}': 'Cor do produto',
            '{descricao_fornecedor}': 'Descrição fornecida pelo fornecedor',
            '{categoria1}': 'Categoria principal',
            '{categoria2}': 'Categoria secundária',
            '{marca}': 'Marca do produto',
            '{preco}': 'Preço formatado (R$ X,XX)'
        }
    
    def export_prompts(self, file_path: str):
        """Exporta prompts para arquivo"""
        try:
            export_data = {
                'template': self.template,
                'system': self.system_prompt,
                'variables': self.get_available_variables(),
                'exported_at': str(Path(__file__).stat().st_mtime)
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Prompts exportados para: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao exportar prompts: {e}")
            return False
    
    def import_prompts(self, file_path: str) -> bool:
        """Importa prompts de arquivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validar dados
            if 'template' not in data or 'system' not in data:
                raise ValueError("Arquivo de prompts inválido")
            
            # Validar template
            is_valid, error_msg = self.validate_template(data['template'])
            if not is_valid:
                raise ValueError(f"Template inválido: {error_msg}")
            
            # Aplicar prompts
            self.template = data['template']
            self.system_prompt = data['system']
            self._save_prompts()
            
            logger.info(f"Prompts importados de: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao importar prompts: {e}")
            return False