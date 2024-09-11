#!/usr/bin/env python3
"""
Flask app to register users
"""

from flask import Flask, request, jsonify
from auth import Auth

app = Flask(__name__)

# Instantiate the Auth object
AUTH = Auth()

@app.route("/users", methods=["POST"])
def register_user():
    """Handles user registration"""
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        
        # Check if email and password are provided
        if not email or not password:
            return jsonify({"message": "email and password required"}), 400

        # Attempt to register the user
        user = AUTH.register_user(email, password)
        
        # Return success response
        return jsonify({"email": user.email, "message": "user created"})

    except ValueError as e:
        # If user already exists, handle the exception and return error response
        return jsonify({"message": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
