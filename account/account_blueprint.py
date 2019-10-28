from flask import Blueprint, request, render_template, make_response, redirect
from consts import ROUTES
from config import config
import requests
import json
import hashlib

account_blueprint = Blueprint('account_blueprint', __name__)


def _sign(value, key):
    coder = hashlib.sha512()
    coder.update(bytearray(value+key, encoding='UTF8'))
    return coder.hexdigest()

@account_blueprint.route(ROUTES.SEND_SMS, methods = ['POST'])
def process_send_sms():
    phone_number = request.form.get('phone_number','')
    purpose = request.form.get('purpose','')
    csrf = request.form.get('_csrf','')
    if csrf == '' or csrf != request.cookies.get('csrf',''):
        return '',403
    form = {
        'phone_number': phone_number,
        'purpose': purpose,
        'sign': _sign(phone_number, config['server']['keeer_secret_key'])
    }
    response = requests.post('https://account.keeer.net/api/ess/send_sms_by_sign' , form, headers = {'User-agent': 'Mozilla/5.0'})
    print(phone_number + config['server']['keeer_secret_key'])
    print(response.json())
    return json.dumps(response.json())
    
@account_blueprint.route(ROUTES.LOGIN, methods = ['GET', 'POST'])
def process_login():
    if request.method == 'GET':
        return render_template('login.html', has_error=False)
    else:
        if 'login' in request.form:
            # this is a login request 
            try:
                form = {
                    'identity': request.form['identity'],
                    'password': request.form['password']
                }
                response = requests.post('https://account.keeer.net/api/ess/login' , form, headers = {'User-agent': 'Mozilla/5.0'})
                response = response.json()
                if response['status'] == 0:
                    if response['result']['status'] == 0:
                        flask_response = make_response(redirect('/'))
                        flask_response.set_cookie('kas-account-token', response['result']['result'])
                        flask_response.set_cookie('Max-Age', '604800')
                        return flask_response
                return render_template('login.html', has_error=True, request_status = response['status'], api_status = response['result']['status'])
            except Exception as e:
                return str(e), 401
        else:
            try:
                form = {
                    'phone_number': request.form['phone_number'],
                    'password': request.form['password'],
                    'verification_code': request.form['verification_code']
                }
                response = requests.post('https://account.keeer.net/api/ess/register' , form, headers = {'User-agent': 'Mozilla/5.0'})
                if response.status_code != 200:
                    return '<h1>%s : %s</h1>'%(response.status_code, response.text), response.status_code
                response = response.json()
                if response['status'] == 0:
                    if response['result']['status'] == 0:
                        token = response['result']['result']
                        form = {
                            'token': token,
                            'nickname': request.form['nickname'],
                        }
                        print('New user registered successfully; setting nickname...')
                        set_nickname_response = requests.post('https://account.keeer.net/api/profile/set_nickname' , form, headers = {'User-agent': 'Mozilla/5.0'})
                        if set_nickname_response.status_code != 200:
                            return '<h1>%s : %s</h1>'%(set_nickname_response.status_code, set_nickname_response.text), set_nickname_response.status_code
                        set_nickname_response = set_nickname_response.json()
                        if set_nickname_response['status'] == 0 and set_nickname_response['result']['status'] == 0:
                            flask_response = make_response(redirect('/'))
                            flask_response.set_cookie('kas-account-token', token)
                            return flask_response
                return render_template('login.html', has_error=True, request_status = response['status'], api_status = response['result']['status'])
            except Exception as e:
                return str(e), 500