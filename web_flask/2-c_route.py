#!/usr/bin/python3
"""Script that starts a Flask web application"""
from flask import Flask


wapp = Flask(__name__)


@wapp.route('/', strict_slashes=False)
def greetings():
    """Method that displays "Hello HBNB!" in route '/'."""
    return "Hello HBNB!"


@wapp.route('/hbnb', strict_slashes=False)
def greet_hbnb():
    """Method that displays "HBNB" in route '/hbnb'."""
    return "HBNB"


@wapp.route('/c/<text>', strict_slashes=False)
def c_route(text):
    """Method that displays c and <text> in route '/c/<text>."""
    text = text.replace('_', ' ')
    return ("C {}".format(text))


if __name__ == "__main__":
    wapp.run(host='0.0.0.0', port=5000)
