import requests
import random
import time
import webbrowser
import sys

class MoviePicker:
    def __init__(self):
        # ------------------------------------------------------------------
        # TODO: PASTE YOUR TMDB API KEY BELOW
        # You can get one for free at: https://www.themoviedb.org/settings/api
        # ------------------------------------------------------------------
        self.api_key = "YOUR_TMDB_API_KEY_HERE" 
        self.base_url = "https://api.themoviedb.org/3"
        
        if self.api_key == "YOUR_TMDB_API_KEY_HERE":
            print("⚠️  ERROR: You need to set your API Key in the script first!")
            print("   Please open the file and replace 'YOUR_TMDB_API_KEY_HERE' with your actual key.")
            sys.exit(1)

        self.genres = {}

    def fetch_genres(self):
        """Fetches the official list of movie genres from TMDB."""
        url = f"{self.base_url}/genre/movie/list"
        params = {"api_key": self.api_key, "language": "en-US"}
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            # Create a dictionary mapping lowercase names to IDs
            for genre in data['genres']:
                self.genres[genre['name'].lower()] = genre['id']
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching genres: {e}")
            sys.exit(1)

    def get_movie_recommendation(self, genre_name):
        """Fetches top rated movies for a specific genre and picks one."""
        genre_id = self.genres.get(genre_name.lower())
        
        if not genre_id:
            print(f"❌ Sorry, I don't recognize the genre '{genre_name}'.")
            print(f"   Available genres: {', '.join(title().capitalize() for title in list(self.genres.keys())[:5])}...")
            return None

        print(f"\n🍿  Searching for highly-rated {genre_name.capitalize()} movies...")
        time.sleep(1) # Simulating "thinking"

        # Discover movies endpoint
        url = f"{self.base_url}/discover/movie"
        params = {
            "api_key": self.api_key,
            "with_genres": genre_id,
            "sort_by": "vote_average.desc", # Get top rated
            "vote_count.gte": 500,          # Ensure it has enough votes to be credible
            "language": "en-US",
            "page": random.randint(1, 3)    # Randomize the page to get variety
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            results = response.json().get('results', [])
            
            if not results:
                print("No movies found.")
                return None
                
            return random.choice(results)

        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching movies: {e}")
            return None

    def display_movie(self, movie):
        """Nicely formats and prints movie details."""
        title = movie['title']
        date = movie.get('release_date', 'Unknown')[:4]
        rating = movie['vote_average']
        overview = movie['overview']
        
        print("\n" + "="*50)
        print(f"🎬  TOP PICK: {title.upper()} ({date})")
        print("="*50)
        print(f"⭐  Rating: {rating}/10")
        print(f"📝  Overview: {overview}")
        print("-" * 50)
        
        # Integration links
        print("\n🔗  Where to find reviews:")
        print(f"   1. Rotten Tomatoes: https://www.rottentomatoes.com/search?search={requests.utils.quote(title)}")
        print(f"   2. IMDb Search:     https://www.imdb.com/find?q={requests.utils.quote(title)}")
        print("="*50)
        
        choice = input("\nOpen reviews in browser? (y/n): ").lower()
        if choice == 'y':
            webbrowser.open(f"https://www.rottentomatoes.com/search?search={requests.utils.quote(title)}")
            print("Opening Rotten Tomatoes...")

    def run(self):
        print("\n--- 🎥 PYTHON MOVIE PICKER (API EDITION) ---")
        self.fetch_genres()
        
        while True:
            print("\nAvailable Genres: Action, Comedy, Drama, Horror, Sci-Fi, Romance...")
            user_genre = input("What genre are you in the mood for? (or 'q' to quit): ").strip()
            
            if user_genre.lower() == 'q':
                print("Goodbye! 🍿")
                break
            
            movie = self.get_movie_recommendation(user_genre)
            
            if movie:
                self.display_movie(movie)

if __name__ == "__main__":
    # Ensure requests is installed
    try:
        import requests
    except ImportError:
        print("This script requires the 'requests' library.")
        print("Please run: pip install requests")
        sys.exit(1)

    app = MoviePicker()
    app.run()