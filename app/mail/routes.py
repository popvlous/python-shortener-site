import base64
import datetime
import hashlib
import json
import os
import shutil
from datetime import time
from io import BytesIO

from flask import render_template, request, make_response, session, jsonify, redirect, url_for, current_app
from flask_login import login_required
from jinja2 import TemplateNotFound

import config
from app.base.forms import LoginForm
from app.mail import blueprint
from app.util.captcha import Captcha
from app.util.util import check_encrypt, check_encrypt_muti, check_encrypt_test, check_encrypt_dropzone


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
            files_lists = os.listdir('app/base/static/temp/' + mail_id + '/')
            return render_template('mail/picupload.html', id=mail_id, file_lists=files_lists)
        else:
            current_app.logger.error(f' 上傳以保存完成，進行解密作業 ')

        # 将二进制转换成字符串
        #if type(data_json) == bytes:
        #data_json = data_json.decode('utf8')

        # 删除前面的 'data:image/png;base64,'
        #img_data = data_json.split(',')[1]

        #data = json.loads(data_json)
        #id = data['id']

        #return redirect(url_for('mail.upload', id=id, file_lists=files_list))

        #驗證圖片
        files_list = os.listdir('app/base/static/temp/' + mail_id + '/')
        result = check_encrypt_dropzone(mail_id, files_list)

        # 用base64.b64decode()转化
        #f = open('test.jpg', 'wb')
        #f.write(base64.b64decode(img_data))
        #f.close()
        result_json = json.loads(result)
        #判斷驗證結果
        if result_json.get('status'):
            message = "圖片驗證失敗 原因:" + result_json['error']
            status_code = result_json['status']
            current_app.logger.error(f' 圖片驗證失敗 { message } status: {status_code}  ')
            return render_template('page-500.html', message=message), int(status_code)
        else:
            current_app.logger.error(f' 加密郵件id {mail_id} 驗證成功  ')
        #顯示解密結果
        if result_json:
            #return result
            #return render_template('mail/picupload.html', id=id, file_lists=file_lists)
            #return redirect(url_for('mail.show', content=result['content'], email=result['email']))
            if result_json['code'] == 0:
                data = result_json['data']
                return render_template('mail/show.html', content=str(data['mailbody']), attachment=data['attachment'])
            else:
                message = "圖片驗證失敗,失敗原因：" + str(result_json['message']) + " code: " + str(result_json['code'])
                current_app.logger.error(f' 圖片驗證失敗 {message} ')
                return render_template('page-500.html', message=message), 500
        else:
            message = "圖片驗證失敗"
            current_app.logger.error(f' 圖片驗證失敗 {message} ')
            return render_template('page-500.html', message=message), 500
    else:
        mail_id = request.args.get('id')
        if not os.path.isdir('app/base/static/temp/' + mail_id):
            os.makedirs('app/base/static/temp/' + mail_id)
        else:
            shutil.rmtree('app/base/static/temp/' + mail_id)
            os.mkdir('app/base/static/temp/' + mail_id)
        if not mail_id:
            message = "URL遺失id參數"
            return render_template('page-500.html', message=message), 500
        return render_template('mail/picupload.html', id=mail_id)
    return render_template('page-500.html', message=message), 500



@blueprint.route('/mail/show', methods=['POST', 'GET'])
def show():
    content = request.args['content']
    email = request.args['email']
    return render_template('mail/show.html', email=email, content=content)
