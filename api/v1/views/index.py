#!/usr/bin/python3

"""
Creates a route for status
"""

import json
from api.v1.views import app_views


@app_views.route("/status")
def status():
    """
    Returns json
    """
    return json.dumps({"status": "OK"})
