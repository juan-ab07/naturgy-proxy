from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permitir CORS para pruebas

@app.route('/naturgy', methods=['GET'])
def get_naturgy_data():
    cups = request.args.get('cups')
    if not cups:
        return jsonify({"error": "Falta el parámetro CUPS"}), 400

    url = f"https://services.zapotek-pre.adn.naturgy.com/pricing/sips/technical_infos/ELECTRICITY?cups={cups}&energyType=ELECTRICITY"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Origin": "https://front-calculator.zapotek-pre.adn.naturgy.com",
        "Referer": "https://front-calculator.zapotek-pre.adn.naturgy.com/"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return jsonify({"error": "No se pudo obtener la información", "status": response.status_code}), response.status_code
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
