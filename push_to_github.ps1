# Push RetailHub to GitHub
$ProjectRoot = $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "               PUSHING RETAILHUB TO GITHUB PUBLIC REPO                " -ForegroundColor White
Write-Host "      Repository: https://github.com/prashppk123/retailhub.git        " -ForegroundColor Gray
Write-Host "======================================================================" -ForegroundColor Cyan

# 1. Add safe directory exception
$gitPath = "C:\Program Files\Git\cmd\git.exe"
if (-not (Test-Path $gitPath)) { $gitPath = "git" }

& $gitPath config --global --add safe.directory $ProjectRoot.Replace('\', '/')
& $gitPath config --global --add safe.directory $ProjectRoot

# 2. Init
if (-not (Test-Path "$ProjectRoot\.git")) {
    & $gitPath init
}

# 3. Config
& $gitPath config user.name "prashppk123"
& $gitPath config user.email "prashppk123@users.noreply.github.com"
& $gitPath branch -M main

# 4. Remote
& $gitPath remote remove origin 2>$null
& $gitPath remote add origin "https://github.com/prashppk123/retailhub.git"

# 5. Commit
Write-Host "`nStaging files and creating commit..." -ForegroundColor Yellow
& $gitPath add .
& $gitPath commit -m "Initial commit: RetailHub multi-tier system (SQL, .NET, Python, and Web Dashboard)"

# 6. Push
Write-Host "`n======================================================================" -ForegroundColor Cyan
Write-Host "Pushing to GitHub (https://github.com/prashppk123/retailhub.git)..." -ForegroundColor Green
Write-Host "If a GitHub authentication prompt pops up, please log in." -ForegroundColor Yellow
Write-Host "======================================================================`n" -ForegroundColor Cyan

& $gitPath push -u origin main --force

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n======================================================================" -ForegroundColor Cyan
    Write-Host "[SUCCESS] Published to GitHub successfully!" -ForegroundColor Green
    Write-Host "`n1. Repository URL:" -ForegroundColor White
    Write-Host "   https://github.com/prashppk123/retailhub" -ForegroundColor Cyan
    Write-Host "`n2. Enable GitHub Pages to share live link with friends:" -ForegroundColor White
    Write-Host "   a. Go to: https://github.com/prashppk123/retailhub/settings/pages" -ForegroundColor Gray
    Write-Host "   b. Select Branch: 'main' / Folder: '/ (root)'" -ForegroundColor Gray
    Write-Host "   c. Click Save." -ForegroundColor Gray
    Write-Host "`n   Live Website Link for your friends:" -ForegroundColor Yellow
    Write-Host "   https://prashppk123.github.io/retailhub/" -ForegroundColor Green
    Write-Host "======================================================================" -ForegroundColor Cyan
} else {
    Write-Host "`nPush finished with status code $LASTEXITCODE." -ForegroundColor Yellow
}

Read-Host "`nPress Enter to exit..."
