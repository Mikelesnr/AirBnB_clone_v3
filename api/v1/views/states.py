#!/usr/bin/python3
"""view for state to handle restful APIs
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def states(state_id=None):
    """REST API for state
    """
    states = storage.all('State')

    if request.method == 'GET':
        if not state_id:
            temp = []
            for obj in states.values():
                temp.append(obj.to_dict())
            return jsonify(temp)

        key = 'State.' + state_id
        try:
            return jsonify(states[key].to_dict())
        except KeyError:
            abort(404)

    elif request.method == 'DELETE':
        try:
            key = 'State.' + state_id
            storage.delete(states[key])
            storage.save()
            return jsonify({}), 200
        except:
            abort(404)

    elif request.method == 'POST':
        if request.is_json:
            body_request = request.get_json()
        else:
            abort(400, 'Not a JSON')

        if 'name' in body_request:
            new_state = State(**body_request)
            storage.new(new_state)
            storage.save()
            return jsonify(new_state.to_dict()), 201
        else:
            abort(400, 'Missing name')

    elif request.method == 'PUT':
        key = 'State.' + state_id
        try:
            state = states[key]

            if request.is_json:
                body_request = request.get_json()
            else:
                abort(400, 'Not a JSON')

            for key, value in body_request.items():
                if key != 'id' and key != 'created_at' and key != 'updated_at':
                    setattr(state, key, value)

            storage.save()
            return jsonify(state.to_dict()), 200

        except KeyError:
            abort(404)
