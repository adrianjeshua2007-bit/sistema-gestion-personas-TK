# ejecutar-app.ps1
Write-Host "🎯 Iniciando Sistema de Gestión de Personas" -ForegroundColor Green

# Verificar que XLaunch está ejecutándose
if (-not (Get-Process -Name "vcxsrv" -ErrorAction SilentlyContinue)) {
    Write-Host "⚠️  Iniciando XLaunch..." -ForegroundColor Yellow
    Start-Process "C:\Program Files\VcXsrv\xlaunch.exe"
    Start-Sleep -Seconds 3
}

# Ejecutar la aplicación desde la imagen Docker
docker run -it --rm `
    -e DISPLAY=host.docker.internal:0 `
    -e QT_X11_NO_MITSHM=1 `
    -v sistema-gestion-data:/app/data `
    -v /tmp/.X11-unix:/tmp/.X11-unix `
    sistema-gestion-personas:1.0

Write-Host "👋 Aplicación cerrada" -ForegroundColor Cyan