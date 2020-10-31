from getpass import getpass
import sys
from object_detection.db import get_or_create_auth_user
from werkzeug.security import generate_password_hash
from settings import MONGO_LINK
from pymongo import MongoClient

CLIENT = MongoClient(MONGO_LINK)
DB = CLIENT["testdb"]

username = input('Введите имя пользователя: ')
password = getpass('Введите пароль: ')
password2 = getpass('Повторите пароль: ')
if not password == password2:
    sys.exit(0)

user = get_or_create_auth_user(DB, username, generate_password_hash(password), role='admin')
print('User with id {} added'.format(username))