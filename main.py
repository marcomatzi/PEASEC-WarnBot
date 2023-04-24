import configparser
import tkinter as tk

import UI
from telegram_api import TelegramBot
from collector import Collector
import logging
from UI import App
import asyncio      # Used for API and UI parallel
import threading    # Used for API and UI parallel
telegram_api = None

def main():
    global telegram_api
    config = configparser.ConfigParser()
    config.read("config.ini")
    config_telegram = config["TelegramAPI"]

    telegram_api = config_telegram["KEY"]
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    bot = TelegramBot(telegram_api, app)

    last_update_id = None
    while True:
        # Updates im Chat des Bots
        updates = bot.get_updates(last_update_id)
        if updates and len(updates["result"]) > 0:
            bot.process_updates(updates)
            last_update_id = updates["result"][-1]["update_id"] + 1
        else:
            last_update_id = None

        # Updates im json der Warn-API / DB

def start_collector():
    config = configparser.ConfigParser()
    config.read("config.ini")
    config_db = config["Datenbank"]
    config_warn = config["WarnAppsAPI"]
    server = config_warn['NINA']
    db = config_db['PATH']
    c = Collector(server, db)
    c.catch_warnings(None)


def start_function_thread():
    thread_telegram_api = threading.Thread(target=main)
    thread_collector = threading.Thread(target=start_collector)
    #thread_gui = threading.Thread(target=UI.App.start)

    thread_telegram_api.start()
    thread_collector.start()
    #thread_gui.start()

if __name__ == '__main__':
    #asyncio.run(main())
    app = App(telegram_api)

    start_function_thread()

    app.mainloop()