import requests
from bs4 import BeautifulSoup

def test_language_scraping(genre, language):
    """Scrapes IMDb for top rated movies in a genre and original language."""
    # Try 'original_language' parameter
    url = f"https://www.imdb.com/search/title/?genres={genre}&original_language={language}&sort=user_rating,desc&title_type=feature&num_votes=10000,"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:
        print(f"Requesting {url}...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        print("Response received.")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        items = soup.select('.ipc-metadata-list-summary-item')
        print(f"Found {len(items)} items.")
        
        for item in items[:3]:
            title_tag = item.select_one('.ipc-title__text')
            if title_tag:
                print(f"Found title: {title_tag.get_text()}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Testing Hindi (hi)...")
    test_language_scraping("action", "hi")
    print("\nTesting Spanish (es)...")
    test_language_scraping("action", "es")
