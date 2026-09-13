# URL Shortener with Analytics

![Python](https://img.shields.io/badge/python-3.11-blue) ![Flask](https://img.shields.io/badge/flask-3.0-black) ![SQLAlchemy](https://img.shields.io/badge/sqlalchemy-ORM-red)


A Flask-based URL shortener with click analytics - built to understand how services like Bitly work under the hood.

## Screenshots

![Homepage](docs/screenshot-home.png)

![Feature](docs/screenshot-feature.png)

## Live Demo
[**Live Demo -> https://url-shortener-jh9y.onrender.com/**](https://url-shortener-jh9y.onrender.com/)

## Features

- Create short links from long URLs

## Screenshots

![Homepage](docs/screenshot-home.png)

![Feature](docs/screenshot-feature.png)
- Redirect short links to originals
- Track every click (timestamp, referrer, user agent)
- REST API for programmatic link creation
- Analytics endpoint (30-day clicks, top referrers)
- Live dashboard with Chart.js visualizations
- Per-link analytics modal

## Tech Stack

- **Backend:** Flask 3, SQLAlchemy

## Screenshots

![Homepage](docs/screenshot-home.png)

![Feature](docs/screenshot-feature.png)
- **Database:** SQLite
- **Frontend:** Vanilla HTML/CSS/JS + Chart.js
- **Deployment:** Render

## Setup

```bash

## Screenshots

![Homepage](docs/screenshot-home.png)

![Feature](docs/screenshot-feature.png)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then visit http://127.0.0.1:5000

## What I Learned

- URL-safe code generation with Python's secrets module

## Screenshots

![Homepage](docs/screenshot-home.png)

![Feature](docs/screenshot-feature.png)
- Logging real click data with SQLAlchemy relationships
- Designing a clean REST API
- Structuring a Flask app for growth
- Visualizing data with Chart.js

## License

MIT

## Screenshots

![Homepage](docs/screenshot-home.png)

![Feature](docs/screenshot-feature.png)
