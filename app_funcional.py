#!/usr/bin/env python3
"""
Aplicação funcional completa do Gerador de Descrições
"""

import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import pandas as pd
from pathlib import Path

# Adicionar o diretório raiz ao path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

class GeradorDescricoesApp:
    """Aplicação principal do Gerador de Descrições"""
    
    def __init__(self, root):
        self.root = root
        self.df = None
        self.results = []
        
        # Importar módulos
        try:
            from app.ui.styles import UIStyles
            from app.core.generator import DescriptionGenerator
            from app.core.ai_client import AIClient
            from app.utils.file_handler import FileHandler
            
            self.styles = UIStyles('dark')
            self.generator = DescriptionGenerator()
            self.ai_client = AIClient()
            self.file_handler = FileHandler()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar módulos:\n{e}")
            sys.exit(1)
        
        self.setup_window()
        self.create_widgets()
        self.check_system()
    
    def setup_window(self):
        """Configura a janela principal"""
        self.root.title("🚀 Gerador de Descrições Pro v1.0")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        self.root.configure(bg=self.styles.colors['bg_primary'])
    
    def create_widgets(self):
        """Cria todos os widgets"""
        # Header
        header_frame = tk.Frame(self.root, **self.styles.get_frame_style('header'))
        header_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            header_frame,
            text="🚀 Gerador de Descrições Pro",
            **self.styles.get_label_style('title')
        ).pack(side='left', padx=10, pady=10)
        
        self.status_system = tk.Label(
            header_frame,
            text="🔍 Verificando...",
            **self.styles.get_label_style('secondary')
        )
        self.status_system.pack(side='right', padx=10, pady=10)
        
        # Arquivo
        file_frame = tk.LabelFrame(
            self.root,
            text="📁 Arquivo de Dados",
            **self.styles.get_frame_style('card'),
            fg=self.styles.colors['fg_primary'],
            font=self.styles.get_font(11, 'bold')
        )
        file_frame.pack(fill='x', padx=10, pady=5)
        
        file_inner = tk.Frame(file_frame, **self.styles.get_frame_style())
        file_inner.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            file_inner,
            text="Planilha:",
            **self.styles.get_label_style()
        ).pack(side='left', padx=5)
        
        self.file_var = tk.StringVar()
        self.file_entry = tk.Entry(
            file_inner,
            textvariable=self.file_var,
            **self.styles.get_entry_style(),
            width=50
        )
        self.file_entry.pack(side='left', padx=5, fill='x', expand=True)
        
        tk.Button(
            file_inner,
            text="📂 Procurar",
            command=self.browse_file,
            **self.styles.get_button_style('primary')
        ).pack(side='right', padx=5)
        
        tk.Button(
            file_inner,
            text="📋 Template",
            command=self.create_template,
            **self.styles.get_button_style('secondary')
        ).pack(side='right', padx=2)
        
        self.file_info = tk.Label(
            file_frame,
            text="Nenhum arquivo selecionado",
            **self.styles.get_label_style('secondary')
        )
        self.file_info.pack(anchor='w', padx=10, pady=5)
        
        # Controles
        controls_frame = tk.LabelFrame(
            self.root,
            text="⚙️ Controles",
            **self.styles.get_frame_style('card'),
            fg=self.styles.colors['fg_primary'],
            font=self.styles.get_font(11, 'bold')
        )
        controls_frame.pack(fill='x', padx=10, pady=5)
        
        btn_frame = tk.Frame(controls_frame, **self.styles.get_frame_style())
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(
            btn_frame,
            text="🚀 Gerar Descrições",
            command=self.start_generation,
            **self.styles.get_button_style('success')
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="💾 Salvar Resultados",
            command=self.save_results,
            **self.styles.get_button_style('primary')
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="🧪 Teste Rápido",
            command=self.quick_test,
            **self.styles.get_button_style('warning')
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="🗑️ Limpar Cache",
            command=self.clear_cache,
            **self.styles.get_button_style('error')
        ).pack(side='right', padx=5)
        
        # Progresso
        progress_frame = tk.Frame(controls_frame, **self.styles.get_frame_style())
        progress_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            progress_frame,
            text="Progresso:",
            **self.styles.get_label_style()
        ).pack(side='left', padx=5)
        
        self.progress = ttk.Progressbar(
            progress_frame,
            mode='determinate',
            length=400
        )
        self.progress.pack(side='left', fill='x', expand=True, padx=5)
        
        self.progress_label = tk.Label(
            progress_frame,
            text="0/0 (0%)",
            **self.styles.get_label_style('secondary')
        )
        self.progress_label.pack(side='right', padx=5)
        
        # Resultados
        results_frame = tk.LabelFrame(
            self.root,
            text="📊 Resultados",
            **self.styles.get_frame_style('card'),
            fg=self.styles.colors['fg_primary'],
            font=self.styles.get_font(11, 'bold')
        )
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Área de texto com scrollbar
        text_frame = tk.Frame(results_frame, **self.styles.get_frame_style())
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.results_text = tk.Text(
            text_frame,
            **self.styles.get_text_style(),
            wrap=tk.WORD
        )
        self.results_text.pack(side='left', fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(text_frame, orient='vertical', command=self.results_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        # Status bar
        status_frame = tk.Frame(self.root, **self.styles.get_frame_style('header'))
        status_frame.pack(fill='x', padx=10, pady=5)
        
        self.status_label = tk.Label(
            status_frame,
            text="Pronto",
            **self.styles.get_label_style('secondary')
        )
        self.status_label.pack(side='left', padx=10, pady=5)
        
        self.stats_label = tk.Label(
            status_frame,
            text="",
            **self.styles.get_label_style('secondary')
        )
        self.stats_label.pack(side='right', padx=10, pady=5)
    
    def check_system(self):
        """Verifica status do sistema"""
        def check():
            try:
                if self.ai_client.is_available():
                    models = self.ai_client.get_models()
                    installed = [m for m in models if m.installed]
                    
                    if installed:
                        self.status_system.configure(
                            text=f"✅ Ollama OK ({len(installed)} modelos)",
                            **self.styles.get_label_style('success')
                        )
                    else:
                        self.status_system.configure(
                            text="⚠️ Nenhum modelo instalado",
                            **self.styles.get_label_style('warning')
                        )
                else:
                    self.status_system.configure(
                        text="❌ Ollama offline",
                        **self.styles.get_label_style('error')
                    )
            except Exception as e:
                self.status_system.configure(
                    text="❌ Erro no sistema",
                    **self.styles.get_label_style('error')
                )
        
        threading.Thread(target=check, daemon=True).start()
    
    def browse_file(self):
        """Procura arquivo"""
        file_types = [
            ("Arquivos Excel", "*.xlsx *.xls"),
            ("Arquivos CSV", "*.csv"),
            ("Todos os arquivos", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Selecionar arquivo de dados",
            filetypes=file_types
        )
        
        if filename:
            self.file_var.set(filename)
            self.load_file(filename)
    
    def load_file(self, filename):
        """Carrega arquivo"""
        try:
            self.df = self.file_handler.read_file(filename)
            
            if self.df is not None:
                self.df = self.file_handler.clean_data(self.df)
                validation = self.file_handler.validate_columns(self.df)
                
                if validation['valid']:
                    info_text = f"✅ {validation['total_rows']} produtos carregados"
                    self.file_info.configure(
                        text=info_text,
                        **self.styles.get_label_style('success')
                    )
                    self.update_status(f"Arquivo carregado: {Path(filename).name}")
                else:
                    missing = ", ".join(validation['missing_required'])
                    info_text = f"❌ Colunas obrigatórias faltando: {missing}"
                    self.file_info.configure(
                        text=info_text,
                        **self.styles.get_label_style('error')
                    )
            else:
                self.file_info.configure(
                    text="❌ Erro ao carregar arquivo",
                    **self.styles.get_label_style('error')
                )
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar arquivo:\n{e}")
    
    def create_template(self):
        """Cria template"""
        filename = filedialog.asksaveasfilename(
            title="Salvar template",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )
        
        if filename:
            if self.file_handler.export_template(filename):
                messagebox.showinfo("Sucesso", f"Template criado em:\n{filename}")
                self.update_status("Template criado com sucesso")
            else:
                messagebox.showerror("Erro", "Erro ao criar template")
    
    def start_generation(self):
        """Inicia geração"""
        if self.df is None:
            messagebox.showwarning("Aviso", "Carregue um arquivo primeiro!")
            return
        
        if not self.ai_client.is_available():
            messagebox.showerror("Erro", "Ollama não está disponível!")
            return
        
        threading.Thread(target=self.generate_descriptions, daemon=True).start()
    
    def generate_descriptions(self):
        """Gera descrições"""
        try:
            self.update_status("Iniciando geração...")
            self.progress['value'] = 0
            self.progress['maximum'] = len(self.df)
            
            def progress_callback(current, total):
                self.progress['value'] = current
                percentage = int((current / total) * 100)
                self.progress_label.configure(text=f"{current}/{total} ({percentage}%)")
                self.update_status(f"Gerando... {current}/{total}")
                self.root.update_idletasks()
            
            descriptions = self.generator.generate_from_dataframe(
                self.df, 
                progress_callback=progress_callback
            )
            
            self.df['Descrição Comercial'] = descriptions
            self.display_results()
            
            successful = sum(1 for desc in descriptions if not desc.startswith('ERRO'))
            self.update_status(f"Concluído: {successful}/{len(descriptions)} sucessos")
            
            # Som de conclusão
            self.root.bell()
            
        except Exception as e:
            self.update_status(f"Erro: {e}")
            messagebox.showerror("Erro", f"Erro na geração:\n{e}")
    
    def display_results(self):
        """Exibe resultados"""
        self.results_text.delete('1.0', tk.END)
        
        for i, row in self.df.iterrows():
            nome = row.get('Nome', '')
            descricao = row.get('Descrição Comercial', '')
            
            self.results_text.insert(tk.END, f"📦 {nome}\n")
            self.results_text.insert(tk.END, f"{descricao}\n")
            self.results_text.insert(tk.END, "-" * 80 + "\n\n")
    
    def save_results(self):
        """Salva resultados"""
        if self.df is None or 'Descrição Comercial' not in self.df.columns:
            messagebox.showwarning("Aviso", "Nenhum resultado para salvar!")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Salvar resultados",
            defaultextension=".xlsx",
            filetypes=[
                ("Excel files", "*.xlsx"),
                ("CSV files", "*.csv")
            ]
        )
        
        if filename:
            if self.file_handler.save_file(self.df, filename):
                messagebox.showinfo("Sucesso", f"Resultados salvos em:\n{filename}")
                self.update_status(f"Resultados salvos: {Path(filename).name}")
            else:
                messagebox.showerror("Erro", "Erro ao salvar arquivo")
    
    def quick_test(self):
        """Teste rápido"""
        def test():
            try:
                from app.core.models import Product
                
                product = Product(
                    nome="Produto Teste",
                    material="Plástico",
                    cor="Azul",
                    descricao_fornecedor="Produto de teste",
                    categoria1="Teste",
                    categoria2="Demo"
                )
                
                self.update_status("Executando teste rápido...")
                result = self.generator.generate_single(product, use_cache=False)
                
                if result.success:
                    self.results_text.delete('1.0', tk.END)
                    self.results_text.insert('1.0', f"🧪 TESTE RÁPIDO\n\n")
                    self.results_text.insert(tk.END, f"📦 {product.nome}\n")
                    self.results_text.insert(tk.END, f"⏱️ Tempo: {result.generation_time:.2f}s\n")
                    self.results_text.insert(tk.END, f"🤖 Modelo: {result.model_used}\n\n")
                    self.results_text.insert(tk.END, f"📝 Descrição:\n{result.description}\n")
                    
                    self.update_status(f"Teste concluído em {result.generation_time:.2f}s")
                else:
                    messagebox.showerror("Erro", f"Falha no teste: {result.error_message}")
                    
            except Exception as e:
                messagebox.showerror("Erro", f"Erro no teste: {e}")
        
        threading.Thread(target=test, daemon=True).start()
    
    def clear_cache(self):
        """Limpa cache"""
        try:
            self.generator.clear_cache()
            self.update_status("Cache limpo com sucesso")
            messagebox.showinfo("Sucesso", "Cache limpo com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao limpar cache: {e}")
    
    def update_status(self, message):
        """Atualiza status"""
        self.status_label.configure(text=message)
        print(f"Status: {message}")

def main():
    """Função principal"""
    try:
        root = tk.Tk()
        app = GeradorDescricoesApp(root)
        
        print("🚀 Aplicação funcional iniciada!")
        print("📱 Interface com botões funcionais carregada")
        print("🎯 Pronto para gerar descrições!")
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        messagebox.showerror("Erro Fatal", f"Erro ao iniciar aplicação:\n{e}")

if __name__ == "__main__":
    main()