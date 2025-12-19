# ejecutar_servicio_pagos.ps1
Write-Host "================================================================" -ForegroundColor Yellow
Write-Host "            INICIANDO SERVICIO DE PAGOS                         " -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Yellow
Write-Host ""

$dirScript = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "Buscando servicio de pagos..." -ForegroundColor Yellow
Write-Host ""

# Buscar servicio_pagos.py
$archivos = Get-ChildItem -Path $dirScript -Filter "servicio_pagos.py" -Recurse -File -ErrorAction SilentlyContinue

if ($archivos) {
    $archivo = $archivos[0]
    Write-Host "Encontrado:" $archivo.FullName -ForegroundColor Green
    Write-Host ""
    Write-Host "Iniciando servicio..." -ForegroundColor Cyan
    Write-Host ""
    
    Set-Location $archivo.DirectoryName
    python $archivo.Name
    
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Gray
    pause
    exit
}

# Si no se encontró
Write-Host "ERROR: No se encontro servicio_pagos.py" -ForegroundColor Red
Write-Host ""
Write-Host "Verifica que exista el archivo:" -ForegroundColor Yellow
Write-Host "servicios/servicio_pagos.py"
Write-Host ""
pause