from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/naturgy", methods=["GET"])
def proxy():
    cups = request.args.get("cups")
    if not cups:
        return jsonify({"error": "Falta el parámetro cups"}), 400

    url = f"https://services.zapotek-pre.adn.naturgy.com/pricing/sips/technical_infos/ELECTRICITY?cups={cups}&energyType=ELECTRICITY"

    headers = {
        "Origin": "https://front-calculator.zapotek-pre.adn.naturgy.com",
        "Referer": "https://front-calculator.zapotek-pre.adn.naturgy.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    return (
        jsonify(response.json()) if response.status_code == 200 
        else (f"❌ Error al consultar: {response.status_code}", response.status_code)
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
