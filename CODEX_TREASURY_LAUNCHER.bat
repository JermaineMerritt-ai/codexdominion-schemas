@echo off
title Codex Treasury & Dawn Dispatch Launcher

echo.
echo 🏛️===============================================🏛️
echo         CODEX TREASURY & DAWN DISPATCH SYSTEM
echo              Unified Command Interface
echo 🏛️===============================================🏛️
echo.

cd /d "C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion"

:MENU
echo 📋 Available Commands:
echo.
echo 1. System Status
echo 2. Treasury Summary
echo 3. Dawn Dispatch
echo 4. Add Transaction (Affiliate)
echo 5. Add Transaction (Stock)
echo 6. Add Transaction (AMM)
echo 7. Full System Report
echo 8. Exit
echo.

set /p choice="Select option (1-8): "

if "%choice%"=="1" goto STATUS
if "%choice%"=="2" goto TREASURY
if "%choice%"=="3" goto DAWN
if "%choice%"=="4" goto AFFILIATE
if "%choice%"=="5" goto STOCK
if "%choice%"=="6" goto AMM
if "%choice%"=="7" goto REPORT
if "%choice%"=="8" goto EXIT

echo Invalid choice. Please select 1-8.
goto MENU

:STATUS
echo.
echo 🔍 System Status:
python codex_unified_launcher.py status
echo.
pause
goto MENU

:TREASURY
echo.
echo 💰 Treasury Summary:
python codex_unified_launcher.py treasury summary --days 30
echo.
pause
goto MENU

:DAWN
echo.
echo 🌅 Dawn Dispatch:
python codex_unified_launcher.py dawn dispatch
echo.
pause
goto MENU

:AFFILIATE
echo.
set /p order_id="Enter Order ID: "
set /p amount="Enter Amount: "
echo.
echo Processing affiliate transaction...
python codex_unified_launcher.py treasury ingest --stream affiliate --order-id %order_id% --amount %amount%
echo.
pause
goto MENU

:STOCK
echo.
set /p symbol="Enter Stock Symbol: "
set /p amount="Enter Amount: "
echo.
echo Processing stock transaction...
python codex_unified_launcher.py treasury ingest --stream stock --symbol %symbol% --amount %amount%
echo.
pause
goto MENU

:AMM
echo.
set /p pool_id="Enter Pool ID: "
set /p amount="Enter Amount: "
echo.
echo Processing AMM transaction...
python codex_unified_launcher.py treasury ingest --stream amm --pool-id %pool_id% --amount %amount%
echo.
pause
goto MENU

:REPORT
echo.
echo 📋 Comprehensive System Report:
python codex_unified_launcher.py report
echo.
pause
goto MENU

:EXIT
echo.
echo 🔥 Thank you for using Codex Treasury System!
echo The eternal flame protects all operations.
echo.
pause
exit
