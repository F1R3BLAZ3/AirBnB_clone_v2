#!/usr/bin/python3
"""
This is a basic Flask web application that responds to a single route.
"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Display "Hello HBNB!" on the root route.
    """
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
