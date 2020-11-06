from glob import glob
from utils import main_keyboard, send_picture, get_picture, give_menu
import os
import numpy as np
import settings
from pymongo import MongoClient
from db import get_or_create_user, save_detected_defects, save_car_counts
from db import defects_stat, cars_stat
from processing import process_picture
from cars_counting import detect_all_autos
from dl import CARS_RCNN_MODEL, DEFECTS_MODEL, LABEL_ENCODER

CLIENT = MongoClient(settings.MONGO_LINK)
DB = CLIENT["testdb"]


def detect_defects(update, context):
    user = get_or_create_user(DB, update.effective_user, update.message.chat.id)
    os.makedirs("downloads", exist_ok=True)
    if 'last_image' not in context.user_data:
        update.message.reply_text("Загрyзите изображение")
        return
    # send_picture(update=update, context=context, picture_filename=file_name)
    print("Ищем дефекты на " + context.user_data['last_image'])
    result, y_pred = process_picture(DEFECTS_MODEL, LABEL_ENCODER, context.user_data['last_image'])
    save_detected_defects(DB, update.effective_user.id, y_pred, result, img_name = context.user_data['last_image'])
    print(result)
    update.message.reply_text("Это " + result)


def get_stats(update, context):
    results = defects_stat(DB)
    total = cars_stat(DB)
    text = f"""изображений с асфальтом: {results[0]}
    изображений с дефектом: {results[1]}
    изображений с посторонним предметом: {results[2]}
    всего машин: {total}"""
    update.message.reply_text(text)


def count_cars(update, context):
    update.message.reply_text("Пожалуйста подождите - идет обработка")
    user = get_or_create_user(DB, update.effective_user, update.message.chat.id)
    os.makedirs("downloads", exist_ok=True)
    if 'last_image' not in context.user_data:
        update.message.reply_text("Загрyзите изображение")
        return
    print("Ищем машины на " + context.user_data['last_image'])
    car_count, msg, out_file = detect_all_autos(CARS_RCNN_MODEL, context.user_data['last_image'])
    save_car_counts(DB, update.effective_user.id, car_count, 0.0, img_name = context.user_data['last_image'])
    chat_id = update.effective_chat.id
    with open(out_file, 'rb') as img:
        context.bot.send_photo(chat_id=chat_id, photo=img)
    update.message.reply_text(msg)
    

def start(update, context):
    update.message.reply_text("Hello")
