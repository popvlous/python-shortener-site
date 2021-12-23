# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from datetime import datetime

from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer, BadSignature, SignatureExpired
from sqlalchemy.exc import InvalidRequestError

from app import db, login_manager


class Users(db.Document, UserMixin):
    meta = {'collection': 'User'}
    # _id = db.ObjectIdField()
    # id = db.IntField()
    username = db.StringField()
    email = db.StringField()
    password = db.StringField()
    BaseCreateTime = db.DateTimeField(required=True, default=datetime.utcnow())
    BaseCreatorId = db.IntField()
    BaseModifyTime = db.DateTimeField(required=True, default=datetime.utcnow())
    BaseVersion = db.IntField()
    BaseIsDelete = db.IntField()
    Salt = db.StringField()
    RealName = db.StringField()
    DepartmentId = db.IntField()
    Gender = db.IntField()
    Birthday = db.StringField()
    Portrait = db.StringField()
    Mobile = db.StringField()
    LoginCount = db.IntField()
    UserStatus = db.IntField()
    IsSystem = db.IntField()
    IsOnline = db.IntField()
    Remark = db.StringField()
    WebToken = db.StringField()
    ApiToken = db.StringField()
    # roleusers = relationship('RolesUsers', backref=backref('RolesUsers', order_by=id))
    # roleusers = db.DocumentField(RolesUsers)
    confirm = db.IntField()
    csrf_token = db.StringField()
    register = db.StringField()
    organize = db.ListField(db.ObjectIdField())

    # meta = {'strict': False}

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

        return False

    def get_id(self):
        return str(self.username)

    # Required for administrative interface
    def __unicode__(self):
        return self.login

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

    def create_confirm_token(self, expires_in=3600):
        """
        利用itsdangerous來生成令牌，透過current_app來取得目前flask參數['SECRET_KEY']的值
        :param expiration: 有效時間，單位為秒
        :return: 回傳令牌，參數為該註冊用戶的id
        """
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'user_email': self.email})

    def validate_confirm_token(self, token):
        """
        驗證回傳令牌是否正確，若正確則回傳True
        :param token:驗證令牌
        :return:回傳驗證是否正確，正確為True
        """
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)  # 驗證
        except SignatureExpired:
            #  當時間超過的時候就會引發SignatureExpired錯誤
            return False
        except BadSignature:
            #  當驗證錯誤的時候就會引發BadSignature錯誤
            return False
        return data



@login_manager.user_loader
def user_loader(username):
    try:
        user = Users.objects(username=username).first()
    except Exception as e:
        return False
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if not username:
        return None
    user = Users.objects(username=username).first()
    return user if user else None
