#!/usr/bin/env python3
"""module for a basic Flask app"""

from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()
app.url_map.strict_slashes = False


@app.route("/")
def welcome():
    """Return a welcome message"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """Endpoint to register a new user"""
    try:
        email = request.form.get("email")
        password = request.form.get("password")

        # Register the user using the Auth object
        AUTH.register_user(email, password)

        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        # Catch ValueError if email is already registered
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
