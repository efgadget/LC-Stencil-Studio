@echo off
title LC Stencil Studio

cd /d "%~dp0"

echo ===================================
echo Avvio LC Stencil Studio...
echo ===================================

if not exist ".venv\Scripts\activate.bat" (
    echo.
    echo ERRORE: Ambiente virtuale .venv non trovato!
    pause
    exit /b
)

call .venv\Scripts\activate.bat

python src\main.py

pause