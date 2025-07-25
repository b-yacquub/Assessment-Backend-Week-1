"""This file defines the API routes."""

# pylint: disable = no-name-in-module

from datetime import datetime, date

from flask import Flask, Response, request, jsonify

from date_functions import (convert_to_datetime, get_day_of_week_on,
                            get_days_between, get_current_age)

app_history = [{}, {}, {}]

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
        add_to_history(request)
        data = request.json
        if len(data) != 2:
            return {"error": "Missing required data."}, 400
        required = ['first', 'last']
        for key in data.keys():
            if key not in required:
                return {"error": "Missing required data."}, 400
        try:
            first_date = convert_to_datetime(data['first'])
            last_date = convert_to_datetime(data['last'])
        except ValueError:
            return {
                "error": "Unable to convert value to datetime."
            }, 400
        days = get_days_between(first_date, last_date)
        return {'days': days}, 200


@app.route("/weekday", methods=["POST"])
def weekday():
    if request.method == "POST":
        add_to_history(request)
        data = request.json
        if 'date' not in data.keys():
            return {"error": "Missing required data."}, 400

        try:
            date_week = convert_to_datetime(data['date'])
        except ValueError:
            return {
                "error": "Unable to convert value to datetime."
            }, 400
        day = get_day_of_week_on(date_week)
        add_to_history(request)
        return {'weekday': day}, 200


@app.route("/history", methods=["GET"])
def history():
    if request.method == "GET":
        args = request.args.to_dict()
        number = (args.get("number"))
        if number != None:
            nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                    '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
            if number not in nums:
                return {
                    "error": "Number must be an integer between 1 and 20."
                }, 400
            if int(number) > 0 and int(number) < 21:
                return app_history[:int(number)], 200

        return app_history[:5], 200


@app.route("/current_age", methods=["GET"])
def age():
    if request.method == "GET":
        args = request.args.to_dict()
        date_input = (args.get("date"))
        if date_input == None:
            return {
                "error": "Date parameter is required."
            }, 400
        try:
            valid_date = datetime.strptime(date_input, '%Y-%m-%d')
        except ValueError:
            return {
                "error": "Value for data parameter is invalid."
            }, 400
        valid_age = get_current_age(valid_date)
        return {"current_age": valid_age}, 200


if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.run(port=8080, debug=True)
