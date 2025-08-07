import datetime
from .exts import db
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 新增：关联用户
    author = db.relationship('User', backref='articles')       # 新增：建立关系

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
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(255), default='/static/avatar/default.png')
    last_checkin_date = db.Column(db.Date)  # 上次签到日期

    # 等级系统
    level = db.Column(db.Integer, default=1)  # 等级
    exp = db.Column(db.Integer, default=0)    # 当前经验

    # 时间戳
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f'<User {self.username}>'

    def add_exp(self, amount):
        """增加经验值并自动判断升级"""
        if self.level >= 5:
            return
        self.exp += amount
        while self.exp >= self.exp_needed() and self.level < 5:
            self.exp -= self.exp_needed()
            self.level += 1

    def exp_needed(self):
        """计算当前等级升级所需经验"""
        return 100 + (self.level - 1) * 50
