from config import config
from flask import Flask
import waitress


server = Flask(__name__)


from account.account_blueprint import account_blueprint
from index.index_blueprint import index_blueprint
from buy_ticket.buy_blueprint import buy_blueprint
from tickets.ticket_blueprint import ticket_blueprint
from admin.admin_blueprint import admin_blueprint

server.register_blueprint(account_blueprint)
server.register_blueprint(index_blueprint)
server.register_blueprint(buy_blueprint)
server.register_blueprint(ticket_blueprint)
server.register_blueprint(admin_blueprint)

if __name__ == '__main__':
    if config['server']['debug'] == 'True':
        server.run(
            host = config['server']['host'],
            port = config['server']['port'],
            debug = True
        )
    else:
        waitress.serve(
            server,
            host = config['server']['host'],
            port = config['server']['port']
        )