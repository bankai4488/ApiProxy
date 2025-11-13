from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/check_gamepass", methods=["GET"])
def check_gamepass():
    gamepass_id = request.args.get("id")
    if not gamepass_id:
        return jsonify({"error": "Missing 'id' parameter"}), 400

    url = f"https://apis.roblox.com/game-passes/v1/game-passes/{gamepass_id}/details"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Extract feature info
    features = data.get("priceInformation", {}).get("enabledFeatures", [])
    has_regional = "RegionalPricing" in features

    return jsonify({
        "gamePassId": gamepass_id,
        "regionalPricing": has_regional
    })
