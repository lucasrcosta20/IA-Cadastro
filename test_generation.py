#!/usr/bin/env python3
"""
Teste de geração de descrições
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

def test_ollama_connection():
    """Testa conexão com Ollama"""
    print("🔍 Testando conexão com Ollama...")
    
    try:
        from app.core.ai_client import AIClient
        
        client = AIClient()
        
        if client.is_available():
            print("✅ Ollama está rodando")
            
            # Listar modelos
            models = client.get_models()
            installed_models = [m for m in models if m.installed]
            
            if installed_models:
                print(f"✅ {len(installed_models)} modelos instalados:")
                for model in installed_models:
                    print(f"   • {model.name} ({model.size})")
                return True, installed_models[0].id
            else:
                print("⚠️ Nenhum modelo instalado")
                return False, None
        else:
            print("❌ Ollama não está rodando")
            return False, None
            
    except Exception as e:
        print(f"❌ Erro ao conectar com Ollama: {e}")
        return False, None

def test_description_generation():
    """Testa geração de descrição"""
    print("\n🚀 Testando geração de descrição...")
    
    try:
        from app.core.generator import DescriptionGenerator
        from app.core.models import Product
        
        # Criar produto de teste
        product = Product(
            nome="Vaso Decorativo Moderno",
            material="Cerâmica",
            cor="Branco",
            descricao_fornecedor="Vaso elegante para decoração",
            categoria1="Decoração",
            categoria2="Casa"
        )
        
        # Criar gerador
        generator = DescriptionGenerator()
        
        # Testar geração
        print("⏳ Gerando descrição...")
        result = generator.generate_single(product, use_cache=False)
        
        if result.success:
            print("✅ Descrição gerada com sucesso!")
            print(f"⏱️ Tempo: {result.generation_time:.2f}s")
            print(f"🤖 Modelo: {result.model_used}")
            print(f"📝 Descrição:\n{result.description}")
            return True
        else:
            print(f"❌ Falha na geração: {result.error_message}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na geração: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_batch_generation():
    """Testa geração em lote"""
    print("\n📦 Testando geração em lote...")
    
    try:
        import pandas as pd
        from app.core.generator import DescriptionGenerator
        
        # Criar DataFrame de teste
        test_data = {
            'Nome': [
                'Caneca Personalizada',
                'Almofada Decorativa',
                'Quadro Abstrato'
            ],
            'Material': ['Cerâmica', 'Algodão', 'Canvas'],
            'Cor': ['Azul', 'Bege', 'Colorido'],
            'Descrição Fornecedor': [
                'Caneca para café',
                'Almofada macia',
                'Arte moderna'
            ],
            'Categoria 1': ['Casa', 'Decoração', 'Arte'],
            'Categoria 2': ['Cozinha', 'Sala', 'Quadros']
        }
        
        df = pd.DataFrame(test_data)
        
        # Criar gerador
        generator = DescriptionGenerator()
        
        # Callback de progresso
        def progress_callback(current, total):
            print(f"   Progresso: {current}/{total}")
        
        # Gerar descrições
        print("⏳ Gerando descrições em lote...")
        descriptions = generator.generate_from_dataframe(df, progress_callback)
        
        # Verificar resultados
        successful = sum(1 for desc in descriptions if not desc.startswith('ERRO'))
        print(f"✅ Geração concluída: {successful}/{len(descriptions)} sucessos")
        
        # Mostrar resultados
        for i, (nome, desc) in enumerate(zip(df['Nome'], descriptions)):
            print(f"\n📦 {nome}:")
            print(f"   {desc[:100]}...")
        
        return successful > 0
        
    except Exception as e:
        print(f"❌ Erro na geração em lote: {e}")
        return False

def main():
    """Função principal"""
    print("🧪 TESTE DE GERAÇÃO - Gerador de Descrições Pro")
    print("=" * 60)
    
    # Teste 1: Conexão com Ollama
    ollama_ok, model_id = test_ollama_connection()
    
    if not ollama_ok:
        print("\n❌ Ollama não está disponível. Certifique-se de que:")
        print("1. Ollama está instalado")
        print("2. Ollama está rodando (ollama serve)")
        print("3. Pelo menos um modelo está instalado (ollama pull gemma2:2b)")
        return False
    
    # Teste 2: Geração única
    single_ok = test_description_generation()
    
    if not single_ok:
        print("\n❌ Falha na geração única")
        return False
    
    # Teste 3: Geração em lote
    batch_ok = test_batch_generation()
    
    print("\n" + "=" * 60)
    
    if single_ok and batch_ok:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ O programa está pronto para gerar descrições!")
        print("\n📚 Para usar:")
        print("1. Execute: python run_app.py")
        print("2. Carregue uma planilha Excel/CSV")
        print("3. Clique em 'Gerar Descrições'")
        return True
    else:
        print("⚠️ Alguns testes falharam")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)