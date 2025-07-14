import requests
from bs4 import BeautifulSoup
from newspaper import Article
from utils import save_article_to_db

HTML_SOURCES = {
    'CNN': 'https://edition.cnn.com',
    'BBC': 'https://www.bbc.com/news',
}

SELECTORS = {
    'CNN': '.cd__headline a',
    'BBC': '.gs-c-promo-heading',
}

def scrape_html():
    articles = []
    for source, url in HTML_SOURCES.items():
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        headlines = soup.select(SELECTORS[source])

        for tag in headlines[:10]:  # limit to first 10 articles per source
            link = tag['href']
            if link.startswith('/'):
                link = url + link

            # Use Newspaper3k to extract article details
            article_data = Article(link)
            try:
                article_data.download()
                article_data.parse()

                article = {
                    'title': article_data.title,
                    'summary': article_data.summary or article_data.text[:200],
                    'link': link,
                    'published': article_data.publish_date or '',
                    'source': source
                }
                articles.append(article)
                save_article_to_db(article)
            except Exception as e:
                print(f"Error scraping {link}: {e}")

    print(f"Scraped {len(articles)} articles via HTML scraping.")

if __name__ == "__main__":
    scrape_html()
