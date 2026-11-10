@echo off
setlocal
cd /d "%~dp0"
title Push RetailHub to GitHub

echo ======================================================================
echo                PUSHING RETAILHUB TO GITHUB PUBLIC REPO                
echo       Repository: https://github.com/prashppk123/retailhub.git         
echo ======================================================================
echo.

:: 1. Add safe directory exception for Git
git config --global --add safe.directory "%CD%"
git config --global --add safe.directory "%CD:\=/%"

:: 2. Initialize repository if needed
if not exist ".git" (
    echo Initializing Git repository...
    git init
)

:: 3. Configure Git Identity
git config user.name "prashppk123"
git config user.email "prashppk123@users.noreply.github.com"

:: 4. Set branch to main
git branch -M main

:: 5. Set Remote Origin
git remote remove origin 2>nul
git remote add origin https://github.com/prashppk123/retailhub.git
echo Remote origin set to: https://github.com/prashppk123/retailhub.git
echo.

:: 6. Stage and commit files
echo Staging project files...
git add .

echo Creating commit...
git commit -m "Initial commit: RetailHub multi-tier system (SQL, .NET, Python, and Web Dashboard)"

:: 7. Push to GitHub
echo.
echo ======================================================================
echo Pushing branch 'main' to GitHub...
echo (If prompted, please log into GitHub in the browser window)
echo ======================================================================
echo.

git push -u origin main --force

if %ERRORLEVEL% equ 0 (
    echo.
    echo ======================================================================
    echo [SUCCESS] Your repository has been published to GitHub!
    echo.
    echo 1. View your repository:
    echo    https://github.com/prashppk123/retailhub
    echo.
    echo 2. Enable GitHub Pages to let your friends view the site online:
    echo    a. Open: https://github.com/prashppk123/retailhub/settings/pages
    echo    b. Under "Build and deployment", set Source to: "Deploy from a branch"
    echo    c. Set Branch to: "main" and folder to: "/ (root)"
    echo    d. Click "Save"!
    echo.
    echo    Your public live website link will be:
    echo    https://prashppk123.github.io/retailhub/
    echo ======================================================================
) else (
    echo.
    echo [NOTICE] Push encountered an issue (authentication or existing commits).
    echo If GitHub requires a login, please complete the sign-in prompt and try again.
)

echo.
pause
