#!/usr/bin/python3
"""Module for Amenity objects."""

from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity


@app_views.route("/amenities",
                 methods=["GET"], strict_slashes=False)
def get_amenities():
    """Return a list of Amenity objects in JSON format based on given
    State id"""
    amenities_objs = storage.all(Amenity)
    amenities_list = list()
    for key in list(amenities_objs):
        amenities_list.append(amenities_objs[key].to_dict())
    return (jsonify(amenities_list))


@app_views.route("/amenities/<amenity_id>",
                 methods=["GET"], strict_slashes=False)
def get_amenity(amenity_id):
    """Return a Amenity object in JSON format based on a given id."""
    amenity_obj = storage.get(Amenity, str(amenity_id))
    if (amenity_obj is None):
        return (jsonify({"error": "Not found"}), 404)
    amenity_dict = amenity_obj.to_dict()
    return (jsonify(amenity_dict))


@app_views.route("/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a Amenity object and returns an empty dictionary."""
    amenity_obj = storage.get(Amenity, str(amenity_id))
    if (amenity_obj is None):
        return (jsonify({"error": "Not found"}), 404)
    storage.delete(amenity_obj)
    storage.save()
    return ({}, 200)


@app_views.route("/amenities",
                 methods=["POST"], strict_slashes=False)
def add_amenity():
    """Creates a new Amenity object and returns a JSON format of it."""
    if (request.get_json() is None):
        return ("Not a JSON", 400)
    elif ("name" not in list(request.get_json())):
        return ("Missing name", 400)
    amenity_name = request.get_json()["name"]
    amenity_obj = Amenity(name=amenity_name)
    storage.new(amenity_obj)
    amenity_dict = amenity_obj.to_dict()
    storage.save()
    return (jsonify(amenity_dict), 201)


@app_views.route("amenities/<amenity_id>",
                 methods=["PUT"], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates a Amenity object and return a JSON format of it."""
    amenity_obj = storage.get(Amenity, str(amenity_id))
    if (amenity_obj is None):
        return (jsonify({"error": "Not found"}), 404)
    if (request.get_json() is None):
        return ("Not a JSON", 400)
    ignore_list = ["id", "created_at", "updated_at"]
    for key in list(request.get_json()):
        if key not in ignore_list:
            setattr(amenity_obj, key, request.get_json()[key])
    amenity_dict = amenity_obj.to_dict()
    storage.save()
    return (jsonify(amenity_dict), 200)
