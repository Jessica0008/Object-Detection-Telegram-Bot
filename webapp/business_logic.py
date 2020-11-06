from glob import glob
import os
import numpy as np
from object_detection.processing import process_picture
from object_detection.cars_counting import detect_all_autos
from webapp.user.models import Defects, CarCounts
from webapp.db import DB as db
from webapp.dl import CARS_RCNN_MODEL, DEFECTS_MODEL, LABEL_ENCODER
from sqlalchemy.sql import func



def detect(filename):
    """ Ищем дефекты """
    print("Ищем дефекты на " + filename)
    result, y_pred = process_picture(DEFECTS_MODEL, LABEL_ENCODER, filename)
    row = Defects(image=filename, object_class=int(y_pred), object_label=result)
    db.session.add(row)
    db.session.commit()
    return result


def get_stats():
    """ Расчет общей статистики """
    asphalt_count = Defects.query.filter(Defects.object_class == 0).count()
    defects_count = Defects.query.filter(Defects.object_class == 1).count()
    other_count = Defects.query.filter(Defects.object_class == 2).count()
    tentity = CarCounts.query.with_entities(func.sum(CarCounts.car_count).label('total')).first()
    total = tentity.total
    query_count = CarCounts.query.count()
    asphalt = f"изображений с асфальтом: {asphalt_count}"
    defect = f"изображений с дефектом: {defects_count}"
    other = f"изображений с посторонним предметом {other_count}"
    cars = f"всего найдено машин: {total} по {query_count} запросам"
    return (cars, asphalt, defect, other, [asphalt_count, defects_count, other_count])


def car_count(filename):
    result = detect_all_autos(CARS_RCNN_MODEL, filename)
    row = CarCounts(image=filename, car_count=result[0], ratio=0.0)
    db.session.add(row)
    db.session.commit()
    return result[1:]