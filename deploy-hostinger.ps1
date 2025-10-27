# Deploy do Gerador de Descrições Pro na Hostinger VPS

Write-Host "🚀 DEPLOY - Gerador de Descrições Pro na Hostinger VPS" -ForegroundColor Green
Write-Host "=======================================================" -ForegroundColor Green

# Configurações
$VPS_HOST = "srv1087217.hstgr.cloud"
$VPS_USER = "root"
$REPO_URL = "https://github.com/lucasrcosta20/gerador-descricoes-pro.git"
$APP_DIR = "/root/gerador-descricoes-pro"

Write-Host "📡 Conectando na VPS: $VPS_HOST" -ForegroundColor Yellow

# Comandos para executar na VPS via SSH
$commands = @"
echo '🔧 Preparando ambiente na VPS...'

# Atualizar sistema
apt update && apt upgrade -y

# Instalar Docker se não estiver instalado
if ! command -v docker &> /dev/null; then
    echo '📦 Instalando Docker...'
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    systemctl start docker
    systemctl enable docker
fi

# Instalar Docker Compose se não estiver instalado  
if ! command -v docker-compose &> /dev/null; then
    echo '📦 Instalando Docker Compose...'
    curl -L 'https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)' -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

# Instalar Git se não estiver instalado
if ! command -v git &> /dev/null; then
    echo '📦 Instalando Git...'
    apt install -y git
fi

echo '✅ Dependências instaladas'

# Remover diretório anterior se existir
if [ -d '$APP_DIR' ]; then
    echo '🗑️ Removendo instalação anterior...'
    cd $APP_DIR
    docker-compose down 2>/dev/null || true
    cd /
    rm -rf $APP_DIR
fi

# Clonar repositório
echo '📥 Clonando repositório...'
git clone $REPO_URL $APP_DIR
cd $APP_DIR

echo '✅ Repositório clonado'

# Build e start dos containers
echo '🔨 Building containers...'
docker-compose up -d --build

# Aguardar containers iniciarem
echo '⏳ Aguardando containers iniciarem...'
sleep 30

# Verificar status
echo '📊 Status dos containers:'
docker-compose ps

# Verificar logs
echo '📋 Logs da aplicação:'
docker-compose logs --tail=20

echo '✅ Deploy concluído!'
echo ''
echo '🌐 Aplicação disponível em:'
echo '   http://$VPS_HOST:8000'
echo '   http://72.61.219.206:8000'
echo ''
echo '🔧 Para verificar logs:'
echo '   docker-compose logs -f'
echo ''
echo '🛑 Para parar:'
echo '   docker-compose down'
"@

Write-Host "📝 Comandos preparados. Execute manualmente na VPS:" -ForegroundColor Yellow
Write-Host $commands -ForegroundColor Cyan

Write-Host ""
Write-Host "🔑 Para conectar na VPS, execute:" -ForegroundColor Yellow
Write-Host "ssh root@srv1087217.hstgr.cloud" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Depois execute os comandos acima ou use o script deploy-hostinger.sh" -ForegroundColor Yellow