from flask import Flask, session
from .models import db, Article, Comment, User
from .views import *
from .exts import init_exts

def create_app():
    app = Flask(__name__)

    # -------------------- 注册配置 --------------------
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'awdfgc2323231ef'

    # -------------------- 初始化扩展 --------------------
    init_exts(app)

    # -------------------- 注册蓝图 --------------------
    app.register_blueprint(blue)

    # ✅ 如果你还有 auth 蓝图（用户系统）别忘了注册
    from .user import auth
    app.register_blueprint(auth)

    # -------------------- 全局上下文：注入 user 变量 --------------------

    @app.context_processor
    def inject_user():
        user_id = session.get('user_id')
        user = User.query.get(user_id) if user_id else None
        return dict(user=user)

    # -------------------- 首次启动自动建表 + 添加测试数据 --------------------
    with app.app_context():
        db.create_all()
        if not Article.query.first():
            default_article = Article(title='欢迎来到博客', content='这是第一篇博客文章！')
            db.session.add(default_article)
            db.session.commit()

            comment_1 = Comment(article_id=default_article.id, text='这篇文章非常有用！')
            comment_2 = Comment(article_id=default_article.id, text='感谢分享！')
            db.session.add_all([comment_1, comment_2])
            db.session.commit()

    return app
