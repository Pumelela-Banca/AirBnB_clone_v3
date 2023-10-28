#!/usr/bin/python3
"""create a variable app_views
   which is an instance of Blueprint"""
from flask import Blueprint
'''from api.v1.views.index import *'''


app_views = Blueprint("app_views", url_prefix="/api/v1", __name__)
