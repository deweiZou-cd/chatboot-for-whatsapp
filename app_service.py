import json
import logging

import requests

import configs

def get_app_detail(app_id) -> dict:
    '''
    :param app_id:
    :return: app_data dict
    '''
    headers = {'x-kb-timestamp': '1690419337',
               'x-kb-sign': 'A4A45B86AF64A3919F32165716CC6EB207C8BCDDBAD8509D999C650DBB3D426F',
               'x-kb-app-id': '100001',
               'Content-Type': 'application/json'
               }
    data = {
        "app_id": app_id
    }
    response = requests.post(url=configs.KB_PLATFORM_URL + configs.KB_APP_DETAIL_PATH, headers=headers, json=data)
    logging.info("response from app details API: {}", response.text)
    resp = json.loads(response.text)
    if resp['return_code'] == 0:
        return resp['data']
    else:
        raise Exception("Error: code %d, message = %s" % (resp['return_code'], resp['return_info']))


def get_user_app_list(user_id) -> list:
    url = configs.KB_PLATFORM_URL + configs.KB_MY_APP_PATH
    headers = {
        'x-kb-timestamp': '1690419337',
        'x-kb-sign': 'A4A45B86AF64A3919F32165716CC6EB207C8BCDDBAD8509D999C650DBB3D426F',
        'x-kb-app-id': '100001',
        'x-kb-user-id': user_id,
        'Content-Type': 'application/json'
    }
    data = {}  # Add your JSON data here
    response = requests.post(url, headers=headers, json=data)
    resp = json.loads(response.content)
    if resp['return_code'] == 0:
        return resp['data']['app_list']
    else:
        raise Exception("Error: code %d, message = %s" % (resp['return_code'], resp['return_info']))
