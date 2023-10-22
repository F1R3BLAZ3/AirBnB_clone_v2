#!/usr/bin/python3
"""
This script starts a Flask web application.
"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Display a list of states and their cities."""
    all_states = sorted(list(storage.all(State).values()),
                        key=lambda x: x.name)

    # Load related cities for each state
    state_cities = {}
    for state in all_states:
        state_cities[state.id] = sorted(
            [city for city in state.cities],
            key=lambda city: city.name
        )

    return render_template('8-cities_by_states.html',
                           all_states=all_states, state_cities=state_cities)

@app.teardown_appcontext
def close_session(exception):
    """Remove the current SQLAlchemy Session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
