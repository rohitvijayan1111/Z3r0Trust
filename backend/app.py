from flask import Flask
from flask_cors import CORS
from routes.auth import auth
from db import app as db_app  # your MySQL connection app
from routes.alerts import alerts_bp
from routes.responses import responses_bp
from flask_cors import CORS

app = db_app
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173"]}}, supports_credentials=True)
  # Allow all origins for now

app.register_blueprint(auth, url_prefix='/api/auth')

app.register_blueprint(alerts_bp, url_prefix='/api')
app.register_blueprint(responses_bp, url_prefix='/api')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
