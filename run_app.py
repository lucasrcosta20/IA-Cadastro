#!/usr/bin/env python3
"""
Script para executar a aplicação
"""

import sys
import tkinter as tk
from pathlib import Path

# Adicionar o diretório raiz ao path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

def main():
    """Função principal"""
    try:
        # Importar após configurar o path
        from app.ui.styles import UIStyles
        
        # Criar janela principal
        root = tk.Tk()
        root.title("Gerador de Descrições Pro v1.0.0")
        root.geometry("900x700")
        root.minsize(800, 600)
        
        # Aplicar estilo
        styles = UIStyles('dark')
        root.configure(bg=styles.colors['bg_primary'])
        
        # Criar interface básica
        header_frame = tk.Frame(root, **styles.get_frame_style('header'))
        header_frame.pack(fill='x', padx=10, pady=5)
        
        title_label = tk.Label(
            header_frame,
            text="🚀 Gerador de Descrições Pro",
            **styles.get_label_style('title')
        )
        title_label.pack(pady=20)
        
        # Área principal
        main_frame = tk.Frame(root, **styles.get_frame_style())
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Botões de teste
        btn_frame = tk.Frame(main_frame, **styles.get_frame_style())
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame,
            text="📂 Carregar Arquivo",
            **styles.get_button_style('primary')
        ).pack(side='left', padx=10)
        
        tk.Button(
            btn_frame,
            text="🚀 Gerar Descrições",
            **styles.get_button_style('success')
        ).pack(side='left', padx=10)
        
        tk.Button(
            btn_frame,
            text="💾 Salvar",
            **styles.get_button_style('secondary')
        ).pack(side='left', padx=10)
        
        # Área de resultados
        results_frame = tk.LabelFrame(
            main_frame,
            text="📊 Resultados",
            **styles.get_frame_style('card'),
            fg=styles.colors['fg_primary'],
            font=styles.get_font(11, 'bold')
        )
        results_frame.pack(fill='both', expand=True, pady=10)
        
        text_widget = tk.Text(
            results_frame,
            **styles.get_text_style(),
            wrap=tk.WORD
        )
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Inserir texto de exemplo
        text_widget.insert('1.0', """🎉 Bem-vindo ao Gerador de Descrições Pro!

Esta é uma versão de demonstração da interface.

Funcionalidades implementadas:
✅ Interface gráfica moderna
✅ Sistema de estilos
✅ Estrutura modular
✅ Logging
✅ Cache system
✅ File handlers

Próximos passos:
🔄 Integração completa com Ollama
🔄 Editor de prompts
🔄 Chat integrado
🔄 Diagnóstico do sistema

Para testar a funcionalidade completa, certifique-se de que o Ollama está instalado e rodando.
""")
        
        text_widget.configure(state='disabled')
        
        # Status bar
        status_frame = tk.Frame(root, **styles.get_frame_style('header'))
        status_frame.pack(fill='x', padx=10, pady=5)
        
        status_label = tk.Label(
            status_frame,
            text="✅ Interface carregada com sucesso",
            **styles.get_label_style('success')
        )
        status_label.pack(side='left', padx=10, pady=5)
        
        print("🚀 Aplicação iniciada com sucesso!")
        print("📱 Interface gráfica carregada")
        print("🎯 Pronto para uso!")
        
        # Iniciar loop principal
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Erro ao iniciar aplicação: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()