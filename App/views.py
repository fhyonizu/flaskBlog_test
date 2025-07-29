import json

from flask import Blueprint, render_template, request, redirect, url_for, flash

from .exts import *
from .models import *

blue = Blueprint('article', __name__)


@blue.route('/')
def index():
    articles = get_artics()
    return render_template('index.html', articles=articles)


@blue.route('/artics/')
@cache.cached(timeout=20)
def get_artics():
    articles = Article.query.all()
    return articles


@blue.route('/words/<int:article_id>')
def get_words(article_id):
    article_id = Article.query.get(article_id)
    return render_template('words.html', article=article_id)


@blue.route('/add_comment/<int:article_id>', methods=['POST'])
def add_comment(article_id):
    comment_text = request.form.get('comment')

    if comment_text:
        new_comment = Comment(article_id=article_id, text=comment_text)
        db.session.add(new_comment)
        db.session.commit()
        flash('评论成功', 'success')
    else:
        db.session.rollback()
        flash('评论失败', 'danger')
    return redirect(url_for('article.get_flash'))


@blue.route('/comments/')
@cache.cached(timeout=20)
def get_comments():
    comments = Comment.query.all()
    comments_with_articles = []
    for comment in comments:
        article = Article.query.get(comment.article_id)
        comments_with_articles.append({
            'comment': comment,
            'article': article
        })
    return render_template('comments.html', comments_with_articles=comments_with_articles)


@blue.route('/about/')
def get_about():
    return render_template('about.html')


@blue.route('/chat/')
def get_chat():
    return render_template('chat.html')


@blue.route('/flash/')
def get_flash():
    return render_template('flash.html')

def handle_message(msg):
    print(f"Message: {msg}")
    send(msg, broadcast=True)

@blue.route('/post/', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if not title or not content:
            flash("标题和内容不能为空", "danger")
            return redirect(url_for('article.post'))

        new_article = Article(title=title, content=content)
        db.session.add(new_article)
        db.session.commit()

        flash("文章发布成功", "success")
        return redirect(url_for('article.index'))

    # GET 请求时渲染页面
    return render_template('post.html')


@socketio.on('message')
def handle_message(msg):
    print(f"Message: {msg}")
    send(msg, broadcast=True)

@socketio.on('join')
def handle_join(data):
    print(type(data))
    room = data['room']
    join_room(room)
    send(f"{'用户'+data['username']+'进入了'+ room+'房间'}",room=room)

@socketio.on('leave')
def handle_leave(data):
    room = data['room']
    leave_room(room)
    send(f"{data['username']} 离开了房间: {room}.", room=room)