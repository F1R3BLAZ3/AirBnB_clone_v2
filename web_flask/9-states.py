#!/usr/bin/python3
"""
Start a Flask web application.
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """
    Remove the current SQLAlchemy Session.
    """
    storage.close()


@app.route('/states', strict_slashes=False)
def display_states():
    """
    Display a HTML page with a list of all State objects.
    """
    states = storage.all(State).values()
    states = sorted(states, key=lambda state: state.name)
    return render_template('9-states.html', states=states)


@app.route('/states/<state_id>', strict_slashes=False)
def display_state_cities(state_id):
    """
    Display a HTML page with a list of cities of a specific State.
    """
    state = storage.get(State, state_id)
    if state is None:
        return render_template('9-not_found.html')
    return render_template('9-states.html', state=state)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
