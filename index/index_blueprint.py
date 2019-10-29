from flask import Blueprint, request, render_template,redirect
from consts import ROUTES
from data import data_manager
index_blueprint = Blueprint('index_blueprint', __name__)

@index_blueprint.route(ROUTES.INDEX, methods = ['GET'])
def process_index():
    token = request.cookies.get('kas-account-token','')
    if token == '':
        return redirect('/login')
    try:
        user = data_manager.get_user(token)
        user_info = data_manager.get_user_informtaion(token)
        return render_template('index.html', NICKNAME = user_info['nickname'])
    except Exception as e:
        print('ERROR: %s'%str(e))
        return redirect('/login')
