# -*- coding:utf-8 -*-
from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import current_user, login_required, logout_user, login_user
from docManageSys.forms import LoginForm
from docManageSys.models import Admin
from docManageSys.utils import redirect_back

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('article.index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.first()
        if admin:
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember)
                flash('欢迎回来', 'info')
                return redirect_back()
            flash('无效的用户名或密码', 'warning')
        else:
            flash('没有任何账户', 'warning')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已退出', 'info')
    return redirect_back()
