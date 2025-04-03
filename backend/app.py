from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permitir peticiones desde el frontend

# Base de datos simulada (lista en memoria)
estacionamiento = {}

@app.route("/", methods=["GET"])  # <-- Ruta base para probar si Flask responde
def home():
    return "Servidor Flask en ejecución."

@app.route("/registrar", methods=["POST"])
def registrar():
    datos = request.json
    documento = datos.get("documento")
    
    if documento in estacionamiento:
        return jsonify({"error": "El usuario ya está registrado"}), 400

    estacionamiento[documento] = datos
    return jsonify({"mensaje": "Registro exitoso", "datos": datos})

@app.route("/obtener", methods=["GET"])
def obtener():
    return jsonify(estacionamiento)

if __name__ == "__main__":
    app.run(debug=True)
