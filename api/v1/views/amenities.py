#!/usr/bin/python3
"""
create a route for states
"""
from flask import jsonify, make_response, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def retrieve_all_amenities():
    '''Retrieve all amenities objects in storage'''
    all_amenities_list = []
    for k, v in storage.all("Amenity").items():
        all_amenities_list.append(v.to_dict())
    return jsonify(all_amenities_list)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def retrieve_amenity(amenity_id):
    '''retrieve a specific object'''
    if storage.get("Amenity", amenity_id):
        return jsonify(storage.get("Amenity", amenity_id).to_dict())
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    '''delete an amenity object'''
    if storage.get("Amenity", amenity_id):
        storage.delete(storage.get("Amenity", amenity_id))
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    '''add a state object'''
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    else:
        new_amenity = Amenity(**data)
        new_amenity.save()
        return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    '''update a amenity object'''
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    if not storage.get("Amenity", amenity_id):
        abort(404)
    am = storage.get("Amenity", amenity_id)
    for att, val in data.items():
        if att != 'id' and att != 'created_at' and att != 'updated_at':
            setattr(am, att, val)
    am.save()
    return make_response(jsonify(am.to_dict()), 200)
