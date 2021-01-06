# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, request, current_app
from docManageSys.models import Article


article_bp = Blueprint('article', __name__)


@article_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ARTICLE_PER_PAGE']
    pagination = Article.query.order_by(Article.id).paginate(page, per_page=per_page, error_out=True)
    articles = pagination.items
    return render_template('article/index.html', page=page, pagination=pagination, articles=articles)


@article_bp.route('/article/<int:article_id>')
def show_article(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template('article/article.html', article=article)
