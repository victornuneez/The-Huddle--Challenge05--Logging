# ejecutar_servicio_auth.ps1
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║         🔐 INICIANDO SERVICIO DE AUTENTICACIÓN            ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

$dirScript = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "🔍 Buscando servicio de autenticación..." -ForegroundColor Yellow
Write-Host ""

# Buscar servicio_autenticacion.py
$archivos = Get-ChildItem -Path $dirScript -Filter "servicio_autenticacion.py" -Recurse -File -ErrorAction SilentlyContinue

if ($archivos) {
    $archivo = $archivos[0]
    Write-Host "✅ Encontrado: $($archivo.FullName)" -ForegroundColor Green
    Write-Host ""
    Write-Host "🚀 Iniciando servicio..." -ForegroundColor Cyan
    Write-Host ""
    
    Set-Location $archivo.DirectoryName
    python $archivo.Name
    
    Write-Host ""
    Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Gray
    pause
    exit
}

# Si no, buscar servicio_auth.py
$archivos = Get-ChildItem -Path $dirScript -Filter "servicio_auth.py" -Recurse -File -ErrorAction SilentlyContinue

if ($archivos) {
    $archivo = $archivos[0]
    Write-Host "✅ Encontrado: $($archivo.FullName)" -ForegroundColor Green
    Write-Host ""
    Write-Host "🚀 Iniciando servicio..." -ForegroundColor Cyan
    Write-Host ""
    
    Set-Location $archivo.DirectoryName
    python $archivo.Name
    
    Write-Host ""
    Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Gray
    pause
    exit
}

# Si no se encontró
Write-Host "❌ ERROR: No se encontró servicio_autenticacion.py" -ForegroundColor Red
Write-Host ""
Write-Host "💡 Verifica que la estructura sea:" -ForegroundColor Yellow
Write-Host "   proyecto/"
Write-Host "   └── servicios/"
Write-Host "       └── servicio_autenticacion.py"
Write-Host ""
pause