"""
Janela principal da aplicação
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import pandas as pd
from pathlib import Path

from .styles import UIStyles
from ..core.generator import DescriptionGenerator
from ..core.ai_client import AIClient
from ..core.logger import get_logger
from ..utils.file_handler import FileHandler

logger = get_logger(__name__)

class MainWindow:
    """Janela principal da aplicação"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.styles = UIStyles('dark')
        
        # Inicializar componentes
        try:
            self.generator = DescriptionGenerator()
            self.ai_client = AIClient()
        except Exception as e:
            logger.error(f"Erro ao inicializar componentes: {e}")
            # Usar versões mock para desenvolvimento
            self.generator = None
            self.ai_client = None
        
        # Dados
        self.df = None
        self.results = []
        
        # Configurar janela
        self._setup_window()
        self._create_widgets()
        self._check_system_status()
    
    def _setup_window(self):
        """Configura a janela principal"""
        self.root.configure(bg=self.styles.colors['bg_primary'])
        
        # Configurar grid
        self.root.grid_rowconfigure(0, weight=0)  # Header
        self.root.grid_rowconfigure(1, weight=1)  # Main content
        self.root.grid_rowconfigure(2, weight=0)  # Status bar
        self.root.grid_columnconfigure(0, weight=1)
    
    def _create_widgets(self):
        """Cria todos os widgets da interface"""
        self._create_header()
        self._create_main_content()
        self._create_status_bar()
    
    def _create_header(self):
        """Cria cabeçalho da aplicação"""
        header_frame = tk.Frame(self.root, **self.styles.get_frame_style('header'))
        header_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=5)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Logo/Título
        title_label = tk.Label(
            header_frame,
            text="🚀 Gerador de Descrições Pro",
            **self.styles.get_label_style('title')
        )
        title_label.grid(row=0, column=0, sticky='w', padx=10, pady=10)
        
        # Status do sistema
        self.system_status_label = tk.Label(
            header_frame,
            text="🔍 Verificando sistema...",
            **self.styles.get_label_style('secondary')
        )
        self.system_status_label.grid(row=0, column=1, sticky='e', padx=10, pady=10)
    
    def _create_main_content(self):
        """Cria conteúdo principal"""
        main_frame = tk.Frame(self.root, **self.styles.get_frame_style())
        main_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=5)
        main_frame.grid_rowconfigure(2, weight=1)  # Results area
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Seção de arquivo
        self._create_file_section(main_frame)
        
        # Seção de controles
        self._create_controls_section(main_frame)
        
        # Seção de resultados
        self._create_results_section(main_frame)
    
    def _create_file_section(self, parent):
        """Cria seção de seleção de arquivo"""
        file_frame = tk.LabelFrame(
            parent,
            text="📁 Arquivo de Dados",
            **self.styles.get_frame_style('card'),
            fg=self.styles.colors['fg_primary'],
            font=self.styles.get_font(11, 'bold')
        )
        file_frame.grid(row=0, column=0, sticky='ew', pady=5)
        file_frame.grid_columnconfigure(1, weight=1)
        
        # Campo de arquivo
        tk.Label(
            file_frame,
            text="Planilha:",
            **self.styles.get_label_style()
        ).grid(row=0, column=0, sticky='w', padx=10, pady=10)
        
        self.file_var = tk.StringVar()
        self.file_entry = tk.Entry(
            file_frame,
            textvariable=self.file_var,
            **self.styles.get_entry_style()
        )
        self.file_entry.grid(row=0, column=1, sticky='ew', padx=10, pady=10)
        
        # Botões de arquivo
        btn_frame = tk.Frame(file_frame, **self.styles.get_frame_style())
        btn_frame.grid(row=0, column=2, padx=10, pady=10)
        
        tk.Button(
            btn_frame,
            text="📂 Procurar",
            command=self._browse_file,
            **self.styles.get_button_style('primary')
        ).pack(side='left', padx=2)
        
        tk.Button(
            btn_frame,
            text="📋 Template",
            command=self._create_template,
            **self.styles.get_button_style('secondary')
        ).pack(side='left', padx=2)
        
        # Info do arquivo
        self.file_info_label = tk.Label(
            file_frame,
            text="Nenhum arquivo selecionado",
            **self.styles.get_label_style('secondary')
        )
        self.file_info_label.grid(row=1, column=0, columnspan=3, sticky='w', padx=10, pady=5)
    
    def _create_controls_section(self, parent):
        """Cria seção de controles"""
        controls_frame = tk.LabelFrame(
            parent,
            text="⚙️ Controles",
            **self.styles.get_frame_style('card'),
            fg=self.styles.colors['fg_primary'],
            font=self.styles.get_font(11, 'bold')
        )
        controls_frame.grid(row=1, column=0, sticky='ew', pady=5)
        
        # Botões principais
        btn_main_frame = tk.Frame(controls_frame, **self.styles.get_frame_style())
        btn_main_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(
            btn_main_frame,
            text="🚀 Gerar Descrições",
            command=self._start_generation,
            **self.styles.get_button_style('success')
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_main_frame,
            text="💾 Salvar Resultados",
            command=self._save_results,
            **self.styles.get_button_style('primary')
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_main_frame,
            text="👁️ Visualizar",
            command=self._preview_results,
            **self.styles.get_button_style('secondary')
        ).pack(side='left', padx=5)
        
        # Barra de progresso
        progress_frame = tk.Frame(controls_frame, **self.styles.get_frame_style())
        progress_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            progress_frame,
            text="Progresso:",
            **self.styles.get_label_style()
        ).pack(side='left', padx=5)
        
        self.progress = ttk.Progressbar(
            progress_frame,
            mode='determinate',
            length=300
        )
        self.progress.pack(side='left', fill='x', expand=True, padx=5)
        
        self.progress_label = tk.Label(
            progress_frame,
            text="0/0 (0%)",
            **self.styles.get_label_style('secondary')
        )
        self.progress_label.pack(side='right', padx=5)
    
    def _create_results_section(self, parent):
        """Cria seção de resultados"""
        results_frame = tk.LabelFrame(
            parent,
            text="📊 Resultados",
            **self.styles.get_frame_style('card'),
            fg=self.styles.colors['fg_primary'],
            font=self.styles.get_font(11, 'bold')
        )
        results_frame.grid(row=2, column=0, sticky='nsew', pady=5)
        results_frame.grid_rowconfigure(0, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)
        
        # Área de texto com scrollbar
        text_frame = tk.Frame(results_frame, **self.styles.get_frame_style())
        text_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)
        
        self.results_text = tk.Text(
            text_frame,
            **self.styles.get_text_style(),
            wrap=tk.WORD,
            state='disabled'
        )
        self.results_text.grid(row=0, column=0, sticky='nsew')
        
        # Scrollbar
        scrollbar = tk.Scrollbar(text_frame, orient='vertical', command=self.results_text.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.results_text.configure(yscrollcommand=scrollbar.set)
    
    def _create_status_bar(self):
        """Cria barra de status"""
        status_frame = tk.Frame(self.root, **self.styles.get_frame_style('header'))
        status_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=5)
        status_frame.grid_columnconfigure(1, weight=1)
        
        self.status_label = tk.Label(
            status_frame,
            text="Pronto",
            **self.styles.get_label_style('secondary')
        )
        self.status_label.grid(row=0, column=0, sticky='w', padx=10, pady=5)
    
    def _check_system_status(self):
        """Verifica status do sistema"""
        def check():
            try:
                if self.ai_client and self.ai_client.is_available():
                    self.system_status_label.configure(
                        text="✅ Sistema OK",
                        **self.styles.get_label_style('success')
                    )
                else:
                    self.system_status_label.configure(
                        text="❌ Ollama offline",
                        **self.styles.get_label_style('error')
                    )
            except Exception as e:
                logger.error(f"Erro ao verificar sistema: {e}")
                self.system_status_label.configure(
                    text="❌ Erro no sistema",
                    **self.styles.get_label_style('error')
                )
        
        # Executar em thread separada
        threading.Thread(target=check, daemon=True).start()
    
    def _browse_file(self):
        """Abre diálogo para selecionar arquivo"""
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
            self._load_file(filename)
    
    def _load_file(self, filename: str):
        """Carrega arquivo selecionado"""
        try:
            self.df = FileHandler.read_file(filename)
            
            if self.df is not None:
                # Limpar dados
                self.df = FileHandler.clean_data(self.df)
                
                # Validar colunas
                validation = FileHandler.validate_columns(self.df)
                
                if validation['valid']:
                    info_text = f"✅ {validation['total_rows']} produtos carregados"
                    self.file_info_label.configure(
                        text=info_text,
                        **self.styles.get_label_style('success')
                    )
                    self._update_status(f"Arquivo carregado: {Path(filename).name}")
                else:
                    missing = ", ".join(validation['missing_required'])
                    info_text = f"❌ Colunas obrigatórias faltando: {missing}"
                    self.file_info_label.configure(
                        text=info_text,
                        **self.styles.get_label_style('error')
                    )
            else:
                self.file_info_label.configure(
                    text="❌ Erro ao carregar arquivo",
                    **self.styles.get_label_style('error')
                )
                
        except Exception as e:
            logger.error(f"Erro ao carregar arquivo: {e}")
            messagebox.showerror("Erro", f"Erro ao carregar arquivo:\n{e}")
    
    def _create_template(self):
        """Cria template de planilha"""
        filename = filedialog.asksaveasfilename(
            title="Salvar template",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )
        
        if filename:
            if FileHandler.export_template(filename):
                messagebox.showinfo("Sucesso", f"Template criado em:\n{filename}")
                self._update_status("Template criado com sucesso")
            else:
                messagebox.showerror("Erro", "Erro ao criar template")
    
    def _start_generation(self):
        """Inicia geração de descrições"""
        if self.df is None:
            messagebox.showwarning("Aviso", "Carregue um arquivo primeiro!")
            return
        
        if not self.generator:
            messagebox.showerror("Erro", "Gerador não disponível!")
            return
        
        # Executar em thread separada
        threading.Thread(target=self._generate_descriptions, daemon=True).start()
    
    def _generate_descriptions(self):
        """Gera descrições (executado em thread separada)"""
        try:
            self._update_status("Iniciando geração...")
            self.progress['value'] = 0
            self.progress['maximum'] = len(self.df)
            
            def progress_callback(current, total):
                self.progress['value'] = current
                percentage = int((current / total) * 100)
                self.progress_label.configure(text=f"{current}/{total} ({percentage}%)")
                self._update_status(f"Gerando... {current}/{total}")
                self.root.update_idletasks()
            
            # Gerar descrições
            descriptions = self.generator.generate_from_dataframe(
                self.df, 
                progress_callback=progress_callback
            )
            
            # Adicionar coluna de descrições
            self.df['Descrição Comercial'] = descriptions
            
            # Mostrar resultados
            self._display_results()
            
            # Estatísticas
            successful = sum(1 for desc in descriptions if not desc.startswith('ERRO'))
            
            self._update_status(f"Concluído: {successful}/{len(descriptions)} sucessos")
            
            # Som de conclusão (opcional)
            self.root.bell()
            
        except Exception as e:
            logger.error(f"Erro na geração: {e}")
            self._update_status(f"Erro: {e}")
            messagebox.showerror("Erro", f"Erro na geração:\n{e}")
    
    def _display_results(self):
        """Exibe resultados na área de texto"""
        self.results_text.configure(state='normal')
        self.results_text.delete('1.0', tk.END)
        
        for i, row in self.df.iterrows():
            nome = row.get('Nome', '')
            descricao = row.get('Descrição Comercial', '')
            
            self.results_text.insert(tk.END, f"📦 {nome}\n")
            self.results_text.insert(tk.END, f"{descricao}\n")
            self.results_text.insert(tk.END, "-" * 80 + "\n\n")
        
        self.results_text.configure(state='disabled')
    
    def _save_results(self):
        """Salva resultados em arquivo"""
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
            if FileHandler.save_file(self.df, filename):
                messagebox.showinfo("Sucesso", f"Resultados salvos em:\n{filename}")
                self._update_status(f"Resultados salvos: {Path(filename).name}")
            else:
                messagebox.showerror("Erro", "Erro ao salvar arquivo")
    
    def _preview_results(self):
        """Abre janela de preview dos resultados"""
        if self.df is None:
            messagebox.showwarning("Aviso", "Nenhum dado para visualizar!")
            return
        
        # Implementar janela de preview (placeholder)
        messagebox.showinfo("Preview", "Funcionalidade de preview em desenvolvimento")
    
    def _update_status(self, message: str):
        """Atualiza mensagem de status"""
        self.status_label.configure(text=message)
        logger.info(f"Status: {message}")