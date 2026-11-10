@echo off
setlocal
cd /d "%~dp0"
title RetailHub Git Setup

echo ==================================================================
echo                  RETAILHUB GIT INITIALIZATION                     
echo ==================================================================
echo.

where git >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [NOTICE] Git is not detected in your PATH.
    echo.
    echo To install Git, you can:
    echo   1. Run this command in PowerShell (Administrator / User):
    echo        winget install --id Git.Git -e --source winget
    echo   2. Or download directly from: https://git-scm.com/download/win
    echo.
    echo After installing, reopen your terminal and run this script again.
    echo ==================================================================
    pause
    exit /b 1
)

echo [OK] Git found!
git --version
echo.

if not exist ".git" (
    echo Initializing new Git repository...
    git init
    echo.
) else (
    echo Git repository is already initialized.
    echo.
)

echo Staging project files...
git add .

echo.
echo Committing initial files...
git commit -m "Initial commit: RetailHub multi-tier system (SQL + .NET + Python)"

echo.
echo ==================================================================
echo [SUCCESS] Git repository initialized and initial commit created!
echo.
echo View your commit history with:
echo   git log --oneline
echo ==================================================================
pause
