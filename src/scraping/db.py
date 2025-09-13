import os
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGODB_DB_NAME", "news_aggregator")

def get_db():
    client = MongoClient(MONGODB_URI)
    return client[DB_NAME]

def create_user(username, preferences=None):
    db = get_db()
    users = db.users
    if preferences is None:
        preferences = {"topics": [], "keywords": [], "sources": []}
    users.update_one(
        {"username": username},
        {"$setOnInsert": {"username": username, "preferences": preferences}},
        upsert=True
    )