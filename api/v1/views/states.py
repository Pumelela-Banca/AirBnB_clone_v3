#!/usr/bin/python3
"""
create a route for states
"""
from flask import jsonify, make_response, request, abort
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
        abort(404)


@app_views.route("/states/<state_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    '''delete a state object'''
    if storage.get('State', state_id):
        storage.delete(storage.get('State', state_id))
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    '''add a state object'''
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    if not 'name' in data:
        abort(400, 'Missing name')
    else:
        new_state = State(**data)
        new_state.save()
        return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    '''update a state object'''
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    if not storage.get('State', state_id):
        abort(404)
    st = storage.get('State', state_id) 
    for att, val in data.items():
        if att != 'id' and att != 'created_at' and att != 'updated_at':
            setattr(st, att, val)
    st.save()
    return make_response(jsonify(st.to_dict()), 200)
