#!/usr/bin/python3
"""States views"""
from flask import jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states',
                 strict_slashes=False,
                 methods=['GET', 'POST'])
def view_states():
    """Returns the list of all State objects"""
    if request.method == 'POST':

        # Get the attributes from the request
        data = request.get_json()

        if isinstance(data, dict):
            pass
        else:
            return (jsonify({"error": "Not a JSON"}), 400)

        if 'name' not in data.keys():
            return jsonify({'error': 'Missing name'}), 400

        if 'id' in data.keys():
            data.pop("id")
        if 'created_at' in data.keys():
            data.pop("created_at")
        if 'updated_at' in data.keys():
            data.pop("updated_at")

        # Create the object
        obj = State(**data)

        # Save the object in storage
        storage.new(obj)
        storage.save()
        return jsonify(obj.to_dict()), 201

    if request.method == 'GET':
        states = storage.all("State")
        list = []
        for name, state in states.items():
            list.append(state.to_dict())
        return jsonify(list)


@app_views.route('/states/<id>',
                 strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def view_state(id):
    """Returns a list of all State objects, or delete an
    object if a given id
    """
    state = storage.get(State, id)

    if state is None:
        return abort(404)

    if request.method == 'GET':
        state = state.to_dict()
        return jsonify(state)

    if request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if isinstance(data, dict):
            pass
        else:
            return (jsonify({"error": "Not a JSON"}), 400)

        if 'id' in data.keys():
            data.pop("id")
        if 'created_at' in data.keys():
            data.pop("created_at")
        if 'updated_at' in data.keys():
            data.pop("updated_at")

        for key, value in data.items():
            setattr(state, key, value)

        storage.save()
        return jsonify(state.to_dict())
