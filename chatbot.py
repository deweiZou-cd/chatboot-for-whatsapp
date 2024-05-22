import json
import logging
import time
from typing import List

import requests
import websocket

from configs import CONVERSATION_PLUGIN_MAP
from utils import send_message_text


def analysis_report_message_parse(response):
    """
    Based on the information provided, the AI model is not explicitly mentioned. However, if we are to analyze the financial health of the company in question, which seems to be a web3 project with a team of experienced engineers and entrepreneurs, we can use the financial data provided to assess its current status.\n\nKey Financial Health Indicators:\n\n1. Debt Ratio: At 0.529412, this indicates that the company has more assets than liabilities, which is a positive sign.\n\n2. Current Ratio: The current ratio of 0.818182 suggests that the company may struggle to meet its short-term obligations with its current assets.\n\n3. Working Capital: Positive working capital of $2,000 indicates the company can cover its short-term liabilities, but the amount is relatively small.\n\n4. Assets-to-Equity Ratio: An A/E ratio of 2.125 shows the company is using more than twice the amount of its equity to finance its assets, which could indicate higher leverage.\n\n5. Debt-to-Equity Ratio: A D/E ratio of 1.125 suggests the company has a moderate level of debt compared to its equity.\n\n6. Net Profit Margin: A negative net profit margin of -0.160526 indicates the company is not profitable as of 2023.\n\n7. ROA and ROE: Both ROA (-1.794118) and ROE (-3.8125) are negative, showing poor return on assets and equity, respectively.\n\n8. Gross Profit Margin: A GPM of 0.736842 is healthy, indicating the company retains a good portion of sales after covering the cost of goods sold.\n\n9. Monthly Burn Rate: At -$2,541.67, the company is losing this amount each month.\n\n10. Runway: With a runway of 1.57377 months, the company has a very short time before it runs out of cash if it doesn't change its burn rate or increase its cash balance.\n\nOverall, the company is

    AI Insight

    As a VC analyzing this web3 company, the financials suggest significant risk. The negative net profit margin and short cash runway indicate immediate action is needed to avoid insolvency. The healthy gross profit margin shows potential if costs are managed better. The negative ROA and ROE are concerning, reflecting poor asset and equity management. The moderate debt-to-equity ratio is a silver lining, suggesting some leverage but not excessive. The company's future hinges on its ability to quickly reduce its burn rate, possibly through cost-cutting, efficiency improvements, or pivoting its business model, while seeking additional capital to extend its runway and achieve profitability.
    :param response:
    :return:
    """
    data = json.loads(response.text)['data']
    if data:
        return "\n\nAI Insight\n\n".join(data.values())
    else:
        return "This question is too difficult for me to answer"


def semantic_search_parser(response) -> List[List]:
    data = json.loads(response.text)['data']
    if data:
        results = []
        for i, liner in enumerate(data.split("|\n| ![PDF Icon]")):
            if i > 0:
                results.append([val for val in liner.split("|") if val != "\n"])
        return results
    else:
        return [[' (null) ', ' None ', "This question is too difficult for me to answer"]]


class ChatBot:

    def __init__(self, owner_id, app_id, kb_id, from_wa_number, app_detail):
        self.owner_id = owner_id
        self.app_id = app_id
        self.kb_id = kb_id
        self.session_id = from_wa_number.replace('+', '') + '-' + str(time.time_ns())
        self.app_detail = app_detail
        self.plugin_name = app_detail["app_info"]["plugin_name"]
        if not self.plugin_name in CONVERSATION_PLUGIN_MAP:
            raise Exception("Cannot indentify plugin %s".format(self.plugin_name))


    def deduct_points(self, owner_id, app_id):
        pass


    def proccess_message(self, from_whatsapp_number, message):
        if CONVERSATION_PLUGIN_MAP[self.plugin_name][0] == "WEBSOCKET":
            return self.proccess_message_ws(from_whatsapp_number, message)
        else:
            return self.proccess_message_api(from_whatsapp_number, message)

    def proccess_message_ws(self, from_whatsapp_number, message):
        data = {
            "question": message,  # The user's message/question
            "user_id": self.owner_id,  # ID of the user
            "session_id": self.session_id,  # ID of the session
            "kb_id": self.kb_id,  # ID of the knowledge base
            "app_id": self.app_id,  # ID of the application
            "plugin_config": ""
        }

        # websocket.enableTrace(True)  # Enable WebSocket tracing
        ws = websocket.WebSocket()  # Create a WebSocket object
        ws_address = self.app_detail["app_info"]["plugin_meta_data"]["chatbox_websocket"]["request_url"]
        ws.connect(ws_address)  # Connect to the specified WebSocket URL

        # Send data to the WebSocket server
        ws.send(json.dumps(data))

        # Receive the response from the WebSocket server
        def get_reply() -> str:
            while True:
                dt = ws.recv()
                d = json.loads(dt)
                if d["type"] == "end":
                    break
                else:
                    res = d["message"]
            return res
        reply_msg = get_reply()
        logging.info("the reply message from [websocket]: %s", reply_msg)
        send_message_text(from_whatsapp_number, reply_msg)
        send_message_text(from_whatsapp_number, "Reply /main if you want to choose a new app.")

        # Close the WebSocket connection
        ws.close()

        # return result  # Return the received result from the WebSocket server

    def proccess_message_api(self, from_whatsapp_number, message):
        data_api = self.app_detail["app_info"]["plugin_meta_data"]["data_api"]
        request_url = data_api["request_url"]
        headers = {
            "Content-Type": "application/json",
            "accept": "application/json"
        }
        data = {
            'keyword': message,
            'kb_id': self.app_detail["app_info"]["kb_id"],
            'app_id': self.app_id,
            'user_id': self.owner_id,
            'plugin_config': self.app_detail["app_info"]["plugin_config"]
        }
        response = requests.post(request_url, headers=headers, json=data)
        if self.plugin_name == "Analysis Report":
            reply_msg = analysis_report_message_parse(response)
            reply_msg += "\n\nReply /main if you want to choose a new app."
            logging.info("the reply message from [Analysis Report] data_api is: %s", reply_msg)
            send_message_text(from_whatsapp_number, reply_msg)
            return reply_msg
        elif self.plugin_name == "Semantic Search Citation Finder":
            reply_msg_list = semantic_search_parser(response)
            logging.info("the reply message from [Semantic Search Citation Finder] data_api is: %s", reply_msg_list)
            for i, l in enumerate(reply_msg_list):
                reply_msg = "Chunk {seq}:\n{body}\n".format(seq=i+1, body=l[2])
                send_message_text(from_whatsapp_number, reply_msg)
            send_message_text(from_whatsapp_number, "Reply /main if you want to choose a new app.")
            return reply_msg_list
        elif self.plugin_name == "Semantic Search Document Summariser":
            reply_msg_list = semantic_search_parser(response)
            logging.info("the reply message from [Semantic Search Document Summariser] data_api is: %s", reply_msg_list)
            for i, l in enumerate(reply_msg_list):
                reply_msg = "Chunk {seq}:\n{body}\n".format(seq=i+1, body=l[2])
                send_message_text(from_whatsapp_number, reply_msg)
            send_message_text(from_whatsapp_number, "Reply /main if you want to choose a new app.")
            return reply_msg_list
        elif self.plugin_name == "Semantic Search Citation Finder Llama":
            reply_msg_list = semantic_search_parser(response)
            logging.info("the reply message from [Semantic Search Citation Finder Llama] data_api is: %s", reply_msg_list)
            for i, l in enumerate(reply_msg_list):
                reply_msg = "Chunk {seq}:\n{body}\n".format(seq=i+1, body=l[2])
                send_message_text(from_whatsapp_number, reply_msg)
            send_message_text(from_whatsapp_number, "Reply /main if you want to choose a new app.")
            return reply_msg_list
        elif self.plugin_name == "Semantic Search Document Summariser Llama":
            reply_msg_list = semantic_search_parser(response)
            logging.info("the reply message from [Semantic Search Document Summariser Llama] data_api is: %s", reply_msg_list)
            for i, l in enumerate(reply_msg_list):
                reply_msg = "Chunk {seq}:\n{body}\n".format(seq=i+1, body=l[2])
                send_message_text(from_whatsapp_number, reply_msg)
            send_message_text(from_whatsapp_number, "Reply /main if you want to choose a new app.")
            return reply_msg_list
        send_message_text(from_whatsapp_number, "not implemented yet")
        return "not implemented yet"

