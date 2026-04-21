# config/db.py
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["ai_medlab"]

predictions_collection = db["predictions"]
users_collection = db["users"]