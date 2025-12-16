@echo off
echo.
echo ========================================
echo   CODEX DOMINION - INSTANT PUBLIC URL
echo ========================================
echo.
echo Starting ngrok tunnel...
echo.

start "" "C:\Users\JMerr\ngrok\ngrok.exe" http 5000

timeout /t 5 /nobreak > nul

echo.
echo Your dashboard is now PUBLIC!
echo.
echo Open these URLs:
echo   1. ngrok Dashboard: http://localhost:4040
echo   2. Your public URL will be shown in ngrok window
echo.

start http://localhost:4040

echo.
echo DONE! Check the ngrok window for your public URL
echo.
pause
