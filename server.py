from flask import Flask, request, jsonify, send_from_directory
from app.cookie_ninja import ejecutar_desde_web
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'ninja_interface.html')

@app.route('/ejecutar', methods=['POST'])
def ejecutar():
    data = request.get_json()
    ruta = data.get("archivo")
    url = data.get("url")
    sitekey = data.get("sitekey") if data.get("sitekey") else None

    try:
        resultado = ejecutar_desde_web(ruta, url, sitekey)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/<path:path>')
def static_file(path):
    return send_from_directory(os.getcwd(), path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
