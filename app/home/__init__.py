# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Blueprint

blueprint = Blueprint(
    'home',
    __name__,
    url_prefix='/portal/<lang_code>',
    #url_prefix='/portal',
    template_folder='templates',
    static_folder='static'
)