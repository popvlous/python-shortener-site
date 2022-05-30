# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import binascii
import hashlib
import json
import os

import requests as requests
import http.client
import mimetypes
from codecs import encode
from flask import current_app
from six import unichr


def hash_pass(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash)  # return bytes


def verify_pass(provided_password, stored_password):
    """Verify a stored password against one provided by user"""
    stored_password = stored_password
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def full2half(s):
    n = []
    s = s.decode('utf-8')
    for char in s:
        num = ord(char)
        if num == 0x3000:
            num = 32
        elif 0xFF01 <= num <= 0xFF5E:
            num -= 0xfee0
        num = unichr(num)
    n.append(num)
    return ''.join(n)


def check_encrypt(id, img_data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'id': id,
        'img_data': img_data
    }
    try:
        r = requests.post("https://notify-bot.line.me/oauth/token", headers=headers, data=data)
        res = json.loads(r.content.decode("utf-8").replace("'", '"'))
        current_app.logger.error(f'{id} 驗證圖片成功')
        return res['data']
    except Exception as err:
        current_app.logger.error(f'{id} 驗證圖片發生錯誤: {err}')
        return None


def check_encrypt_muti(id, img_data):
    conn = http.client.HTTPSConnection("agoraite.nexuera.com", 443)
    dataList = []
    boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=id;'))
    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))
    dataList.append(encode(id))
    # for fileinfo in img_data:
    for index in range(len(img_data)):
        if index != (len(img_data) - 1):
            if get_file_extension(img_data[index].filename) == ".jpg":
                dataList.append(encode('--' + boundary))
                dataList.append(
                    encode('Content-Disposition: form-data; name=image; filename={0}'.format(img_data[index].filename)))
                fileType = mimetypes.guess_type('app/base/static/temp/' + id + '/' + img_data[index].filename)[
                               0] or 'application/octet-stream'
                dataList.append(encode('Content-Type: {}'.format(fileType)))
                dataList.append(encode(''))
                with open('app/base/static/temp/' + id + '/' + img_data[index].filename, 'rb') as f:
                    dataList.append(f.read())
            else:
                dataList.append(encode('--' + boundary))
                dataList.append(
                    encode('Content-Disposition: form-data; name=file; filename={0}'.format(img_data[index].filename)))
                fileType = mimetypes.guess_type('app/base/static/temp/' + id + '/' + img_data[index].filename)[
                               0] or 'application/octet-stream'
                dataList.append(encode('Content-Type: {}'.format(fileType)))
                dataList.append(encode(''))
                with open('app/base/static/temp/' + id + '/' + img_data[index].filename, 'rb') as f:
                    dataList.append(f.read())
        else:
            if get_file_extension(img_data[index].filename) == ".jpg":
                dataList.append(encode('--' + boundary))
                dataList.append(
                    encode('Content-Disposition: form-data; name=image; filename={0}'.format(img_data[index].filename)))
                fileType = mimetypes.guess_type('app/base/static/temp/' + id + '/' + img_data[index].filename)[
                               0] or 'application/octet-stream'
                dataList.append(encode('Content-Type: {}'.format(fileType)))
                dataList.append(encode(''))
                with open('app/base/static/temp/' + id + '/' + img_data[index].filename, 'rb') as f:
                    dataList.append(f.read())
                dataList.append(encode('--' + boundary + '--'))
                dataList.append(encode(''))
            else:
                dataList.append(encode('--' + boundary))
                dataList.append(
                    encode('Content-Disposition: form-data; name=file; filename={0}'.format(img_data[index].filename)))
                fileType = mimetypes.guess_type('app/base/static/temp/' + img_data[index].filename)[
                               0] or 'application/octet-stream'
                dataList.append(encode('Content-Type: {}'.format(fileType)))
                dataList.append(encode(''))
                with open('app/base/static/temp/' + id + '/' + img_data[index].filename, 'rb') as f:
                    dataList.append(f.read())
                dataList.append(encode('--' + boundary + '--'))
                dataList.append(encode(''))
    body = b'\r\n'.join(dataList)
    payload = body
    headers = {
        'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
    }
    try:
        conn.request("POST", "/postfix/encryptedemail/decrypt", payload, headers)
        res = conn.getresponse()
        data = res.read()
        return data
    except Exception as err:
        current_app.logger.error(f'{id} 驗證圖片發生錯誤: {err}')
        return None


def check_encrypt_dropzone(id, img_data):
    conn = http.client.HTTPSConnection("agoraite.nexuera.com", 443)
    dataList = []
    boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=id;'))
    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))
    dataList.append(encode(id))
    # for fileinfo in img_data:
    for index in range(len(img_data)):
        if index != (len(img_data) - 1):
            if get_file_extension(img_data[index]) != ".encrypt":
                dataList.append(encode('--' + boundary))
                dataList.append(
                    encode('Content-Disposition: form-data; name=image; filename={0}'.format(img_data[index])))
                fileType = mimetypes.guess_type('app/base/static/temp/' + id + '/' + img_data[index])[
                               0] or 'application/octet-stream'
                dataList.append(encode('Content-Type: {}'.format(fileType)))
                dataList.append(encode(''))
                with open('app/base/static/temp/' + id + '/' + img_data[index], 'rb') as f:
                    dataList.append(f.read())
            else:
                dataList.append(encode('--' + boundary))
                dataList.append(
                    encode('Content-Disposition: form-data; name=file; filename={0}'.format(img_data[index])))
                fileType = mimetypes.guess_type('app/base/static/temp/' + id + '/' + img_data[index])[
                               0] or 'application/octet-stream'
                dataList.append(encode('Content-Type: {}'.format(fileType)))
                dataList.append(encode(''))
                with open('app/base/static/temp/' + id + '/' + img_data[index], 'rb') as f:
                    dataList.append(f.read())
        else:
            if get_file_extension(img_data[index]) != ".encrypt":
                dataList.append(encode('--' + boundary))
                dataList.append(
                    encode('Content-Disposition: form-data; name=image; filename={0}'.format(img_data[index])))
                fileType = mimetypes.guess_type('app/base/static/temp/' + id + '/' + img_data[index])[
                               0] or 'application/octet-stream'
                dataList.append(encode('Content-Type: {}'.format(fileType)))
                dataList.append(encode(''))
                with open('app/base/static/temp/' + id + '/' + img_data[index], 'rb') as f:
                    dataList.append(f.read())
                dataList.append(encode('--' + boundary + '--'))
                dataList.append(encode(''))
            else:
                dataList.append(encode('--' + boundary))
                dataList.append(
                    encode('Content-Disposition: form-data; name=file; filename={0}'.format(img_data[index])))
                fileType = mimetypes.guess_type('app/base/static/temp/' + img_data[index])[
                               0] or 'application/octet-stream'
                dataList.append(encode('Content-Type: {}'.format(fileType)))
                dataList.append(encode(''))
                with open('app/base/static/temp/' + id + '/' + img_data[index], 'rb') as f:
                    dataList.append(f.read())
                dataList.append(encode('--' + boundary + '--'))
                dataList.append(encode(''))
    body = b'\r\n'.join(dataList)
    payload = body
    headers = {
        'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
    }
    try:
        conn.request("POST", "/postfix/encryptedemail/decrypt", payload, headers)
        res = conn.getresponse()
        data = res.read()
        return data
    except Exception as err:
        current_app.logger.error(f'{id} 驗證圖片發生錯誤: {err}')
        return None


def get_file_extension(filename):
    arr = os.path.splitext(filename)
    return arr[len(arr) - 1]


def check_encrypt_test(id, img_data):
    conn = http.client.HTTPSConnection("agoraite.nexuera.com", 443)
    dataList = []
    boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=id;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("47739e22ea214d08a6bbec34414e185a"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=image; filename={0}'.format('022.jpg')))

    fileType = mimetypes.guess_type('app/base/static/temp/022.jpg')[0] or 'application/octet-stream'
    dataList.append(encode('Content-Type: {}'.format(fileType)))
    dataList.append(encode(''))

    with open('app/base/static/temp/022.jpg', 'rb') as f:
        dataList.append(f.read())
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=file; filename={0}'.format('021.jpg.encrypt')))

    fileType = mimetypes.guess_type('app/base/static/temp/021.jpg.encrypt')[0] or 'application/octet-stream'
    dataList.append(encode('Content-Type: {}'.format(fileType)))
    dataList.append(encode(''))

    with open('app/base/static/temp/021.jpg.encrypt', 'rb') as f:
        dataList.append(f.read())
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=file; filename={0}'.format('053.jpg.encrypt')))

    fileType = mimetypes.guess_type('app/base/static/temp/053.jpg.encrypt')[0] or 'application/octet-stream'
    dataList.append(encode('Content-Type: {}'.format(fileType)))
    dataList.append(encode(''))

    with open('app/base/static/temp/053.jpg.encrypt', 'rb') as f:
        dataList.append(f.read())
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=file; filename={0}'.format('mailbody.txt.encrypt')))

    fileType = mimetypes.guess_type('app/base/static/temp/mailbody.txt.encrypt')[0] or 'application/octet-stream'
    dataList.append(encode('Content-Type: {}'.format(fileType)))
    dataList.append(encode(''))

    with open('app/base/static/temp/mailbody.txt.encrypt', 'rb') as f:
        dataList.append(f.read())
    dataList.append(encode('--' + boundary + '--'))
    dataList.append(encode(''))
    body = b'\r\n'.join(dataList)
    payload = body
    headers = {
        'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
    }
    conn.request("POST", "/postfix/encryptedemail/decrypt", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data


def get_outgoing_code(mail_code, mail_id):
    end_point_url = "https://agoraite.nexuera.com/postfix/outermail/getbytoken?id=" + str(mail_id) + "&token=" + str(
        mail_code)
    headers = {'Content-Type': 'Content-Type": "application/json'}
    try:
        r = requests.get(end_point_url, headers=headers, verify=False)
        mail_info = r.content.decode("utf-8").replace("'", '"')
        data = json.loads(mail_info)
        if data['code'] == 0:
            return data
        else:
            err_code = data['code']
            current_app.logger.error(f'{mail_id} 外寄郵件時 發生錯誤代碼: {err_code}')
            return None
    except Exception as err:
        current_app.logger.error(f'{mail_id} 外寄郵件時 發生錯誤: {err}')
        return None


def list_to_string(temp_list):
    listString = ''
    for tmep_info in temp_list:
        if tmep_info['address'] != '':
            listString += ',' + tmep_info['address']
    return listString
