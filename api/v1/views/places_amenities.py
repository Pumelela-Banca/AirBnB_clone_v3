#!/usr/bin/python3
"""
create a route for place amenities
"""
from flask import jsonify, make_response, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_place_amenities(place_id):
    """
    get all amenities for set place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    all_amenities = []
    for obj in place.amenities:
        all_amenities.append(obj.to_dict())
    return jsonify(all_amenities)


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """
    Delete amenity
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """
    Create place amenity
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if amenity.place_id == place_id:
        return make_response(jsonify(amenity.to_dict()), 200)
    else:
        return make_response(jsonify(amenity.to_dict()), 201)
