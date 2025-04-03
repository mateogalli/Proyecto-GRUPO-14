from flask import Flask, request, jsonify

app = Flask(__name__)

# Base de datos temporal (en memoria)
estacionamiento = {}

@app.route("/registrar", methods=["POST"])
def registrar():
    datos = request.json
    documento = datos.get("documento")
    vehiculo = datos.get("vehiculo")
    tiempo = datos.get("tiempo")
    ubicacion = datos.get("ubicacion")
    pago = datos.get("pago")
    lavado = datos.get("lavado", "NO")

    if documento in estacionamiento:
        return jsonify({"error": "El usuario ya tiene un vehículo registrado"}), 400

    # Guardamos los datos en la "base de datos"
    estacionamiento[documento] = {
        "vehiculo": vehiculo,
        "tiempo": tiempo,
        "ubicacion": ubicacion,
        "pago": pago,
        "lavado": lavado
    }
    
    return jsonify({"mensaje": "Registro exitoso", "datos": estacionamiento[documento]}), 200

@app.route("/obtener", methods=["GET"])
def obtener():
    return jsonify(estacionamiento), 200

if __name__ == "__main__":
    app.run(debug=True)
