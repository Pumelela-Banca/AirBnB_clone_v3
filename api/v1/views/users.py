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
    all_users = storage.all(User).values()
    list_all_users = []
    for user in all_users:
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


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def post_user():
    """
    creates new user
    """
    pass
