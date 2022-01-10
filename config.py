# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os

import pymysql

pymysql.install_as_MySQLdb()
from decouple import config

class Config(object):

    basedir    = os.path.abspath(os.path.dirname(__file__))

    # Set up the App SECRET_KEY
    SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_007')

    # This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}?autocommit=true'.format(
        config( 'DB_ENGINE'   , default='mysql'    ),
        config( 'DB_USERNAME' , default='root'       ),
        config( 'DB_PASS'     , default='root'          ),
        config( 'DB_HOST'     , default='127.0.0.1'     ),
        config( 'DB_PORT'     , default=3306            ),
        config( 'DB_NAME'     , default='amus' )
    )

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #flask dropzone
    DROPZONE_UPLOAD_MULTIPLE = True  # enable upload multiple
    DROPZONE_PARALLEL_UPLOADS = 10# set parallel amount
    DROPZONE_ALLOWED_FILE_CUSTOM = True
    DROPZONE_ALLOWED_FILE_TYPE = 'image/*, .pdf, .txt, .encrypt'
    DROPZONE_MAX_FILE_SIZE = 10
    DROPZONE_MAX_FILES = 10000

    # EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=465
    MAIL_USE_SSL=True
    MAIL_DEFAULT_SENDER=('admin', 'popvlous007@gmail.com')
    MAIL_MAX_EMAILS=10
    MAIL_USERNAME='popvlous007@gmail.com'
    MAIL_PASSWORD='Foxconn@890'


class DevelopmentConfig(Config):
    """
    開發環境配置檔
    """
    DEBUG = 1

    # Security
    # SESSION_COOKIE_HTTPONLY  = True
    # REMEMBER_COOKIE_HTTPONLY = True
    # REMEMBER_COOKIE_DURATION = 3600

    # This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}?autocommit=true'.format(
        config( 'DB_ENGINE'   , default='mysql'    ),
        config( 'DB_USERNAME' , default='agora'       ),
        config( 'DB_PASS'     , default='AGo#2021#zKy'          ),
        config( 'DB_HOST'     , default='192.168.100.10'     ),
        config( 'DB_PORT'     , default=3306            ),
        config( 'DB_NAME'     , default='amus_dev' )
    )

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #flask dropzone
    DROPZONE_UPLOAD_MULTIPLE = True  # enable upload multiple
    DROPZONE_PARALLEL_UPLOADS = 10# set parallel amount
    DROPZONE_ALLOWED_FILE_CUSTOM = True
    DROPZONE_ALLOWED_FILE_TYPE = 'image/*, .pdf, .txt, .encrypt'
    DROPZONE_MAX_FILE_SIZE = 10
    DROPZONE_MAX_FILES = 10000

    # EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=465
    MAIL_USE_SSL=True
    MAIL_DEFAULT_SENDER=('admin', 'popvlous007@gmail.com')
    MAIL_MAX_EMAILS=10
    MAIL_USERNAME='popvlous007@gmail.com'
    MAIL_PASSWORD='Foxconn@890'

class ITEConfig(Config):
    DEBUG = 1

    # Security
    # SESSION_COOKIE_HTTPONLY  = True
    # REMEMBER_COOKIE_HTTPONLY = True
    # REMEMBER_COOKIE_DURATION = 3600


    # This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}?autocommit=true'.format(
        config( 'DB_ENGINE'   , default='mysql'    ),
        config( 'DB_USERNAME' , default='agora'       ),
        config( 'DB_PASS'     , default='AGo#2021#zKy'          ),
        config( 'DB_HOST'     , default='192.168.100.10'     ),
        config( 'DB_PORT'     , default=3306            ),
        config( 'DB_NAME'     , default='amus_ite' )
    )

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #flask dropzone
    DROPZONE_UPLOAD_MULTIPLE = True  # enable upload multiple
    DROPZONE_PARALLEL_UPLOADS = 10# set parallel amount
    DROPZONE_ALLOWED_FILE_CUSTOM = True
    DROPZONE_ALLOWED_FILE_TYPE = 'image/*, .pdf, .txt, .encrypt'
    DROPZONE_MAX_FILE_SIZE = 10
    DROPZONE_MAX_FILES = 10000

    # EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=465
    MAIL_USE_SSL=True
    MAIL_DEFAULT_SENDER=('admin', 'popvlous007@gmail.com')
    MAIL_MAX_EMAILS=10
    MAIL_USERNAME='popvlous007@gmail.com'
    MAIL_PASSWORD='Foxconn@890'

class ProductionConfig(Config):
    DEBUG = 0

    # Security
    #SESSION_COOKIE_HTTPONLY  = True
    #REMEMBER_COOKIE_HTTPONLY = True
    #REMEMBER_COOKIE_DURATION = 3600


    # This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}?autocommit=true'.format(
        config( 'DB_ENGINE'   , default='mysql'    ),
        config( 'DB_USERNAME' , default='pyrarcdev'       ),
        config( 'DB_PASS'     , default='dev2021api0322'          ),
        config( 'DB_HOST'     , default='192.168.110.18'     ),
        config( 'DB_PORT'     , default=3306            ),
        config( 'DB_NAME'     , default='amus' )
    )

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #flask dropzone
    DROPZONE_UPLOAD_MULTIPLE = True  # enable upload multiple
    DROPZONE_PARALLEL_UPLOADS = 10# set parallel amount
    DROPZONE_ALLOWED_FILE_CUSTOM = True
    DROPZONE_ALLOWED_FILE_TYPE = 'image/*, .pdf, .txt, .encrypt'
    DROPZONE_MAX_FILE_SIZE = 10
    DROPZONE_MAX_FILES = 10000

    # EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=465
    MAIL_USE_SSL=True
    MAIL_DEFAULT_SENDER=('admin', 'popvlous007@gmail.com')
    MAIL_MAX_EMAILS=10
    MAIL_USERNAME='popvlous007@gmail.com'
    MAIL_PASSWORD='Foxconn@890'


class DebugConfig(Config):
    DEBUG = 2

# Load all possible configurations
config_dict = {
    'production': ProductionConfig,
    'ite': ITEConfig,
    'debug': DebugConfig,
    'development': DevelopmentConfig
}