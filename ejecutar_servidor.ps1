# ejecutar_servidor.ps1
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "            INICIANDO SERVIDOR CENTRAL                          " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Obtener directorio actual
$dirScript = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "[*] Buscando carpeta 'servidor'..." -ForegroundColor Yellow
Write-Host ""

# Buscar carpeta servidor con app.py
$archivos = Get-ChildItem -Path $dirScript -Filter "app.py" -Recurse -File -ErrorAction SilentlyContinue

foreach ($archivo in $archivos) {
    if ($archivo.DirectoryName -like "*servidor*") {
        Write-Host "[OK] Encontrado: $($archivo.FullName)" -ForegroundColor Green
        Write-Host ""
        Write-Host "[*] Iniciando servidor..." -ForegroundColor Cyan
        Write-Host ""
        
        Set-Location $archivo.DirectoryName
        python $archivo.Name
        
        Write-Host ""
        Write-Host "================================================================" -ForegroundColor Gray
        pause
        exit
    }
}

# Si no se encontró
Write-Host "[ERROR] No se encontro servidor/app.py" -ForegroundColor Red
Write-Host ""
Write-Host "[INFO] Verifica que la estructura sea:" -ForegroundColor Yellow
Write-Host "   proyecto/"
Write-Host "   └── servidor/"
Write-Host "       └── app.py"
Write-Host ""
Write-Host "[INFO] Buscando en: $dirScript" -ForegroundColor Gray
Write-Host ""
pause