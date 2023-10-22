#!/usr/bin/python3
"""
This script starts a Flask web application.
"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from flask import request

app = Flask(__name)


@app.teardown_appcontext
def close_session(exception):
    """Remove the current SQLAlchemy Session."""
    storage.close()


@app.route('/states', strict_slashes=False)
def states():
    """Display a list of states."""
    all_states = sorted(list(storage.all(State).values()),
                        key=lambda x: x.name)

    return render_template('9-states.html', all_states=all_states)


@app.route('/states/<state_id>', strict_slashes=False)
def state_cities(state_id):
    """Display cities of a specific state."""
    state = storage.get(State, state_id)
    if state is not None:
        return render_template('9-states.html', state=state)
    else:
        return render_template('9-states.html', not_found=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
