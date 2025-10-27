#!/bin/bash

echo "🚀 Iniciando Gerador de Descrições Pro..."

# Iniciar Ollama em background
echo "📡 Iniciando Ollama..."
ollama serve &

# Aguardar Ollama inicializar
echo "⏳ Aguardando Ollama inicializar..."
sleep 15

# Verificar se Ollama está rodando
if curl -f http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama iniciado com sucesso"
else
    echo "❌ Erro ao iniciar Ollama"
    exit 1
fi

# Baixar modelo padrão se não existir
echo "🤖 Verificando modelo padrão..."
if ! ollama list | grep -q "gemma2:2b"; then
    echo "📥 Baixando modelo Gemma2 2B..."
    ollama pull gemma2:2b
    echo "✅ Modelo baixado com sucesso"
else
    echo "✅ Modelo já disponível"
fi

# Verificar se deve iniciar interface gráfica ou API
if [ "$MODE" = "api" ]; then
    echo "🌐 Iniciando modo API..."
    python -m app.api.main
else
    echo "🖥️ Iniciando modo interface gráfica..."
    # Para Docker, geralmente usamos modo headless
    python -m app.api.main
fi