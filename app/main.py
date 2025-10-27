#!/usr/bin/env python3
"""
Ponto de entrada principal da aplicação
"""

import sys
import os
import tkinter as tk
from pathlib import Path

# Adicionar o diretório raiz ao path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from app.ui.main_window import MainWindow
from app.core.logger import setup_logger

def main():
    """Função principal da aplicação"""
    try:
        # Configurar logging
        logger = setup_logger()
        logger.info("Iniciando Gerador de Descrições Pro v1.0.0")
        
        # Criar janela principal
        root = tk.Tk()
        app = MainWindow(root)
        
        # Configurações da janela
        root.title("Gerador de Descrições Pro v1.0.0")
        root.geometry("900x700")
        root.minsize(800, 600)
        
        # Ícone (se existir)
        icon_path = ROOT_DIR / "assets" / "icon.ico"
        if icon_path.exists():
            root.iconbitmap(str(icon_path))
        
        # Iniciar aplicação
        logger.info("Interface gráfica iniciada")
        root.mainloop()
        
    except Exception as e:
        print(f"Erro fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()