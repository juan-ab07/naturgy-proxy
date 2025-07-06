from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

@app.route('/naturgy')
def consultar_cups():
    cups = request.args.get("cups")
    if not cups:
        return jsonify({"error": "Falta el parámetro 'cups'"}), 400

    url = f"https://services.zapotek-pre.adn.naturgy.com/pricing/sips/technical_infos/ELECTRICITY?cups={cups}&energe=ELECTRICITY"
    headers = {
        "Origin": "https://front-calculator.zapotek-pre.adn.naturgy.com",
        "Referer": "https://front-calculator.zapotek-pre.adn.naturgy.com/"
    }

    try:
        response = requests.get(url, headers=headers)
        return (response.text, response.status_code, {'Content-Type': response.headers.get('Content-Type', 'application/json')})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
