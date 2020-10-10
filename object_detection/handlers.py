from glob import glob
from random import choice
import os
from utils import main_keyboard, send_picture
from imageai.Detection import ObjectDetection


def give_menu(update, context):
    update.message.reply_text(f"Hello, user", reply_markup=main_keyboard())


def get_picture(update, context):

    update.message.reply_text("Обрабатываю фото")
    os.makedirs("downloads", exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[0].file_id)
    filename = os.path.join("downloads", f"{photo_file.file_id}.jpg")
    photo_file.download(filename)
    update.message.reply_text("Файл сохранен")
    give_menu(update, context)
    return filename


def count_cars(update, context):
    update.message.reply_text("Считаем машинки")
    os.makedirs("downloads", exist_ok=True)
    list_of_files = glob(
        "downloads/*.jpg"
    )  # * means all if need specific format then *.csv
    input_file = max(list_of_files, key=os.path.getctime)

    detector = ObjectDetection()

    model_path = "yolo.h5"

    output_file = f"/output/newimage.jpg"

    detector.setModelTypeAsYOLOv3
    detector.setModelPath(model_path)
    detector.loadModel()
    detection = detector.detectObjectsFromImage(
        input_image=input_file, output_image_path=output_file
    )
    number_of_cars = 0
    for eachItem in detection:
        print(eachItem["name"], " : ", eachItem["percentage_probability"])
        if eachItem["name"] == "car":
            number_of_cars += 1

    update.message.reply_text(f"Найдено {number_of_cars} машинок")
    send_picture(update, context, output_file)


def detect_defects(update, context):
    update.message.reply_text("Ищем дефекты")
    os.makedirs("downloads", exist_ok=True)
    user_photo = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join("downloads", f"{user_photo.file_id}.jpg")
    user_photo.download(file_name)
    send_picture(update=update, context=context, picture_filename="bot.png")
    pass
