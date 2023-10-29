#!/usr/bin/python3
"""
create a route for cities
"""
from flask import jsonify, make_response, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_user():
    """
    Gets all users
    """
    all_users = storage.all(User).values()
    list_all_users = []
    for user in all_users:
        list_all_users.append(user.to_dict())

    return jsonify(list_all_users)


