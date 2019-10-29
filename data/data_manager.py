
import requests
import hashlib
from config import config
import pickle
from data.user import User
from consts import TICKET_STATUS, EVENT_INFO

users = {}
tokens = {}

def load_users_from_file():
    global users
    users = {}
    try:
        with open('objects/users.pkl', 'rb') as fr:
            users = pickle.load(fr)
            fr.close()
    except FileNotFoundError:
        return None

def load_tokens_from_file():
    global tokens
    tokens = {}
    try:
        with open('objects/tokens.pkl', 'rb') as fr:
            tokens = pickle.load(fr)
            fr.close()
    except FileNotFoundError:
        return None     
    
def dump_users_to_file():
    global users
    with open('objects/users.pkl', 'wb') as fw:
        pickle.dump(users, fw)
        fw.close()

def dump_tokens_to_file():
    global tokens
    with open('objects/tokens.pkl', 'wb') as fw:
        pickle.dump(tokens, fw)
        fw.close()

load_tokens_from_file()
load_users_from_file()

def _sign(value, key):
    coder = hashlib.sha512()
    coder.update(bytearray(value+key, encoding='UTF8'))
    return coder.hexdigest()

def new_user(token):
    global tokens, users
    response = requests.post(
        'https://account.keeer.net/api/auth/query_kiuid', 
        data = {
            'token': token,
            'sign': _sign(token, config['server']['keeer_secret_key'])
        },
        headers = {
            'User-agent': 'Chrome/78.0.3904.70'
        }
    )
    if response.status_code != 200:
        raise Exception(response.status_code)
        return False
    response = response.json()
    if response['status'] == 0:
        kiuid = response['result']
        if kiuid not in users:
            user = User.from_file(kiuid)
            user = user if user != None else User(kiuid)
            users.update({kiuid: user})
            dump_users_to_file()
        if token not in tokens:
            tokens.update({token: kiuid})
            dump_tokens_to_file()
        return True
    return False

def get_user_informtaion(token):
    response = requests.post(
        'https://account.keeer.net/api/auth/query_information', 
        data = {
            'token': token
        },
        headers = {
            'User-agent': 'Mozilla/5.0'
        }
    ).json()
    if response['status'] == 0 and response['result']['status'] == 0:
        return response['result']['result']

def get_user_kredit_amount(token):
    response = requests.get(
        'https://account.keeer.net/api/kredit/request?token=%s'%token, 
        headers = {
            'User-agent': 'Mozilla/5.0'
        }
    )

    if response.status_code != 200:
        raise Exception(response.status_code)
        return False
    response = response.json()

    if response['status'] == 0:
        return response['result']

def get_user(token):
    if token not in tokens:
        result = new_user(token)
        if not result:
            return None
    return users.get(tokens.get(token, ''), None)

tickets = []

def load_tickets_from_file():
    global tickets
    try:
        with open('objects/tickets.pkl', 'rb') as fr:
            tickets = pickle.load(fr)
            fr.close()
    except FileNotFoundError:
        # generate ticket
        for i in range(5*60+30,8*60,15):
    	    tickets.append({
                'id': (i-5*60+30)//15,
                'body': {
                    'start_time': '2019 年 11 月 1 日 下午 %d 时 %.2d 分'% (i//60,i%60),
                    'free_position': 25
                }
            })
        dump_tickets_to_file()

def dump_tickets_to_file():
    global users
    with open('objects/tickets.pkl', 'wb') as fw:
        pickle.dump(tickets, fw)
        fw.close()

load_tickets_from_file()

ticket_status = {}

def load_ticket_status_from_file():
    global ticket_status
    try:
        with open('objects/ticket_status.pkl', 'rb') as fr:
            ticket_status = pickle.load(fr)
            fr.close()
    except FileNotFoundError:
        return None

def dump_ticket_status_to_file():
    global ticket_status
    with open('objects/ticket_status.pkl', 'wb') as fw:
        pickle.dump(ticket_status, fw)
        fw.close()

def pay(token, amount):
    response = requests.get(
        'https://account.keeer.net/api/pay?token=%s&amount=%s&sign=%s'%(
            token,
            amount,
            _sign(token, config['server']['keeer_secret_key'])
        ),
        headers = {
            'User-agent': 'Mozilla/5.0'
        }
    )
    if response.status_code != 200:
        raise Exception(response.text,response.status_code)
        return False
    response = response.json()
    if response['status'] == 0:
        return True, '成功'
    return False, response['message']

load_ticket_status_from_file()
import uuid

def buy_ticket(token, id):
    global users, tickets, ticket_status
    for i in range(len(tickets)):
        if tickets[i]['id'] == id:
            if tickets[i]['body']['free_position'] < 1:
                return False, "预约已满"
            current_user = users.get(tokens.get(token), None)
            if current_user == None:
                return False, "用户不存在"
            if int(get_user_kredit_amount(token)) < EVENT_INFO.PRICE_PER_PERSON:
                return False, "Kredit 余额不足"
            payment_result =  pay(token, EVENT_INFO.PRICE_PER_PERSON)
            if payment_result[0] == False:
                return False, payment_result[1]

            tickets[i]['body']['free_position'] -= 1
            ticket_id = str(uuid.uuid1())
            ticket_status.update({ticket_id: TICKET_STATUS.UNUSED})
            current_user.add_ticket({
                "id": ticket_id,
                 "info": tickets[i]['body']['start_time']
            })

            dump_users_to_file()
            dump_tickets_to_file()
            dump_ticket_status_to_file()
            return True, '成功'
        
            
