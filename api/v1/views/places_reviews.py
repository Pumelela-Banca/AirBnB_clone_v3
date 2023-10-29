#!/usr/bin/python3
"""
create a route for states
"""
from flask import jsonify, make_response, request, abort
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """
    get all reviews for set place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    all_reviews = []
    for rev in place.reviews:
        all_reviews.append(rev)
    return jsonify(all_reviews)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """
    gets specific review
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """
    Delete review_id
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    return make_response(jsonify({}), 200)
