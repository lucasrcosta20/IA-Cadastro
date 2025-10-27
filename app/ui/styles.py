"""
Estilos e temas da interface gráfica
"""

import tkinter as tk
from typing import Dict, Any

class UIStyles:
    """Classe para gerenciar estilos da UI"""
    
    # Cores do tema escuro
    DARK_THEME = {
        'bg_primary': '#2C3E50',
        'bg_secondary': '#34495E', 
        'bg_tertiary': '#3A4A5C',
        'bg_input': '#4A5A6C',
        'fg_primary': '#ECF0F1',
        'fg_secondary': '#BDC3C7',
        'fg_accent': '#3498DB',
        'success': '#27AE60',
        'warning': '#F39C12',
        'error': '#E74C3C',
        'info': '#3498DB'
    }
    
    # Cores do tema claro
    LIGHT_THEME = {
        'bg_primary': '#FFFFFF',
        'bg_secondary': '#F8F9FA',
        'bg_tertiary': '#E9ECEF',
        'bg_input': '#FFFFFF',
        'fg_primary': '#212529',
        'fg_secondary': '#6C757D',
        'fg_accent': '#007BFF',
        'success': '#28A745',
        'warning': '#FFC107',
        'error': '#DC3545',
        'info': '#17A2B8'
    }
    
    def __init__(self, theme: str = 'dark'):
        self.theme = theme
        self.colors = self.DARK_THEME if theme == 'dark' else self.LIGHT_THEME
        
    def get_font(self, size: int = 10, weight: str = 'normal') -> tuple:
        """Retorna configuração de fonte"""
        return ('Roboto Mono', size, weight)
    
    def get_button_style(self, variant: str = 'primary') -> Dict[str, Any]:
        """Retorna estilo para botões"""
        base_style = {
            'font': self.get_font(10, 'bold'),
            'relief': 'flat',
            'bd': 0,
            'padx': 15,
            'pady': 8,
            'cursor': 'hand2'
        }
        
        if variant == 'primary':
            base_style.update({
                'bg': self.colors['fg_accent'],
                'fg': '#FFFFFF',
                'activebackground': '#2980B9',
                'activeforeground': '#FFFFFF'
            })
        elif variant == 'success':
            base_style.update({
                'bg': self.colors['success'],
                'fg': '#FFFFFF',
                'activebackground': '#229954',
                'activeforeground': '#FFFFFF'
            })
        elif variant == 'warning':
            base_style.update({
                'bg': self.colors['warning'],
                'fg': '#FFFFFF',
                'activebackground': '#D68910',
                'activeforeground': '#FFFFFF'
            })
        elif variant == 'error':
            base_style.update({
                'bg': self.colors['error'],
                'fg': '#FFFFFF',
                'activebackground': '#C0392B',
                'activeforeground': '#FFFFFF'
            })
        else:  # secondary
            base_style.update({
                'bg': self.colors['bg_tertiary'],
                'fg': self.colors['fg_primary'],
                'activebackground': self.colors['bg_secondary'],
                'activeforeground': self.colors['fg_primary']
            })
            
        return base_style
    
    def get_entry_style(self) -> Dict[str, Any]:
        """Retorna estilo para campos de entrada"""
        return {
            'bg': self.colors['bg_input'],
            'fg': self.colors['fg_primary'],
            'font': self.get_font(10),
            'relief': 'solid',
            'bd': 1,
            'insertbackground': self.colors['fg_primary']
        }
    
    def get_label_style(self, variant: str = 'primary') -> Dict[str, Any]:
        """Retorna estilo para labels"""
        base_style = {
            'bg': self.colors['bg_primary'],
            'font': self.get_font(10)
        }
        
        if variant == 'title':
            base_style.update({
                'fg': self.colors['fg_primary'],
                'font': self.get_font(14, 'bold')
            })
        elif variant == 'subtitle':
            base_style.update({
                'fg': self.colors['fg_secondary'],
                'font': self.get_font(12, 'bold')
            })
        elif variant == 'success':
            base_style.update({
                'fg': self.colors['success'],
                'font': self.get_font(10, 'bold')
            })
        elif variant == 'error':
            base_style.update({
                'fg': self.colors['error'],
                'font': self.get_font(10, 'bold')
            })
        elif variant == 'warning':
            base_style.update({
                'fg': self.colors['warning'],
                'font': self.get_font(10, 'bold')
            })
        else:  # primary
            base_style.update({
                'fg': self.colors['fg_primary']
            })
            
        return base_style
    
    def get_frame_style(self, variant: str = 'primary') -> Dict[str, Any]:
        """Retorna estilo para frames"""
        if variant == 'header':
            return {
                'bg': self.colors['bg_secondary'],
                'relief': 'flat',
                'bd': 0
            }
        elif variant == 'card':
            return {
                'bg': self.colors['bg_tertiary'],
                'relief': 'solid',
                'bd': 1
            }
        else:  # primary
            return {
                'bg': self.colors['bg_primary'],
                'relief': 'flat',
                'bd': 0
            }
    
    def get_text_style(self) -> Dict[str, Any]:
        """Retorna estilo para widgets Text"""
        return {
            'bg': self.colors['bg_input'],
            'fg': self.colors['fg_primary'],
            'font': self.get_font(10),
            'relief': 'solid',
            'bd': 1,
            'insertbackground': self.colors['fg_primary'],
            'selectbackground': self.colors['fg_accent'],
            'selectforeground': '#FFFFFF'
        }
    
    def configure_progressbar(self, progressbar) -> None:
        """Configura estilo da barra de progresso"""
        style = progressbar.cget('style') or 'TProgressbar'
        
        # Configurar estilo ttk
        try:
            import tkinter.ttk as ttk
            s = ttk.Style()
            s.configure(style,
                       background=self.colors['fg_accent'],
                       troughcolor=self.colors['bg_tertiary'],
                       borderwidth=0,
                       lightcolor=self.colors['fg_accent'],
                       darkcolor=self.colors['fg_accent'])
        except:
            pass