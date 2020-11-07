from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from webapp.db import DB


class User(DB.Model, UserMixin):
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(64), index=True, unique=True)
    password = DB.Column(DB.String(128))
    role = DB.Column(DB.String(10), index=True)
    
    @property
    def is_admin(self):
        return self.role == "admin"

    def __repr__(self):
        return "<User {} {}>".format(self.id, self.username)
        
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Defects(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    image = DB.Column(DB.String(128), nullable=True)
    object_class = DB.Column(DB.Integer, nullable=False)
    object_label = DB.Column(DB.String(64), nullable=False)


class CarCounts(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    image = DB.Column(DB.String(128), nullable=True)
    car_count = DB.Column(DB.Integer, nullable=False)
    ratio = DB.Column(DB.Float, nullable=False)