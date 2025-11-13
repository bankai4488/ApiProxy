from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)


@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "usage": "GET /check/<gamepass_id>"
    })


@app.route('/check/<int:gamepass_id>')
def check_regional_pricing(gamepass_id):
    try:
        # Roblox API requires authentication
        url = f"https://apis.roblox.com/game-passes/v1/game-passes/{gamepass_id}/details"

        # Get API key from environment variable
        api_key = os.environ.get('ROBLOX_API_KEY')

        headers = {}
        if api_key:
            headers['x-api-key'] = api_key

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 401:
            return jsonify({
                "error": "Unauthorized - API key required",
                "message": "Set ROBLOX_API_KEY environment variable in Render",
                "status_code": 401
            }), 401

        if response.status_code != 200:
            return jsonify({
                "error": "Failed to fetch game pass data",
                "status_code": response.status_code,
                "details": response.text
            }), response.status_code

        data = response.json()

        # Check if RegionalPricing is in enabledFeatures
        enabled_features = data.get('priceInformation', {}).get('enabledFeatures', [])
        has_regional_pricing = 'RegionalPricing' in enabled_features

        return jsonify({
            "gamePassId": gamepass_id,
            "hasRegionalPricing": has_regional_pricing,
            "name": data.get('name'),
            "price": data.get('priceInformation', {}).get('defaultPriceInRobux')
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Request failed",
            "details": str(e)
        }), 500

    except Exception as e:
        return jsonify({
            "error": "Internal error",
            "details": str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)