from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField("submit", render_kw={"class": "btn btn-primary"})


class CarsForm(FlaskForm):
    count_cars = SubmitField("Count Cars", value="count cars", render_kw={"class": "btn btn-primary"})


class DefectsForm(FlaskForm):
    defects = SubmitField("Detect Defects", value="detect defects", render_kw={"class": "btn btn-primary"})


class StatisticsForm(FlaskForm):
    statistics = SubmitField("Statistics", value="statistics", render_kw={"class": "btn btn-primary"})
