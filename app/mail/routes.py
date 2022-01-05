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
from app.base.forms import LoginForm
from app.mail import blueprint
from app.util.captcha import Captcha
from app.util.util import check_encrypt, check_encrypt_muti, check_encrypt_test


@blueprint.route('/index')
def index():
    return render_template('index.html')


@blueprint.route('/mail/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        data_json = request.get_data()
        foem_data = request.form.getlist("file_lists")
        id = request.args.get('id')
        old_file_lists = request.files.getlist('file_lists[]')
        file_lists = request.files.getlist('file[]')
        if not os.path.isdir('app/base/static/temp/' + id):
            os.makedirs('app/base/static/temp/' + id)
        else:
            shutil.rmtree('app/base/static/temp/' + id)
            os.mkdir('app/base/static/temp/' + id)
        if file_lists:
            for filename in file_lists:
                f = ('admin' + str(datetime.datetime.time)).encode('UTF-8')
                name = hashlib.md5(f).hexdigest()[:15]
                filename.save('app/base/static/temp/' + id + '/' + filename.filename)
                current_app.logger.error(f' 上傳檔案 {filename.filename} 暫存完成 ')
            success = True
        else:
            success = False
        # 将二进制转换成字符串
        #if type(data_json) == bytes:
        #    data_json = data_json.decode('utf8')

        # 删除前面的 'data:image/png;base64,'
        #img_data = data_json.split(',')[1]

        #data = json.loads(data_json)
        #id = data['id']

        #驗證圖片
        result = check_encrypt_muti(id, file_lists)

        #測試
        # result = {
        #     "code": 0,
        #     "message": "加密信件解密成功",
        #     "data": {
        #         "mailbody": "<p>move</p ><p>move</p ><p>move</p ><p>move</p ><p>move</p ><p>move</p ><p>move</p ><p>move</p ><p>move</p ><p>move</p ><p>move</p ><p>move</p >",
        #         "attachment": [
        #             {
        #                 "fileName": "021.jpg",
        #                 "fileSize": "365.89 KB",
        #                 "url": "http://127.0.0.1:8080/postfix/encryptedemail/download/61d26c6de8971f4762abdc87/021.jpg"
        #             },
        #             {
        #                 "fileName": "053.jpg",
        #                 "fileSize": "378.22 KB",
        #                 "url": "http://127.0.0.1:8080/postfix/encryptedemail/download/61d26c6ee8971f4762abdc8a/053.jpg"
        #             }
        #         ],
        #         "subject": ""
        #     }
        # }

        # 用base64.b64decode()转化
        #f = open('test.jpg', 'wb')
        #f.write(base64.b64decode(img_data))
        #f.close()
        result_json = json.loads(result)
        data = {}
        #判斷驗證結果
        if result_json.get('status'):
            message = "圖片驗證失敗 原因:" + result_json['error']
            status_code = result_json['status']
            current_app.logger.error(f' 圖片驗證失敗 { message } status: {status_code}  ')
            return render_template('page-500.html', message=message), int(status_code)
        else:
            data = result_json['data']
            current_app.logger.error(f' 加密郵件id {id} 驗證成功  ')
        #顯示解密結果
        if result_json:
            #return result
            #return render_template('mail/picupload.html', id=id, file_lists=file_lists)
            #return redirect(url_for('mail.show', content=result['content'], email=result['email']))
            return render_template('mail/show.html', content=str(data['mailbody']), attachment=data['attachment'])
        else:
            message = "圖片驗證失敗"
            current_app.logger.error(f' 圖片驗證失敗 {message} ')
            return render_template('page-500.html', message=message), 500
    else:
        id = request.args.get('id')
        if not id:
            message = "URL遺失id參數"
            return render_template('page-500.html', message=message), 500
        return render_template('mail/picupload.html', id=id)
    return render_template('page-500.html', message=message), 500



@blueprint.route('/mail/show', methods=['POST', 'GET'])
def show():
    content = request.args['content']
    email = request.args['email']
    return render_template('mail/show.html', email=email, content=content)

