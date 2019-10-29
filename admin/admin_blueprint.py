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
        return '''
        <html>
        <head>
        <style>
          body {
            margin: 0;
            display: flex;
            flex-direction: column;
          }
          h1 {
            height: 32px;
          }
          iframe {
            width: 100%;
            height: calc(100vh - 32px);
          }
        </style>
        </head>
        <body>
          <h1>
          哈，被我发现了！你不是鬼屋的工作人员~ 如果你实在无聊的话，玩玩这个游戏怎么样？
          </h1>
          <iframe src="https://about.keeer.net/256/" class=""></iframe>
        </body>
      </html>'''
    if ticket == '':
        return 'Invalid form', 400
    if data_manager.ticket_status[ticket] != TICKET_STATUS.UNUSED:
          return '<meta name="viewport" content="width=device-width, initial-scale=1.0" /><h1>请注意！这张票已经失效！</h1>'
    data_manager.ticket_status[ticket] = TICKET_STATUS.USED
    return '<meta name="viewport" content="width=device-width, initial-scale=1.0" /><h1>成功检票！</h1>'

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

@admin_blueprint.route(ROUTES.STATS, methods=['GET'])
def process_stats():
    code = request.cookies.get('admin-code','')
    if code == '' or code not in admin_tokens:
        return '''
          <h1>
            <p>哈，被我发现了！你不是鬼屋的工作人员~</p>
          </h1>'''
    
    unused_amount = 0
    for k,v in data_manager.ticket_status.items():
        if v == TICKET_STATUS.UNUSED:
            unused_amount += 1
    sell_ticket_num = len(data_manager.ticket_status)
    unused_ratio = 'N/A'
    if sell_ticket_num > 0:
      unused_ratio = float(unused_amount) / sell_ticket_num * 100
    return '''
    <html lang="zh">
    <head>
    <style>
    body{
        margin: 8px;
       text-align: center;
      }
    </style>
    </head>
    <body>
    <h1>当前门票总出售量：%d 张。</h1>
    <h1>未使用数量：%d 张</h1>
    <h1>门票未使用比例：%s %%</h1>
    <h1>在线管理员数量：%d</h1>
    </body>
    </html>'''%(
        len(data_manager.ticket_status), 
        unused_amount, 
        str(unused_ratio), 
        len(admin_tokens)
    )