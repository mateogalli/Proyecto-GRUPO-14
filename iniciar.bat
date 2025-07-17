@echo off
title Estacionamiento - Instalación y ejecución

echo --------------------------------------
echo Instalando librerías necesarias...
echo --------------------------------------

REM Crea entorno virtual si no existe
if not exist "venv\Scripts\activate" (
    python -m venv venv
)

REM Activa entorno virtual
call venv\Scripts\activate

REM Instala dependencias desde requirements.txt
pip install --upgrade pip
pip install -r requirements.txt

echo --------------------------------------
echo Ejecutando la aplicación Flask...
echo --------------------------------------

REM Ejecuta el backend en una nueva terminal
start cmd /k "cd backend && call ..\venv\Scripts\activate && python app.py"

REM Espera 3 segundos y abre el navegador
timeout /t 3 > nul
start http://localhost:5000
