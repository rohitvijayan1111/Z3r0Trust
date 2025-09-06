from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/alerts', methods=['POST'])
def webhook():
    try:
        # Get JSON payload from request
        data = request.get_json(force=True)

        # Print or log data
        print("Received JSON:", data)

        # Respond to sender
        return jsonify({"status": "success", "received": data}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/alerts', methods=['GET'])
def test_alerts():
    return jsonify({"status": "ok", "message": "GET request received"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
