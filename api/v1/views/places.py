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
    city = storage.get("City", str(city_id))
    if city is None:
        abort(404)
    else:
        all_city_places_list = []
        for v in city.places:
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
    if not data:
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


@app_views.route("/places_search", methods=["POST"],
                 strict_slashes=False)
def place_serach():
    """search place"""
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    if data and len(data):
        states = data.get('states', [])
        cities = data.get('cities', [])
        amenities = data.get('amenities', [])
    if not data or not len(data) or (
            not len(states) and
            not len(cities) and
            not len(amenities)):
        all_places_list = []
        for v in storage.all('Place').values():
            all_places_list.append(v.to_dict())
        return make_response(jsonify(all_places_list), 200)
    res = []
    for state_id in states:
        state = storage.get('State', state_id)
        if state:
            state_cities = state.cities
            for city in state_cities:
                pls = city.places
                for pl in pls:
                    if pl not in res:
                        res.append(pl)
    for city_id in cities:
        city = storage.get('City', city_id)
        if city:
            pls = city.places
            for pl in pls:
                if pl not in res:
                    res.append(pl)
    flag_am = 0
    res_amenity = []
    for amenity_id in amenities:
        amenity = storage.get('Amenity', amenity_id)
        if amenity:
            flag_am = 1
            if not len(res):
                res = storage.all('Place').values()
            for pl in res:
                if amenity in pl.amenities:
                    res_amenity.append(pl)
    final_result = []
    if flag_am == 1:
        for pl in res_amenity:
            final_result.append(pl.to_dict().pop('amenities', None))
    else:
        for pl in res:
            final_result.append(pl.to_dict().pop('amenities', None))
    return make_response(jsonify(final_result), 200)
