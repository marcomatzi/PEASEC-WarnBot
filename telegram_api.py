import requests
import logging
import json

from db_functions import Database
from users import Users
from datetime import datetime


class TelegramBot:
    def __init__(self, token, app):
        self.token = token
        # self.url = f"https://api.telegram.org/bot{token}/"
        self.offset = 0
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.logger = logging.getLogger(__name__)
        self.ui = app

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
    def send_multiple_message(self, text, where=None):
        db = Database()
        userlist = db.get_query("users", where)
        liste = []
        for e in userlist:
            tmp = [e[2], e[5]]  # Zwischenspeichern von name und chat_id
            liste.append(tmp)  # In eine neue Liste einfügen, die nur name und chat_id beinhaltet

        print(liste)

        if (len(liste) > 0):
            for u in liste:
                print(str(u[1]) + ": " + text)
                self.send_message(u[1], text)

        return userlist

    def send_message(self, chat_id, text, quickreply=None):
        now = datetime.now()
        current_time = now.strftime("%d-%m-%Y %H:%M:%S")

        keyboard = {
            "inline_keyboard": [
                [{"text": "Help", "callback_data": "button1"}],
                [{"text": "count_users", "callback_data": "button2"}],
            ]
        }
        keyboard_json = json.dumps(keyboard)
        if quickreply != None:
            params = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "html",
                "reply_markup": keyboard_json
            }
        else:
            params = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "html",
            }
        response = requests.post(f"{self.base_url}/sendMessage", json=params)
        self.ui.insert_send_msg("[{} to {}] {}".format(current_time, chat_id, text))
        if response.status_code == 200:
            self.logger.info("Message sent successfully to chat %s", chat_id)
        else:
            self.logger.error("Failed to send message to chat %s: %s", chat_id, response.text)


    def send_warnings(self):
        db = Database()
        list_of_users = db.get_users("name like 'marco'")

        print(list_of_users)


    def analyse_message(self, user_name, chat_id, text):
        if text == "/start":
            arr_start = ["Hallo <b>" + user_name + "</b>!\n" \
                                             "Der PEASEC Warnbot ist ein Krisenmanagement-Tool für öffentliche Warnungen " \
                                                "über Telegram-Nachrichten. Dieser Bot sendet automatische Hochwasserwarnungen, " \
                                                "Unwetterwarnungen, Polizeimeldungen, Mowas, Biwapp und Katwarn Meldungen in Echtzeit über den öffentlichen " \
                                                "Telegram-Nachrichtenkanal an Sie. Mit diesem Warn-Bot erhalten Sie " \
                                                "automatische Benachrichtigungen über öffentliche Notfälle in Deutschland.\n " \
                                                "Mit <b>/help</b> werden alle Funktionen aufgelistet.",
                         "In den Nächsten Schritten erfolgt die Konfiguration des Bots."]
            return arr_start
        elif text == "/lang":
            return "Bitte teile mir deine Sprache mit. \nOption 1: /lang_de \nOption 2: /lang_en"
        elif text == "/lang_en":
            return "&#9989; Language changed to english! From now on, you will recieve warnings in english (if possible). Otherwise in german."
        elif text == "/lang_de":
            return "&#9989; Sprache wurde auf deutsch gesetzt! Absofort erhalten Sie Warnungen in deutsch."
        elif text == "/stop":
            return "&#9989; Dienst wurde pausiert."
        elif text == "/kuendigen":
            return "&#9989; Sie wurden aus der Datenbank gelöscht. Absofort erhalten Sie keine weiteren Meldungen mehr!\n Hoffentlich bis bald! :)"
        elif text == "/help":
            return "/lang (einstellen der Sprache)\n" \
                   "/stop (Pausieren des Dienstes)\n" \
                   "/kuendigen (Austrag aus dem Dienst)\n" \
                   "/count_users (Zeigt die Anzahl der Nutzende an)\n" \
                   "/disclaimer (Gibt den Disclaimer aus)\n" \
                   "/Notfalltipps (Gibt einige Tipps in Notfällen aus)\n" \
                   "/Quelle (Gibt die Quelle der Warnungen aus)\n" \
                   "bald noch mehr...!"
        elif text == "/count_users":
            return "&#10069; Aktuell sind mir " + str(Database.count_rows("users")) + " aktive Nutzer bekannt. \nHoffentlich wachsen wir noch als Community!!"
        elif text == "/Notfalltipps":
            return "https://nina.api.proxy.bund.dev/api31/appdata/gsb/notfalltipps/DE/notfalltipps.json"
        elif text == "/Quelle":
            return "ALle Warnungen stammen aus der offiziellen NINA API, welche vom Bundesamt für Bevölkerungsschutz gepflegt wird. Alle übermittelten Warnungen, werden ungefiltert über diesen Bot verbreitet."
        elif text == "/disclaimer":
            return "&#128679; Folgt."
        else:
            return "&#10060; Fehler: Diese Nachricht konnte nicht verarbeitet werden. Möglicherweise wurde ich nicht für die gewünschte Aktion entwickelt. \n \n Mit <b>/help</b> werden alle Funktionen angezeigt."

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

            if "callback_query" in update:
                callback_data = update["callback_query"]["data"]
                user_id = update["callback_query"]["message"]["from"]["id"]
                chat_id = update["callback_query"]["message"]["chat"]["id"]
                fname = update["callback_query"]["message"]["from"]["first_name"]
                text = "&#10060; Unknown.."
                if callback_data == "button1":
                    text = "/help"

            message = update.get("message")
            if message:
                user_id = message["from"]["id"]
                chat_id = message["chat"]["id"]
                fname = message["from"]["first_name"]
                u = Users(user_id)

                if u.check_user(user_id):
                    self.logger.warning("[User Warning] User muss angelegt werden!")
                    userdata = [
                        user_id,
                        message["from"]["first_name"],
                        chat_id
                    ]
                    u.new_user(userdata)
                if "text" in message:
                    text = message["text"]

            now = datetime.now()
            current_time = now.strftime("%d-%m-%Y %H:%M:%S")
            # self.ui.sidebar_button_event("[{}] UID {} in chat {}: \n    {}".format(current_time, user_id, chat_id, text))
            self.ui.insert_update("[{}] {}".format(current_time, text))

            self.logger.info("Received message from user %s in chat %s: %s", user_id, chat_id, text)
            msg = self.analyse_message(fname, chat_id, text)
            # TODO: Delete DEV Abfrage
            if (chat_id == 784506299):
                if isinstance(msg, list):
                    for m in msg:
                        self.ui.insert_send_msg("[{} to {}] {}".format(current_time, chat_id, m))
                        self.send_message(chat_id, m, True)
                else:
                    self.ui.insert_send_msg("[{} to {}] {}".format(current_time, chat_id, msg))
                    self.send_message(chat_id, msg)
