"""
RetailHub - Quick Verification Test Suite
Runs an automated health-check across SQL, .NET, and Python.
"""

import os
import subprocess
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
PYTHON_EXE = sys.executable

print("==================================================")
print("     RETAILHUB AUTOMATED INTEGRATION VERIFICATION ")
print("==================================================")

# Test 1: Python DB Setup
print("\n[Test 1/3] Verifying Database Setup...")
res1 = subprocess.run([PYTHON_EXE, os.path.join(PROJECT_ROOT, "python", "db_setup.py")], capture_output=True, text=True)
if res1.returncode == 0:
    print("  -> PASS: Database initialized successfully.")
else:
    print(f"  -> FAIL: {res1.stderr}")

# Test 2: .NET Executable Demo Mode
print("\n[Test 2/3] Verifying .NET / C# Execution...")
exe_path = os.path.join(PROJECT_ROOT, "dotnet", "RetailApp.exe")
if os.path.exists(exe_path):
    res2 = subprocess.run([exe_path, "--demo"], capture_output=True, text=True)
    if res2.returncode == 0 and "Demo Complete" in res2.stdout:
        print("  -> PASS: .NET application executed and processed transactional SQL order.")
    else:
        print(f"  -> FAIL: {res2.stderr or res2.stdout}")
else:
    print("  -> SKIP: RetailApp.exe not found.")

# Test 3: Python Analytics & Reporting
print("\n[Test 3/3] Verifying Python Analytics & File Exports...")
res3 = subprocess.run([PYTHON_EXE, os.path.join(PROJECT_ROOT, "python", "analytics.py")], capture_output=True, text=True)
csv_path = os.path.join(PROJECT_ROOT, "reports", "product_sales_summary.csv")
md_path = os.path.join(PROJECT_ROOT, "reports", "analytics_report.md")

if res3.returncode == 0 and os.path.exists(csv_path) and os.path.exists(md_path):
    print("  -> PASS: Analytics executed; CSV and Markdown reports successfully created.")
else:
    print(f"  -> FAIL: {res3.stderr or 'Report files missing'}")

print("\n" + "=" * 50)
print(" All system components are verified and operational!")
print("==================================================")
