#!/usr/bin/python3
"""
Creates a route for status
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status")
def status():
    """
    Returns json
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def statistic():
    """
    Returns count for all classes
    """
    cls_dict = {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")}
    return jsonify(cls_dict)
