@echo off
title Dawn Dispatch - Daily Ritual

echo.
echo 🌅===============================================🌅
echo            CODEX DAWN DISPATCH SYSTEM
echo              Daily Sovereignty Ritual
echo 🌅===============================================🌅
echo.

cd /d "C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion"

echo 📊 Checking current dawn status...
python dawn_dispatch_simple.py status

echo.
echo 🔥 Executing dawn dispatch ritual...
python dawn_dispatch_simple.py dispatch

echo.
echo ✅ Dawn dispatch ritual completed!
echo 📜 Proclamation archived to data/proclamation.md
echo 💾 Ledger updated in codex_ledger.json
echo.

pause
