#!/usr/bin/python3
"""Module of index file."""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route("/status")
def status():
    """Returns status in JSON."""
    status_dict = {"status": "OK"}
    return (jsonify(status_dict))


@app_views.route("/stats")
def objs_count():
    """Returns the count of objects in JSON format."""
    count_dict = dict()
    for key in list(classes):
        count_dict[key] = storage.count(classes[key])
    return (jsonify(count_dict))
