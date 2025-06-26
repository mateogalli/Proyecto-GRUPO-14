@echo off
title Estacionamiento - Instalación y ejecución

echo --------------------------------------
echo Instalando librerías necesarias...
echo --------------------------------------

REM Crea entorno virtual (opcional, pero recomendado)
python -m venv venv
call venv\Scripts\activate

REM Instala dependencias
pip install --upgrade pip
pip install blinker==1.9.0 ^
    click==8.1.8 ^
    colorama==0.4.6 ^
    Flask==3.1.0 ^
    flask-cors==5.0.1 ^
    iniconfig==2.1.0 ^
    itsdangerous==2.2.0 ^
    Jinja2==3.1.6 ^
    MarkupSafe==3.0.2 ^
    packaging==25.0 ^
    pillow==11.2.1 ^
    pluggy==1.6.0 ^
    Pygments==2.19.2 ^
    pytest==8.4.1 ^
    qrcode==8.2 ^
    Werkzeug==3.1.3

echo --------------------------------------
echo Ejecutando la aplicación Flask...
echo --------------------------------------

REM Ejecuta el backend
start cmd /k "cd backend && python app.py"

REM Espera 3 segundos y abre el navegador
timeout /t 3 > nul
start http://localhost:5000
