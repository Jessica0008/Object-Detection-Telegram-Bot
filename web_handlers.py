from glob import glob
import os
import numpy as np
import settings
from pymongo import MongoClient
from object_detection.db import save_detected_defects, save_car_counts, defects_stat, cars_stat
from object_detection.processing import process_picture

CLIENT = MongoClient(settings.MONGO_LINK)
DB = CLIENT["testdb"]


def detect_defects(filename):
    print("Ищем дефекты на " + filename)
    # result, y_pred = process_picture(filename)
    # save_detected_defects(DB, "web_user", y_pred, result)
    return "дефект"


def get_stats():
    """ Расчет общей статистики """
    results = defects_stat(DB)
    total = cars_stat(DB)
    text = "\n изображений с асфальтом: " + str(results[0])
    text += "\n изображений с дефектом: " + str(results[1])
    text += "\n изображений с посторонним предметом: " + str(results[2])
    text += "\n всего машин: " + str(total)
    return text


def count_cars(filename):
    save_car_counts(db, "web_user", np.random.randint(15), 0.0)
    return "всего машин 7"