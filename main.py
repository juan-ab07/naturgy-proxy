from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# --- Endpoint 1: Información básica (dirección, localidad, etc.) ---
@app.route("/naturgy", methods=["GET"])
def naturgy_proxy():
    cups = request.args.get("cups")
    if not cups:
        return jsonify({"error": "CUPS es requerido"}), 400

    url = f"https://naturgy-pre-naturgy-location-api.ed-integrations.com/v1/cups/{cups}?sessionId=b90a9881-9ecd-3d4f-47ab-1a1a5fa4d306&componentSessionID=b90a9881-9ecd-3d4f-47ab-1a1a5fa4d306_i78cd6fj&step=0&category=electricity&provider=newco&cups=&postalCode=hide"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return jsonify({"error": f"Error al consultar: {response.status_code}"}), response.status_code
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- Endpoint 2: Información técnica (potencia, consumo, etc.) ---
@app.route("/datos-tecnicos", methods=["GET"])
def datos_tecnicos():
    cups = request.args.get("cups")
    if not cups:
        return jsonify({"error": "CUPS es requerido"}), 400

    url = f"https://services.zapotek-pre.adn.naturgy.com/pricing/sips/technical_infos/ELECTRICITY?cups={cups}&energyType=ELECTRICITY"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Origin": "https://front-calculator.zapotek-pre.adn.naturgy.com",
        "Referer": "https://front-calculator.zapotek-pre.adn.naturgy.com/"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return jsonify({"error": f"Error al consultar: {response.status_code}"}), response.status_code
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- Arranque de la aplicación ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
