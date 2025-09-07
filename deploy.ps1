# deploy.ps1 - Script de despliegue Docker
Write-Host "🚀 Desplegando Sistema de Gestión de Personas" -ForegroundColor Green

# Parar y eliminar contenedores previos
docker stop sistema-gestion-app 2>$null
docker rm sistema-gestion-app 2>$null

# Construir nueva imagen
Write-Host "📦 Construyendo imagen Docker..." -ForegroundColor Yellow
docker build -t sistema-gestion-personas:1.0 .

# Crear volumen para datos si no existe
if (-not (docker volume ls -q | Where-Object { $_ -eq "sistema-gestion-data" })) {
    docker volume create sistema-gestion-data
}

# Ejecutar la aplicación
Write-Host "🎯 Iniciando aplicación..." -ForegroundColor Green
docker run -d \
    --name sistema-gestion-app \
    -e DISPLAY=host.docker.internal:0 \
    -e QT_X11_NO_MITSHM=1 \
    -v sistema-gestion-data:/app/data \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    --restart unless-stopped \
    sistema-gestion-personas:1.0

Write-Host "✅ Despliegue completado!" -ForegroundColor Green
Write-Host "📊 Ver logs: docker logs sistema-gestion-app" -ForegroundColor Cyan
Write-Host "🚪 Detener: docker stop sistema-gestion-app" -ForegroundColor Cyan