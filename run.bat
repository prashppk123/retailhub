@echo off
setlocal
cd /d "%~dp0"
title RetailHub Launcher

:MENU
cls
echo ==================================================================
echo                  RETAILHUB PROJECT LAUNCHER                       
echo         (SQL Database + .NET Console + Python Analytics)          
echo ==================================================================
echo.
echo   1. Initialize / Reset SQL Database (schema.sql + seed.sql)
echo   2. Run .NET / C# Inventory & Order Manager
echo   3. Run Python Analytics & Export Reports (CSV + Markdown)
echo   4. Start Local Web Server (http://127.0.0.1:8080)
echo   5. Host on Local Wi-Fi / LAN (Access from phones/other PCs)
echo   6. Host on Public Internet (Access from ANY network via Tunnel)
echo   7. Recompile .NET Application (using csc.exe)
echo   8. Push to GitHub Public Repository (github.com/prashppk123)
echo   0. Exit
echo.
echo ==================================================================
set /p choice="Enter choice [0-8]: "

set PYTHON_EXE=C:\Users\prash\AppData\Local\Programs\Python\Python315\python.exe
if not exist "%PYTHON_EXE%" set PYTHON_EXE=python

if "%choice%"=="1" (
    echo.
    "%PYTHON_EXE%" "python\db_setup.py"
    pause
    goto MENU
)
if "%choice%"=="2" (
    echo.
    if not exist "dotnet\RetailApp.exe" (
        echo Compiling RetailApp.exe first...
        call "dotnet\build.bat"
    )
    "dotnet\RetailApp.exe"
    goto MENU
)
if "%choice%"=="3" (
    echo.
    "%PYTHON_EXE%" "python\analytics.py"
    pause
    goto MENU
)
if "%choice%"=="4" (
    echo.
    "%PYTHON_EXE%" "python\api_server.py"
    pause
    goto MENU
)
if "%choice%"=="5" (
    echo.
    call "host_lan.bat"
    goto MENU
)
if "%choice%"=="6" (
    echo.
    call "host_public.bat"
    goto MENU
)
if "%choice%"=="7" (
    echo.
    call "dotnet\build.bat"
    goto MENU
)
if "%choice%"=="8" (
    echo.
    call "push_to_github.bat"
    goto MENU
)
if "%choice%"=="0" (
    exit /b 0
)

echo Invalid choice!
pause
goto MENU
