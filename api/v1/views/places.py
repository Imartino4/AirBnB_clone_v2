#!/usr/bin/python3
"""Flask api module for places"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from models.state import State
from models.amenity import Amenity


@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def all_places(city_id):
    """list of all place objects"""
    place_list = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for place in city.places:
        place_list.append(place.to_dict())
    return jsonify(place_list)


@app_views.route("/places/<places_id>", methods=['GET'],
                 strict_slashes=False)
def places_by_id(places_id):
    """list one place object"""
    place = storage.get(Place, places_id)
    if place is None:
        abort(404)
    return place.to_dict()


@app_views.route("/places/<places_id>", methods=['DELETE'],
                 strict_slashes=False)
def places_delete(places_id):
    """Delete a place object"""
    place = storage.get(Place, places_id)
    if place is None:
        abort(404)
    else:
        place.delete()
        storage.save()
        return {}, 200


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def places_post(city_id):
    """list of all place objects"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    body = request.get_json()
    if body is None:
        abort(400, description="Not a JSON")
    if 'user_id' not in body.keys():
        abort(400, description="Missing user_id")
    user = storage.get(User, body.get('user_id'))
    if user is None:
        abort(404)
    if 'name' not in body.keys():
        abort(400, description="Missing name")
    body['city_id'] = city_id
    place = Place(**body)
    place.save()
    return place.to_dict(), 201


@app_views.route("/places/<places_id>", methods=['PUT'], strict_slashes=False)
def places_put(places_id):
    """list of all place objects"""
    place = storage.get(Place, places_id)
    if place is None:
        abort(404)
    body = request.get_json()
    if body is None:
        abort(400, description="Not a JSON")
    ignored_keys = ('id', 'user_id', 'city_id' 'created_at', 'updated_at')
    for key, value in body.items():
        if key not in ignored_keys:
            setattr(place, key, value)
    storage.save()
    return place.to_dict(), 200


@app_views.route("/places_search", methods=['POST'],
                 strict_slashes=False)
def search_place():
    """Search places, filtering by state, city and amenities"""
    body = request.get_json()
    if body is None:
        return 'Not a JSON', 400
    places = []
    states_id_list = body.get('states')
    cities_list = []
    if (states_id_list):
        for id in states_id_list:
            state = storage.get(State, id)
            if (state is not None):
                for city in state.cities:
                    cities_list.append(city)
    cities_id_list = body.get('cities')
    if (cities_id_list):
        for id in cities_id_list:
            city = storage.get(City, id)
            if city is not None and city not in cities_list:
                cities_list.append(city)
    if (len(cities_list) == 0):
        for place in storage.all(Place).values():
            places.append(place)
    else:
        for city in cities_list:
            for place in city.places:
                places.append(place)
    places_cleared = places.copy()
    for place in places:
        check = 0
        if body.get('amenities'):
            for id in body.get('amenities'):
                curr_amenity = storage.get(Amenity, id)
                if (curr_amenity and curr_amenity not in place.amenities):
                    check = 1
                    break
        if check == 1:
            places_cleared.remove(place)
    places = places_cleared
    for i in range(len(places)):
        places[i] = places[i].to_dict()
        if 'amenities' in places[i].keys():
            places[i].pop('amenities')
    return jsonify(places)
