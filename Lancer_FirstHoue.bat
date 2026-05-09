@echo off
setlocal enabledelayedexpansion
echo ==========================================
echo    DEMARRAGE DU PROJET FIRSTHOUE (BTS)
echo ==========================================

:: Trouver l'adresse IP locale
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /R /C:"IPv4 Address" /C:"Adresse IPv4"') do (
    set "IP=%%a"
    set "IP=!IP:~1!"
)

echo Activation de l'environnement virtuel...
call venv\Scripts\activate
echo.

echo Verification et application des migrations...
python backend\manage.py makemigrations
python backend\manage.py migrate
echo.

echo ------------------------------------------
echo ACCES DEPUIS VOTRE ORDINATEUR :
echo http://127.0.0.1:8000/
echo.
echo ACCES DEPUIS VOTRE TELEPHONE (Meme Wi-Fi) :
echo http://%IP%:8000/
echo ------------------------------------------
echo.

echo Lancement du serveur...
start http://127.0.0.1:8000/
python backend\manage.py runserver 0.0.0.0:8000
pause
