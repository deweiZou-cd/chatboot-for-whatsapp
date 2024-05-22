# Standard library import
import logging
# Third-party imports
from typing import List

from twilio.rest import Client

import configs

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = configs.TWILIO_ACCOUNT_SID
auth_token = configs.TWILIO_AUTH_TOKEN
client = Client(account_sid, auth_token)
twilio_number = configs.TWILIO_NUMBER

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Sending message logic through Twilio Messaging API
def send_message_text(to_number, body_text: str):
    def split_string(input_string, chunk_size=1600) -> List[str]:
        result = []
        current_chunk = ""
        current_length = 0
        for char in input_string:
            current_chunk += char
            current_length += 1
            if current_length == chunk_size:
                result.append(current_chunk)
                current_chunk = ""
                current_length = 0
        if current_chunk:
            result.append(current_chunk)
        return result

    logger.info("Sending the response to this number: %s", to_number)
    try:
        body_text_list = split_string(body_text)
        for text in body_text_list:
            message = client.messages.create(
                from_=f"whatsapp:{twilio_number}",
                body=text,
                to=f"whatsapp:{to_number}"
            )
            logger.info(f"Message sent to {to_number}: {message.body}")
    except Exception as e:
        logger.error(f"Error sending message to {to_number}: {e}")

