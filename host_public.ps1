# RetailHub Public Host Launcher (PowerShell)
$ProjectRoot = $PSScriptRoot
Set-Location $ProjectRoot

$PythonExe = "C:\Users\prash\AppData\Local\Programs\Python\Python315\python.exe"
if (-not (Test-Path $PythonExe)) { $PythonExe = "python" }

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "             RETAILHUB PUBLIC INTERNET HOSTING (TUNNEL)               " -ForegroundColor White
Write-Host "  Allows access from ANY network worldwide (Mobile 4G/5G, remote, etc) " -ForegroundColor Gray
Write-Host "======================================================================" -ForegroundColor Cyan

# 1. Start Python backend server in background job
Write-Host "`n1. Starting RetailHub backend server on port 8080..." -ForegroundColor Yellow
$serverJob = Start-Job -ScriptBlock {
    param($py, $root)
    Set-Location $root
    & $py "$root\python\api_server.py"
} -ArgumentList $PythonExe, $ProjectRoot

Start-Sleep -Seconds 2

# 2. Start localtunnel
Write-Host "2. Creating secure public HTTPS tunnel via localtunnel..." -ForegroundColor Green
Write-Host "----------------------------------------------------------------------" -ForegroundColor DarkGray
Write-Host " Share the generated 'https://...' URL below to access from ANY network!" -ForegroundColor Cyan
Write-Host "----------------------------------------------------------------------`n" -ForegroundColor DarkGray

try {
    & npx --yes localtunnel --port 8080
}
finally {
    Stop-Job $serverJob -ErrorAction SilentlyContinue
    Remove-Job $serverJob -ErrorAction SilentlyContinue
    Write-Host "`nServer job terminated." -ForegroundColor Gray
}
