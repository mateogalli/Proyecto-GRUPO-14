from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Base de datos simulada
estacionamiento = {}  # clave: documento
ocupacion = {}  # clave: ubicacion, valor: documento

# Rutas existentes
@app.route("/", methods=["GET"])
def home():
    return "Servidor Flask en ejecución."

@app.route("/registrar", methods=["POST"])
def registrar():
    datos = request.json
    documento = datos.get("documento")
    ubicacion = datos.get("ubicacion")

    if documento in estacionamiento:
        return jsonify({"error": "El usuario ya está registrado"}), 400

    if ubicacion in ocupacion:
        return jsonify({"error": "Ubicación ocupada"}), 400

    estacionamiento[documento] = datos
    ocupacion[ubicacion] = documento

    return jsonify({"mensaje": "Registro exitoso", "datos": datos})

@app.route("/obtener", methods=["GET"])
def obtener():
    return jsonify(estacionamiento)

# NUEVA: Obtener mapa del estado actual
@app.route("/mapa", methods=["GET"])
def obtener_mapa():
    filas = "ABCDEFGHIJKLMNO"
    columnas = list(range(1, 16))
    mapa = []

    for fila in filas:
        fila_actual = []
        for columna in columnas:
            ubicacion = f"{fila}{columna}"
            if ubicacion in ocupacion:
                fila_actual.append({"ubicacion": ubicacion, "estado": "ocupado"})
            else:
                fila_actual.append({"ubicacion": ubicacion, "estado": "libre"})
        mapa.append(fila_actual)

    return jsonify(mapa)

# NUEVA: Retirar vehículo por documento
@app.route("/retirar", methods=["DELETE"])
def retirar():
    datos = request.json
    documento = datos.get("documento")

    if documento not in estacionamiento:
        return jsonify({"error": "Documento no encontrado"}), 404

    ubicacion = estacionamiento[documento]["ubicacion"]
    ocupacion.pop(ubicacion, None)
    estacionamiento.pop(documento)

    return jsonify({"mensaje": f"Vehículo con documento {documento} retirado correctamente."})

if __name__ == "__main__":
    app.run(debug=True)
