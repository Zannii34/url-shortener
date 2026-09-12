from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Link(db.Model):
    __tablename__ = 'links'
    id = db.Column(db.Integer, primary_key=True)
    short_code = db.Column(db.String(10), unique=True, nullable=False, index=True)
    original_url = db.Column(db.String(2048), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    click_count = db.Column(db.Integer, default=0)
    clicks = db.relationship('Click', backref='link', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'short_code': self.short_code,
            'original_url': self.original_url,
            'click_count': self.click_count,
            'created_at': self.created_at.isoformat()
        }


class Click(db.Model):
    __tablename__ = 'clicks'
    id = db.Column(db.Integer, primary_key=True)
    link_id = db.Column(db.Integer, db.ForeignKey('links.id'), nullable=False)
    clicked_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    referrer = db.Column(db.String(512))
    user_agent = db.Column(db.String(512))
    country = db.Column(db.String(2))
