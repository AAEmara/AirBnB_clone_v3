#!/usr/bin/python3
"""Module for Place objects."""

from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.place import Place


@app_views.route("/cities/<city_id>/places",
                 methods=["GET"], strict_slashes=False)
def get_places(city_id):
    """Return a list of Place objects in JSON formatn based on city_id."""
    city_obj = storage.get(City, str(city_id))
    if (city_obj is None):
        return (jsonify({"error": "Not found"}), 404)
    places_objs = storage.all(Place)
    places_list = list()
    for key in list(places_objs):
        places_list.append(places_objs[key].to_dict())
    return (jsonify(places_list))


@app_views.route("/places/<place_id>",
                 methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """Return a Place object in JSON format based on a given id."""
    place_obj = storage.get(Place, str(place_id))
    if (place_obj is None):
        return (jsonify({"error": "Not found"}), 404)
    place_dict = place_obj.to_dict()
    return (jsonify(place_dict))


@app_views.route("/places/<place_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object and returns an empty dictionary."""
    place_obj = storage.get(Place, str(place_id))
    if (place_obj is None):
        return (jsonify({"error": "Not found"}), 404)
    storage.delete(place_obj)
    storage.save()
    return ({}, 200)


@app_views.route("/cities/<city_id>/places",
                 methods=["POST"], strict_slashes=False)
def add_place(city_id):
    """Creates a new Place object and returns a JSON format of it."""
    place_obj = storage.get(Place, str(place_id))
    if (place_obj is None):
        return (jsonify({"error": "Not found"}), 404)
    if (request.get_json() is None):
        return ("Not a JSON", 400)
    if ("user_id" not in list(request.get_json())):
        return ("Missing user_id", 400)
    user_obj = storage.get(User, str(request.get_json()["user_id"]))
    if (user_obj is None):
        return (jsonify({"error": "Not found"}), 404)
    if ("name" not in list(request.get_json())):
        return ("Missing name", 400)
    place_name = request.get_json()["name"]
    user_id = request.get_json()["user_id"]
    place_obj = Place(name=place_name, city_id=city_id, user_id=user_id)
    storage.new(place_obj)
    place_dict = place_obj.to_dict()
    storage.save()
    return (jsonify(place_dict), 201)


@app_views.route("places/<place_id>",
                 methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object and return a JSON format of it."""
    place_obj = storage.get(Place, str(place_id))
    if (place_obj is None):
        return (jsonify({"error": "Not found"}), 404)
    if (request.get_json() is None):
        return ("Not a JSON", 400)
    ignore_list = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key in list(request.get_json()):
        if key not in ignore_list:
            setattr(place_obj, key, request.get_json()[key])
    place_dict = place_obj.to_dict()
    storage.save()
    return (jsonify(place_dict), 200)
