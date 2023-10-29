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
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """
    Create review
    """
    data = request.get_json()
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not data:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")

    user = storage.get(User, data["user_id"])
    if not user:
        abort(404)
    if "text" not in data:
        abort(400, "Missing text")
    data["place_id"] = place_id
    new_rev = Review(**data)
    new_rev.save()
    return make_response(jsonify(new_rev.to_dict()), 201)


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """
    updates a review
    """
    review = storage.get(Review, review_id)
    data = request.get_json()
    if not review:
        abort(404)
    if not data:
        abort(400, "Not a JSON")
    skip = ['id', 'email', 'created_at', 'updated_at']
    for k, v in data.items():
        if k not in skip:
            setattr(review, k, v)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
