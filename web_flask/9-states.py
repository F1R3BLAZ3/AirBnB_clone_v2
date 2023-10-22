#!/usr/bin/python3
"""
Starts a Flask web application.
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def list_states(id=None):
    """Displays a list of all State objects or
    City objects linked to a State."""
    all_states = sorted(storage.all(State).values(),
                        key=lambda state: state.name)

    if id:
        state = storage.get(State, id)
        cities = sorted(state.cities,
                        key=lambda city: city.name) if state else None
        return render_template('9-states.html',
                               selected_state=state, cities=cities)

    return render_template('9-states.html', states=all_states)


@app.teardown_appcontext
def close_session(exception):
    """Closes the current SQLAlchemy session."""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
