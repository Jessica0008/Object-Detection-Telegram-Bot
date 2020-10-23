from glob import glob
from utils import main_keyboard, send_picture, get_picture, give_menu
import os
import numpy as np
import settings
from pymongo import MongoClient
from db import get_or_create_user, save_detected_defects, save_car_counts
from db import defects_stat, cars_stat
from processing import process_picture

CLIENT = MongoClient(settings.MONGO_LINK)
DB = CLIENT["testdb"]


def detect_defects(update, context):
    user = get_or_create_user(DB, update.effective_user, update.message.chat.id)
    os.makedirs("downloads", exist_ok=True)
    if 'last_image' not in context.user_data:
        update.message.reply_text("Загрyзите изображение")
        return
    # send_picture(update=update, context=context, picture_filename=file_name)
    print("Ищем дефекты")
    result, y_pred = process_picture(context.user_data['last_image'])
    save_detected_defects(DB, update.effective_user.id, y_pred, result)
    print(result)
    update.message.reply_text("Это " + result)


def get_stats(update, context):
    results = defects_stat(DB)
    total = cars_stat(DB)
    text = "\n изображений с асфальтом: " + str(results[0])
    text += "\n изображений с дефектом: " + str(results[1])
    text += "\n изображений с посторонним предметом: " + str(results[2])
    text += "\n всего машин: " + str(total)
    update.message.reply_text(text)


def count_cars(update, context):
    user = get_or_create_user(DB, update.effective_user, update.message.chat.id)
    save_car_counts(DB, update.effective_user.id, np.random.randn(15), 0.0)
    pass
