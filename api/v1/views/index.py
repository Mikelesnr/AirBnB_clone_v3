#!/usr/bin/python3
"""Status of my API endpoint
"""
from api.v1.views import app_views
from flask import request, jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """Rest API
    """
    if request.method == 'GET':
        res = {"status": "OK"}
        return jsonify(res)


@app_views.route('/stats', methods=['GET'])
def stats():
    """Rest API
    """
    if request.method == 'GET':
        res = {}
        cls = {
            "Amenity": "amenities",
            "city": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
        }
        for key, value in cls.items():
            res[value] = storage.count(key)
        return jsonify(res)
