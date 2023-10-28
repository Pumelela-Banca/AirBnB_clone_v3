#!/usr/bin/python3
"""
create a route for states
"""
from flask import jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def retrieve_all_state():
    '''Retrieve all states objects in storage'''
    all_state_list = []
    for k, v in storage.all(State).items():
        all_state_list.append(v.to_dict())
    return jsonify(all_state_list)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def retrieve_state(state_id):
    '''retrieve a specific object'''
    if storage.get('State', state_id):
        return jsonify(storage.get('State', state_id).to_dict())
    else:
        return make_response(jsonify({'error': "Not found"}), 404)


@app_views.route("/states/<state_id>", methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    '''delete a state object'''
    if storage.get('State', state_id):
        storage.delete(storage.get('State', state_id))
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        return make_response(jsonify({'error': "Not found"}), 404)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def add_state():
    '''add a state object'''
    try:
        data = request.get_json()
    except Exception:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    if not data or 'name' not in data:
        return make_response(jsonify({'error': "Missing name"}), 400)
    else:
        new_state = State(name=data.get('name'))
        storage.new(new_state)
        storage.save()
        return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    '''update a state object'''
    if not storage.get('State', state_id):
        return make_response(jsonify({'error': "Not found"}), 404)
    else:
        st = storage.get('State', state_id)
    try:
        data = request.get_json()
    except Exception:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    for att, val in data.items():
        if att != 'id' and att != 'created_at' and att != 'updated_at':
            setattr(st, att, val)
    storage.save()
    return make_response(jsonify(st.to_dict()), 200)
