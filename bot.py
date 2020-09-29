from settings import API_KEY, PROXY_PASSWORD, PROXY_URL, PROXY_USERNAME
from handlers import greet_user
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
import logging
from glob import glob
from random import randint, choice  



PROXY = {'proxy_url': PROXY_URL,
        'urllib3_proxy_kwargs': {
        'username': PROXY_USERNAME,
        'password': PROXY_PASSWORD
    }
}

def main():
    # Создаем бота и передаем ему ключ для авторизации на серверах Telegram
    mybot = Updater(API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))

    # Командуем боту начать ходить в Telegram за сообщениями
    mybot.start_polling()
    # Запускаем бота, он будет работать, пока мы его не остановим принудительно
    mybot.idle()

if __name__ == "__main__":
    main()
