#!/usr/bin/env python3
"""
API Flask para o Gerador de Descrições
"""

import sys
import os
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import io
import base64

# Adicionar o diretório raiz ao path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

# Importar módulos da aplicação
try:
    from app.core.generator import DescriptionGenerator
    from app.core.ai_client import AIClient
    from app.core.models import Product
    from app.utils.file_handler import FileHandler
except ImportError as e:
    print(f"Erro ao importar módulos: {e}")
    sys.exit(1)

# Criar aplicação Flask
app = Flask(__name__)
CORS(app)

# Inicializar componentes
try:
    generator = DescriptionGenerator()
    ai_client = AIClient()
    file_handler = FileHandler()
except Exception as e:
    print(f"Erro ao inicializar componentes: {e}")
    generator = None
    ai_client = None
    file_handler = None

@app.route('/')
def home():
    """Página inicial"""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check"""
    try:
        ollama_status = ai_client.is_available() if ai_client else False
        models = ai_client.get_models() if ai_client else []
        installed_models = [m for m in models if m.installed]
        
        return jsonify({
            'status': 'healthy',
            'ollama_available': ollama_status,
            'models_installed': len(installed_models),
            'models': [m.name for m in installed_models]
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/test', methods=['POST'])
def test_generation():
    """Testa geração de uma descrição"""
    try:
        if not generator:
            return jsonify({'error': 'Gerador não disponível'}), 500
        
        # Produto de teste
        product = Product(
            nome="Produto Teste API",
            material="Plástico",
            cor="Azul",
            descricao_fornecedor="Produto para teste da API",
            categoria1="Teste",
            categoria2="API"
        )
        
        # Gerar descrição
        result = generator.generate_single(product, use_cache=False)
        
        if result.success:
            return jsonify({
                'success': True,
                'description': result.description,
                'generation_time': result.generation_time,
                'model_used': result.model_used
            })
        else:
            return jsonify({
                'success': False,
                'error': result.error_message
            }), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate', methods=['POST'])
def generate_descriptions():
    """Gera descrições para produtos"""
    try:
        if not generator:
            return jsonify({'error': 'Gerador não disponível'}), 500
        
        data = request.get_json()
        
        if 'products' not in data:
            return jsonify({'error': 'Lista de produtos não fornecida'}), 400
        
        products = []
        for p in data['products']:
            product = Product(
                nome=p.get('nome', ''),
                material=p.get('material'),
                cor=p.get('cor'),
                descricao_fornecedor=p.get('descricao_fornecedor'),
                categoria1=p.get('categoria1'),
                categoria2=p.get('categoria2')
            )
            products.append(product)
        
        # Gerar descrições
        results = generator.generate_batch(products)
        
        # Preparar resposta
        response_data = []
        for result in results:
            response_data.append({
                'product_name': result.product.nome,
                'success': result.success,
                'description': result.description if result.success else None,
                'error': result.error_message if not result.success else None,
                'generation_time': result.generation_time
            })
        
        return jsonify({
            'success': True,
            'results': response_data,
            'total_processed': len(results),
            'successful': sum(1 for r in results if r.success)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload e processamento de planilha"""
    try:
        if not generator or not file_handler:
            return jsonify({'error': 'Serviços não disponíveis'}), 500
        
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        # Ler arquivo
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file.stream)
        else:
            df = pd.read_excel(file.stream)
        
        # Limpar dados
        df = file_handler.clean_data(df)
        
        # Validar colunas
        validation = file_handler.validate_columns(df)
        
        if not validation['valid']:
            return jsonify({
                'error': 'Colunas obrigatórias faltando',
                'missing': validation['missing_required']
            }), 400
        
        # Gerar descrições
        descriptions = generator.generate_from_dataframe(df)
        
        # Adicionar descrições ao DataFrame
        df['Descrição Comercial'] = descriptions
        
        # Converter para JSON para resposta
        result_data = df.to_dict('records')
        
        return jsonify({
            'success': True,
            'data': result_data,
            'total_products': len(df),
            'successful_generations': sum(1 for desc in descriptions if not desc.startswith('ERRO'))
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/template')
def download_template():
    """Download template de planilha"""
    try:
        if not file_handler:
            return jsonify({'error': 'File handler não disponível'}), 500
        
        # Criar template
        template_df = file_handler.create_template()
        
        # Converter para Excel em memória
        output = io.BytesIO()
        template_df.to_excel(output, index=False)
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='template_produtos.xlsx'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def get_stats():
    """Estatísticas do sistema"""
    try:
        stats = {}
        
        if generator:
            stats.update(generator.get_stats())
        
        if ai_client:
            stats['ollama_available'] = ai_client.is_available()
            models = ai_client.get_models()
            stats['models'] = [{'name': m.name, 'installed': m.installed} for m in models]
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    
    print(f"🚀 Iniciando API do Gerador de Descrições")
    print(f"📡 Porta: {port}")
    print(f"🔧 Debug: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)