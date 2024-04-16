#!/usr/bin/python3
"""
    create a route on the object app_views
"""


from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """return a json"""
    return jsonify({"status": "OK"})
