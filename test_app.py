#!/usr/bin/env python3
"""
Script de teste da aplicação
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

def test_imports():
    """Testa importações dos módulos"""
    print("🧪 Testando importações...")
    
    try:
        from app.core.models import Product, GenerationResult, AIModel
        print("✅ Models OK")
        
        from app.core.ai_client import AIClient
        print("✅ AI Client OK")
        
        from app.core.cache import CacheManager
        print("✅ Cache Manager OK")
        
        from app.core.generator import DescriptionGenerator
        print("✅ Description Generator OK")
        
        from app.utils.prompt_manager import PromptManager
        print("✅ Prompt Manager OK")
        
        from app.utils.file_handler import FileHandler
        print("✅ File Handler OK")
        
        from app.ui.styles import UIStyles
        print("✅ UI Styles OK")
        
        from app.ui.main_window import MainWindow
        print("✅ Main Window OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na importação: {e}")
        return False

def test_basic_functionality():
    """Testa funcionalidades básicas"""
    print("\n🔧 Testando funcionalidades básicas...")
    
    try:
        # Testar modelo Product
        from app.core.models import Product
        product = Product(
            nome="Produto Teste",
            material="Plástico",
            cor="Azul"
        )
        print(f"✅ Produto criado: {product.nome}")
        
        # Testar PromptManager
        from app.utils.prompt_manager import PromptManager
        pm = PromptManager()
        prompt = pm.format_prompt(product)
        print("✅ Prompt formatado com sucesso")
        
        # Testar FileHandler
        from app.utils.file_handler import FileHandler
        template_df = FileHandler.create_template()
        print(f"✅ Template criado: {len(template_df)} linhas")
        
        # Testar CacheManager
        from app.core.cache import CacheManager
        cache = CacheManager()
        print(f"✅ Cache inicializado: {cache.size()} entradas")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ui():
    """Testa interface gráfica"""
    print("\n🖥️ Testando interface gráfica...")
    
    try:
        import tkinter as tk
        from app.ui.main_window import MainWindow
        
        # Criar janela de teste
        root = tk.Tk()
        root.withdraw()  # Esconder janela
        
        app = MainWindow(root)
        print("✅ Interface criada com sucesso")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ Erro na interface: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🚀 TESTE - Gerador de Descrições Pro")
    print("=" * 50)
    
    tests = [
        ("Importações", test_imports),
        ("Funcionalidades", test_basic_functionality),
        ("Interface", test_ui)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSOU")
            else:
                print(f"❌ {test_name}: FALHOU")
        except Exception as e:
            print(f"❌ {test_name}: ERRO - {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! Aplicação pronta para uso.")
        print("\n📚 Para executar:")
        print("python app/main.py")
    else:
        print("⚠️ Alguns testes falharam. Verifique os erros acima.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)