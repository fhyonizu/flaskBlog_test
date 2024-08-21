import datetime
from .exts import db

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    comments = db.relationship('Comment', backref='article', lazy=True)

    def __repr__(self):
        return f"Article(title='{self.title}', timestamp='{self.timestamp}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Comment(text='{self.text}')"
