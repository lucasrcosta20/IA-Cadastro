#!/usr/bin/env python3
"""
Teste simples da aplicação
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

def main():
    print("🧪 Teste simples...")
    
    try:
        # Testar importação direta
        import app.ui.main_window as mw
        print("✅ Módulo main_window importado")
        
        # Verificar se a classe existe
        if hasattr(mw, 'MainWindow'):
            print("✅ Classe MainWindow encontrada")
            
            # Testar criação da classe (sem Tkinter)
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()
            
            app = mw.MainWindow(root)
            print("✅ MainWindow criada com sucesso")
            
            root.destroy()
            
        else:
            print("❌ Classe MainWindow não encontrada no módulo")
            print(f"Atributos disponíveis: {dir(mw)}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()