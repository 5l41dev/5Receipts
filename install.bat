@echo off
title 5Receipts — Installer
color 0D

echo.
echo ============================================
echo    5Receipts — Installer
echo ============================================
echo.

REM ─── Check Python ───────────────────────────────────────────────────────────
echo [1/3] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo  [ERROR] Python is not installed or not in PATH.
    echo  Download it from: https://www.python.org/downloads/
    echo  Make sure to check "Add Python to PATH" during install.
    echo.
    pause
    exit /b 1
)
python --version
echo  Python found.
echo.

REM ─── Install dependencies ───────────────────────────────────────────────────
echo [2/3] Installing dependencies...
pip install -r requirements.txt -q
if %errorlevel% neq 0 (
    echo.
    echo  [ERROR] Failed to install dependencies.
    echo  Make sure pip is working: python -m pip install --upgrade pip
    echo.
    pause
    exit /b 1
)
echo  Dependencies installed.
echo.

REM ─── Create config.json ────────────────────────────────────────────────────
echo [3/3] Setting up config...
if not exist "config.json" (
    if exist "config.example.json" (
        copy "config.example.json" "config.json" >nul
        echo  Created config.json from config.example.json
        echo.
        echo  ─────────────────────────────────────────────────
        echo  IMPORTANT: Open config.json and fill in ALL values
        echo  before running the bot.
        echo  ─────────────────────────────────────────────────
    ) else (
        echo  [WARNING] config.example.json not found.
        echo  Create a config.json manually — see README for format.
    )
) else (
    echo  config.json already exists — skipping.
)
echo.

REM ─── Create output directory ───────────────────────────────────────────────
if not exist "receipt\updatedrecipies" (
    mkdir "receipt\updatedrecipies" >nul 2>&1
)

echo ============================================
echo    Setup complete!
echo ============================================
echo.
echo  Next steps:
echo    1. Edit config.json with your bot token + settings
echo    2. Run start.bat to launch the bot
echo.
pause
