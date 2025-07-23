from flask import Flask  # 导入 Flask 类
from .models import db, Article, Comment  # 导入模型
from .views import *
from .exts import init_exts

def create_app():
    app = Flask(__name__)  # 初始化 Flask 应用
    app.register_blueprint(blue)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'awdfgc2323231ef'

    init_exts(app)

    with app.app_context():
        db.create_all()  # 创建数据库表格

        # 插入默认数据
        if not Article.query.first():  # 如果没有文章，则插入默认文章
            default_article = Article(title='欢迎来到博客', content='这是第一篇博客文章！')
            db.session.add(default_article)
            db.session.commit()

            # 插入与默认文章相关的评论
            comment_1 = Comment(article_id=default_article.id, text='这篇文章非常有用！')
            comment_2 = Comment(article_id=default_article.id, text='感谢分享！')
            db.session.add(comment_1)
            db.session.add(comment_2)
            db.session.commit()

    return app
