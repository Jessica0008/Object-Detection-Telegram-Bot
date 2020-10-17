from glob import glob
from utils import main_keyboard, send_picture, get_picture, give_menu
import os


def detect_defects(update, context):
    print("Ищем дефекты")
    update.message.reply_text("Ищем дефекты")
    os.makedirs("downloads", exist_ok=True)
    user_photo = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join("downloads", f"{user_photo.file_id}.jpg")
    user_photo.download(file_name)
    send_picture(update=update, context=context, picture_filename="../bot.png")
    pass


def count_cars(update, context):
    pass