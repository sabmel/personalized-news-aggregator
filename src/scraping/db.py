import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB_NAME")

def get_db():
    client = MongoClient(MONGODB_URI)
    db = client[DB_NAME]
    return db
