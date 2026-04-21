from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from pymongo import MongoClient

auth_bp = Blueprint("auth", __name__)

bcrypt = Bcrypt()

client = MongoClient("mongodb://localhost:27017/")
db = client["medlab"]
users = db["users"]

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    hashed_pw = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

    user = {
        "name": data["name"],
        "email": data["email"],
        "password": hashed_pw,
        "role": data["role"]  # patient / doctor / nurse
    }

    users.insert_one(user)

    return jsonify({"message": "User registered successfully"})

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    user = users.find_one({"email": data["email"]})

    if user and bcrypt.check_password_hash(user["password"], data["password"]):
        token = create_access_token(identity={
            "email": user["email"],
            "role": user["role"]
        })

        return jsonify({
            "token": token,
            "role": user["role"]
        })

    return jsonify({"message": "Invalid credentials"}), 401