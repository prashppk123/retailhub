@echo off
setlocal
cd /d "%~dp0"
title RetailHub - Public Internet Host (Any Network)

set PYTHON_EXE=C:\Users\prash\AppData\Local\Programs\Python\Python315\python.exe
if not exist "%PYTHON_EXE%" set PYTHON_EXE=python

echo ======================================================================
echo              RETAILHUB PUBLIC INTERNET HOSTING (TUNNEL)              
echo   Allows access from ANY network (Mobile 4G/5G, remote, etc.)        
echo ======================================================================
echo.

:: Check if npx is available
where npx >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Node.js / npx was not detected in PATH.
    echo Please make sure Node.js is installed or use Local Wi-Fi hosting (host_lan.bat).
    pause
    exit /b 1
)

echo 1. Starting RetailHub Python backend server in background...
start /b "" "%PYTHON_EXE%" "python\api_server.py"

:: Wait 2 seconds for server to start
timeout /t 2 /nobreak >nul

echo.
echo 2. Generating a secure public HTTPS tunnel for port 8080...
echo.
echo ----------------------------------------------------------------------
echo  Look for the "url is: https://..." line below.
echo  Share that public URL with anyone on ANY network to open your site!
echo ----------------------------------------------------------------------
echo.

call npx --yes localtunnel --port 8080

pause
