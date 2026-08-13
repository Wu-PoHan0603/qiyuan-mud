@echo off
setlocal
cd /d "%~dp0"

python release_check.py || exit /b 1
python -m unittest discover -s tests -p "test_*.py" || exit /b 1
python -m PyInstaller --noconfirm --clean QiyuanCultivation.spec || exit /b 1

echo.
echo Build complete: dist\QiyuanCultivation\QiyuanCultivation.exe
endlocal
