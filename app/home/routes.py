from io import BytesIO

from flask import render_template, request, make_response, session, jsonify, redirect, url_for, current_app
from flask_babel import gettext
from flask_login import login_required
from jinja2 import TemplateNotFound

from app.base.forms import LoginForm
from app.home import blueprint
from app.util.captcha import Captcha
from app.util.util import full2half


#@blueprint.route('/', defaults={'path': 'index.html'})
@blueprint.route('/<template>')
def route_template(template):
    try:
        message = gettext(u'Hello World!')

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template(template, segment=segment)

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except:
        return render_template('page-500.html'), 500



@blueprint.route('/index')
def index():
    return render_template('/index.html')


@blueprint.route('/message', methods=['GET', 'POST'])
def message():

    # assign form data to variables
    name = request.form.get('name', '', type=str)
    email = request.form.get('email', '', type=str)
    subject = request.form.get('subject', '', type=str)
    message = request.form.get('message', '', type=str)
    captcha = request.form.get('captcha').lower()
    s_captcha = session['imageCode'].lower().replace(' ', '')
    if captcha == s_captcha:
        pass
    else:
        current_app.logger.error(f'{email} 輸入發生錯誤: 輸入為{captcha} 驗證碼為{s_captcha}')
        return "圖型驗證碼輸入不符"
    return "OK"


@blueprint.route("/captcha")
def graph_captcha():
    """
    使用定義好的圖形驗證碼類，來製作驗證碼
    以驗證碼為鍵、驗證碼為值（為了用戶的體驗，讓其忽略大小寫）存儲在redis緩存中
    通過BytesIO位元組流的方式保存和訪問圖片
    :return: 圖片響應
    """
    # 獲取驗證碼
    text, image = Captcha.gene_graph_captcha()
    #cpcache.set(text.lower(), text.lower())

    # BytesIO:位元組流
    out = BytesIO()
    # 保存圖片
    image.save(out, "png")
    # 存儲完圖片，將文件的指針指向文件頭，使下次保存圖片能覆蓋前面保存的圖片，節省空間
    out.seek(0)
    # 訪問圖片，並將其作為一個響應返回給前臺
    resp = make_response(out.read())
    resp.content_type = "image/png"
    session['imageCode'] = text
    return resp

# Helper - Extract current page name from request
def get_segment( request ):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
