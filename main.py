
import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# WARNING: Hardcoded credentials. Use environment variables in production.
PROTEO_USER = 'RICAV'
PROTEO_PASSWORD = '3691474'
PROTEO_BASE_URL = 'http://insuaminca.proteoerp.org:50080/proteoerp/api'

@app.route('/proteo/login', methods=['POST'])
def proteo_login():
    try:
        response = requests.post(
            f'{PROTEO_BASE_URL}/login/login',
            json={'user': PROTEO_USER, 'password': PROTEO_PASSWORD},
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred during Proteo login: {http_err} - {response.text}")
        return jsonify({'message': f'Error logging into ProteoERP: {response.status_code} - {response.text}'}), response.status_code
    except requests.exceptions.RequestException as req_err:
        print(f"Request exception occurred during Proteo login: {req_err}")
        return jsonify({'message': 'Failed to connect to ProteoERP login service', 'error': str(req_err)}), 500
    except Exception as e:
        print(f"An unexpected error occurred during Proteo login: {e}")
        return jsonify({'message': 'An unexpected error occurred', 'error': str(e)}), 500

@app.route('/proteo/clients', methods=['POST'])
def proteo_get_clients():
    try:
        data = request.get_json()
        api_key = data.get('apiKey')

        if not api_key:
            return jsonify({'message': 'API key is required'}), 400

        proteo_response = requests.post(
            f'{PROTEO_BASE_URL}/scli/get',
            headers={
                'Content-Type': 'application/json',
                'AUTHORIZATION': api_key,
            },
            json={
                'filters': {'tipo': '1'},
                'fields': 'cliente,nombre,rifci',
            }
        )
        proteo_response.raise_for_status()
        return jsonify(proteo_response.json()), proteo_response.status_code
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred fetching Proteo clients: {http_err} - {proteo_response.text}")
        return jsonify({'message': f'Error fetching clients from ProteoERP: {proteo_response.status_code} - {proteo_response.text}'}), proteo_response.status_code
    except requests.exceptions.RequestException as req_err:
        print(f"Request exception occurred fetching Proteo clients: {req_err}")
        return jsonify({'message': 'Failed to connect to ProteoERP client service', 'error': str(req_err)}), 500
    except Exception as e:
        print(f"An unexpected error occurred fetching Proteo clients: {e}")
        return jsonify({'message': 'An unexpected error occurred', 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", default=4000))
    app.run(debug=True, host='0.0.0.0', port=port)
