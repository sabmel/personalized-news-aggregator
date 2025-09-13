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

def filter_articles(user_prefs, articles):
    """
    user_prefs: dict {topics: [], keywords: [], sources: []}
    articles: list of dicts [{title, summary, source, ...}]
    """
    filtered = []
    for article in articles:
        title = article.get("title", "").lower()
        source = article.get("source", "")
        
        if any(topic.lower() in title for topic in user_prefs.get("topics", [])):
            filtered.append(article)
        elif any(kw.lower() in title for kw in user_prefs.get("keywords", [])):
            filtered.append(article)
        elif source in user_prefs.get("sources", []):
            filtered.append(article)
    return filtered
