from flask import Blueprint, request, render_template,redirect, send_file
from consts import ROUTES, EVENT_INFO, TICKET_STATUS
from data import data_manager


ticket_blueprint = Blueprint('ticket_blueprint', __name__)

from server import server


@ticket_blueprint.route(ROUTES.TICKETS, methods=['GET'])
def process_tickets():
    token = request.cookies.get('kas-account-token','')
    if token == '':
        return redirect('/login')
    user = data_manager.get_user(token)
    amount = data_manager.get_user_kredit_amount(token)
    user_info = data_manager.get_user_informtaion(token)
    print(user._tickets)
    return render_template(
        'tickets.html',
        AVALIABLE_AMOUNT = int(amount),
        PRICE = EVENT_INFO.PRICE_PER_PERSON,
        NICKNAME = user_info['nickname'],
        TICKETS = user._tickets,
        STATUS = data_manager.ticket_status,
        STATUS_TO_STRING = TICKET_STATUS.STATUS_MESSAGE,
        SERVER_ADDRESS = 'https://ticket.keeer.net'
    )


