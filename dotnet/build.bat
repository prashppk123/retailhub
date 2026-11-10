@echo off
echo ========================================================
echo Building RetailApp C# Application (.NET)
echo ========================================================

set CSC_PATH=C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe

if not exist "%CSC_PATH%" (
    echo [ERROR] csc.exe compiler not found at %CSC_PATH%
    pause
    exit /b 1
)

echo Compiling C# source files...
"%CSC_PATH%" /target:exe /out:"%~dp0RetailApp.exe" /r:System.Web.Extensions.dll /recurse:"%~dp0*.cs"

if %ERRORLEVEL% equ 0 (
    echo [SUCCESS] Build succeeded! Created %~dp0RetailApp.exe
) else (
    echo [ERROR] Build failed with error code %ERRORLEVEL%
)

pause
