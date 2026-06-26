from flask import (
    Blueprint,
    request,
    jsonify
)

from database.db import db
from database.models import User

auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route(
    "/register",
    methods=["POST"]
)
def register():

    data = request.json

    username = data["username"]
    password = data["password"]

    existing_user = (
        User.query
        .filter_by(
            username=username
        )
        .first()
    )

    if existing_user:

        return jsonify(
            {
                "message":
                "Username already exists"
            }
        ), 400

    user = User(
        username=username,
        password_hash=password
    )

    db.session.add(user)
    db.session.commit()

    return jsonify(
        {
            "message":
            "Registration successful"
        }
    )


@auth_bp.route(
    "/login",
    methods=["POST"]
)
def login():

    data = request.json

    username = data["username"]
    password = data["password"]

    user = (
        User.query
        .filter_by(
            username=username
        )
        .first()
    )

    if not user:

        return jsonify(
            {
                "message":
                "User not found"
            }
        ), 404

    if user.password_hash != password:

        return jsonify(
            {
                "message":
                "Wrong password"
            }
        ), 401

    return jsonify(
        {
            "message":
            "Login success"
        }
    )