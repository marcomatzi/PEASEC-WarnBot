import requests
import logging

import db_functions
from users import Users

class TelegramBot:
    def __init__(self, token):
        self.token = token
        # self.url = f"https://api.telegram.org/bot{token}/"
        self.offset = 0
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.logger = logging.getLogger(__name__)

    """
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
    """

    def get_updates(self, offset=None):
        params = {
            "timeout": 100,
            "offset": offset
        }
        response = requests.get(f"{self.base_url}/getUpdates", params=params)
        if response.status_code == 200:
            return response.json()
        else:
            self.logger.error("Failed to get updates: %s", response.text)
            return None

    """
    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        response = requests.post(self.url + 'sendMessage', params)
        result_json = response.json()
        if not result_json['ok']:
            raise Exception('Error sending message')
    """

    def send_message(self, chat_id, text):
        params = {
            "chat_id": chat_id,
            "text": text
        }
        response = requests.post(f"{self.base_url}/sendMessage", json=params)
        if response.status_code == 200:
            self.logger.info("Message sent successfully to chat %s", chat_id)
        else:
            self.logger.error("Failed to send message to chat %s: %s", chat_id, response.text)

    def analyse_message(self,user_id, chat_id, text):
        if text == "/start":
            return "Hier stehen demnächst alle Infos!\n /help zeigt alle Optionen an."
        elif text == "/lang":
            return "Bitte teile mir deine Sprache mit. \nOption 1: /lang_de \nOption 2: /lang_en"
        elif text == "/lang_en":
            return "Language changed to english! From now on, you will recieve warnings in english (if possible). Otherwise in german."
        elif text == "/lang_de":
            return "Sprache wurde auf deutsch gesetzt! Absofort erhalten Sie Warnungen in deutsch."
        elif text == "/stop":
            return "Dienst wurde pausiert."
        elif text == "/kuendigen":
            return "Sie wurden aus der Datenbank gelöscht. Absofort erhalten Sie keine weiteren Meldungen mehr!\n Hoffentlich bis bald! :)"
        elif text == "/help":
            return "/lang (einstellen der Sprache)\n" \
                   "/stop (Pausieren des Dienstes)\n" \
                   "/kuendigen (Austrag aus dem Dienst)\n" \
                   "/help (Hilfe)"
        elif text == "/count_users":
            return "Aktuell sind mir " + str(db_functions.Database.count_rows("users")) + " aktive Nutzer bekannt. \nHoffentlich wachsen wir noch als Community!!"
        else:
            return "I received your message!"


    """def run(self, reply_func):
        while True:
            updates = self.get_updates()
            for update in updates:
                print(update)
                message = update.get('message')
                if message and 'text' in message:
                    chat_id = message['chat']['id']

                    uid = message['from']['id']
                    u = Users.__init__(uid)
                    userdata = [
                        message['from']['first_name'],
                        message['from']['language_code'],
                        ""                                  # Welche Warnungen sollen gesendet werden? INT 1-x
                    ]
                    u.check_user(uid, userdata)

                    text = message['text']
                    if '/start' in text:
                        text = 'Einleitung coming soon!'
                    reply = reply_func(text)
                    self.send_message(chat_id, reply)
                else:
                    reply = reply_func("Aktuell können nur Text-MSG verarbeitet werden")
                    self.send_message(chat_id, reply)
            time.sleep(5)"""

    def process_updates(self, updates):
        for update in updates["result"]:
            message = update.get("message")
            if message:
                user_id = message["from"]["id"]
                chat_id = message["chat"]["id"]
                u = Users(user_id)

                if u.check_user(user_id):
                    self.logger.warning("[User Warning] User muss angelegt werden!")
                    userdata = [
                        user_id,
                        message["from"]["first_name"],
                        chat_id
                    ]
                    u.new_user(userdata)

                text = message["text"]
                self.logger.info("Received message from user %s in chat %s: %s", user_id, chat_id, text)
                msg = self.analyse_message(user_id, chat_id, text)

                self.send_message(chat_id, msg)
