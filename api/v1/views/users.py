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


@app_views.route('/user/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
    gets specific user
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())
