#!/usr/bin/python3
"""Using Flask in this module."""

from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(self):
    """Closing the storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Returning a Not Found 404 JSON response."""
    return (jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host_var = "HBNB_API_HOST"
    port_var = "HBNB_API_PORT"
    if (getenv(host_var) is None):
        host_val = "0.0.0.0"
    else:
        host_val = getenv(host_var)
    if (getenv(port_var) is None):
        port_val = "5000"
    else:
        port_val = getenv(port_var)
    app.run(host=host_val, port=port_val, threaded=True)
