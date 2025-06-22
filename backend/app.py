from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import math
import os
import qrcode

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

#Generar un QR
QR_FOLDER = os.path.join("QR")
os.makedirs(QR_FOLDER, exist_ok=True)

def generar_qr(documento, tipo, ubicacion, entry_time):
    contenido = f"Documento: {documento}\nTipo: {tipo}\nUbicación: {ubicacion}\nIngreso: {entry_time}"
    qr = qrcode.make(contenido)
    nombre_archivo = f"{documento}.png"
    ruta = os.path.join(QR_FOLDER, nombre_archivo)
    qr.save(ruta)
    return ruta

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
    info_basica = (tipo, pago, lavado)
    estacionamiento[documento] = {
        "info": info_basica,
        "ubicacion": ubicacion,
        "entry_time": now.isoformat()
    }
    ocupacion[ubicacion] = documento

    # ✅ Generar QR automáticamente
    generar_qr(documento, tipo, ubicacion, now.strftime("%Y-%m-%d %H:%M:%S"))

    return jsonify({
        "mensaje": "Registro exitoso",
        "documento": documento,
        "ubicacion": ubicacion,
        "entry_time": now.isoformat()
    })


# Obtener todos los datos del estacionamiento
@app.route("/obtener", methods=["GET"])
def obtener():
    return jsonify(estacionamiento)

# Obtener mapa de ubicaciones
@app.route("/mapa", methods=["GET"])
def obtener_mapa():
    filas    = "ABCDEFGHIJ"
    columnas = list(range(1, 16))

    def construir_fila(f):
        return list(map(
            lambda c: {"ubicacion": f + str(c),"estado":"ocupado" if f + str(c) in ocupacion else "libre"}, columnas))

    mapa = list(map(construir_fila, filas))
    return jsonify(mapa)

# Retirar un vehículo
@app.route("/retirar", methods=["DELETE"])
def retirar():
    documento = request.json.get("documento")

    if documento not in estacionamiento:
        return jsonify({"error": "Documento no encontrado"}), 404

    info = estacionamiento[documento]
    tipo, pago, lavado = info["info"]  # ← Y de ACA sale la tupla
    entry_time = datetime.fromisoformat(info["entry_time"])
    exit_time  = datetime.now()
    diferencia = exit_time - entry_time
    horas = math.ceil(diferencia.total_seconds() / 3600)

    # Cálculo del costo
    costo = horas * TARIFA_HORA
    if pago == "QR":
        costo += costo * RECARGO_QR
    if lavado == "SI":
        costo += PRECIOS_LAVADO.get(tipo, 0)

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

@app.route("/QR/<filename>")
def servir_qr(filename):
    return send_from_directory("QR", filename)

if __name__ == "__main__":
    app.run(debug=True)
