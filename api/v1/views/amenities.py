#!/usr/bin/python3
"""
    Create a new view for Amenity objects
    that handles all default RESTFul API actions
"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenity():
    """Retrieve a list of all amenity objects"""
    amenities = storage.all(Amenity)
    amenity_list = []
    for amenity in amenities.values():
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieve a Amenity object by ID"""
    amenities = storage.get(Amenity, amenity_id)
    if amenities is None:
        abort(404)
    return jsonify(amenities.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete a amenities object by id"""
    amenitie = storage.get(Amenity, amenity_id)
    if amenitie is None:
        abort(404)

    storage.delete(amenitie)
    storage.save()

    return {}, 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """create a new amenity"""
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()

    if 'name' not in data:
        abort(400, 'Missing name')

    new_amenitie = Amenity(name=data['name'])
    storage.new(new_amenitie)
    storage.save()
    return jsonify(new_amenitie.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenities(amenity_id):
    """update an amenities object"""
    amenities = storage.get(Amenity, amenity_id)
    if not amenities:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenities, key, value)

    storage.save()
    return jsonify(amenities.to_dict()), 200
