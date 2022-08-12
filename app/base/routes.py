# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Python modules
import os

# Flask modules
from flask import render_template, request, url_for, redirect, send_from_directory, current_app
from flask_login import (
    login_user,
    logout_user
)

from app.base import blueprint
# provide login manager with load_user callback
from app.base.forms import RegisterForm, LoginForm
from app.model.models import Users
# Logout user
from app.util.util import verify_pass, hash_pass


@blueprint.route('/')
def route_default():
    return redirect(url_for('home.index'))


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('base.login'))


# Register a new user
@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    # declare the Registration Form
    form = RegisterForm(request.form)

    msg = None
    success = False

    if request.method == 'GET':
        return render_template('accounts/register.html', form=form, msg=msg)

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str)
        email = request.form.get('email', '', type=str)

        # filter User out of database through username
        user = Users.query.filter_by(user=username).first()

        # filter User out of database through username
        user_by_email = Users.query.filter_by(email=email).first()

        if user or user_by_email:
            msg = 'Error: User exists!'

        else:

            pw_hash = hash_pass(password)

            user = Users(username, email, pw_hash)

            user.save()

            msg = 'User created, please <a href="' + url_for('base.login') + '">login</a>'
            success = True

    else:
        msg = 'Input error'

    return render_template('accounts/register.html', form=form, msg=msg, success=success)


# Authenticate user
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # Declare the login form
    form = LoginForm(request.form)

    # Flask message injected into the page, in case of any errors
    msg = None

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str)

        # filter User out of database through username
        user = Users.query.filter_by(user=username).first()

        if user:

            if verify_pass(password, user.password):
                login_user(user)
                current_app.logger.error(f'{username} 登入成功 ')
                return redirect(url_for('home.index'))
            else:
                current_app.logger.error(f'{username} 輸入發生錯誤: 輸入密碼為{password} ')
                msg = "Wrong password. Please try again."
        else:
            current_app.logger.error(f'{username} 找不到對應的user ')
            msg = "Unknown user"

    return render_template('accounts/login.html', form=form, msg=msg)


# App main route + generic routing
# @blueprint.route('/', defaults={'path': 'index.html'})
# @blueprint.route('/<path>')
# def index(path):
#     if not current_user.is_authenticated:
#         return redirect(url_for('base.login'))
#
#     try:
#
#         if not path.endswith('.html'):
#             path += '.html'
#
#         # Serve the file (if exists) from app/templates/FILE.html
#         #return render_template('templates/' + path)
#         return redirect(url_for('home.index'))
#
#     except TemplateNotFound:
#         return render_template('home/page-404.html'), 404
#
#     except:
#         logout_user()
#         return render_template('home/page-500.html'), 500


# Return sitemap
@blueprint.route('/sitemap.xml')
def sitemap():
    return send_from_directory(os.path.join(blueprint.root_path, 'base/static'), 'sitemap.xml')