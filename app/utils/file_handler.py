"""
Manipulador de arquivos (Excel, CSV, etc.)
"""

import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional

from ..core.logger import get_logger

logger = get_logger(__name__)

class FileHandler:
    """Manipulador de arquivos de dados"""
    
    SUPPORTED_EXTENSIONS = ['.xlsx', '.xls', '.csv']
    
    @staticmethod
    def read_file(file_path: str) -> Optional[pd.DataFrame]:
        """Lê arquivo Excel ou CSV"""
        try:
            path = Path(file_path)
            
            if not path.exists():
                raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
            
            if path.suffix.lower() not in FileHandler.SUPPORTED_EXTENSIONS:
                raise ValueError(f"Formato não suportado: {path.suffix}")
            
            # Ler arquivo baseado na extensão
            if path.suffix.lower() == '.csv':
                df = pd.read_csv(file_path, encoding='utf-8')
            else:  # Excel
                df = pd.read_excel(file_path)
            
            logger.info(f"Arquivo carregado: {file_path} ({len(df)} linhas)")
            return df
            
        except Exception as e:
            logger.error(f"Erro ao ler arquivo {file_path}: {e}")
            return None
    
    @staticmethod
    def save_file(df: pd.DataFrame, file_path: str) -> bool:
        """Salva DataFrame em arquivo"""
        try:
            path = Path(file_path)
            
            # Criar diretório se não existir
            path.parent.mkdir(parents=True, exist_ok=True)
            
            # Salvar baseado na extensão
            if path.suffix.lower() == '.csv':
                df.to_csv(file_path, index=False, encoding='utf-8')
            else:  # Excel
                df.to_excel(file_path, index=False)
            
            logger.info(f"Arquivo salvo: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao salvar arquivo {file_path}: {e}")
            return False
    
    @staticmethod
    def validate_columns(df: pd.DataFrame) -> Dict[str, Any]:
        """Valida colunas necessárias no DataFrame"""
        required_columns = ['Nome']
        optional_columns = ['Material', 'Cor', 'Descrição Fornecedor', 'Categoria 1', 'Categoria 2', 'Marca', 'Preço']
        
        result = {
            'valid': True,
            'missing_required': [],
            'missing_optional': [],
            'extra_columns': [],
            'total_rows': len(df),
            'columns_found': list(df.columns)
        }
        
        # Verificar colunas obrigatórias
        for col in required_columns:
            if col not in df.columns:
                result['missing_required'].append(col)
                result['valid'] = False
        
        # Verificar colunas opcionais
        for col in optional_columns:
            if col not in df.columns:
                result['missing_optional'].append(col)
        
        # Identificar colunas extras
        all_expected = required_columns + optional_columns
        for col in df.columns:
            if col not in all_expected:
                result['extra_columns'].append(col)
        
        return result
    
    @staticmethod
    def get_sample_data(df: pd.DataFrame, n_rows: int = 5) -> Dict[str, Any]:
        """Retorna amostra dos dados para preview"""
        try:
            sample = df.head(n_rows)
            
            return {
                'sample_data': sample.to_dict('records'),
                'total_rows': len(df),
                'columns': list(df.columns),
                'dtypes': df.dtypes.to_dict(),
                'null_counts': df.isnull().sum().to_dict()
            }
            
        except Exception as e:
            logger.error(f"Erro ao gerar amostra: {e}")
            return {}
    
    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """Limpa e padroniza dados"""
        try:
            # Fazer cópia para não modificar original
            cleaned_df = df.copy()
            
            # Remover linhas completamente vazias
            cleaned_df = cleaned_df.dropna(how='all')
            
            # Preencher valores NaN com string vazia para colunas de texto
            text_columns = ['Nome', 'Material', 'Cor', 'Descrição Fornecedor', 'Categoria 1', 'Categoria 2', 'Marca']
            for col in text_columns:
                if col in cleaned_df.columns:
                    cleaned_df[col] = cleaned_df[col].fillna('').astype(str).str.strip()
            
            # Limpar coluna de preço se existir
            if 'Preço' in cleaned_df.columns:
                cleaned_df['Preço'] = pd.to_numeric(cleaned_df['Preço'], errors='coerce')
            
            # Remover linhas sem nome (obrigatório)
            if 'Nome' in cleaned_df.columns:
                cleaned_df = cleaned_df[cleaned_df['Nome'].str.len() > 0]
            
            logger.info(f"Dados limpos: {len(df)} -> {len(cleaned_df)} linhas")
            return cleaned_df
            
        except Exception as e:
            logger.error(f"Erro ao limpar dados: {e}")
            return df
    
    @staticmethod
    def create_template() -> pd.DataFrame:
        """Cria template de planilha"""
        template_data = {
            'Nome': ['Produto Exemplo 1', 'Produto Exemplo 2'],
            'Material': ['Plástico', 'Metal'],
            'Cor': ['Azul', 'Preto'],
            'Descrição Fornecedor': ['Produto de alta qualidade', 'Item resistente'],
            'Categoria 1': ['Eletrônicos', 'Casa'],
            'Categoria 2': ['Acessórios', 'Decoração'],
            'Marca': ['Marca A', 'Marca B'],
            'Preço': [29.90, 45.50]
        }
        
        return pd.DataFrame(template_data)
    
    @staticmethod
    def export_template(file_path: str) -> bool:
        """Exporta template de planilha"""
        try:
            template_df = FileHandler.create_template()
            return FileHandler.save_file(template_df, file_path)
        except Exception as e:
            logger.error(f"Erro ao exportar template: {e}")
            return False