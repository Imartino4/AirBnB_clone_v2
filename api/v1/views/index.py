#!/usr/bin/python3
""" Index """
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/status')
def status():
    """ Return status """
    return {"status": "OK"}


@app_views.route('/stats')
def counter():
    """Retrieves the number of each obj by type"""
    n_dict = {}
    for name, cls in classes.items():
        n_dict[name] = storage.count(cls)
    return(n_dict)
