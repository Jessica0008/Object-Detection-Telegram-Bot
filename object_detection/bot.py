from settings import API_KEY, PROXY_PASSWORD, PROXY_URL, PROXY_USERNAME
from handlers import detect_defects
from utils import give_menu, send_picture, get_picture
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
import logging
from glob import glob
from random import randint, choice


PROXY = {
    "proxy_url": PROXY_URL,
    "urllib3_proxy_kwargs": {"username": PROXY_USERNAME, "password": PROXY_PASSWORD},
}


def main():
    # Создаем бота и передаем ему ключ для авторизации на серверах Telegram
    bot = Updater(API_KEY, use_context=True)

    dp = bot.dispatcher
    # dp.add_handler(CommandHandler("start", give_menu))

    dp.add_handler(MessageHandler(Filters.photo, get_picture))
    # dp.add_handler(MessageHandler(Filters.regex("^(Count Cars)$"), count_cars))
    dp.add_handler(MessageHandler(Filters.regex("^(Detect Defects)$"), detect_defects))

    # Командуем боту начать ходить в Telegram за сообщениями
    bot.start_polling()
    # Запускаем бота, он будет работать, пока мы его не остановим принудительно
    bot.idle()


if __name__ == "__main__":
    main()
