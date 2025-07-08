from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Opcional: define tu proxy con IP española en variable de entorno HTTP_PROXY
PROXY = os.getenv("HTTP_PROXY")
proxies = {"http": PROXY, "https": PROXY} if PROXY else None

# Cabeceras idénticas a las que usa el front de Naturgy
HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "es-ES,es;q=0.9",
    "Origin": "https://front-calculator.zapotek.adn.naturgy.com",
    "Referer": "https://front-calculator.zapotek.adn.naturgy.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Sec-CH-UA": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": '"Windows"',
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137 Safari/537.36"
    ),
}

def fetch_technical_infos(cups: str):
    session = requests.Session()
    session.headers.update(HEADERS)
    if proxies:
        session.proxies.update(proxies)

    # 1) Inicializar sesión y obtener cookie/session
    cups_search_url = (
        "https://services.zapotek.adn.naturgy.com/pricing/sips/"
        f"CupsSearch.tsx?cups={cups}"
    )
    r1 = session.get(cups_search_url)
    r1.raise_for_status()

    # 2) Petición final a technical_infos
    info_url = (
        "https://services.zapotek.adn.naturgy.com/pricing/sips/"
        f"technical_infos/ELECTRICITY?cups={cups}&energyType=ELECTRICITY"
    )
    r2 = session.get(info_url)
    r2.raise_for_status()
    return r2.json()

@app.route("/naturgy", methods=["GET"])
def naturgy_proxy():
    cups = request.args.get("cups")
    if not cups:
        return jsonify({"error": "CUPS es requerido"}), 400
    try:
        data = fetch_technical_infos(cups)
        return jsonify(data)
    except requests.HTTPError as e:
        status = e.response.status_code
        return jsonify({"error": f"HTTP {status}"}), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
