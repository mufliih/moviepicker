import random
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Static list of genres for IMDb
GENRES = {
    "action": "action",
    "adventure": "adventure",
    "animation": "animation",
    "biography": "biography",
    "comedy": "comedy",
    "crime": "crime",
    "drama": "drama",
    "family": "family",
    "fantasy": "fantasy",
    "film-noir": "film-noir",
    "history": "history",
    "horror": "horror",
    "music": "music",
    "musical": "musical",
    "mystery": "mystery",
    "romance": "romance",
    "sci-fi": "sci-fi",
    "sport": "sport",
    "thriller": "thriller",
    "war": "war",
    "western": "western"
}

# Map Language Name to IMDb Code
LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Malayalam": "ml",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Bengali": "bn",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Urdu": "ur",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh",
    "Russian": "ru",
    "Portuguese": "pt",
    "Arabic": "ar"
}

def get_imdb_movies(genre, language_code="en"):
    """Scrapes IMDb for top rated movies in a genre."""
    # IMDb Advanced Search URL
    url = f"https://www.imdb.com/search/title/?genres={genre}&languages={language_code}&sort=user_rating,desc&title_type=feature&num_votes=1000,"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        movies = []
        # Parse IMDb's new list structure (approximate selectors, IMDb changes often)
        # We look for the main list items
        items = soup.select('.ipc-metadata-list-summary-item')
        
        for item in items[:20]: # Look at top 20
            try:
                title_tag = item.select_one('.ipc-title__text')
                if not title_tag: continue
                
                title = title_tag.get_text().split('. ', 1)[-1] # Remove ranking number "1. "
                
                # Rating
                rating_tag = item.select_one('.ipc-rating-star--base')
                rating = rating_tag.get_text().split()[0] if rating_tag else "N/A"
                
                # Year
                metadata = item.select('.sc-b189961a-8.kLaxqf.dli-title-metadata-item')
                year = metadata[0].get_text() if metadata else "Unknown"
                
                # Image
                img_tag = item.select_one('img.ipc-image')
                poster = img_tag['src'] if img_tag else ""
                
                # Overview (Description) - often hidden or requires deeper parsing, so we use a generic one or try to find it
                desc_tag = item.select_one('.ipc-html-content-inner-div')
                overview = desc_tag.get_text() if desc_tag else "No overview available."

                movies.append({
                    "title": title,
                    "release_date": year,
                    "vote_average": rating,
                    "overview": overview,
                    "poster_path": poster # Full URL from IMDb
                })
            except Exception:
                continue
                
        return movies
    except Exception as e:
        print(f"Scraping error: {e}")
        return []

@app.route('/')
def index():
    # Pass list of language names for the datalist
    return render_template('index.html', genres=GENRES, languages=sorted(LANGUAGES.keys()))

@app.route('/recommend', methods=['POST'])
def recommend():
    genre = request.form.get('genre')
    language_name = request.form.get('language', 'English')
    
    # Lookup code, default to English if not found
    language_code = LANGUAGES.get(language_name, 'en')
    
    if not genre:
        return redirect(url_for('index'))
    
    # Try scraping
    movies = get_imdb_movies(genre, language_code)
    
    if not movies:
        return render_template('index.html', error=f"Unable to fetch {language_name} movies from IMDb. Please try again later.", genres=GENRES, languages=sorted(LANGUAGES.keys()))

    movie = random.choice(movies)

    # Adjust poster path logic for template (IMDb returns full URL, TMDB returned partial)
    # We need to hack the template slightly or normalize here.
    # Let's normalize here: if it starts with http, use it as is.
    
    return render_template('result.html', movie=movie, genre=genre, language=language_name)

if __name__ == "__main__":
    app.run(debug=True)
