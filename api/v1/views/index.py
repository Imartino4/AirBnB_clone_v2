#!/usr/bin/python3
""" Index """
from api.v1.views import app_views

@app_views.route("/status")
def status():
    json_return = {
        "status": "OK"
        }
    return(json_return)