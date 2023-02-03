import configparser
import requests
import json
import time


class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.url = f"https://api.telegram.org/bot{token}/"
        self.offset = 0

    def get_updates(self):
        params = {'offset': self.offset, 'timeout': 100}
        response = requests.get(self.url + 'getUpdates', params)
        result_json = response.json()
        if result_json['ok']:
            updates = result_json['result']
            self.offset = updates[-1]['update_id'] + 1
            return updates
        else:
            raise Exception('Error getting updates')

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        response = requests.post(self.url + 'sendMessage', params)
        result_json = response.json()
        if not result_json['ok']:
            raise Exception('Error sending message')

    def log_message(self, message, reply):
        with open('log.txt', 'a') as file:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            file.write(f"{current_time}: Message - {message}, Reply - {reply}\n")

    def run(self, reply_func):
        while True:
            updates = self.get_updates()
            for update in updates:
                message = update.get('message')
                if message:
                    chat_id = message['chat']['id']
                    text = message['text']
                    reply = reply_func(text)
                    self.send_message(chat_id, reply)
                    self.log_message(text, reply)
