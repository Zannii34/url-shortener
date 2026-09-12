"""Seed the URL shortener with sample data for first-time visitors."""
from app import create_app, db, Link, Click  # type: ignore
from datetime import datetime, timedelta
import random


def seed():
    app = create_app()
    with app.app_context():
        # Only seed if empty
        if Link.query.count() > 0:
            print("[SKIP] Database already has links")
            return

        samples = [
            ("https://github.com/Zannii34/pyserve", "PyServe GitHub repo"),
            ("https://zannii34.github.io", "Portfolio homepage"),
            ("https://pyserve.fly.dev", "PyServe live demo"),
            ("https://receipt-scanner-wtai.onrender.com/", "Receipt Scanner demo"),
            ("https://www.python.org", "Python.org"),
        ]

        for url, _ in samples:
            import secrets, string
            alphabet = string.ascii_letters + string.digits
            code = "".join(secrets.choice(alphabet) for _ in range(6))
            while Link.query.filter_by(short_code=code).first():
                code = "".join(secrets.choice(alphabet) for _ in range(6))

            link = Link(short_code=code, original_url=url, click_count=0)
            db.session.add(link)
            db.session.flush()

            # Add some clicks
            for _ in range(random.randint(2, 15)):
                click = Click(
                    link_id=link.id,
                    referrer=random.choice(["Direct", "twitter.com", "linkedin.com", "google.com"]),
                    user_agent="Mozilla/5.0 (sample data)",
                    clicked_at=datetime.utcnow() - timedelta(days=random.randint(0, 14)),
                )
                link.click_count += 1
                db.session.add(click)

        db.session.commit()
        print(f"[OK] Seeded {len(samples)} links with sample clicks")


if __name__ == "__main__":
    seed()