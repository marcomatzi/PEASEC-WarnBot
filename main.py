from telegram_api import TelegramBot


def reply_func(text):
    # Implement your reply logic here
    return 'Automatic reply: ' + text

bot = TelegramBot('KEY')
bot.run(reply_func)