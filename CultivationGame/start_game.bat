@echo off
cd /d "%~dp0"
python Main.py
if errorlevel 1 (
  echo.
  echo Game failed to start. Check Python, Requirements.txt, and logs\error.log.
  pause
)

