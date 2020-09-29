from glob import glob
from random import choice

from utils import main_keyboard


def greet_user(update, context):
    update.message.reply_text( main_keyboard() )
