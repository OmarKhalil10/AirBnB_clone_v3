#!/usr/bin/python3
"""States views"""
from flask import jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.review import Review
from models.user import User


@app_views.route('/places/<id>/reviews',
                 strict_slashes=False,
                 methods=['GET', 'POST'])
def view_reviews_of_place(id):
    """Returns a list of all reviews of a place, or delete a
    review if a given id
    """
    place = storage.get(Place, id)

    if place is None:
        return abort(404)

    if request.method == 'GET':

        list = []
        for review in place.reviews:
            list.append(review.to_dict())
        return jsonify(list)

    if request.method == 'POST':
        # Get the attributes from the request
        data = request.get_json()
        user = storage.get(User, id)

        if user is None:
            return abort(404)

        if isinstance(data, dict):
            pass
        else:
            return jsonify({"error": "Not a JSON"}), 400

        if 'user_id' not in data.keys():
            return jsonify({'error': 'Missing user_id'}), 400

        if 'text' not in data.keys():
            return jsonify({'error': 'Missing text'}), 400

        if 'id' in data.keys():
            data.pop("id")
        if 'created_at' in data.keys():
            data.pop("created_at")
        if 'updated_at' in data.keys():
            data.pop("updated_at")

        data.update({"place_id": id})

        # Create the object
        obj = Review(**data)

        # Save the object in storage
        storage.new(obj)
        storage.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/review/<id>',
                 strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def view_review_id(id):
    """Returns or erases a city"""
    review_obj = storage.get(Review, id)

    if review_obj is None:
        return abort(404)

    if request.method == 'GET':
        return jsonify(review_obj.to_dict())

    if request.method == 'DELETE':
        storage.delete(review_obj)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if isinstance(data, dict):
            pass
        else:
            return jsonify({"error": "Not a JSON"}), 400

        if 'id' in data.keys():
            data.pop("id")
        if 'created_at' in data.keys():
            data.pop("created_at")
        if 'updated_at' in data.keys():
            data.pop("updated_at")

        for key, value in data.items():
            setattr(review_obj, key, value)

        storage.save()
        return jsonify(review_obj.to_dict())
