#!/usr/bin/python3
"""
Starts a Flask web application
"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def list_states():
    """Display a list of all State objects sorted by name (A->Z)"""
    states = sorted(storage.all(State).values(), key=lambda x: x.name)
    return render_template('9-states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def list_cities_by_state(id):
    """Display a list of City objects linked to the State with the given ID."""
    state = storage.get(State, id)
    if state:
        cities = sorted(state.cities, key=lambda x: x.name)
        return render_template('9-states.html',
                               selected_state=state, cities=cities)
    return render_template('9-states.html')


@app.teardown_appcontext
def close_session(exception):
    """Remove the current SQLAlchemy Session."""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
