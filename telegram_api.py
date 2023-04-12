import requests
import logging
import json

from db_functions import Database
from users import Users
from datetime import datetime
import time

class TelegramBot:
    def __init__(self, token, app):
        self.token = token
        # self.url = f"https://api.telegram.org/bot{token}/"
        self.offset = 0
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.logger = logging.getLogger(__name__)
        self.ui = app

    def get_updates(self, offset=None):
        """
        Ruft die JSON Datei von Telegram ab. Alle neuen Nachrichten werden ausgelesen.
        :param offset: beinhaltet die letzte UpdateID aus der JSON. Damit wird überprüft ob es neue Nachrichten gibt.
        :return: Inhalt von JSON oder None
        """
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

    def send_msg_keyboard(self, chat_id, message, opt_keyboard):
        # Keyboard-Daten im JSON-Format
        """keyboard = {
            "keyboard": [
                ["Option 1", "Option 2"],
                ["Option 3", "Option 4"],
                ["Option 5"]
            ],
            "one_time_keyboard": True,
            "resize_keyboard": True
        }"""
        keyboard = {
            "keyboard": opt_keyboard,
            "one_time_keyboard": True,
            "resize_keyboard": True  # ,
            # 'is_persistent': True
        }
        # Nachricht, die das Keyboard enthält
        # message = "Wählen Sie eine Option aus dem Keyboard"

        # Keyboard als JSON-codierten String
        keyboard_json = json.dumps(keyboard)

        # Parameter für die Telegram API Anfrage
        params = {
            'chat_id': chat_id,
            'text': message,
            'reply_markup': keyboard_json
        }

        # Anfrage an die Telegram-API senden
        response = requests.post(f"{self.base_url}/sendMessage", data=params)

        # Statuscode überprüfen
        if response.status_code == 200:
            print('Keyboard wurde erfolgreich gesendet')
        else:
            print('Es gab ein Problem beim Senden des Keyboards')

    def send_photo(self, chat_id, photo_url, caption=None, parse_mode=None, reply_markup=None,
                   disable_notification=False):
        params = {
            "chat_id": chat_id,
            "photo": photo_url,
            "disable_notification": disable_notification,
        }
        if caption and len(caption) < 1026:
            params["caption"] = caption
        if parse_mode:
            params["parse_mode"] = parse_mode
        if reply_markup:
            params["reply_markup"] = reply_markup

        response = requests.post(f"{self.base_url}/sendPhoto", json=params)

        return response

    def message_replace(self, msg):
        msg = msg.replace("<br/>", "\n")
        msg = msg.replace("<br>", "\n")

        return msg

    def send_message(self, chat_id, text, quickreply=None):
        now = datetime.now()
        current_time = now.strftime("%d-%m-%Y %H:%M:%S")

        """
        NOT USED:
        
        keyboard = {
            "inline_keyboard": [
                [{"text": "Help", "callback_data": "button1"}],
                [{"text": "count_users", "callback_data": "button2"}],
            ]
        }"""

        keyboard_json = json.dumps(quickreply)
        text = self.message_replace(text)
        if quickreply != None:
            params = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "HTML",
                "reply_markup": keyboard_json
            }
        else:
            params = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "HTML",
            }
        response = requests.post(f"{self.base_url}/sendMessage", json=params)
        # self.ui.insert_send_msg("[{} to {}] {}".format(current_time, chat_id, text))
        if response.status_code == 200:
            self.logger.info("Message sent successfully to chat %s", chat_id)
        else:
            self.logger.error("Failed to send message to chat %s: %s", chat_id, response.text)

    def split_text(self, text):
        """
        Teilt einen String in 4000 Zeichen auf, weil die Maximallänge knapp 4000 Zeichen pro Nachricht in Telegram ist!
        :return:
        """
        chunks = []

        split_index = text.rfind(" ", 0, 1025)
        chunks.append(text[:split_index])
        text = text[split_index + 1:]

        while len(text) > 1025:
            split_index = text.rfind(" ", 0, 4000)
            chunks.append(text[:split_index])
            text = text[split_index + 1:]

        chunks.append(text)

        print(chunks)
        return chunks

    def send_warnings(self, wid, version=None, chatid=None, username=None):
        """
        TODO: Sendet warnungen raus -> (1) Bild (2) Text (3) Verhalten (4) weitere Infos und Button mit Url
        Sendet die Warnmeldungen raus
        Verbindet SendMessage und SendImage
        :return:
        """

        if version is None or version == "":
            results = Database.get_query("warning_information", "wid='{}' GROUP BY version".format(wid))
        else:
            results = Database.get_query("warning_information",
                                         "wid='{}' and version={} GROUP BY version".format(wid, version))
        highest_res = results[0]

        if len(results) < 2:
            result = highest_res
        else:
            for r in results:
                if r[2] > highest_res[2]:
                    print("replace")
                    highest_res = r
            result = highest_res

        # Username nutzen als persönliche Anrede
        if username is None:
            warnmeldung_txt = str(result[5]) + ": " + result[8] + "\n\n" + str(
                result[9]) + "\n\n" + "<b>Anweisung:</b> " + str(result[21]) + "<b>Herausgeber:</b> " + str(
                result[7]) + "  (" + str(result[10]) + ")" + "\n" + "<b>Dringlichkeit:</b> " + str(
                result[15]) + "\n" + "<b>Schweregrad:</b> " + str(
                result[16]) + "\n" + "<b>Wahrscheinlichkeit:</b> " + str(
                result[17]) + "\n\n" + "<b>Seit dem:</b> " + str(result[18]) + "\n" + "<b>Bis zum:</b> " + str(
                result[20]) + "\n\n" + "<b>Diese Warnmeldung gilt für :</b> " + str(result[11])
        else:
            warnmeldung_txt = "Hallo " + str(username) + "! Es gibt eine neue Warnmeldung -> \n" + str(result[5]) + ": " + result[8] + "\n\n" + str(
                result[9]) + "\n\n" + "<b>Anweisung:</b> " + str(result[21]) + "<b>Herausgeber:</b> " + str(
                result[7]) + "  (" + str(result[10]) + ")" + "\n" + "<b>Dringlichkeit:</b> " + str(
                result[15]) + "\n" + "<b>Schweregrad:</b> " + str(
                result[16]) + "\n" + "<b>Wahrscheinlichkeit:</b> " + str(
                result[17]) + "\n\n" + "<b>Seit dem:</b> " + str(result[18]) + "\n" + "<b>Bis zum:</b> " + str(
                result[20]) + "\n\n" + "<b>Diese Warnmeldung gilt für :</b> " + str(result[11])

        # Warntext wird auf länge geprüft und ggf. aufgeteilt
        warnmeldung_txt = self.message_replace(warnmeldung_txt)

        if len(warnmeldung_txt) <= 1025:                    # 1025 Chars ist die maximale Anzahl für die Caption eines Fotos.
            if result[10] != "":
                reply_markup = {
                    "inline_keyboard": [
                        [{"text": "%s" % str(result[7]), "url": "%s" % str(result[10]) }]
                    ]
                }
            else:
                reply_markup = None

            if result[13] == "" or result[13] == "None":
                self.send_photo(chatid, "https://cdn.icon-icons.com/icons2/1808/PNG/512/warning_115257.png", warnmeldung_txt, "HTML", reply_markup)
            else:
                self.send_photo(chatid, result[13], warnmeldung_txt, "HTML", reply_markup)

        else:
            warn_msg = self.split_text(warnmeldung_txt)
            print(len(warn_msg))

            i = 0
            for m in warn_msg:
                if result[10] != "":
                    reply_markup = {
                        "inline_keyboard": [
                            [{"text": "%s" % str(result[7]), "url": "%s" % str(result[10]) }]
                        ]
                    }
                else:
                    reply_markup = None

                if i == 0:
                    print("Only img with %s" % reply_markup)
                    if i != len(warn_msg)-1:
                        reply_markup = None

                    if result[13] == "" or result[13] == "None":
                        self.send_photo(chatid, "https://cdn.icon-icons.com/icons2/1808/PNG/512/warning_115257.png", m, "HTML", reply_markup)
                    else:
                        self.send_photo(chatid, result[13], m, "HTML", reply_markup)

                elif i == len(warn_msg)-1:                  # Letzte Nachricht enthält eine Schnellantwort mit der URL
                    self.send_message(chatid, m, reply_markup)
                else:
                    self.send_message(chatid, m)
                i += 1

    def startSetup(self, chatid, username, phase, keyboard=None):
        """
        Startet das Setup des Bots für den gegebenen User. Hierfür wird auch eine Phase übergeben um den Status zu tracken.
        :param userid:
        :param phase:
        :return:
        """
        print("startSetup")
        if phase == 0:
            msg = "Hallo <b>" + username + "</b>!\n" \
                                           "Der PEASEC Warnbot ist ein Krisenmanagement-Tool für öffentliche Warnungen " \
                                           "über Telegram-Nachrichten. Dieser Bot sendet automatische Hochwasserwarnungen, " \
                                           "Unwetterwarnungen, Polizeimeldungen, Mowas, Biwapp und Katwarn Meldungen in Echtzeit über den öffentlichen " \
                                           "Telegram-Nachrichtenkanal an Sie. Mit diesem Warn-Bot erhalten Sie " \
                                           "automatische Benachrichtigungen über öffentliche Notfälle in Deutschland.\n " \
                                           "Mit <b>/help</b> können jederzeit alle Funktionen aufgelistet werden."
            self.send_message(chatid, msg)
            msg = "&#10071; Der Bot speichert folgende Daten:\n" \
                  "-> Ihre Telegram ID (um Sie identifizieren zu können)\n" \
                  "-> Diese Chat-ID (um Warnmeldungen versenden zu können)\n" \
                  "-> Ihren Telegram-Namen (um Persönlicher kommunizieren zu können)\n\n" \
                  "Sollten Sie den Einstellungsprozess fortfahren, stimmen Sie dem Speichern zu. Sie können jederzeit mit /abmelden alle Daten löschen!"
            self.send_message(chatid, msg)
            msg = "In welcher Sprache soll der Bot Warnmeldungen zusenden? Bitte die richtige Option auswählen.."
            msg_keyboard = [
                ["Deutsch", "English"]
            ]

            self.send_msg_keyboard(chatid, msg, msg_keyboard)

        elif phase == 1:
            """
            Phase 1: Auswahl Deutsch
            """
            msg = "&#9989; Sprache wurde auf Deutsch festgelegt. Ab sofort erhalten Sie alle Warnmeldungen auf Deutsch."
            self.send_message(chatid, msg)
            msg = "Schritt 2: Über welche Warnmeldungen soll der Bot Nachrichten senden?\nMehrfachauswahl möglich..\n\nFÜr weitere Informationen können die Webseiten aufgerufen werden durch\n" \
                  "/mowas\n/katwarn\n/biwapp"
            msg_keyboard = [
                ["Unwetterwarnungen (DE)", "Hochwasser"],
                ["Polizeimeldungen", "MoWaS"],
                ["Biwapp", "Katwarn"],
                ["Alle Warnmeldungen (empfohlen)"]
            ]
            self.send_msg_keyboard(chatid, msg, msg_keyboard)


        elif phase == 2:
            """
            Phase 2: Auswahl English
            """
            msg = "&#9989; English was chosen as the language. Unfortunately, this language is not yet fully integrated," \
                  " therefore the warning messages are sent in German."
            self.send_message(chatid, msg)
            msg = "Schritt 2: About which alerts should the bot send messages?\nMultiple selection possible..\nFor more information, the web pages can be accessed by\n" \
                  "/mowas\n/katwarn\n/biwapp"
            msg_keyboard = [
                ["Unwetterwarnungen (DE)", "Hochwasser"],
                ["Polizeimeldungen", "MoWaS"],
                ["Biwapp", "Katwarn"],
                ["Alle Warnmeldungen (empfohlen)"]
            ]
            self.send_msg_keyboard(chatid, msg, msg_keyboard)

    def analyse_message(self, user_name, chat_id, text):
        """
        Prüfung der Nachricht auf Befehle. Es wird nicht auf Beitext geprüft, sondern nur auf reine Befehle.
        Hier werden alle Statischen Antworte definiert und als return ausgegeben.
        :param user_name: String - Der Name des Users (Telegram-Name)
        :param chat_id: Int - Die Chat ID des Users, um Anwtorten senden zu können
        :param text: String - Der Text der Nachricht.
        :return: String
        """
        possible_warnmeldungen_setup = [[1, "Unwetterwarnungen (DE)"], [2, "Hochwasser"], [3, "Polizeimeldungen"],
                                        [4, "MoWaS"], [5, "Biwapp"],
                                        [6, "Katwarn"], [7, "Alle Warnmeldungen (empfohlen)"]]
        if text == "/start":
            self.startSetup(chat_id, user_name, 0)

            """arr_start = ["Hallo <b>" + user_name + "</b>!\n" \
                                                   "Der PEASEC Warnbot ist ein Krisenmanagement-Tool für öffentliche Warnungen " \
                                                   "über Telegram-Nachrichten. Dieser Bot sendet automatische Hochwasserwarnungen, " \
                                                   "Unwetterwarnungen, Polizeimeldungen, Mowas, Biwapp und Katwarn Meldungen in Echtzeit über den öffentlichen " \
                                                   "Telegram-Nachrichtenkanal an Sie. Mit diesem Warn-Bot erhalten Sie " \
                                                   "automatische Benachrichtigungen über öffentliche Notfälle in Deutschland.\n " \
                                                   "Mit <b>/help</b> werden alle Funktionen aufgelistet.",
                         "In den Nächsten Schritten erfolgt die Konfiguration des Bots."]
            return arr_start"""
            return None
        elif text == "Deutsch":
            self.startSetup(chat_id, user_name, 1)
        elif text == "English":
            self.startSetup(chat_id, user_name, 2)
        elif "Unwetterwarnungen" in text:
            msg_keyboard = [
                ["Hochwasser"],
                ["Polizeimeldungen", "MoWaS"],
                ["Biwapp", "Katwarn"],
                ["Alle Warnmeldungen (empfohlen)"]
            ]
            self.send_msg_keyboard(chat_id, "Weitere Warnmeldungsarten?", msg_keyboard)
        elif "Alle Warnmeldungen" in text:
            self.send_message(chat_id,
                              "&#9989; Setup abgeschlossen! \n Das Setup kann jederzeit neu gestartet werden durch /start")

        elif text == "/stop":
            return "&#9989; Dienst wurde pausiert."
        elif text == "/abmelden":
            return "&#9989; Sie wurden aus der Datenbank gelöscht. Ab sofort erhalten Sie keine weiteren Meldungen mehr!\nHoffentlich bis bald!"
        elif text == "/help":
            return "/stop (Pausieren des Dienstes)\n" \
                   "/abmelden (Austrag aus dem Dienst)\n" \
                   "/count_users (Zeigt die Anzahl der Nutzende an)\n" \
                   "/disclaimer (Gibt den Disclaimer aus)\n" \
                   "/Notfalltipps (Gibt einige Tipps in Notfällen aus)\n" \
                   "/Quelle (Gibt die Quelle der Warnungen aus)"
        elif text == "/count_users":
            return "&#10069; Aktuell sind mir " + str(
                Database.count_rows("users")) + " aktive Nutzer bekannt. \nHoffentlich wachsen wir noch als Community!!"
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
        """
        Inhalt der Nachricht aus der Update JSON wird analysiert. Wenn die Narchricht vom Bot verwertet werden kann,
        wird diese beantwortet. Ansonsten wirft der Bot eine Fehlermeldung.
        :param updates: Inhalt der neuen Nachrichten aus der JSON (liste)
        :return:
        """
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
                    # TODO: Setup starten und User durchleiten
                    userdata = [
                        user_id,
                        message["from"]["first_name"],
                        chat_id
                    ]
                    u.new_user(userdata)
                    print("Test")
                    # Startet des Setup, um den User komplett ins System zu integrieren
                    self.startSetup(chat_id, fname, 0)
                    return None

                if "text" in message:
                    text = message["text"]
                else:
                    text = "unknown"

            # Aktuelle Uhrzeit abfragen für LOG
            now = datetime.now()
            current_time = now.strftime("%d-%m-%Y %H:%M:%S")

            # Anzeigen/Einfügen ins UI
            self.ui.insert_update("[{}] {}".format(current_time, text))

            self.logger.info("Received message from user %s in chat %s: %s", user_id, chat_id, text)

            # Textnachricht wird analysiert und gegen bekannte Befehle geprüft
            msg = self.analyse_message(fname, chat_id, text)

            # Wenn es kein return-Wert gibt. Kommt z.B beim Setup vor.
            if msg is None:
                continue
            # Prüfen ob die Antwort eine Reihe von Text ist (aufgeteilt in mehrere Texte)
            if isinstance(msg, list):
                for m in msg:
                    self.ui.insert_send_msg("[{} to {}] {}".format(current_time, chat_id, m))
                    self.send_message(chat_id, m, True)
            else:
                self.ui.insert_send_msg("[{} to {}] {}".format(current_time, chat_id, msg))
                self.send_message(chat_id, msg)
