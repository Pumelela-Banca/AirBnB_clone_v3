#!/usr/bin/python3
"""
create a route for cities
"""
from flask import jsonify, make_response, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Gets all users
    """
    users = storage.all(User).values()
    list_all_users = []
    for user in users:
        list_all_users.append(user.to_dict())
    return jsonify(list_all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
    gets specific user
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<users_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    Deletes specific user
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """
    creates new user
    """
    data = request.get_json(silent=True)
    if not data:
        abort(400, "Not a JSON")
    if "email" not in data:
        abort(400, "Missing email")
    if "password" not in data:
        abort(400, "Missing password")
    new = User(**data)
    new.save()
    return make_response(jsonify(new.to_dict()), 201)


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """
    updates user
    """
    user = storage.get(User, user_id)
    data = request.get_json(silent=True)
    if not user:
        abort(404)
    if not data:
        abort(400, "Not a JSON")
    skip = ['id', 'email', 'created_at', 'updated_at']
    for k, v in data.items():
        if k not in skip:
            setattr(user, k, v)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
