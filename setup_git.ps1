# RetailHub Git Repository Setup Script
$ProjectRoot = $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "                 RETAILHUB GIT INITIALIZATION                     " -ForegroundColor White
Write-Host "==================================================================" -ForegroundColor Cyan

$gitCmd = Get-Command git -ErrorAction SilentlyContinue

if (-not $gitCmd) {
    Write-Host "`n[NOTICE] Git is not yet installed on this machine." -ForegroundColor Yellow
    Write-Host "To install Git for Windows, you can either:"
    Write-Host "  1. Run this in your PowerShell terminal:" -ForegroundColor Green
    Write-Host "     winget install --id Git.Git -e --source winget`n" -ForegroundColor White
    Write-Host "  2. Or download the installer from:" -ForegroundColor Green
    Write-Host "     https://git-scm.com/download/win`n" -ForegroundColor White
    Write-Host "Once installed, restart your terminal and run this script again." -ForegroundColor Gray
    Read-Host "`nPress Enter to exit..."
    exit 1
}

Write-Host "`n[OK] Git is available: " -ForegroundColor Green -NoNewline
& git --version

if (-not (Test-Path "$ProjectRoot\.git")) {
    Write-Host "`nInitializing new Git repository..." -ForegroundColor Yellow
    & git init
} else {
    Write-Host "`nRepository already initialized." -ForegroundColor Gray
}

# Configure user identity if not already configured
$userName = (& git config user.name)
if (-not $userName) {
    & git config user.name "Developer"
    & git config user.email "developer@example.local"
    Write-Host "Configured default local Git user identity." -ForegroundColor Gray
}

Write-Host "Staging project files..." -ForegroundColor Yellow
& git add .

Write-Host "Creating initial commit..." -ForegroundColor Yellow
& git commit -m "Initial commit: RetailHub multi-tier system (SQL + .NET + Python)"

Write-Host "`n==================================================================" -ForegroundColor Cyan
Write-Host "[SUCCESS] Repository initialized and initial commit created!" -ForegroundColor Green
Write-Host "Run 'git log --oneline' to view your commit history." -ForegroundColor Gray
Write-Host "==================================================================" -ForegroundColor Cyan
