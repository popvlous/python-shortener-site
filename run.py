# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from sys import exit

from decouple import config
from flask_migrate import Migrate

from app import create_app, db
from config import config_dict

# WARNING: Don't run with debug turned on in production!
FLASK_ENV = config('FLASK_ENV', default="development", cast=str)
FLASK_DEBUG = config('FLASK_DEBUG', default="1", cast=bool)


try:
    app_config = config_dict[FLASK_ENV]
except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, ITE, development, Production] ')


app = create_app(app_config)
Migrate(app, db)

if FLASK_ENV:
    app.logger.info('DEBUG       = ' + str(FLASK_DEBUG))
    app.logger.info('Environment = ' + FLASK_ENV)
    app.logger.info('DBMS        = ' + str(app_config.SQLALCHEMY_DATABASE_URI))

# .ENV檔案中設定測試環境DEBUG=True , 正式環境DEBUG=False
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)