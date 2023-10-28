#!/usr/bin/python3
"""
create a flask app
"""
import sys
sys.path.append('../..')
from os import environ
from flask import Flask
from models import storage
from api.v1.views import app_views


app =  Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(exception=None):
    """ tear down function
    """
    storage.close()


if __name__ == "__main__":
    if environ.get("HBNB_API_HOST"):
        _host = environ.get("HBNB_API_HOST")
    else:
        _host = '0.0.0.0'
    if environ.get("HBNB_API_PORT"):
        _port = environ.get("HBNB_API_PORT")
    else:
        _port = '5000'
    app.run(host=_host, port=_port, threaded=True)
