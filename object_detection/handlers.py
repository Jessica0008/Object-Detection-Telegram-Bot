from glob import glob
from random import choice
import os
import numpy as np
import settings
from utils import main_keyboard, send_picture
from pymongo import MongoClient
from db import get_or_create_user, save_detected_defects, save_car_counts
from db import defects_stat, cars_stat

CLIENT = MongoClient(settings.MONGO_LINK)
DB = CLIENT["testdb"]


def give_menu(update, context):
    update.message.reply_text( f'Hello, user', reply_markup=main_keyboard() )


def count_cars(update, context):
    user = get_or_create_user(DB, update.effective_user, update.message.chat.id)
    update.message.reply_text("Считаем машинки")
    save_car_counts(DB, update.effective_user.id, np.random.randint(9), 0.)
    os.makedirs("downloads", exist_ok=True)
    user_photo = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join("downloads", f"{user_photo.file_id}.jpg")
    user_photo.download(file_name)
    send_picture(update=update, context=context, picture_filename="../bot.png")
    pass


def detect_defects(update, context):
    user = get_or_create_user(DB, update.effective_user, update.message.chat.id)
    print("Ищем дефекты")
    update.message.reply_text("Ищем дефекты")
    save_detected_defects(DB, update.effective_user.id, np.random.randint(2), "")
    os.makedirs("downloads", exist_ok=True)
    user_photo = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join("downloads", f"{user_photo.file_id}.jpg")
    user_photo.download(file_name)
    send_picture(update=update, context=context, picture_filename="../bot.png")


def get_stats(update, context):
    results = defects_stat(DB)
    total = cars_stat(DB)
    text = "\n изображений с асфальтом: " + str(results[0])
    text += "\n изображений с дефектом: " + str(results[1])
    text += "\n изображений с посторонним предметом: " + str(results[2])
    text += "\n всего машин: " + str(total)
    update.message.reply_text(text)
