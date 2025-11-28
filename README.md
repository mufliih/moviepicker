# Movie Picker - AI-Powered Movie Recommendations

A Flask web application that helps you discover movies based on genre and language preferences, powered by IMDb data.

## Features

- 🎬 **Genre Selection**: Choose from 20+ movie genres
- 🌍 **Language Support**: Search movies in 20+ languages including English, Hindi, Malayalam, Tamil, Telugu, and more
- 🔄 **Try Another**: Get different recommendations without changing your preferences
- 🎨 **Modern UI**: Beautiful glassmorphism design with smooth animations
- 📱 **Responsive**: Works seamlessly on all devices

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, Vanilla JavaScript
- **Data Source**: IMDb (Web Scraping with BeautifulSoup)
- **Deployment**: Vercel

## Local Development

1. Clone the repository:
```bash
git clone <your-repo-url>
cd e-commerce
```

2. Create a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to `http://127.0.0.1:5000`

## Deployment to Vercel

This project is configured for easy deployment to Vercel:

1. Push your code to GitHub
2. Import the project in Vercel
3. Deploy!

The `vercel.json` configuration file is already set up.

## Project Structure

```
├── app.py              # Main Flask application
├── templates/          # HTML templates
│   ├── base.html      # Base template with layout
│   ├── index.html     # Home page
│   └── result.html    # Movie recommendation page
├── static/            # Static assets
│   ├── style.css     # Styles
│   └── logo.png      # Favicon
├── requirements.txt   # Python dependencies
└── vercel.json       # Vercel deployment config
```

## License

MIT
