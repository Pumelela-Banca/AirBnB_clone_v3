#!/usr/bin/python3
"""
Creates a route for status
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status")
def status():
    """
    Returns json
    """
    return jsonify({"status": "OK"})
