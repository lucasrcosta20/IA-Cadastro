# 🚀 Gerador de Descrições Comerciais Pro

Sistema profissional para geração automática de descrições comerciais usando IA local (Ollama) com interface gráfica moderna.

## ✨ Funcionalidades

- **Interface Gráfica Moderna** - Tkinter com design profissional
- **IA Local** - Ollama com múltiplos modelos (Gemma, Phi3, TinyLlama)
- **Processamento em Lote** - Planilhas Excel com milhares de produtos
- **Chat Integrado** - Conversa direta com a IA
- **Editor de Prompts** - Personalização completa dos prompts
- **Sistema de Cache** - Performance otimizada
- **Diagnóstico Completo** - Verificação automática do sistema
- **Deploy Docker** - Containerização para produção

## 🛠️ Tecnologias

- **Python 3.11+**
- **Tkinter** - Interface gráfica
- **Ollama** - IA local
- **Pandas** - Processamento de dados
- **Docker** - Containerização
- **Flask** - API web (opcional)

## 🚀 Quick Start

### Instalação Local

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/gerador-descricoes-pro.git
cd gerador-descricoes-pro

# Instalar dependências
pip install -r requirements.txt

# Configurar Ollama
ollama pull gemma2:2b

# Executar aplicação
python app.py
```

### Deploy Docker

```bash
# Build e run
docker compose up -d --build

# Acesso web
http://localhost:8080
```

## 📊 Performance

| Modelo | Velocidade | Qualidade | Tamanho |
|--------|------------|-----------|---------|
| TinyLlama | ~5-8s | Básica | 637MB |
| Gemma2 2B | ~15-20s | Boa | 1.6GB |
| Phi3 Mini | ~25-30s | Excelente | 2.3GB |

## 🎯 Casos de Uso

- **E-commerce** - Descrições para milhares de produtos
- **Marketplaces** - Padronização de conteúdo
- **Catálogos** - Geração em massa
- **SEO** - Conteúdo otimizado para busca

## 📁 Estrutura do Projeto

```
gerador-descricoes-pro/
├── app/                    # Aplicação principal
│   ├── core/              # Lógica de negócio
│   ├── ui/                # Interface gráfica
│   ├── api/               # API Flask
│   └── utils/             # Utilitários
├── config/                # Configurações
├── docker/                # Docker files
├── docs/                  # Documentação
├── tests/                 # Testes
└── scripts/               # Scripts auxiliares
```

## 🔧 Configuração

### Modelos Disponíveis

```python
MODELOS = {
    "gemma2:2b": "Equilibrado - Recomendado",
    "phi3:mini": "Alta qualidade",
    "tinyllama": "Velocidade máxima"
}
```

### Personalização de Prompts

```python
TEMPLATE_PROMPT = """
Crie uma descrição comercial para:
Nome: {nome}
Material: {material}
Cor: {cor}
Categoria: {categoria1}
"""
```

## 📈 Roadmap

- [x] Interface gráfica completa
- [x] Integração com Ollama
- [x] Sistema de cache
- [x] Chat integrado
- [ ] API REST completa
- [ ] Dashboard web
- [ ] Integração com APIs de e-commerce
- [ ] Análise de sentimento
- [ ] Geração de imagens (DALL-E)

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Add nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

- **Issues**: [GitHub Issues](https://github.com/seu-usuario/gerador-descricoes-pro/issues)
- **Documentação**: [Wiki](https://github.com/seu-usuario/gerador-descricoes-pro/wiki)
- **Chat**: Discord/Telegram (em breve)

---

**Desenvolvido com ❤️ para automatizar descrições comerciais**