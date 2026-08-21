@echo off
title 5Receipts — Running
color 0D

echo.
echo ============================================
echo    5Receipts — Starting bot...
echo ============================================
echo.

REM ─── Sanity check ──────────────────────────────────────────────────────────
if not exist "config.json" (
    echo  [ERROR] config.json not found!
    echo  Run install.bat first, then fill in your settings.
    echo.
    pause
    exit /b 1
)

REM ─── Run ───────────────────────────────────────────────────────────────────
python main.py
if %errorlevel% neq 0 (
    echo.
    echo  [ERROR] Bot crashed. Check the error above.
    echo.
)
echo.
echo  Bot stopped.
pause
