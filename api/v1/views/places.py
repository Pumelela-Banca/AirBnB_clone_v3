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
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    if len(data.keys()) == 0:
        all_places_list = []
        for v in storage.all('Place').values():
            all_places_list.append(v.to_dict())
        return jsonify(all_places_list)
    flag = 0
    for val in data.values():
        if len(val) != 0:
            flag = 1
            break
    if flag == 0:
        all_places_list = []
        for v in storage.all('Place').values():
            all_places_list.append(v.to_dict())
        return jsonify(all_places_list)
    res = []
    if data.get('states') and len(data.get('states')) > 0:
        for state_id in data.get('states'):
            st = storage.get('State', state_id)
            if st:
                state_cities = st.cities
                for ct in state_cities:
                    pls = ct.places
                    for pl in pls:
                        res.append(pl)
    if data.get('cities') and len(data.get('cities')) > 0:
        for city_id in data.get('cities'):
            ct = storage.get('City', city_id)
            if ct:
                pls = ct.places
                for pl in pls:
                    res.append(pl)
    res_amenity = []
    flag_am = 0
    if data.get('amenities') and len(data.get('amenities')) > 0:
        flag_am = 1
        for amenity_id in data.get('amenities'):
            amenity = storage.get('Amenity', amenity_id)
            if len(res) == 0:
                for pl in storage.all('Place').values():
                    if amenity in pl.amenities:
                        res_amenity.append(pl)
            else:
                for pl in res:
                    if amenity in pl.amenities:
                        res_amenity.append(pl)
    final_result = []
    if flag_am == 1:
        for pl in res_amenity:
            final_result.append(pl.to_dict())
    else:
        for pl in res:
            final_result.append(pl.to_dict())
    return make_response(jsonify(final_result), 200)
