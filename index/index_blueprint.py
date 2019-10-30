from flask import Blueprint, request, render_template,redirect, make_response
from consts import ROUTES
from data import data_manager
index_blueprint = Blueprint('index_blueprint', __name__)

import logging 
logger = logging.getLogger('index_logger')

@index_blueprint.route(ROUTES.INDEX, methods = ['GET'])
def process_index():
    token = request.cookies.get('kas-account-token','')
    if token == '':
        return redirect('/login')
    try:
        user = data_manager.get_user(token)
        user_info = data_manager.get_user_informtaion(token)
        rsp = make_response(render_template('index.html', NICKNAME = user_info['nickname']))
        rsp.set_cookie('kas-account-token', token, domain='.keeer.net')
        return rsp
    except Exception as e:
        logger.exception('Error %s'%str(e))
        print('ERROR: %s'%str(e))
        return redirect('/login')
