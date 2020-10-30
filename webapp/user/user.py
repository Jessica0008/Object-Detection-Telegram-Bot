from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):

    def __init__(self, login, role):
        super.__init__()
        self.id = login
        self.username = login
        self.role = role

    def get_username(self):
        return self.login

    def get_role(self):
        return self.role
        
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
