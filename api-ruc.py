from flask import Flask, jsonify, request
import requests
from dotenv import load_dotenv
import os

# Cargar variables de entorno (en este caso, el token)
load_dotenv()

app = Flask(__name__)

# Definir el token manualmente (ya que me pasaste el token)
TOKEN = 'apis-token-10713.PAAkKb3ZBpvqWHrYW1JtyNDeS1pfW36Y'

# Ruta para consulta parcial de RUC
@app.route('/api/ruc/parcial/<ruc>', methods=['GET'])
def consulta_parcial(ruc):
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {TOKEN}'
    }
    url = f'https://api.apis.net.pe/v2/sunat/ruc'
    params = {'numero': ruc}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

# Ruta para consulta extendida de RUC
@app.route('/api/ruc/extendida/<ruc>', methods=['GET'])
def consulta_extendida(ruc):
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {TOKEN}'
    }
    url = f'https://api.apis.net.pe/v2/sunat/ruc/full'
    params = {'numero': ruc}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
