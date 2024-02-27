#!/usr/bin/python3
"""Module for Amenity objects."""

from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User


@app_views.route("/users",
                 methods=["GET"], strict_slashes=False)
def get_users():
    """Return a list of User objects in JSON format."""
    users_objs = storage.all(User)
    users_list = list()
    for key in list(users_objs):
        users_list.append(users_objs[key].to_dict())
    return (jsonify(users_list))


@app_views.route("/users/<user_id>",
                 methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """Return a User object in JSON format based on a given id."""
    user_obj = storage.get(User, str(user_id))
    if (user_obj is None):
        return (jsonify({"error": "Not found"}), 404)
    user_dict = user_obj.to_dict()
    return (jsonify(user_dict))


@app_views.route("/users/<user_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object and returns an empty dictionary."""
    user_obj = storage.get(User, str(user_id))
    if (user_obj is None):
        return (jsonify({"error": "Not found"}), 404)
    storage.delete(user_obj)
    storage.save()
    return ({}, 200)


@app_views.route("/users",
                 methods=["POST"], strict_slashes=False)
def add_users():
    """Creates a new User object and returns a JSON format of it."""
    if (request.get_json() is None):
        return ("Not a JSON", 400)
    elif ("email" not in list(request.get_json())):
        return ("Missing email", 400)
    elif ("password" not in list(request.get_json())):
        return ("Missing password", 400)
    user_obj = User(email=email, password=password)
    storage.new(user_obj)
    user_dict = user_obj.to_dict()
    storage.save()
    return (jsonify(user_dict), 201)


@app_views.route("users/<user_id>",
                 methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """Updates a User object and return a JSON format of it."""
    user_obj = storage.get(User, str(user_id))
    if (user_obj is None):
        return (jsonify({"error": "Not found"}), 404)
    if (request.get_json() is None):
        return ("Not a JSON", 400)
    ignore_list = ["id", "email", "created_at", "updated_at"]
    for key in list(request.get_json()):
        if key not in ignore_list:
            setattr(user_obj, key, request.get_json()[key])
    user_dict = user_obj.to_dict()
    storage.save()
    return (jsonify(user_dict), 200)
