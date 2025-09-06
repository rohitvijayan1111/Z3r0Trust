from flask import Flask
from flask_cors import CORS
from routes.auth import auth
from routes.alerts import alerts_bp
from routes.responses import responses_bp
from routes.appeals import appeals_bp
from routes.proxy_routes import proxy_bp   # ✅ new

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

# Register blueprints
app.register_blueprint(auth, url_prefix="/api/auth")
app.register_blueprint(alerts_bp, url_prefix="/api")
app.register_blueprint(responses_bp, url_prefix="/api")
app.register_blueprint(appeals_bp, url_prefix="/api")
app.register_blueprint(proxy_bp, url_prefix="/api")  # ✅ mount proxy routes


if __name__ == "__main__":
    app.run(debug=True, port=5000)
