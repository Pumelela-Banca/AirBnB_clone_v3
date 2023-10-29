#!/usr/bin/python3
"""
create a route for states
"""
from flask import jsonify, make_response, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def retrieve_all_places_in_city(city_id):
    '''Retrieve all places objects linked to the city'''
    allplaces = storage.get("City", str(city_id)).places
    if allplaces is None:
        abort(404)
    else:
        all_city_places_list = []
        for v in allplaces:
            all_city_places_list.append(v.to_dict())
        return jsonify(all_city_places_list)


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
def retrieve_place(place_id):
    '''retrieve a specific object'''
    if storage.get("Place", place_id):
        return jsonify(storage.get("Place", place_id).to_dict())
    else:
        abort(404)


@app_views.route("/places/<place_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    '''delete an Place object'''
    if storage.get("Place", place_id):
        storage.delete(storage.get("Place", place_id))
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route("/cities/<city_id>/places",
                 methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    '''add a place object'''
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing name')
    if storage.get("City", city_id) is None:
        abort(404)
    if storage.get("User", data['user_id']) is None:
        abort(404)
    data['city_id'] = city_id
    new_place = Place(**data)
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def update_place(place_id):
    '''update a place object'''
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    if not storage.get("Place", place_id):
        abort(404)
    pl = storage.get("Place", place_id)
    for att, val in data.items():
        if att not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(pl, att, val)
    pl.save()
    return make_response(jsonify(pl.to_dict()), 200)
