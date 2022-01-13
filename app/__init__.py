# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import logging
from importlib import import_module
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, request, g
from flask_babel import Babel
from flask_login import LoginManager
# from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_dropzone import Dropzone

db = SQLAlchemy()
dropzone = Dropzone()
babel = Babel()
login_manager: LoginManager = LoginManager()

def register_extensions(app):
    db.init_app(app)
    dropzone.init_app(app)
    login_manager.init_app(app)
    babel.init_app(app)

    # @babel.localeselector
    # def get_locale():
    #     # if a user is logged in, use the locale from the user settings
    #     user = getattr(g, 'user', None)
    #     if user is not None:
    #         return user.locale
    #     # otherwise try to guess the language from the user accept
    #     # header the browser transmits.  We support de/fr/en in this
    #     # example.  The best match wins.
    #     return request.accept_languages.best_match(['en'])
    #
    # @babel.timezoneselector
    # def get_timezone():
    #     user = getattr(g, 'user', None)
    #     if user is not None:
    #         return user.timezone

def register_blueprints(app):
    for module_name in ('base', 'home', 'mail'):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

def register_i18n(app):
    """Register i18n with the Flask application."""
    defalut_language_str = app.config['DEFAULT_LANGUAGE']
    support_language_list = app.config['SUPPORTED_LANGUAGES']

    # 1 Get parameter lang_code from route
    @app.url_value_preprocessor
    def get_lang_code(endpoint, values):
        if values is not None:
            g.lang_code = values.pop('lang_code', defalut_language_str)

    # 2 Check lang_code type is in config
    @app.before_request
    def ensure_lang_support():
        lang_code = g.get('lang_code', None)
        if lang_code and lang_code not in support_language_list:
            g.lang_code = request.accept_languages.best_match(
                support_language_list)

    # 3 Setting babel
    @babel.localeselector
    def get_locale():
        return g.get('lang_code')

    # 4 Check lang_code exist after step1 pop parameter of lang_code
    @app.url_defaults
    def set_language_code(endpoint, values):
        if 'lang_code' in values or not g.lang_code:
            return
        if app.url_map.is_endpoint_expecting(endpoint, 'lang_code'):
            values['lang_code'] = g.lang_code

#修改CSS對應位置
def create_app(config):
    app = Flask(__name__, static_folder='base/static', static_url_path='/portal/<lang_code>/static')
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    register_i18n(app)
    configure_database(app)
    formatter = logging.Formatter(
        "[%(asctime)s][%(module)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s")
    handler = TimedRotatingFileHandler(
        "logs/flask.log", when="D", interval=1, backupCount=15,
        encoding="UTF-8", delay=False, utc=True)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    return app