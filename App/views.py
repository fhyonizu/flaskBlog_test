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
    return redirect(url_for('article.index'))


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


@blue.route('/music/')
def get_amusic():
    return render_template('music.html')
