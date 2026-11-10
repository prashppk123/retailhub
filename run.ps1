# RetailHub PowerShell Launcher
$ProjectRoot = $PSScriptRoot
Set-Location $ProjectRoot

$PythonExe = "C:\Users\prash\AppData\Local\Programs\Python\Python315\python.exe"
if (-not (Test-Path $PythonExe)) { $PythonExe = "python" }

function Show-Menu {
    Clear-Host
    Write-Host "==================================================================" -ForegroundColor Cyan
    Write-Host "                 RETAILHUB PROJECT LAUNCHER                       " -ForegroundColor White
    Write-Host "        (SQL Database + .NET Console + Python Analytics)          " -ForegroundColor Gray
    Write-Host "==================================================================" -ForegroundColor Cyan
    Write-Host "  1. Initialize / Reset SQL Database" -ForegroundColor Yellow
    Write-Host "  2. Run .NET / C# Management Console" -ForegroundColor Green
    Write-Host "  3. Run Python Analytics & Export Reports" -ForegroundColor Magenta
    Write-Host "  4. Start Local Web Server (http://127.0.0.1:8080)" -ForegroundColor Blue
    Write-Host "  5. Host on Local Wi-Fi / LAN (Share with phones on Wi-Fi)" -ForegroundColor DarkCyan
    Write-Host "  6. Host on Public Internet (Access from ANY network via Tunnel)" -ForegroundColor Green
    Write-Host "  7. Recompile .NET Application (csc.exe)" -ForegroundColor DarkYellow
    Write-Host "  8. Push to GitHub Public Repository (github.com/prashppk123)" -ForegroundColor Magenta
    Write-Host "  0. Exit" -ForegroundColor Red
    Write-Host "==================================================================" -ForegroundColor Cyan
}

do {
    Show-Menu
    $choice = Read-Host "Enter choice [0-8]"
    Write-Host ""

    switch ($choice) {
        "1" {
            & $PythonExe "$ProjectRoot\python\db_setup.py"
            Read-Host "`nPress Enter to return to menu..."
        }
        "2" {
            $exePath = "$ProjectRoot\dotnet\RetailApp.exe"
            if (-not (Test-Path $exePath)) {
                Write-Host "Compiling RetailApp.exe..." -ForegroundColor Yellow
                & "C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe" /target:exe /out:$exePath /r:System.Web.Extensions.dll /recurse:"$ProjectRoot\dotnet\*.cs"
            }
            & $exePath
        }
        "3" {
            & $PythonExe "$ProjectRoot\python\analytics.py"
            Read-Host "`nPress Enter to return to menu..."
        }
        "4" {
            & $PythonExe "$ProjectRoot\python\api_server.py"
        }
        "5" {
            & $PythonExe "$ProjectRoot\python\api_server.py"
        }
        "6" {
            & "$ProjectRoot\host_public.ps1"
            Read-Host "`nPress Enter to continue..."
        }
        "7" {
            Write-Host "Compiling .NET application..." -ForegroundColor Yellow
            & "C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe" /target:exe /out:"$ProjectRoot\dotnet\RetailApp.exe" /r:System.Web.Extensions.dll /recurse:"$ProjectRoot\dotnet\*.cs"
            Write-Host "Done!" -ForegroundColor Green
            Read-Host "`nPress Enter to continue..."
        }
        "8" {
            & "$ProjectRoot\push_to_github.ps1"
            Read-Host "`nPress Enter to continue..."
        }
        "0" {
            Write-Host "Goodbye!" -ForegroundColor Cyan
            break
        }
        default {
            Write-Host "Invalid choice." -ForegroundColor Red
            Start-Sleep -Seconds 1
        }
    }
} while ($choice -ne "0")
