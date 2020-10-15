from glob import glob
from random import choice
import os
from utils import main_keyboard, send_picture


def give_menu(update, context):
    update.message.reply_text( f'Hello, user', reply_markup=main_keyboard() )


def count_cars(update, context):
    update.message.reply_text("Считаем машинки")
    os.makedirs("downloads", exist_ok=True)
    user_photo = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join("downloads", f"{user_photo.file_id}.jpg")
    user_photo.download(file_name)
    send_picture(update=update, context=context, picture_filename="../bot.png")
    pass


def detect_defects(update, context):
    print("Ищем дефекты")
    update.message.reply_text("Ищем дефекты")
    os.makedirs("downloads", exist_ok=True)
    user_photo = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join("downloads", f"{user_photo.file_id}.jpg")
    user_photo.download(file_name)
    send_picture(update=update, context=context, picture_filename="../bot.png")
    pass
