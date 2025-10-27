#!/usr/bin/env python3
"""
Script de configuração inicial do projeto
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_step(message: str):
    """Imprime uma etapa do setup"""
    print(f"\n🔧 {message}")

def run_command(command: str, check: bool = True) -> bool:
    """Executa um comando do sistema"""
    try:
        result = subprocess.run(command, shell=True, check=check, 
                              capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro: {e}")
        if e.stderr:
            print(e.stderr)
        return False

def check_python_version():
    """Verifica versão do Python"""
    print_step("Verificando versão do Python...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ é necessário")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def install_dependencies():
    """Instala dependências Python"""
    print_step("Instalando dependências Python...")
    
    # Atualizar pip
    run_command(f"{sys.executable} -m pip install --upgrade pip")
    
    # Instalar requirements
    requirements_file = Path(__file__).parent.parent / "requirements.txt"
    if requirements_file.exists():
        return run_command(f"{sys.executable} -m pip install -r {requirements_file}")
    else:
        print("❌ Arquivo requirements.txt não encontrado")
        return False

def check_ollama():
    """Verifica se Ollama está instalado"""
    print_step("Verificando Ollama...")
    
    # Verificar se ollama está no PATH
    if run_command("ollama --version", check=False):
        print("✅ Ollama encontrado")
        return True
    else:
        print("❌ Ollama não encontrado")
        print("📥 Instale o Ollama: https://ollama.com/download")
        return False

def setup_ollama_model():
    """Configura modelo padrão do Ollama"""
    print_step("Configurando modelo padrão (gemma2:2b)...")
    
    # Verificar se modelo já existe
    result = subprocess.run("ollama list", shell=True, 
                          capture_output=True, text=True)
    
    if "gemma2:2b" in result.stdout:
        print("✅ Modelo gemma2:2b já instalado")
        return True
    
    # Baixar modelo
    print("📥 Baixando modelo gemma2:2b (pode demorar alguns minutos)...")
    return run_command("ollama pull gemma2:2b")

def create_directories():
    """Cria diretórios necessários"""
    print_step("Criando diretórios...")
    
    root_dir = Path(__file__).parent.parent
    directories = ["data", "logs", "cache", "assets"]
    
    for dir_name in directories:
        dir_path = root_dir / dir_name
        dir_path.mkdir(exist_ok=True)
        print(f"📁 {dir_name}/")
    
    return True

def create_env_file():
    """Cria arquivo .env de exemplo"""
    print_step("Criando arquivo de configuração...")
    
    env_content = """# Configurações do Gerador de Descrições Pro

# Ollama
OLLAMA_URL=http://localhost:11434
OLLAMA_TIMEOUT=60
DEFAULT_MODEL=gemma2:2b

# Geração
TEMPERATURE=0.7
MAX_TOKENS=500
MAX_WORKERS=2
USE_CACHE=true

# Interface
UI_THEME=dark
WINDOW_SIZE=900x700
FONT_FAMILY=Roboto Mono
FONT_SIZE=10

# API
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=false
CORS_ENABLED=true

# Logging
LOG_LEVEL=INFO
LOG_ROTATION=daily
LOG_MAX_FILES=30
"""
    
    env_file = Path(__file__).parent.parent / ".env.example"
    env_file.write_text(env_content)
    print("✅ Arquivo .env.example criado")
    
    # Criar .env se não existir
    actual_env = Path(__file__).parent.parent / ".env"
    if not actual_env.exists():
        actual_env.write_text(env_content)
        print("✅ Arquivo .env criado")
    
    return True

def run_tests():
    """Executa testes básicos"""
    print_step("Executando testes básicos...")
    
    # Teste de importação
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from app.core.ai_client import AIClient
        from app.core.models import Product
        
        # Teste de conexão com Ollama
        client = AIClient()
        if client.is_available():
            print("✅ Conexão com Ollama OK")
        else:
            print("⚠️ Ollama não está rodando (execute 'ollama serve')")
        
        print("✅ Importações OK")
        return True
        
    except Exception as e:
        print(f"❌ Erro nos testes: {e}")
        return False

def main():
    """Função principal do setup"""
    print("🚀 SETUP - Gerador de Descrições Pro")
    print("=" * 50)
    
    steps = [
        ("Verificar Python", check_python_version),
        ("Criar diretórios", create_directories),
        ("Instalar dependências", install_dependencies),
        ("Verificar Ollama", check_ollama),
        ("Configurar modelo", setup_ollama_model),
        ("Criar configurações", create_env_file),
        ("Executar testes", run_tests)
    ]
    
    success_count = 0
    
    for step_name, step_func in steps:
        try:
            if step_func():
                success_count += 1
            else:
                print(f"⚠️ Falha em: {step_name}")
        except Exception as e:
            print(f"❌ Erro em {step_name}: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Setup concluído: {success_count}/{len(steps)} etapas")
    
    if success_count == len(steps):
        print("🎉 Setup completo! Execute 'python app/main.py' para iniciar")
    else:
        print("⚠️ Algumas etapas falharam. Verifique os erros acima.")
    
    print("\n📚 Próximos passos:")
    print("1. Execute 'ollama serve' se não estiver rodando")
    print("2. Execute 'python app/main.py' para iniciar a aplicação")
    print("3. Ou 'docker-compose up' para usar Docker")

if __name__ == "__main__":
    main()