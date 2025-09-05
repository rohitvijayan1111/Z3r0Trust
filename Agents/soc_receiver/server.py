from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/soc", methods=["POST"])
def soc_receiver():
    data = request.json
    print("📡 SOC Receiver got alert:", data)

    # You can extend this to log into a DB, file, or incident dashboard
    return jsonify({"status": "SOC received", "alert": data}), 200

@app.route("/ping")
def ping():
    return "SOC Receiver is running"

if __name__ == "__main__":
    app.run(port=6002)
