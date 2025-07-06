from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route("/naturgy", methods=["GET"])
def naturgy_proxy():
    cups = request.args.get("cups")

    if not cups:
        return jsonify({"error": "CUPS no proporcionado"}), 400

    try:
        url = f"https://services.zapotek-pre.adn.naturgy.com/pricing/sips/technical_infos/ELECTRICITY?cups={cups}&energe=ELECTRICITY"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Origin": "https://front-calculator.zapotek-pre.adn.naturgy.com",
            "Referer": "https://front-calculator.zapotek-pre.adn.naturgy.com/",
            "Accept": "application/json",
            "Accept-Language": "es-ES,es;q=0.9",
            "Connection": "keep-alive"
        }

        response = requests.get(url, headers=headers)

        return jsonify({
            "status": response.status_code,
            "response": response.json() if response.status_code == 200 else response.text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Puerto 10000 explícitamente
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
