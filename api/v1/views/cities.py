#!/usr/bin/python3
"""view for city to handle restful APIs
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def city(state_id):
    """Rest API for city
    """
    cities = storage.all(City)
    states = storage.all(State)

    if request.method == "GET":
        state_key = "State." + state_id
        try:
            state = states[state_key]
            for city in state.cities:
                cities = [city.to_dict()]
                return jsonify(cities)
        except KeyError:
            abort(404)

    elif request.method == "POST":
        if request.is_json:
            body_request = request.get_json()
        else:
            abort(400, "Not a JSON")
        if 'name' in body_request:
            state_key = "State." + state_id
            if state_key not in states:
                abort(404)
            body_request.update({"state_id": state_id})
            new_city = City(**body_request)
            storage.new(new_city)
            storage.save()
            return jsonify(new_city.to_dict()), 201
        else:
            abort(400, "Missing name")


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def cities_id(city_id):
    """
    """
    cities = storage.all(City)

    if request.method == "GET":
        if not city_id:
            for obj in cities.values():
                objec = [obj.to_dict()]
                return jsonify(objec)
        key = "City." + city_id
        try:
            return jsonify(cities[key].to_dict())
        except KeyError:
            abort(404)

    elif request.method == "DELETE":
        try:
            key = "City." + city_id
            storage.delete(cities[key])
            storage.save()
            return jsonify({}), 200
        except:
            abort(404)

    elif request.method == "PUT":
        city_key = "City." + city_id
        try:
            city = cities[city_key]
        except KeyError:
            abort(404)
        if request.is_json:
            new = request.get_json()
        else:
            abort(400, "Not a JSON")
        for key, value in new.items():
            if key != "id" and key != "state_id" and key != "created_at" and\
               key != "updated_at":
                setattr(city, key, value)
            storage.save()
            return city.to_dict(), 200
