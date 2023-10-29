#!/usr/bin/python3
"""
create a route for cities
"""
from flask import jsonify, make_response, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route("/states/<state_id>/cities",
                 methods=['GET'], strict_slashes=False)
def get_all_city(id_state):
    """
    gets all city objects
    """
    list_city = []
    state = storage.get("State", id_state)
    if state is None:
        abort(404)
    for city in state.cities:
        list_city.append(city.to_dict())
    return jsonify(list_city)


@app_views.route('/cities/<city_id>/',
                 methods=['GET'], strict_slashes=False)
def get_city(id_city):
    """
    gets city
    """
    city = storage.get("City", id_city)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """
    deletes city object
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """
    Create new city
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404, "Not a JSON")
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")

    data = request.get_json()
    city = City(**data)
    city.state_id = state_id
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """
    update city
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")

    data = request.get_json()
    skip = ["id", "state_id", "created_at", "updated_at"]
    for k, v in data.items():
        if k in skip:
            continue
        setattr(city, k, v)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
