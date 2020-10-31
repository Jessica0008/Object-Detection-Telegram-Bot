from glob import glob
import os
import numpy as np
import settings
from pymongo import MongoClient
from object_detection.db import save_detected_defects, save_car_counts, defects_stat, cars_stat
from object_detection.processing import process_picture

CLIENT = MongoClient(settings.MONGO_LINK)
DB = CLIENT["testdb"]


def detect(filename):
    print("Ищем дефекты на " + filename)
    result, y_pred = process_picture(filename)
    save_detected_defects(DB, "web_user", y_pred, result)
    return result


def get_stats():
    """ Расчет общей статистики """
    results = defects_stat(DB)
    total = cars_stat(DB)
    asphalt_count = results[0]
    defect_count = results[1]
    other_obj_count = results[2]
    text = f"""
    изображений с асфальтом: {asphalt_count}
    изображений с дефектом: {defect_count}
    изображений с посторонним предметом: {other_obj_count}
    всего машин: {total}"""
    return text


def count(filename):
    save_car_counts(DB, "web_user", np.random.randint(15), 0.0)
    return "всего машин 1"