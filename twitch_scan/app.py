import json

import requests
import os
import sendslack


def lambda_handler(event, context):
    # 前の状態取得
    before_s = getStatus()
    after_s = getTwitchStatus()
    before_s = before_s == 'true' or before_s == True

    if before_s == after_s:
        return {
            'status': 'no_change'
        }
    
    setStatus(after_s)

    if after_s:
        message = '配信始めた\nhttps://www.twitch.tv/yamada_ai_'
        sendslack.send_slack(message)
    else:
        message = '配信やめた\nhttps://www.twitch.tv/yamada_ai_'
        sendslack.send_slack(message)

    return {
        'status': 'change'
    }

# 前状態を取得
def getStatus():
    query = os.getenv('query')
    uri = os.getenv('GAS_API_ENDPOINR') + query
    try:
        response = getRequest(uri).text
    except:
        return None

    return response

# 状態をセット
def setStatus(status):
    uri = os.getenv('GAS_API_ENDPOINR')
    data = {
        'status': status
    }
    try:
        requests.post(uri, json=data)
    except:
        return None
    
    return None

# Twitchの上京を取得
def getTwitchStatus():
    client_id = os.getenv('client_id')
    authorization = 'Bearer ' + os.getenv('authorization')
    query = os.getenv('query')
    uri = os.getenv('TWITCH_API_STATUS') + query
    header={
        'Client-ID': client_id,
        'Authorization': authorization
    }
    try:
        response = getRequest(uri, header).json()['data'][0]['is_live']
    except:
        return None

    return response

# GETリクエスト投げる
def getRequest(uri, header = {}):
    try:
        response = requests.get(uri, headers=header)
    except Exception as e:
        print(e)
        return None

    return response
