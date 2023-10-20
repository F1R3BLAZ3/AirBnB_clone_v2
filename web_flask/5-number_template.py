#!/usr/bin/python3
"""
This is a Flask web application with routes for displaying HTML pages.
"""

from flask import Flask, render_template

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


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_variable(text="is_cool"):
    """
    Display "Python " followed by the value of the text variable.
    Replace underscore (_) symbols with a space.
    """
    return "Python " + text.replace("_", " ")


@app.route('/number/<int:n>', strict_slashes=False)
def is_number(n):
    """
    Display "n is a number" only if n is an integer.
    """
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """
    Display an HTML page with a dynamic number inside an H1 tag.
    """
    return render_template('5-number.html', n=n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
