import feedparser
from utils import save_article_to_db

RSS_FEEDS = {
    'BBC': 'http://feeds.bbci.co.uk/news/rss.xml',
    'CNN': 'https://rss.cnn.com/rss/edition.rss',
    'Reuters': 'https://www.reutersagency.com/feed/?best-topics=business-finance',
    'HackerNews': 'https://news.ycombinator.com/rss',
    'TechCrunch': 'https://techcrunch.com/feed/',
    'Bloomberg': 'https://www.bloomberg.com/feed/podcast/surveillance.xml',
    'ESPN': 'https://www.espn.com/espn/rss/news',
    'BuzzFeed': 'https://www.buzzfeed.com/world.xml'
}

def scrape_rss():
    articles = []
    for source, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries:
            article = {
                'title': entry.title,
                'summary': entry.get('summary', ''),
                'link': entry.link,
                'published': entry.get('published', ''),
                'source': source
            }
            articles.append(article)
            save_article_to_db(article)
    print(f"Scraped {len(articles)} articles from RSS feeds.")

if __name__ == "__main__":
    scrape_rss()
