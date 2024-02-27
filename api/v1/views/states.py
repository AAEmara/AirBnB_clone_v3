#!/usr/bin/python3
"""Module for State objects."""

from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def all():
    """Return all State objects in JSON format."""
    all_states = storage.all(State)
    all_list = list()
    for key in all_states:
        all_list.append(all_states[key].to_dict())
    return (jsonify(all_list))


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """Return a State object in JSON format based on a given id."""
    state_obj = storage.get(State, str(state_id))
    if (state_obj is None):
        return (jsonify({"error": "Not found"}), 404)
    state_dict = state_obj.to_dict()
    return (jsonify(state_dict))


@app_views.route("/states/<state_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object in JSON format based on given id."""
    state_obj = storage.get(State, str(state_id))
    if (state_obj is None):
        return (jsonify({"error": "Not found"}), 404)
    storage.delete(state_obj)
    storage.save()
    return ({}, 200)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def add_state():
    """Posting a new State object and return a JSON format."""
    if (request.get_json() is None):
        return ("Not a JSON", 400)
    elif ("name" not in list(request.get_json())):
        return ("Missing name", 400)
    state_name = request.get_json()["name"]
    state_obj = State(name=state_name)
    storage.new(state_obj)
    state_dict = state_obj.to_dict()
    storage.save()
    return (jsonify(state_dict), 201)


@app_views.route("/states/<state_id>",
                 methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """Updating the desired State object and return a JSON format."""
    state_obj = storage.get(State, str(state_id))
    if (state_obj is None):
        return (jsonify({"error": "Not found"}), 404)
    if (request.get_json() is None):
        return ("Not a JSON", 400)
    ignore_list = ["id", "created_at", "updated_at"]
    for key in list(request.get_json()):
        if key not in ignore_list:
            setattr(state_obj, key, request.get_json()[key])
    state_dict = state_obj.to_dict()
    storage.save()
    return (jsonify(state_dict), 200)
