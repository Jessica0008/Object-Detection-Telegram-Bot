from random import choice, randint
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram import InputMediaPhoto, ForceReply

def send_picture(update, context, picture_filename):
    #cat_photos_list = glob('images/cat*.jp*g')
    #picture_filename = choice(photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(picture_filename, 'rb'), reply_markup=main_keyboard())

def main_keyboard():
    return ReplyKeyboardMarkup(
        [
            ['Count Cars'],
            ['Detect Defects']
        ])
