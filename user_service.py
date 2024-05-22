import logging

from models import WhatsAppUserInformation
def get_user_id(user_wa_number):
    # blocked by implementation of API, return a default value first
    # return "c9a65e38-8d86-426a-8773-5d863cb696c3"
    try:
        user_info = WhatsAppUserInformation.query.filter_by(whatsapp_number=user_wa_number).first()
        if user_info:
            return user_info.user_id
        else:
            return None  # Return None if no user with the specified whatsapp_number is found
    except Exception as e:
        logging.error("Error while getting userid using whatsapp number : %s", e)
        return None