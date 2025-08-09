from db import get_db
from datetime import datetime

db = get_db()

# Insert a dummy doc (idempotent by link)
doc = {
    "title": "Smoke Test",
    "summary": "Testing Mongo insert.",
    "link": "https://example.com/smoke-test",
    "published": str(datetime.utcnow()),
    "source": "TEST",
    "scraped_at": datetime.utcnow(),
}

db.articles.update_one({"link": doc["link"]}, {"$set": doc}, upsert=True)

print("Count in articles:", db.articles.count_documents({}))
print("One doc:", db.articles.find_one({"link": doc["link"]}))
