from flask import Blueprint, render_template, request, redirect, url_for
from .models import *

blue = Blueprint('article', __name__)

@blue.route('/')
def base():
    articles = get_artics()
    return render_template('index2.html', articles=articles)

@blue.route('/artics/')
def get_artics():
    articles = Article.query.all()
    return articles

@blue.route('/words/<int:article_id>')
def get_words(article_id):
    article_id = Article.query.get(article_id)
    return render_template('words.html',article_id = article_id)

@blue.route('/add_comment/<int:article_id>', methods=['POST'])
def add_comment(article_id):
    comment_text = request.form.get('comment')
    if comment_text:
        new_comment = Comment(article_id=article_id, text=comment_text)
        db.session.add(new_comment)
        db.session.commit()
    return redirect(url_for('user.base'))