from flask import Blueprint, request, render_template,redirect, make_response
from consts import ROUTES, TICKET_STATUS, EVENT_INFO
from data import data_manager
admin_blueprint = Blueprint('admin_blueprint', __name__)
import uuid
admin_tokens = []
@admin_blueprint.route(ROUTES.ADMIN_SCAN, methods=['GET'])
def process_admin_scan():
    code = request.cookies.get('admin-code','')
    ticket = request.args.get('ticket','')
    if code == '' or code not in admin_tokens:
        return '<h1>你不是鬼屋的工作人员，这样没有用的（讲道理，你想你这张票直接作废么？）</p1>'
    if ticket == '':
        return 'Invalid form', 400
    data_manager.ticket_status[ticket] = TICKET_STATUS.USED
    return '<h1>成功检票！</h1>'

@admin_blueprint.route(ROUTES.ADMIN_LOGIN, methods=['GET','POST'])
def process_admin_login():
    if request.method == 'GET':
        return '''
        <!DOCTYPE HTML>
        <html>
          <head>
            <style>
            body::before, body::after {
              content: ' ';
              flex: auto;
              height: 10vh;
            }
            .container {
                display: flex;
                flex-direction: row;
            }
            .input-box {
                  margin: 16px;
                  width: 50%;
                  height: 10vh;
                  font-size: 48px;
                  background-color: #f5fafd;
                  border-width: thick;
                  border-color: #002d4d;
                  border-radius: 24px;
                  padding: 8px;
            }
            .submit-button {
                width: 30%;
                font-size: 36px;
                padding: 16px;
                margin: 16px;
                border-radius: 16px;
                background-color: #424242;
                color: #ffffff;
                box-shadow: 0px 2px 1px -1px rgba(0, 0, 0, 0.2), 0px 1px 1px 0px rgba(0, 0, 0, 0.14), 0px 1px 3px 0px rgba(0,0,0,.12);
            }
            </style>
          </head>
          <body>
            <form action="/admin" method="POST" style="margin-top: 32vh;">
              <input class="input-box" type="text" name="password" />
              <button class="submit-button">我是管理员！</button>
            </form>
          </body>
        </html>
        '''
    password = request.form.get('password','')
    if password != EVENT_INFO.ADMIN_PASSWORD:
        return '<h1>错误的密码，你不是管理员！</h1>'
    rsp = make_response('登录成功！')
    token = str(uuid.uuid1())
    rsp.set_cookie('admin-code',token, max_age=60*60*4)
    admin_tokens.append(token)
    return rsp