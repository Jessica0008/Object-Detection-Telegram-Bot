from random import choice, randint
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram import InputMediaPhoto, ForceReply
import os
import glob
from re import search


def give_menu(update, context):
    update.message.reply_text(f"Hello, user", reply_markup=main_keyboard())


def send_picture(update, context, picture_filename):
    # cat_photos_list = glob('images/cat*.jp*g')
    # picture_filename = choice(photos_list)
    chat_id = update.effective_chat.id
    jpg_file = open(picture_filename, "rb")
    context.bot.send_photo(
        chat_id=chat_id,
        photo=jpg_file,
        reply_markup=main_keyboard(),
    )
    jpg_file.close()


def get_picture_token(chat_id):
    jpg_images = glob.glob(f"downloads/{chat_id}-*.jpg")
    if len(jpg_images) < 1:
        return 1
    else:
        max_token = 0
        for image in jpg_images:
            token = int(search("\-(.*?)\.", image).group(1))
            if token > max_token:
                max_token = token
        return max_token + 1


def get_picture(update, context):

    update.message.reply_text("Обрабатываю фото")
    os.makedirs("downloads", exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[0].file_id)

    token = get_picture_token(context.chat_id)
    filename = os.path.join("downloads", f"{context.chat_id}-{token}.jpg")
    photo_file.download(filename)

    update.message.reply_text("Файл сохранен")
    give_menu(update, context)
    return filename


def main_keyboard():
    return ReplyKeyboardMarkup([["Count Cars"], ["Detect Defects"]])
