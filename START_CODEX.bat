@echo off
title Codex Dominion - Full Stack Launcher

echo.
echo  ██████╗ ██████╗ ██████╗ ███████╗██╗  ██╗
echo ██╔════╝██╔═══██╗██╔══██╗██╔════╝╚██╗██╔╝
echo ██║     ██║   ██║██║  ██║█████╗   ╚███╔╝
echo ██║     ██║   ██║██║  ██║██╔══╝   ██╔██╗
echo ╚██████╗╚██████╔╝██████╔╝███████╗██╔╝ ██╗
echo  ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
echo.
echo          DOMINION Trading Platform
echo.

powershell -ExecutionPolicy Bypass -File "%~dp0launch-codex-development.ps1"

pause
