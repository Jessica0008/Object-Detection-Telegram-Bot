from glob import glob
import os
import numpy as np
from webapp.settings import MONGO_LINK
from pymongo import MongoClient
from object_detection.db import save_detected_defects, save_car_counts, defects_stat, cars_stat
from object_detection.processing import process_picture

CLIENT = MongoClient(MONGO_LINK)
DB = CLIENT["testdb"]


def detect(filename):
    print("Ищем дефекты на " + filename)
    result, y_pred = process_picture(filename)
    save_detected_defects(DB, "web_user", y_pred, result)
    return result


def get_stats():
    """ Расчет общей статистики """
    results = defects_stat(DB)
    asp_count = results[0]
    def_count = results[1]
    oth_count = results[2]
    total = cars_stat(DB)
    asphalt = f"изображений с асфальтом: {asp_count}"
    defect = f"изображений с дефектом: {def_count}"
    other = f"изображений с посторонним предметом: {oth_count}"
    cars = f"всего машин: {total}"
    return (asphalt, defect, other, cars)


def count(filename):
    save_car_counts(DB, "web_user", np.random.randint(15), 0.0)
    return "всего машин 1"