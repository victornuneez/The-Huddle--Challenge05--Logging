# ejecutar_servicio_email.ps1
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
Write-Host "║            📧 INICIANDO SERVICIO DE EMAIL                 ║" -ForegroundColor Magenta
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Magenta
Write-Host ""

$dirScript = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "🔍 Buscando servicio de email..." -ForegroundColor Yellow
Write-Host ""

# Buscar servicio_email.py
$archivos = Get-ChildItem -Path $dirScript -Filter "servicio_email.py" -Recurse -File -ErrorAction SilentlyContinue

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
Write-Host "❌ ERROR: No se encontró servicio_email.py" -ForegroundColor Red
Write-Host ""
Write-Host "💡 Verifica que la estructura sea:" -ForegroundColor Yellow
Write-Host "   proyecto/"
Write-Host "   └── servicios/"
Write-Host "       └── servicio_email.py"
Write-Host ""
pause