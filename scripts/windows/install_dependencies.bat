d@echo off
echo Installing dependencies for PhiGEN Password Vault...
echo.

pip install --upgrade pip
pip install PyQt6
pip install cryptography

echo.
echo ===============================================
echo Installation complete!
echo.
echo To run the password vault:
echo   python password_vault_functional.py
echo ===============================================
pause
