from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import math
import os

app = Flask(__name__, static_folder="")  
CORS(app)

# Base de datos en memoria
estacionamiento = {}   
ocupacion = {}         

# Tarifas
TARIFA_HORA   = 2000
RECARGO_QR    = 0.10    
PRECIOS_LAVADO = {"MOTO":4000,"AUTO":10000,"CAMIONETA":15000}

# Servir index.html desde la raíz
@app.route("/", methods=["GET"])
def home():
    return send_from_directory(os.getcwd(), "index.html")

# Registrar un vehículo
@app.route("/registrar", methods=["POST"])
def registrar():
    datos = request.json

    documento, ubicacion, tipo, pago, lavado = map(lambda k: datos.get(k), ["documento", "ubicacion", "tipo", "pago", "lavado"])

    if documento in estacionamiento:
        return jsonify({"error": "Documento ya registrado"}), 400
    if ubicacion in ocupacion:
        return jsonify({"error": "Ubicación ocupada"}), 400

    now = datetime.now()
    estacionamiento[documento] = {"tipo":tipo,"pago":pago,"lavado":lavado,"ubicacion":ubicacion,"entry_time": now.isoformat()}
    ocupacion[ubicacion] = documento

    return jsonify({"mensaje":"Registro exitoso","documento":documento,"ubicacion":ubicacion,"entry_time":  now.isoformat()})

# RUTA Y FUNCION PARA ALMACENAR LOS DATOS
@app.route("/obtener", methods=["GET"])
def obtener():
    return jsonify(estacionamiento)

# A PARTIR DE ACA EL MAPA
@app.route("/mapa", methods=["GET"])
def obtener_mapa():
    filas    = "ABCDEFGHIJ"
    columnas = list(range(1, 16))

    def construir_fila(f):
        return list(map(
            lambda c: {"ubicacion": f + str(c),"estado":"ocupado" if f + str(c) in ocupacion else "libre"}, columnas))

    mapa = list(map(construir_fila, filas))
    return jsonify(mapa)

# A PARTIR DE ACA LO DE RETIRO DEL VIHUCULO
@app.route("/retirar", methods=["DELETE"])
def retirar():
    documento = request.json.get("documento")

    if documento not in estacionamiento:
        return jsonify({"error": "Documento no encontrado"}), 404

    info = estacionamiento[documento]
    entry_time = datetime.fromisoformat(info["entry_time"])
    exit_time  = datetime.now()
    diferencia = exit_time - entry_time
    horas = math.ceil(diferencia.total_seconds() / 3600)

    # Cálculo del costo
    costo = horas * TARIFA_HORA
    if info["pago"] == "QR":
        costo += costo * RECARGO_QR
    if info["lavado"] == "SI":
        costo += PRECIOS_LAVADO.get(info["tipo"], 0)

    ubicacion = info["ubicacion"]
    ocupacion.pop(ubicacion, None)
    estacionamiento.pop(documento)

    return jsonify({
        "mensaje":    "Vehículo retirado correctamente",
        "documento":  documento,
        "ubicacion":  ubicacion,
        "entry_time": entry_time.isoformat(),
        "exit_time":  exit_time.isoformat(),
        "horas":      horas,
        "costo":      int(costo)
    })

if __name__ == "__main__":
    app.run(debug=True)
