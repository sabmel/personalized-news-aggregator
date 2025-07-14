from db import get_db
from datetime import datetime

def save_article_to_db(article):
    db = get_db()
    articles_collection = db.articles

    article_document = {
        "title": article["title"],
        "summary": article.get("summary", ""),
        "link": article["link"],
        "published": article.get("published", ""),
        "source": article["source"],
        "scraped_at": datetime.utcnow()
    }

    # Avoid duplicates based on unique URL
    articles_collection.update_one(
        {"link": article["link"]},
        {"$setOnInsert": article_document},
        upsert=True
    )
