#!/usr/bin/python3
"""States views"""
from flask import jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.user import User
from models.place import Place


@app_views.route('/cities/<id>/places',
                 strict_slashes=False,
                 methods=['GET', 'POST'])
def view_places(id):
    """Returns a list of all places of a city, or delete a
    place if a given id
    """
    city = storage.get(City, id)
    user = storage.get(User, id)

    if city is None:
        return abort(404)

    if request.method == 'GET':

        list = []
        for place in city.places:
            list.append(place.to_dict())
        return jsonify(list)

    if request.method == 'POST':
        # Get the attributes from the request
        if user is None:
            return abort(404)

        data = request.get_json()

        if isinstance(data, dict):
            pass
        else:
            return jsonify({"error": "Not a JSON"}), 400

        if 'name' not in data.keys():
            return jsonify({'error': 'Missing name'}), 400

        if 'user_id' not in data.keys():
            return jsonify({'error': 'Missing user_id'}), 400

        data.update({"place_id": id})

        # Create the object
        obj = Place(**data)

        # Save the object in storage
        storage.new(obj)
        storage.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/places/<id>',
                 strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def view_place_by_id(id):
    """Returns or erases a place"""
    place = storage.get(Place, id)

    if place is None:
        return abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if isinstance(data, dict):
            pass
        else:
            return jsonify({"error": "Not a JSON"}), 400

        for key, value in data.items():
            if key not in ["id", "user_id", "city_id",
                           "created_at", "updated_at"]:
                setattr(place, key, value)

        storage.save()
        return jsonify(place.to_dict()), 200
