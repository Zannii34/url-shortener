from app import create_app, db
from models import Link, Click
from datetime import datetime, timedelta
import secrets, string, random


def seed():
    app = create_app()
    with app.app_context():
        if Link.query.count() > 0:
            print('Database already has links')
            return

        samples = [
            'https://github.com/Zannii34/pyserve',
            'https://zannii34.github.io',
            'https://pyserve.fly.dev',
            'https://receipt-scanner-wtai.onrender.com/',
            'https://www.python.org',
        ]

        alphabet = string.ascii_letters + string.digits

        for url in samples:
            code = ''.join(secrets.choice(alphabet) for _ in range(6))
            while Link.query.filter_by(short_code=code).first():
                code = ''.join(secrets.choice(alphabet) for _ in range(6))

            link = Link(short_code=code, original_url=url, click_count=0)
            db.session.add(link)
            db.session.flush()

            for _ in range(random.randint(2, 15)):
                click = Click(
                    link_id=link.id,
                    referrer=random.choice(['Direct', 'twitter.com', 'linkedin.com', 'google.com']),
                    user_agent='Mozilla/5.0 (sample)',
                    clicked_at=datetime.utcnow() - timedelta(days=random.randint(0, 14)),
                )
                link.click_count += 1
                db.session.add(click)

        db.session.commit()
        print(f'Seeded {len(samples)} links')


if __name__ == '__main__':
    seed()