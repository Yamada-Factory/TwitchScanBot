# import urllib
import json
import os
import requests

# webhook url
webhook_url = os.getenv('SLACK_WEBHOOK')
# username
slack_username = os.getenv('SLACK_USERNAME')
avatar_url = os.getenv('SLACK_ICON')

def send_slack(message=''):
    send_data = {
        'username': slack_username,
        'avatar_url': avatar_url,
        'content': message
    }
    header = {
        'Content-Type': 'application/json'
    }

    res = requests.post(webhook_url, json=send_data, headers=header)
    print(res.status_code)

