#!/usr/bin/python3
"""
    create a route on the object app_views
"""


from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """return a json"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def number_object():
    """retrieves the number of each objects by type"""
    classes = {
        "states": State,
        "cities": City,
        "amenities": Amenity,
        "places": Place,
        "reviews": Review,
        "users": User
    }
    counts = {cls_key: storage.count(cls_val) for cls_key, cls_val in classes.items()}
    return jsonify(counts)
