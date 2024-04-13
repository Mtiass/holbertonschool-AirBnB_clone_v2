#!/usr/bin/python3
"""Script starts a Flask web application"""
from models import storage
from models.state import State
from flask import Flask, render_template

wapp = Flask(__name__)


@wapp.route("/states_list", strict_slashes=False)
def st_list():
    """Method to display a HTML page."""
    states = storage.all(State)
    return (render_template("7-states_list.html", states=states))


@wapp.teardown_appcontext
def teardown():
    """Method that removes the current SQLAlchemy session"""
    storage.close()


if __name__ == '__main__':
    wapp.run(host="0.0.0.0", port=5000)
