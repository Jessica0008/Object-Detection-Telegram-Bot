from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from flask import request
import os
import requests
from webapp.business_logic import detect, count, get_stats, DB
from webapp.forms import LoginForm
from webapp.user.user import User
from webapp.user.db_tools import get_auth_user


def create_app():
    # Press Shift+F10 to execute it or replace it with your code.
    # Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
    app = Flask(__name__, static_url_path='/webapp/static')
    app.config.from_pyfile('settings.py')
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'


    @login_manager.user_loader
    def load_user(user_id):
        return get_auth_user(DB, user_id)


    def process_file(request):
        file = request.files['file']
        if file:
            os.makedirs("webapp/static", exist_ok=True)
            file_name = os.path.join("webapp", "static", file.filename)
            file.save(file_name)
            return file_name


    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))


    @app.route("/login")
    def login():
        title = "Login"
        form = LoginForm()
        return render_template('login.html', title=title, form=form)


    @app.route('/stat')
    @login_required
    def show_stat():
        answers = get_stats()
        return render_template('show_stat.html', answers=answers)


    @app.route('/process_login', methods=['POST'])
    def process_login():
        form = LoginForm()
        form.validate_on_submit()
        if form.validate_on_submit():
            user = get_auth_user(DB, form.username.data)
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Вы вошли на сайт')
                return redirect(url_for('index'))

        flash('Неправильное имя пользователя или пароль')
        return redirect(url_for('login'))


    @app.route("/error")
    def error():
        text = "Server error during file transfer - try again"
        return render_template('index.html', main_text=text)


    @app.route("/")
    def index():
        text = "Object Detection"
        return render_template('index.html', main_text=text)


    @app.route('/cars/', methods = ['GET', 'POST'])
    def count_cars():
        if request.method =='POST':
            file_name = process_file(request)
            if file_name is None:
                return error()
            answer = count(file_name)
            return render_template('show_cars.html', main_img="/" + file_name, answer=answer)
        return render_template('submit.html', main_text="Count cars")


    @app.route('/defects/', methods = ['GET', 'POST'])
    def detect_defects():
        if request.method =='POST':
            file_name = process_file(request)
            if file_name is None:
                return error()
            answer = detect(file_name)
            return render_template('show_result.html', main_img="/" + file_name, answer=answer)
        return render_template('submit.html', main_text="Detect defects")

    return app
