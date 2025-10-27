# 🚀 Deploy na Hostinger VPS

## Passo a passo para deploy do Gerador de Descrições Pro

### 1. Conectar na VPS

```bash
ssh root@srv1087217.hstgr.cloud
# Senha: Qn--1913DwYslcF@3Bw
```

### 2. Instalar dependências (se necessário)

```bash
# Atualizar sistema
apt update && apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
systemctl start docker
systemctl enable docker

# Instalar Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Instalar Git
apt install -y git
```

### 3. Clonar e executar

```bash
# Remover instalação anterior (se existir)
rm -rf /root/gerador-descricoes-pro

# Clonar repositório
git clone https://github.com/lucasrcosta20/gerador-descricoes-pro.git /root/gerador-descricoes-pro

# Entrar no diretório
cd /root/gerador-descricoes-pro

# Build e start
docker-compose up -d --build
```

### 4. Verificar status

```bash
# Ver containers rodando
docker-compose ps

# Ver logs
docker-compose logs -f

# Testar aplicação
curl http://localhost:8000/health
```

### 5. Acessar aplicação

- **Interface**: http://srv1087217.hstgr.cloud:8000
- **Health Check**: http://srv1087217.hstgr.cloud:8000/health
- **Teste API**: http://srv1087217.hstgr.cloud:8000/api/test

### 6. Comandos úteis

```bash
# Parar containers
docker-compose down

# Reiniciar containers
docker-compose restart

# Ver logs em tempo real
docker-compose logs -f

# Atualizar aplicação
git pull
docker-compose up -d --build

# Limpar containers antigos
docker system prune -f
```

### 7. Troubleshooting

**Se der erro de porta ocupada:**
```bash
# Ver o que está usando a porta 8000
netstat -tlnp | grep 8000

# Matar processo se necessário
kill -9 <PID>
```

**Se Ollama não iniciar:**
```bash
# Entrar no container
docker-compose exec web bash

# Verificar Ollama
ollama list
ollama pull gemma2:2b
```

**Se der erro de memória:**
```bash
# Verificar uso de memória
free -h
docker stats

# Limpar cache se necessário
docker system prune -f
```

### 8. Monitoramento

```bash
# Ver uso de recursos
htop

# Ver logs do sistema
journalctl -f

# Ver status dos containers
docker-compose ps
docker stats
```

## 🎯 URLs de Acesso

- **Principal**: http://srv1087217.hstgr.cloud:8000
- **Por IP**: http://72.61.219.206:8000
- **Health**: http://srv1087217.hstgr.cloud:8000/health
- **API Test**: http://srv1087217.hstgr.cloud:8000/api/test

## 📊 Endpoints da API

- `GET /` - Interface web
- `GET /health` - Status do sistema
- `POST /api/test` - Teste de geração
- `POST /api/generate` - Gerar descrições
- `POST /api/upload` - Upload de planilha
- `GET /api/template` - Download template
- `GET /api/stats` - Estatísticas

## 🔧 Configurações

O sistema usa as seguintes portas:
- **8000**: API Flask
- **11434**: Ollama (interno)

Volumes Docker:
- `ollama_data`: Dados do Ollama
- `./data`: Dados da aplicação
- `./logs`: Logs
- `./cache`: Cache