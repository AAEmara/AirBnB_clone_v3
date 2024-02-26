#!/usr/bin/python3
"""Module of index file."""

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """Returns status in JSON."""
    status_dict = {"status": "OK"}
    return (jsonify(status_dict))
