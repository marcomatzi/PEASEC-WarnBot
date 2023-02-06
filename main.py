import tkinter as tk

import UI
from telegram_api import TelegramBot
import logging
from UI import App
import asyncio      # Used for API and UI parallel
import threading    # Used for API and UI parallel


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    bot = TelegramBot("5979163637:AAFsR0MwfvPb9FwB2oPQKPQJlnkmkcZmKmg", app)

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

def start_function_thread():
    thread_telegram_api = threading.Thread(target=main)
    #thread_gui = threading.Thread(target=UI.App.start)

    thread_telegram_api.start()
    #thread_gui.start()

if __name__ == '__main__':
    #asyncio.run(main())
    app = App()

    start_function_thread()

    app.mainloop()