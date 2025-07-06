from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

@app.route("/naturgy", methods=["GET"])
def naturgy_proxy():
    cups = request.args.get("cups")
    if not cups:
        return jsonify({"error": "CUPS es requerido"}), 400

    url = f"https://services.zapotek-pre.adn.naturgy.com/pricing/sips/technical_infos/ELECTRICITY?cups={cups}&energyType=ELECTRICITY"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "es-ES,es;q=0.9",
        "Referer": "https://www.naturgy.es/",
        "Origin": "https://www.naturgy.es",
        "Connection": "keep-alive"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return jsonify({"error": f"Error al consultar: {response.status_code}"}), response.status_code
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
