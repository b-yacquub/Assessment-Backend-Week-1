"""This file defines the API routes."""

# pylint: disable = no-name-in-module

from datetime import datetime, date

from flask import Flask, Response, request, jsonify

from date_functions import (convert_to_datetime, get_day_of_week_on,
                            get_days_between, get_current_age)

app_history = []

app = Flask(__name__)


def add_to_history(current_request):
    """Adds a route to the app history."""
    app_history.append({
        "method": current_request.method,
        "at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "route": current_request.endpoint
    })


def clear_history():
    """Clears the app history."""
    app_history.clear()


@app.get("/")
def index():
    """Returns an API welcome messsage."""
    return jsonify({"message": "Welcome to the Days API."})


@app.route("/between", methods=["POST"])
def between():
    if request.method == "POST":
        data = request.json
        if len(data) != 2:
            return {"error": "Missing required data."}, 400
        required = ['first', 'last']
        for key in data.keys():
            if key not in required:
                return {"error": "Missing required data."}, 400
        try:
            first = datetime.strptime(data[0], '%d.%m.%Y')
        except ValueError:
            return {
                "error": "Unable to convert value to datetime."
            }

        return get_days_between(first, second), 200


if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.run(port=8080, debug=True)
