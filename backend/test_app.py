from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import time


from app import login,app, estacionamiento, ocupacion


def test_login_correcto():
    assert login("bautista", "contrabauti") == True
    assert login("mateo", "contramate") == True

def test_login_con_mayusculas():
    assert login("MATEO", "contramate") == True

def test_login_con_espacios():
    assert login("  alvaro  ", "contraalvaro") == True

def test_login_incorrecto():
    assert login("bautista", "malacontra") == False
    assert login("noexiste", "cualquiercosa") == False

def test_login_campos_vacios():
    assert login("", "") == False
    assert login("matias", "") == False


def test_registrar_y_obtener():
    client = app.test_client()

   
    estacionamiento.clear()
    ocupacion.clear()

    datos = {
        "documento": "12345678",
        "ubicacion": "A1",
        "tipo": "AUTO",
        "pago": "EFECTIVO",
        "lavado": "NO"
    }

    
    response = client.post("/registrar", json=datos)
    assert response.status_code == 200
    data = response.get_json()
    assert data["mensaje"] == "Registro exitoso"
    assert data["documento"] == datos["documento"]
    assert data["ubicacion"] == datos["ubicacion"]

    
    response = client.get("/obtener")
    assert response.status_code == 200
    datos_obtenidos = response.get_json()
    assert datos["documento"] in datos_obtenidos
    assert datos_obtenidos[datos["documento"]]["tipo"] == "AUTO"
