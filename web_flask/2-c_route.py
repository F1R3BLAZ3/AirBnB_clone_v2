#!/usr/bin/python3
"""
This is a Flask web application with three routes.
"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Display "Hello HBNB!" on the root route.
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Display "HBNB" on the '/hbnb' route.
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_variable(text):
    """
    Display "C " followed by the value of the text variable.
    Replace underscore (_) symbols with a space.
    """
    return "C " + text.replace("_", " ")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
