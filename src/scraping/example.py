from db import get_db, create_user
from utils import filter_articles

# Step 1: create a user with preferences
create_user("sabrina", {
    "topics": ["technology", "finance"],
    "keywords": ["AI", "quant"],
    "sources": ["BBC", "TechCrunch"]
})

# Step 2: fetch user preferences
db = get_db()
user = db.users.find_one({"username": "sabrina"})
prefs = user["preferences"]

# Step 3: get recent articles
articles = list(db.articles.find().limit(50))

# Step 4: filter them
personalized = filter_articles(prefs, articles)

print("Personalized Feed:")
for a in personalized[:5]:
    print(a["source"], "-", a["title"])
