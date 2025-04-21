# app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import math
import os

app = Flask(__name__, static_folder="")  
CORS(app)

# Base de datos en memoria
estacionamiento = {}   # { documento: datos }
ocupacion = {}         # { ubicacion: documento }

# Tarifas
TARIFA_HORA   = 2000
RECARGO_QR    = 0.10    # 10%
PRECIOS_LAVADO = {
    "MOTO":     4000,
    "AUTO":    10000,
    "CAMIONETA":15000
}


# Servir index.html desde la raíz para evitar problemas de file://
@app.route("/", methods=["GET"])
def home():
    return send_from_directory(os.getcwd(), "index.html")


# Registrar un vehículo
@app.route("/registrar", methods=["POST"])
def registrar():
    datos    = request.json
    documento= datos.get("documento")
    ubicacion= datos.get("ubicacion")
    tipo     = datos.get("tipo")
    pago     = datos.get("pago")     # "EFECTIVO" o "QR"
    lavado   = datos.get("lavado")   # "SI" o "NO"

    # Validaciones
    if documento in estacionamiento:
        return jsonify({"error": "Documento ya registrado"}), 400
    if ubicacion in ocupacion:
        return jsonify({"error": "Ubicación ocupada"}), 400

    # Hora de entrada
    now = datetime.now()
    estacionamiento[documento] = {
        "tipo":       tipo,
        "pago":       pago,
        "lavado":     lavado,
        "ubicacion":  ubicacion,
        "entry_time": now.isoformat()
    }
    ocupacion[ubicacion] = documento

    return jsonify({
        "mensaje":     "Registro exitoso",
        "documento":   documento,
        "ubicacion":   ubicacion,
        "entry_time":  now.isoformat()
    })


# Obtener todas las reservas activas (para debug/ver)
@app.route("/obtener", methods=["GET"])
def obtener():
    return jsonify(estacionamiento)


# Obtener estado del mapa
@app.route("/mapa", methods=["GET"])
def obtener_mapa():
    filas   = "ABCDEFGHIJKLMNO"
    columnas= list(range(1,16))
    mapa = []
    for f in filas:
        fila_actual = []
        for c in columnas:
            u = f + str(c)
            fila_actual.append({
                "ubicacion": u,
                "estado":    "ocupado" if u in ocupacion else "libre"
            })
        mapa.append(fila_actual)
    return jsonify(mapa)


# Retirar vehículo y calcular costo
@app.route("/retirar", methods=["DELETE"])
def retirar():
    datos     = request.json
    documento = datos.get("documento")

    if documento not in estacionamiento:
        return jsonify({"error": "Documento no encontrado"}), 404

    info       = estacionamiento[documento]
    entry_time = datetime.fromisoformat(info["entry_time"])
    exit_time  = datetime.now()

    # Horas totales redondeadas hacia arriba
    delta  = exit_time - entry_time
    horas  = math.ceil(delta.total_seconds() / 3600)

    # Costo base
    costo = horas * TARIFA_HORA

    # Recargo QR
    if info["pago"] == "QR":
        costo += costo * RECARGO_QR

    # Lavado opcional
    if info["lavado"] == "SI":
        costo += PRECIOS_LAVADO.get(info["tipo"], 0)

    # Liberar plaza
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
