#!/usr/bin/python3
"""
Starts a Flask web application
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name)


@app.route('/states', strict_slashes=False)
@app.route('/states/<state_id>', strict_slashes=False)
def list_states_and_cities(state_id=None):
    """Display the states and cities listed in alphabetical order"""
    states = storage.all(State)
    state = None

    if state_id:
        state = states.get(state_id)

    return render_template('9-states.html', states=states.values(), state=state)


@app.teardown_appcontext
def close_session(exception):
    """Closes the current SQLAlchemy Session."""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
