#!/usr/bin/python3
"""
Starts a Flask web application.
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def close_session(exception):
    """Closes the current SQLAlchemy session."""
    storage.close()


@app.route('/states', strict_slashes=False)
def list_states():
    """Displays a list of all State objects present in DBStorage."""
    states = storage.all(State).values()
    return render_template('9-states.html', states=sorted(states, key=lambda x: x.name))


@app.route('/states/<id>', strict_slashes=False)
def list_cities_by_state(id):
    """Displays a list of City objects linked to the State with the given ID."""
    state = storage.get(State, id)
    if state:
        cities = sorted(state.cities, key=lambda x: x.name)
        return render_template('9-states.html', selected_state=state, cities=cities)
    return render_template('9-states.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
