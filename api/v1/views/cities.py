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
    for city in storage.all(City).values():
        list_city.append(city.to_dict())
    return jsonify(list_city)


@app_views.route('/cities/<city_id>/',
                 methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
    gets city
    """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """
    deletes city object
    """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """
    Create new city
    """
    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    city = City(**data)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """
    update city
    """
    data = request.get_json(silent=True)
    city = storage.get("City", city_id)
    if data is None:
        abort(404, "Not a JSON")
    if not city:
        abort(404)

    skip = ["id", "state_id", "created_at", "updated_at"]
    for k, v in data.items():
        if k not in skip:
            setattr(city, k, v)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
