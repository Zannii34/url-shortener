# URL Shortener with Analytics

A Flask-based URL shortener with click analytics - built to understand how services like Bitly work under the hood.

## Live Demo
_Coming soon - deploying to Render_

## Features

- Create short links from long URLs
- Redirect short links to originals
- Track every click (timestamp, referrer, user agent)
- REST API for programmatic link creation
- Analytics endpoint (30-day clicks, top referrers)
- Live dashboard with Chart.js visualizations
- Per-link analytics modal

## Tech Stack

- **Backend:** Flask 3, SQLAlchemy
- **Database:** SQLite
- **Frontend:** Vanilla HTML/CSS/JS + Chart.js
- **Deployment:** Render

## Setup

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then visit http://127.0.0.1:5000

## What I Learned

- URL-safe code generation with Python's secrets module
- Logging real click data with SQLAlchemy relationships
- Designing a clean REST API
- Structuring a Flask app for growth
- Visualizing data with Chart.js

## License

MIT
