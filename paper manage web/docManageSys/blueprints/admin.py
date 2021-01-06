# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required
from docManageSys.models import Article
from docManageSys.forms import ArticleInfoForm
from docManageSys.utils import redirect_back
from docManageSys.extensions import db


admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/article/new', methods=['GET', 'POST'])
@login_required
def new_article():
    form = ArticleInfoForm()
    if form.validate_on_submit():
        title = form.title.data
        author = form.author.data
        abstract = form.abstract.data
        publication_date = form.publication_date.data
        provenance = form.provenance.data
        article_level = form.article_level.data
        comment = form.comment.data
        provider = form.provider.data
        category = form.category.data
        annotation = form.annotation.data
        article = Article(title=title, author=author, abstract=abstract, publication_date=publication_date,
                          provenance=provenance, article_level=article_level, comment=comment, provider=provider,
                          category=category, annotation=annotation)
        db.session.add(article)
        db.session.commit()
        flash('创建成功', 'success')
        return redirect(url_for('article.show_article', article_id=article.id))
    return render_template('admin/new_article.html', form=form)


@admin_bp.route('/post/<int:article_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    form = ArticleInfoForm()
    article = Article.query.get_or_404(article_id)
    if form.validate_on_submit():
        article.title = form.title.data
        article.author = form.author.data
        article.abstract = form.abstract.data
        article.publication_date = form.publication_date.data
        article.provenance = form.provenance.data
        article.article_level = form.article_level.data
        article.comment = form.comment.data
        article.provider = form.provider.data
        article.category = form.category.data
        article.annotation = form.annotation.data
        db.session.commit()
        flash('编辑成功', 'success')
        return redirect(url_for('article.show_article', article_id=article.id))
    form.title.data = article.title
    form.author.data = article.author
    form.abstract.data = article.abstract
    form.publication_date.data = article.publication_date
    form.provenance.data = article.provenance
    form.article_level.data = article.article_level
    form.comment.data = article.comment
    form.provider.data = article.provider
    form.category.data = article.category
    form.annotation.data = article.annotation
    return render_template('admin/edit_article.html', form=form)


@admin_bp.route('/article/<int:article_id>/delete', methods=['POST'])
@login_required
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    flash('已删除', 'success')
    return redirect_back()
