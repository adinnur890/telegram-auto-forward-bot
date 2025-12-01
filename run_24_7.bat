@echo off
title Auto 24/7 Pulsa Bot - Running
echo ========================================
echo    AUTO 24/7 PULSA BOT LAUNCHER
echo ========================================
echo.
echo 🤖 Starting fully automated bot...
echo 📝 Logs will be saved to auto_24_7.log
echo 🔄 Bot will run continuously without stopping
echo ⚠️  Close this window to stop the bot
echo.
echo ========================================
echo.

:loop
python bot_auto_24_7.py
echo.
echo ⚠️  Bot stopped unexpectedly!
echo 🔄 Auto-restarting in 30 seconds...
echo 📝 Check auto_24_7.log for details
timeout /t 30 /nobreak >nul
echo 🚀 Restarting bot...
goto loop