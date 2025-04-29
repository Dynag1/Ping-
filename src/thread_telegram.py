# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass
import requests
import json
from src import db


def main(message):
    variables = db.lire_param_mail()
    chat_id1 = variables[5]
    id1 = chat_id1.split(",")
    for id in id1:
        send_telegram_message(message, id)


def send_telegram_message(message, chat_id):
    api = "5584289469:AAHYRhZhDCXKE5l1v1UbLs-MUKGPoimMYAQ"
    responses = {}
    proxies = None
    headers = {'Content-Type': 'application/json',
               'Proxy-Authorization': 'Basic base64'}
    data_dict = {'chat_id': chat_id,
                 'text': message,
                 'parse_mode': 'HTML',
                 'disable_notification': False}
    data = json.dumps(data_dict)
    url = f'https://api.telegram.org/bot{api}/sendMessage'
    try:
        responses = requests.post(url,
                                     data=data,
                                     headers=headers,
                                     proxies=proxies,
                                     verify=False)
    except Exception as inst:
        print((inst))
        responses = "un problème est survenu"
        pass
    return responses

