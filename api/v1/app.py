#!/usr/bin/env python3
"""Rest API"""

from flask import Flask, jsonify
from datetime import datetime
from api.v1.views import app_views
from flasgger import Swagger
from models import storage
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from werkzeug.exceptions import RequestEntityTooLarge
import os


load_dotenv()


app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

UPLOAD_FOLDER = os.path.join(os.getcwd(), "assets")
MAX_CONTENT_LENGTH = 5 * 1024 * 1024
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

swagger = Swagger(app)

app.register_blueprint(app_views)


@app.route("/", methods=["GET"])
def index():
    """Root endpoint """
    resp = {"status": "OK", "time": datetime.now()}
    return jsonify(resp)


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request"}), 400


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


@app.errorhandler(RequestEntityTooLarge)
def handle_large_request(error):
    """Handle file too large errors (413)"""
    return jsonify({"error": "File too large. Maximum size is 5 MB."}), 413


@app.teardown_appcontext
def shutdown_session(exception=None):
    """Cleanup logic after each request"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
