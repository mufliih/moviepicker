import requests
from bs4 import BeautifulSoup

def get_imdb_movies(genre):
    """Scrapes IMDb for top rated movies in a genre."""
    # IMDb Advanced Search URL
    url = f"https://www.imdb.com/search/title/?genres={genre}&sort=user_rating,desc&title_type=feature&num_votes=25000,"
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
        
        movies = []
        # Parse IMDb's new list structure (approximate selectors, IMDb changes often)
        # We look for the main list items
        items = soup.select('.ipc-metadata-list-summary-item')
        print(f"Found {len(items)} items.")
        
        for item in items[:5]: # Look at top 5 for test
            try:
                title_tag = item.select_one('.ipc-title__text')
                if not title_tag: continue
                
                title = title_tag.get_text().split('. ', 1)[-1] # Remove ranking number "1. "
                print(f"Found title: {title}")
                
                movies.append(title)
            except Exception as e:
                print(f"Error parsing item: {e}")
                continue
                
        return movies
    except Exception as e:
        print(f"Scraping error: {e}")
        return []

if __name__ == "__main__":
    movies = get_imdb_movies("action")
    print(f"Result: {movies}")
