from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import math
import os

frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
app = Flask(__name__, static_folder=frontend_path, static_url_path='')  
CORS(app)

# Base de datos en memoria
estacionamiento = {}   
ocupacion = {}         

# Tarifas
TARIFA_HORA   = 2000
RECARGO_QR    = 0.10    
PRECIOS_LAVADO = {"MOTO": 4000, "AUTO": 10000, "CAMIONETA": 15000}

# Servir index.html desde la raíz
@app.route("/", methods=["GET"])
def home():
    return send_from_directory(frontend_path, "index.html")

@app.route("/<path:filename>")
def frontend_files(filename):
    return send_from_directory(frontend_path, filename)

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
        "tipo": tipo,
        "pago": pago,
        "lavado": lavado,
        "ubicacion": ubicacion,
        "entry_time": now.isoformat()
    }
    ocupacion[ubicacion] = documento

    return jsonify({
        "mensaje": "Registro exitoso",
        "documento": documento,
        "ubicacion": ubicacion,
        "entry_time": now.isoformat()
    })

@app.route("/obtener", methods=["GET"])
def obtener():
    try:
        with open("datos_estacionamiento.txt", "w", encoding="utf-8") as archivo:
            for doc, datos in estacionamiento.items():
                linea = (
                    f"Documento: {doc}, "
                    f"Tipo: {datos['tipo']}, "
                    f"Pago: {datos['pago']}, "
                    f"Lavado: {datos['lavado']}, "
                    f"Ubicación: {datos['ubicacion']}, "
                    f"Entrada: {datos['entry_time']}\n"
                )
                archivo.write(linea)
        return jsonify(estacionamiento)
    except Exception as e:
        return jsonify({"error": f"No se pudo guardar el archivo: {str(e)}"}), 500

@app.route("/datos_estacionamiento.txt")
def descargar_archivo():
    return send_from_directory(os.getcwd(), "datos_estacionamiento.txt", as_attachment=True)

@app.route("/mapa", methods=["GET"])
def obtener_mapa():
    filas    = "ABCDEFGHIJ"
    columnas = list(range(1, 16))

    def construir_fila(f):
        return [{"ubicacion": f + str(c), "estado": "ocupado" if f + str(c) in ocupacion else "libre"} for c in columnas]

    mapa = list(map(construir_fila, filas))
    return jsonify(mapa)

@app.route("/retirar", methods=["DELETE"])
def retirar():
    documento = request.json.get("documento")

    if documento not in estacionamiento:
        return jsonify({"error": "Documento no encontrado"}), 404

    info = estacionamiento[documento]
    tipo, pago, lavado = info["info"]
    entry_time = datetime.fromisoformat(info["entry_time"])
    exit_time = datetime.now()
    diferencia = exit_time - entry_time
    horas = math.ceil(diferencia.total_seconds() / 3600)

    costo = horas * TARIFA_HORA
    if pago == "QR":
        costo += costo * RECARGO_QR
    if lavado == "SI":
        costo += PRECIOS_LAVADO.get(tipo, 0)

    ubicacion = info["ubicacion"]
    ocupacion.pop(ubicacion, None)
    estacionamiento.pop(documento)

    return jsonify({
        "mensaje": "Vehículo retirado correctamente",
        "documento": documento,
        "ubicacion": ubicacion,
        "entry_time": entry_time.isoformat(),
        "exit_time": exit_time.isoformat(),
        "horas": horas,
        "costo": int(costo),
        "pago": pago
    })

# Ruta para servir la imagen genérica qrRetiro.png
@app.route("/QR/qrRetiro.png")
def servir_qr_estatico():
    return send_from_directory(os.path.join(os.path.dirname(__file__), "QR"), "qrRetiro.png")

if __name__ == "__main__":
    app.testing = False
    app.run(debug=True)

USUARIOS_AUTORIZADOS = {
    "bautista": "contrabauti",
    "alvaro": "contraalvaro",
    "mateo": "contramate",
    "matias": "contramati"
}

def login(nombre, password):
    nombre = nombre.strip().lower()
    return USUARIOS_AUTORIZADOS.get(nombre) == password
