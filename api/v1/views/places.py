#!/usr/bin/python3
"""
    Create a new view for place objects that handles
    all default RESTFul API actions
"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_state(state_id):
    """Retrieve a list of all state_id objects"""
    state = storage.get(Place, state_id)
    if not state:
        abort(404, description="State not found")

    place_list = []
    for place in state.cities:
        place_list.append(place.to_dict())

    return jsonify(place_list)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieve a place object by its ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Delete a City object by its ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()

    return {}, 200


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Create a new place"""
    if not request.is_json:
        abort(400, 'Not a JSON')

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json(silent=True)

    if 'user_id' not in data:
        abort(400, 'Missing user_id')

    if 'name' not in data:
        abort(400, "Missing name")

    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)

    new_place = Place(city_id=city_id,
                      user_id=data['user_id'], name=data['name'])

    storage.new(new_place)
    storage.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Update a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if not request.is_json:
        abort(400, 'Not a JSON')

    data = request.get_json()

    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    storage.save()

    return jsonify(place.to_dict()), 200
