#!/usr/bin/python3
"""cities file"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.state import State
from models.city import City
from models import storage


@app_views.route("/states/<state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def allCity(state_id):
    """list of all city objects"""
    city_list = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for city in state.cities:
        city_list.append(city.to_dict())
    return jsonify(city_list)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def city_by_id(city_id):
    """list one city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return city.to_dict()


@app_views.route("/cities/<city_id>", methods=['DELETE'], strict_slashes=False)
def city_delete(city_id):
    """Delete a city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        city.delete()
        storage.save()
        return {}, 200


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def city_post(state_id):
    """list of all city objects"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    body = request.get_json()
    if body is None:
        abort(400, description="Not a JSON")
    if 'name' not in body.keys():
        abort(400, description="Missing name")
    body['state_id'] = state_id
    city = City(**body)
    city.save()
    return city.to_dict(), 201


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def city_put(city_id):
    """list of all city objects"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    body = request.get_json()
    if body is None:
        abort(400, description="Not a JSON")
    ignored_keys = ('id', 'state_id', 'created_at', 'updated_at')
    for key, value in body.items():
        if key not in ignored_keys:
            setattr(city, key, value)
    storage.save()
    return city.to_dict(), 200
