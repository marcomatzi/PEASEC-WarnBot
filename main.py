import db_functions
from telegram_api import TelegramBot
import logging
import asyncio
from UI import TelegramBotGUI


async def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    bot = TelegramBot("5979163637:AAFsR0MwfvPb9FwB2oPQKPQJlnkmkcZmKmg")

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
    asyncio.run(main())
