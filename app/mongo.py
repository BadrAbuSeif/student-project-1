from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URL", "mongodb://mongo:27017"))
db = client["app_logs"]
logs_collection = db["logs"]