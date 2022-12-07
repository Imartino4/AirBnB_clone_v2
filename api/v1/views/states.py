#!/usr/bin/python3
""" handles all default RESTFul API actions for State objects """
from flask import Flask, request, abort, jsonify
from models import storage
from api.v1.views import app_views
from models.state import State

# app_views.url_map.strict_slashes = False


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<s_id>', methods=['GET'], strict_slashes=False)
def get_obj(s_id=None):
    """Retrieve all states objects"""
    dict_list = []
    if s_id is None:
        for state_objs in storage.all(State).values():
            dict_list.append(state_objs.to_dict())
        return dict_list
    else:
        for k, v in storage.all(State).items():
            if v.id == s_id:
                return (v.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_obj(state_id):
    """Deletes state obj with state_id"""
    inst = storage.get(State, state_id)
    if inst:
        storage.delete(inst)
        storage.save()
        return ({}, 200)
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_obj():
    """Creates a new instance of State"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    elif 'name' not in request.get_json():
        abort(400, 'Missing name')

    new_state_obj = State(**request.get_json())
    new_state_obj.save()
    new_s_dict = new_state_obj.to_dict()
    return(new_s_dict, 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_obj(state_id):
    """Updates an instance of State"""
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state_obj, k, v)
    state_obj.save()
    return (jsonify(state_obj.to_dict()), 200)
