# src/backend/app.py
import os
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient, DESCENDING
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGODB_DB_NAME", "news_aggregator")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)
CORS(app)

def ensure_user(username: str):
    db.users.update_one(
        {"username": username},
        {"$setOnInsert": {"username": username,
                          "preferences": {"topics": [], "keywords": [], "sources": []}}},
        upsert=True
    )

def filter_articles(user_prefs: dict, articles: list) -> list:
    topics = [t.lower() for t in user_prefs.get("topics", [])]
    keywords = [k.lower() for k in user_prefs.get("keywords", [])]
    sources = set(user_prefs.get("sources", []))
    filtered = []
    for a in articles:
        title = (a.get("title") or "").lower()
        source = a.get("source", "")
        if any(t in title for t in topics):
            filtered.append(a)
        elif any(k in title for k in keywords):
            filtered.append(a)
        elif source in sources:
            filtered.append(a)
    return filtered

@app.route("/")
def root():
    return jsonify({"ok": True, "message": "Backend up. Try /health or /api/articles/sabrina"}), 200

@app.route("/health")
def health():
    return jsonify({"ok": True, "time": datetime.utcnow().isoformat()}), 200

@app.route("/routes")
def routes():
    return jsonify(sorted([str(r) for r in app.url_map.iter_rules()])), 200

@app.route("/api/users/<username>", methods=["GET"])
def get_user(username):
    ensure_user(username)
    user = db.users.find_one({"username": username}, {"_id": 0})
    return jsonify(user), 200

@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json(force=True) or {}
    username = data.get("username")
    preferences = data.get("preferences", {"topics": [], "keywords": [], "sources": []})
    if not username:
        return jsonify({"error": "username is required"}), 400
    ensure_user(username)
    db.users.update_one({"username": username}, {"$set": {"preferences": preferences}})
    user = db.users.find_one({"username": username}, {"_id": 0})
    return jsonify(user), 201

@app.route("/api/users/<username>/preferences", methods=["PUT"])
def update_prefs(username):
    ensure_user(username)
    data = request.get_json(force=True) or {}
    prefs = data.get("preferences")
    if not isinstance(prefs, dict):
        return jsonify({"error": "preferences must be an object"}), 400
    prefs.setdefault("topics", [])
    prefs.setdefault("keywords", [])
    prefs.setdefault("sources", [])
    db.users.update_one({"username": username}, {"$set": {"preferences": prefs}})
    user = db.users.find_one({"username": username}, {"_id": 0})
    return jsonify(user), 200

@app.route("/api/articles/<username>", methods=["GET"])
def get_articles(username):
    ensure_user(username)
    user = db.users.find_one({"username": username}, {"_id": 0})
    prefs = user.get("preferences", {"topics": [], "keywords": [], "sources": []})
    limit = int(request.args.get("limit", 100))

    cursor = db.articles.find({}).sort("scraped_at", DESCENDING).limit(limit)
    articles = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        articles.append(doc)

    personalized = filter_articles(prefs, articles)
    result = personalized if personalized else articles
    return jsonify(result), 200

if __name__ == "__main__":
    # IMPORTANT: This prints the exact URL. Use it.
    app.run(host="127.0.0.1", port=5000, debug=True)
