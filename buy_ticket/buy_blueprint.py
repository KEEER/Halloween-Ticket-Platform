from flask import Blueprint, request, render_template,redirect, make_response
from consts import ROUTES, EVENT_INFO
from data import data_manager

buy_blueprint = Blueprint('buy_blueprint', __name__)

@buy_blueprint.route(ROUTES.BUY_TICKET, methods=['GET'])
def process_buy_ticket():
    token = request.cookies.get('kas-account-token','')
    if token == '':
        return redirect('/login')
    amount = data_manager.get_user_kredit_amount(token)
    user_info = data_manager.get_user_informtaion(token)
    return render_template(
        'buy.html', 
        AVALIABLE_AMOUNT = int(amount), 
        PRICE = EVENT_INFO.PRICE_PER_PERSON,
        NICKNAME = user_info['nickname'],
        TICKETS = data_manager.tickets
    )
@buy_blueprint.route(ROUTES.RECHARGE_REDIRECT, methods = ['GET'])
def process_recharge_redirect():
    redirect_response = make_response(redirect('https://account.keeer.net/pay?amount=%s'%EVENT_INFO.PRICE_PER_PERSON))
    redirect_response.set_cookie('kas-account-token', request.cookies.get('kas-account-token',''), max_age=5*60)
    print('Recharge redirecting...')
    return redirect_response

@buy_blueprint.route(ROUTES.CONFIRM_PAGE, methods=['GET', 'POST'])
def process_confirm_page():
    if request.method == 'GET':
        id = request.args.get('id','')
        if id == '':
            return redirect('/buy')
        try:
            id = int(id)
        except ValueError:
            return redirect('/buy')
        print(data_manager.tickets[id])
        return render_template(
            'confirm.html',
            PRICE = EVENT_INFO.PRICE_PER_PERSON,
            TICKET = data_manager.tickets[id]
        )
    else:
        id = request.form.get('id','')
        token = request.cookies.get('kas-account-token', '')
        if id == '':
            return redirect('/buy')
        if token == '':
            return redirect('/login')
        try:
            id = int(id)
        except ValueError:
            return redirect('/buy')
        
        buy_result = data_manager.buy_ticket(token, id)
        print(buy_result)
        return render_template(
            'result.html',
            SUCCEED = buy_result[0],
            MESSAGE = buy_result[1]
        )

@buy_blueprint.route(ROUTES.TERMS, methods=['GET'])
def process_terms():
    return render_template('terms.html')

