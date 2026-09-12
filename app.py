from flask import Flask, render_template, request, redirect, jsonify, abort
from models import db, Link, Click
from utils.shortener import generate_short_code
from datetime import datetime, timedelta
from collections import Counter
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///shortener.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.before_request
def ensure_tables():
    if not hasattr(app, '_tables_created'):
        with app.app_context():
            db.create_all()
        app._tables_created = True


# ============================================
# Public routes
# ============================================

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = (request.form.get('url') or '').strip()
        if not url:
            return render_template('index.html', error='URL is required.'), 400
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        if len(url) > 2048:
            return render_template('index.html', error='URL is too long.'), 400

        code = generate_short_code()
        while Link.query.filter_by(short_code=code).first():
            code = generate_short_code()

        link = Link(short_code=code, original_url=url)
        db.session.add(link)
        db.session.commit()

        short_url = f"{request.host_url}{code}"
        return render_template('index.html', short_url=short_url, original=url)

    return render_template('index.html')


@app.route('/<code>')
def redirect_short(code):
    link = Link.query.filter_by(short_code=code).first()
    if not link:
        return render_template('404.html'), 404

    click = Click(
        link_id=link.id,
        referrer=(request.referrer or 'Direct')[:500],
        user_agent=(request.headers.get('User-Agent') or '')[:500],
        clicked_at=datetime.utcnow()
    )
    link.click_count = (link.click_count or 0) + 1
    db.session.add(click)
    db.session.commit()

    return redirect(link.original_url)


@app.route('/dashboard')
def dashboard():
    links = Link.query.order_by(Link.created_at.desc()).all()
    total_links = len(links)
    total_clicks = sum(l.click_count or 0 for l in links)
    today = datetime.utcnow().date()
    clicks_today = Click.query.filter(Click.clicked_at >= datetime.combine(today, datetime.min.time())).count()

    return render_template(
        'dashboard.html',
        links=links,
        total_links=total_links,
        total_clicks=total_clicks,
        clicks_today=clicks_today
    )


# ============================================
# API routes
# ============================================

@app.route('/api/links', methods=['POST'])
def api_create_link():
    data = request.get_json(silent=True) or {}
    url = (data.get('url') or '').strip()
    if not url:
        return jsonify({'error': 'url is required'}), 400
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    code = generate_short_code()
    while Link.query.filter_by(short_code=code).first():
        code = generate_short_code()

    link = Link(short_code=code, original_url=url)
    db.session.add(link)
    db.session.commit()

    return jsonify({
        'short_code': code,
        'short_url': f"{request.host_url}{code}",
        'original_url': url
    }), 201


@app.route('/api/links', methods=['GET'])
def api_list_links():
    links = Link.query.order_by(Link.created_at.desc()).all()
    return jsonify([l.to_dict() for l in links])


@app.route('/api/links/<code>/analytics', methods=['GET'])
def api_link_analytics(code):
    link = Link.query.filter_by(short_code=code).first()
    if not link:
        return jsonify({'error': 'link not found'}), 404

    # Clicks over last 30 days
    since = datetime.utcnow() - timedelta(days=30)
    clicks = Click.query.filter(Click.link_id == link.id, Click.clicked_at >= since).all()

    # Group by day
    by_day = Counter(c.clicked_at.strftime('%Y-%m-%d') for c in clicks)
    days = []
    for i in range(29, -1, -1):
        d = (datetime.utcnow() - timedelta(days=i)).strftime('%Y-%m-%d')
        days.append({'date': d, 'count': by_day.get(d, 0)})

    # Top referrers
    referrers = Counter(c.referrer or 'Direct' for c in clicks)
    top_referrers = [{'name': r, 'count': n} for r, n in referrers.most_common(5)]

    return jsonify({
        'short_code': code,
        'total_clicks': link.click_count,
        'by_day': days,
        'top_referrers': top_referrers
    })


@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
