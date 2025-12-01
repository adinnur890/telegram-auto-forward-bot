@echo off
title Auto Pulsa Bot 24/7
echo 🤖 Starting Auto Pulsa Bot...
echo ⚡ Bot will run in background
echo 👋 Close this window to stop bot
echo.

:loop
python bot_auto_pulsa.py
echo.
echo ❌ Bot stopped! Restarting in 30 seconds...
timeout /t 30 /nobreak >nul
goto loop