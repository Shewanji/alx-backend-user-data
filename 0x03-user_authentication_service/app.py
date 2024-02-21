#!/usr/bin/env python3
"""module for a basic Flask app"""

from flask import Flask, jsonify, request, abort, redirect
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


@app.route("/sessions", methods=["POST"])
def login():
    """Login endpoint"""

    # Retrieve email and password from form data
    email = request.form.get("email")
    password = request.form.get("password")

    # Check if login information is correct
    if not AUTH.valid_login(email, password):
        # If login information is incorrect, abort with 401 Unauthorized status
        abort(401)

    # If login information is correct, create a new session for the user
    session_id = AUTH.create_session(email)

    # Set session ID as a cookie in the response
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)

    return response


@app.route("/sessions", methods=["DELETE"])
def logout():
    """Logout endpoint"""

    # Retrieve session ID from the cookie
    session_id = request.cookies.get("session_id")

    # Find user with the requested session ID
    user = AUTH.get_user_from_session_id(session_id)

    # If user exists, destroy the session and redirect to GET /
    if user:
        AUTH.destroy_session(user.id)
        return redirect("/")
    else:
        # If user does not exist, respond with a 403 Forbidden status
        return jsonify({"message": "Forbidden"}), 403


@app.route("/profile", methods=["GET"])
def profile():
    """Profile endpoint"""

    # Retrieve session ID from the cookie
    session_id = request.cookies.get("session_id")

    # Find user with the requested session ID
    user = AUTH.get_user_from_session_id(session_id)

    # If user exists, respond with user's email and 200 status
    if user:
        return jsonify({"email": user.email}), 200
    else:
        return jsonify({"message": "Forbidden"}), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
