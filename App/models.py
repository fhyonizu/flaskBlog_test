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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # 用户信息
    username = db.Column(db.String(50), nullable=False, unique=True)  # 用户名
    email = db.Column(db.String(100), nullable=False, unique=True)  # 邮箱
    password = db.Column(db.String(255), nullable=False)  # 密码（建议加密存储）
    avatar = db.Column(db.String(255), default='/static/avatar/default.png')  # 头像路径
    level = db.Column(db.Integer, default=1)  # 等级（默认1）

    # 时间戳
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f'<User {self.username}>'
