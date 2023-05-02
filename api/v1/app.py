#!/usr/bin/python3
"""Defines flask aplications"""

from models import storage
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort
from flask_cors import CORS

app = Flask(__name__)


app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def error_handler(error):
    """Error handler, 404 response"""
    response = jsonify({"error": "Not found"})
    return response, 404


@app.teardown_appcontext
def teardown(exception):
    """Close process"""
    storage.close()


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = int(getenv('HBNB_API_PORT', default=5000))
    app.run(host=host, port=port, threaded=True)
