import logging

from flask import Flask, request
from database import db
from app_service import *
from chatbot import ChatBot
from utils import send_message_text
from user_service import get_user_id

import pymysql
pymysql.install_as_MySQLdb()

# A dictionary to store user sessions with their corresponding chatbots
USER_APP_SESSION_MAP = {}

WHATSAPP_NUMBER_APP_MAP = {}

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'mysql://{DB_USERNAME}:{DB_PASSWD}@{DB_HOST}:{DB_PORT}/{DB_WORKING_DATABASE}?ssl_ca=cacert.pem'.format(
        DB_USERNAME=configs.DB_USERNAME,
        DB_PASSWD=configs.DB_PASSWD,
        DB_PORT=configs.DB_PORT,
        DB_HOST=configs.DB_HOST,
        DB_WORKING_DATABASE=configs.DB_WORKING_DATABASE
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_ECHO'] = True
    db.init_app(app)
    return app

app = create_app()


from models import WhatsAppUserInformation


@app.route('/deploy_wa_app', methods=['POST'])
def create_mapping():
    with app.app_context():
        data = request.get_json()
        user_id = data['user_id']
        app_id = data['app_id']
        whatsapp_number = data['whatsapp_number']
        entity = WhatsAppUserInformation(user_id=user_id, app_id=app_id, whatsapp_number=whatsapp_number)
        db.session.add(entity)
        db.session.commit()
        return "Success", 200


@app.route('/message', methods=['POST'])
def twilio_message():
    form_data = request.form
    from_whatsapp_number = form_data['From'].split("whatsapp:")[-1]
    to_whatsapp_number = form_data['To'].split("whatsapp:")[-1]
    message_content = form_data['Body']
    logging.info("get message from twilio: %s", {"From": from_whatsapp_number,
                                                 "To": to_whatsapp_number,
                                                 "message_content": message_content})
    if message_content.startswith("/"):
        if message_content == "/show_all_bots":
            WHATSAPP_NUMBER_APP_MAP[to_whatsapp_number] = {}
            # show all app to user
            app_botname_map = {}
            try:
                app_botname_map = get_user_app(to_whatsapp_number)
            except:
                app_botname_map = {}
                send_message_text(from_whatsapp_number, "I encountered some error.")
                return 'Error while querying database', 500
            reply_content = "Select an app you want to use: \n"
            i = 1
            for app_id, botname in app_botname_map.items():
                reply_content += "Reply /app_{sq} to use app [{botname}]\n".format(
                    sq=i, botname=botname)
                WHATSAPP_NUMBER_APP_MAP[to_whatsapp_number]["app_{sq}".format(sq=i)] = (app_id, botname)
                i += 1
            send_message_text(from_whatsapp_number, reply_content)
        elif message_content == "/main":
            try:
                app_botname_map = get_user_app(to_whatsapp_number)
                if len(app_botname_map) > 0:
                    reply_content = generate_choice_content(to_whatsapp_number, app_botname_map)
                    send_message_text(from_whatsapp_number, reply_content)
                    return 'Success', 200
                else:
                    send_message_text(from_whatsapp_number, "There are no available app now...")
                    return 'There are no available app now...', 200
            except:
                send_message_text(from_whatsapp_number, "I encountered some error.")
                return 'Error while querying database', 500
        else:
            (app_id, botname) = WHATSAPP_NUMBER_APP_MAP[to_whatsapp_number].get(message_content[1:])
            if botname:
                app_detail = get_app_detail(app_id)
                logging.info("get user_id: {}", app_detail["app_info"]["user_id"])
                logging.info("get kb_id: {}", app_detail["app_info"]["kb_id"])
                chatbot: ChatBot = ChatBot(app_detail["app_info"]["user_id"], app_id, app_detail["app_info"]["kb_id"],
                                           from_whatsapp_number, app_detail)
                USER_APP_SESSION_MAP[from_whatsapp_number] = chatbot
                reply_message = "Let's start the chat :)"
                return send_message_text(from_whatsapp_number, reply_message)
            else:
                reply_message = "Wrong option. Please select a chatbot in the list."
                send_message_text(from_whatsapp_number, reply_message)
    elif not from_whatsapp_number in USER_APP_SESSION_MAP:
        try:
            app_botname_map = get_user_app(to_whatsapp_number)
            if len(app_botname_map) > 0:
                reply_content = generate_choice_content(to_whatsapp_number, app_botname_map)
                logging.info("The WHATSAPP_NUMBER_APP_MAP is: %s", WHATSAPP_NUMBER_APP_MAP)
                send_message_text(from_whatsapp_number, reply_content)
                return 'Success', 200
            else:
                send_message_text(from_whatsapp_number, "There are no available app now...")
                return 'There are no available app now...', 200
        except:
            send_message_text(from_whatsapp_number, "I encountered some error.")
            return 'Error while querying database', 500
    else:
        # It's an existing session
        chatbot: ChatBot = USER_APP_SESSION_MAP.get(from_whatsapp_number)
        # Get the message
        # Send the message to the chatbot and get reply
        chatbot.proccess_message(from_whatsapp_number, message_content)
        return "", 200
    return "", 200


def generate_choice_content( to_whatsapp_number, app_botname_map):
    WHATSAPP_NUMBER_APP_MAP[to_whatsapp_number] = {}
    reply_content = "Select an app you want to use: \n"
    if len(app_botname_map) <= 5:
        i = 1
        for app_id, botname in app_botname_map.items():
            reply_content += "Reply /app_{sq} to use app [{botname}]\n".format(
                sq=i, botname=botname)
            WHATSAPP_NUMBER_APP_MAP[to_whatsapp_number]["app_{sq}".format(sq=i)] = (app_id, botname)
            i += 1
    else:
        logging.info("app_botname_map: {}", app_botname_map)
        i = 1
        for app_id, botname in app_botname_map.items():
            reply_content += "Reply /app_{sq} to use app [{botname}]\n".format(
                sq=i, botname=botname)
            WHATSAPP_NUMBER_APP_MAP[to_whatsapp_number]["app_{sq}".format(sq=i)] = (app_id, botname)
            i += 1
            if i > 5:
                reply_content += "Reply /show_all_bots to show all App.\n"
                break
    reply_content += "\nEnd."
    return reply_content


def get_user_app(user_wa_number):
    app_botname_map = {}
    try:
        # user_app_list: list[WhatsAppUserInformation] = WhatsAppUserInformation.query.filter_by(
        #     whatsapp_number=user_wa_number).all()
        # Store botnames in a list

        # get all app from my app API
        # user_service.get_user_id(user_wa_number)
        userid = get_user_id(user_wa_number)
        if not userid:
            logging.info("Cannot find user_id of Whatsapp number %s", user_wa_number)
            return app_botname_map
        app_list = get_user_app_list(userid)
        for app in app_list:
            app_botname_map[app["app_id"]] = app["app_name"]
    except:
        raise Exception("Error while querying database")
    return app_botname_map


# Function to generate button objects for the response
def generate_buttons(app_botname_map: dict):
    buttons = []
    for app_id, botname in app_botname_map.items():
        button = {
            "type": "reply",
            "reply": {
                "id": app_id,
                "title": botname,
            }
        }
        buttons.append(button)
    return buttons


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5002)
