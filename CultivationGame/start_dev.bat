@echo off
cd /d "%~dp0"
python dev_runner.py
if errorlevel 1 pause

