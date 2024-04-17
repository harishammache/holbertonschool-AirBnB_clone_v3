#!/usr/bin/python3
"""
    Create a new view for City objects that handles
    all default RESTFul API actions
"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_by_state(state_id):
    """Retrieve a list of all City objects for a specific State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404, description="State not found")

    city_list = []
    for city in state.cities:
        city_list.append(city.to_dict())

    return jsonify(city_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieve a City object by its ID"""
    city = storage.get(City, city_id)
    if not city:
        abort(404, description="City not found")

    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Delete a City object by its ID"""
    city = storage.get(City, city_id)
    if not city:
        abort(404, description="City not found")

    storage.delete(city)
    storage.save()

    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Create a new City in a specific State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404, description="State not found")

    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")

    if 'name' not in data:
        abort(400, description="Missing name")

    new_city = City(name=data['name'], state_id=state_id)
    storage.new(new_city)
    storage.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """Update a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404, description="City not found")

    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")

    ignore_keys = {'id', 'state_id', 'created_at', 'updated_at'}
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)

    storage.save()

    return jsonify(city.to_dict()), 200
