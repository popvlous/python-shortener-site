import base64
import datetime
import hashlib
import json
import os
import shutil
from datetime import time
from io import BytesIO

from flask import render_template, request, make_response, session, jsonify, redirect, url_for, current_app
from flask_babel import gettext
from flask_login import login_required
from jinja2 import TemplateNotFound

import config
from app.base.forms import LoginForm
from app.mail import blueprint
from app.util.captcha import Captcha
from app.util.util import check_encrypt, check_encrypt_muti, check_encrypt_test, check_encrypt_dropzone, \
    get_outgoing_code, list_to_string


@blueprint.route('/index')
def index():
    return render_template('index.html')


@blueprint.route('/mail/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        mail_id = request.args.get('id')
        if not os.path.isdir('app/base/static/temp/' + mail_id):
            os.makedirs('app/base/static/temp/' + mail_id)
        if not request.form.get("check_mail"):
            # for filename in file_lists:
            #     f = ('admin' + str(datetime.datetime.time)).encode('UTF-8')
            #     name = hashlib.md5(f).hexdigest()[:15]
            #     filename.save('app/base/static/temp/' + id + '/' + filename.filename)
            #     current_app.logger.error(f' 上傳檔案 {filename.filename} 暫存完成 ')
            for key, f in request.files.items():
                if key.startswith('file'):
                    f.save(os.path.join('app/base/static/temp/' + mail_id + '/', f.filename))
                    current_app.logger.info(
                        f' 圖片上傳至服務器 {f.filename} , file_location : app/base/static/temp/{mail_id}/ ')
            files_lists = os.listdir('app/base/static/temp/' + mail_id + '/')
            default_message = gettext(u'Drop files here to upload')
            return render_template('mail/picupload.html', id=mail_id, file_lists=files_lists,
                                   default_message=default_message)
        else:
            files_lists = os.listdir('app/base/static/temp/' + mail_id + '/')
            files_lists_count = 0
            if files_lists:
                files_lists_count = len(files_lists)
            current_app.logger.info(f' 上傳以保存完成，進行解密作業 上傳檔案數量共 {str(files_lists_count)} 個')

        # 将二进制转换成字符串
        # if type(data_json) == bytes:
        # data_json = data_json.decode('utf8')

        # 删除前面的 'data:image/png;base64,'
        # img_data = data_json.split(',')[1]

        # data = json.loads(data_json)
        # id = data['id']

        # return redirect(url_for('mail.upload', id=id, file_lists=files_list))

        # 驗證圖片
        files_list = os.listdir('app/base/static/temp/' + mail_id + '/')
        result = check_encrypt_dropzone(mail_id, files_list)

        # 用base64.b64decode()转化
        # f = open('test.jpg', 'wb')
        # f.write(base64.b64decode(img_data))
        # f.close()
        result_json = json.loads(result)
        # 判斷驗證結果
        if result_json.get('status'):
            message = "圖片驗證失敗 原因:" + result_json['error']
            status_code = result_json['status']
            current_app.logger.error(f' 圖片驗證失敗 {message} status: {status_code}  ')
            return render_template('mail/mail500.html', message=message, mail_id=mail_id)
        else:
            current_app.logger.info(f' 加密郵件id {mail_id} 驗證成功  ')
        # 顯示解密結果
        if result_json:
            # return result
            # return render_template('mail/picupload.html', id=id, file_lists=file_lists)
            # return redirect(url_for('mail.show', content=result['content'], email=result['email']))
            if result_json['code'] == 0:
                data = result_json['data']
                current_app.logger.info(f' 顯示解密文件於頁面  ')
                return render_template('mail/show.html', content=str(data['mailbody']), attachment=data['attachment'])
            else:
                message = "圖片驗證失敗,失敗原因：" + str(result_json['message']) + " code: " + str(result_json['code'])
                current_app.logger.error(f' 圖片驗證失敗 {message} ')
                return render_template('mail/mail500.html', message=message, mail_id=mail_id)
        else:
            message = "圖片驗證失敗"
            current_app.logger.error(f' 圖片驗證失敗 {message} ')
            return render_template('mail/mail500.html', message=message, mail_id=mail_id)
    else:
        mail_id = request.args.get('id')
        if not os.path.isdir('app/base/static/temp/' + mail_id):
            os.makedirs('app/base/static/temp/' + mail_id)
        else:
            shutil.rmtree('app/base/static/temp/' + mail_id)
            os.mkdir('app/base/static/temp/' + mail_id)
        if not mail_id:
            message = "URL遺失id參數"
            return render_template('mail/mail500.html', message=message, mail_id=mail_id)

        # 利用重導向切換語言
        current_language = request.accept_languages.best
        session['language'] = current_language
        return redirect(request.host_url + "portal/" + current_language + "/mail/uploadfile?id=" + mail_id)
        # return render_template('mail/picupload.html', id=mail_id, default_message=default_message)
        # return redirect(url_for('mail.lan', id=mail_id))
    return render_template('mail/mail500.html', message=message, mail_id=mail_id)


@blueprint.route('/mail/show', methods=['POST', 'GET'])
def show():
    content = request.args['content']
    email = request.args['email']
    return render_template('mail/show.html', email=email, content=content)


@blueprint.route('/mail/code', methods=['POST', 'GET'])
def code():
    if request.method == 'POST':
        mail_id = request.args.get('id')
        mail_token = request.args.get('token')
        mail_code = request.form['mail_code']
        mail_response = get_outgoing_code(mail_code, mail_id)
        if not mail_response:
            return render_template('mail/mail500.html', message='id或token有誤，無法取得郵件資訊')
        mail_detail = mail_response['data']
        data = mail_detail['maildetail']
        mail_cc = list_to_string(data['cc'])
        mail_attachment = data['attachment']
        mail_sendDate = data['sendDate']
        mail_subject = data['subject']
        if data['html']:
            mail_plain = data['html']
        else:
            mail_plain = data['plain']
        mail_from = data['from']['address']
        mail_to = list_to_string(data['to'])[1:]
        return render_template('mail/outgoing.html', id=mail_id, token=mail_token, mail_cc=mail_cc, mail_attachment=mail_attachment,
                               mail_sendDate=mail_sendDate, mail_plain=mail_plain, mail_from=mail_from, mail_to=mail_to, mail_subject=mail_subject)
    mail_id = request.args.get('id') if 'id' in request.args else None
    mail_token = request.args.get('token') if 'token' in request.args else None
    if not mail_id:
        return render_template('mail/mail500.html', message='連結不存在id參數')
    if not mail_token:
        return render_template('mail/mail500.html', message='連結不存在token參數')
    return render_template('mail/code.html', id=mail_id, token=mail_token)


@blueprint.route('/mail/uploadfile', methods=['POST', 'GET'])
def lan():
    if request.method == 'POST':
        mail_id = request.args.get('id')
        if not os.path.isdir('app/base/static/temp/' + mail_id):
            os.makedirs('app/base/static/temp/' + mail_id)
        if not request.form.get("check_mail"):
            for key, f in request.files.items():
                if key.startswith('file'):
                    f.save(os.path.join('app/base/static/temp/' + mail_id + '/', f.filename))
                    current_app.logger.info(
                        f' 圖片上傳至服務器 {f.filename} , file_location : app/base/static/temp/{mail_id}/ ')
            files_lists = os.listdir('app/base/static/temp/' + mail_id + '/')
            default_message = gettext(u'Drop files here to upload')
            return render_template('mail/picupload.html', id=mail_id, file_lists=files_lists,
                                   default_message=default_message)
        else:
            files_lists = os.listdir('app/base/static/temp/' + mail_id + '/')
            files_lists_count = 0
            if files_lists:
                files_lists_count = len(files_lists)
            current_app.logger.info(f' 上傳以保存完成，進行解密作業 上傳檔案數量共 {str(files_lists_count)} 個')

        # 驗證圖片
        files_list = os.listdir('app/base/static/temp/' + mail_id + '/')
        result = check_encrypt_dropzone(mail_id, files_list)
        result_json = json.loads(result)

        # 判斷驗證結果
        if result_json.get('status'):
            message = "圖片驗證失敗 原因:" + result_json['error']
            status_code = result_json['status']
            current_app.logger.error(f' 圖片驗證失敗 {message} status: {status_code}  ')
            return render_template('mail/mail500.html', message=message, mail_id=mail_id)
        else:
            current_app.logger.info(f' 加密郵件id {mail_id} 驗證成功  ')
        # 顯示解密結果
        if result_json:
            if result_json['code'] == 0:
                data = result_json['data']
                current_app.logger.info(f' 顯示解密文件於頁面  ')
                return render_template('mail/show.html', content=str(data['mailbody']), attachment=data['attachment'])
            else:
                message = "圖片驗證失敗,失敗原因：" + str(result_json['message']) + " code: " + str(result_json['code'])
                current_app.logger.error(f' 圖片驗證失敗 {message} ')
                # 刪除對應目錄
                shutil.rmtree('app/base/static/temp/' + mail_id)
                return render_template('mail/mail500.html', message=message, mail_id=mail_id)
        else:
            message = "圖片驗證失敗"
            current_app.logger.error(f' 圖片驗證失敗 {message} ')
            return render_template('mail/mail500.html', message=message, mail_id=mail_id)
    else:
        default_message = gettext(u'Drop files here to upload')
    mail_id = request.args.get('id')
    if not mail_id:
        message = "連結郵件id遺失,請重新點擊郵件連結"
        current_app.logger.error(f' 網址連結失敗 {message} ')
        return render_template('mail/mail500.html', message=message, mail_id=mail_id)
    return render_template('mail/picupload.html', id=mail_id, default_message=default_message)


@blueprint.route('/mail/reload', methods=['POST', 'GET'])
def reload():
    mail_id = request.args.get('mail_id')
    if not mail_id:
        message = '郵件id遺失，請重新點擊郵件連結'
        current_app.logger.error(f' 網址連結失敗 {message} ')
        return render_template('mail/mail500.html', message=message, mail_id=mail_id)
    current_language = request.accept_languages.best
    session['language'] = current_language
    current_app.logger.error(f' 解密郵件頁面重新載入 ')
    return redirect(request.host_url + "portal/" + current_language + "/mail/uploadfile?id=" + mail_id)
