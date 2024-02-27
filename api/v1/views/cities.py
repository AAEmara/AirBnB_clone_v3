#!/usr/bin/python3
"""Module for City objects."""

from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities",
                 methods=["GET"], strict_slashes=False)
def get_cities(state_id):
    """Return a list of City objects in JSON format based on given State id"""
    state_obj = storage.get(State, str(state_id))
    if (state_obj is None):
        return (jsonify({"error": "Not found"}), 404)
    cities_objs = storage.all(City)
    cities_list = list()
    for key in cities_objs:
        if (cities_objs[key].state_id == state_obj.id):
            cities_list.append(cities_objs[key].to_dict())
    return (jsonify(cities_list))


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """Return a City object in JSON format based on a given id."""
    city_obj = storage.get(City, str(city_id))
    if (city_obj is None):
        return (jsonify({"error": "Not found"}), 404)
    city_dict = city_obj.to_dict()
    return (jsonify(city_dict))


@app_views.route("/cities/<city_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object and returns an empty dictionary."""
    city_obj = storage.get(City, str(city_id))
    if (city_obj is None):
        return (jsonify({"error": "Not found"}), 404)
    storage.delete(city_obj)
    storage.save()
    return ({}, 200)


@app_views.route("/states/<state_id>/cities",
                 methods=["POST"], strict_slashes=False)
def add_city(state_id):
    """Creates a new City object and returns a JSON format of it."""
    state_obj = storage.get(State, str(state_id))
    if (state_obj is None):
        return (jsonify({"error": "Not found"}), 404)
    if (request.get_json() is None):
        return ("Not a JSON", 400)
    elif ("name" not in list(request.get_json())):
        return ("Missing name", 400)
    city_name = request.get_json()["name"]
    city_obj = City(name=city_name, state_id=state_id)
    storage.new(city_obj)
    city_dict = city_obj.to_dict()
    storage.save()
    return (jsonify(city_dict), 201)


@app_views.route("/cities/<city_id>",
                 methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """Updates a City object and return a JSON format of it."""
    city_obj = storage.get(City, str(city_id))
    if (city_obj is None):
        return (jsonify({"error": "Not found"}), 404)
    if (request.get_json() is None):
        return ("Not a JSON", 400)
    ignore_list = ["id", "created_at", "updated_at"]
    for key in list(request.get_json()):
        if key not in ignore_list:
            setattr(city_obj, key, request.get_json()[key])
    city_dict = city_obj.to_dict()
    storage.save()
    return (jsonify(city_dict), 200)
