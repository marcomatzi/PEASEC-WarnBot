from telegram_api import TelegramBot
import logging

"""def reply_func(text):
    # Implement your reply logic here
    return 'Automatic reply: ' + text

bot = TelegramBot('5979163637:AAFsR0MwfvPb9FwB2oPQKPQJlnkmkcZmKmg')
# root = tk.Tk()
# app = Application(master=root)
# app.update_listbox("Starting bot...")
# app.mainloop()
bot.run(reply_func)"""


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    bot = TelegramBot("KEY")

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


if __name__ == '__main__':
    main()
