#!/usr/bin/python3
"""Start a Flask web application to display states and cities"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__)


@app.teardown_appcontext
def close_session(exception):
    """Closes the SQLAlchemy session"""
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Display a list of states and their cities"""
    states = list(storage.all(State).values())
    states.sort(key=lambda state: state.name)

    return render_template('8-cities_by_states.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
