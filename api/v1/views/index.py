#!/usr/bin/python3
"""
    create a route on the object app_views
"""


from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.user import User
from models.review import Review


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """return a json"""
    return jsonify({"status": "OK"})


@app_views.route("/api/v1/stats", methods=['GET'], strict_slashes=False)
def number_object():
    """retrieves the number of each objects by type"""
    stats = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(stats)
