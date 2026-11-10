@echo off
setlocal
cd /d "%~dp0"
title RetailHub - Local Network Host (Wi-Fi / LAN)

set PYTHON_EXE=C:\Users\prash\AppData\Local\Programs\Python\Python315\python.exe
if not exist "%PYTHON_EXE%" set PYTHON_EXE=python

echo ======================================================================
echo           RETAILHUB LOCAL AREA NETWORK HOST (Wi-Fi / LAN)             
echo ======================================================================
echo.
echo Starting RetailHub server on all network interfaces (0.0.0.0:8080)...
echo.
"%PYTHON_EXE%" "python\api_server.py"

pause
