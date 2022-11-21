#!/usr/bin/python3
"""initiate a flask app
"""

from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

host = getenv('HBNB_API_HOST', '0.0.0.0')
port = getenv('HBNB_API_PORT', 5000)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """call close method
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """custom 404 page
    """
    err = {'error': 'Not found'}
    return jsonify(err), 404


if __name__ == "__main__":
    app.run(host=host, port=port, debug=True)
