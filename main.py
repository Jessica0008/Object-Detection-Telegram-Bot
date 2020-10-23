from flask import Flask, render_template
from flask import request, redirect
import os
import requests

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
app = Flask(__name__)


def count():
    pass


def main_processing(request, proc_func, redirect_func):
    try:
        file = request.files['file']
        if file:
            os.makedirs("downloads", exist_ok=True)
            file_name = os.path.join("downloads", file.filename)
            file.save(file_name)
            proc_func(file_name)
            return redirect_func()
    except(requests.RequestException, ValueError):
        return error()


@app.route("/error")
def error():
    text = "Server error during file transfer - try again"
    return render_template('index.html', main_text=text)


@app.route("/")
def hello():
    text = "Object Detection"
    return render_template('index.html', main_text=text)


@app.route('/cars/',methods = ['GET', 'POST'])
def count_cars():
    if request.method =='POST':
        return main_processing(request, count, hello)
    text = "Count cars"
    return render_template('submit.html', main_text=text)


@app.route('/defects/',methods = ['GET', 'POST'])
def detect_defects():
    if request.method =='POST':
        return main_processing(request, count, hello)
    text = "Detect defects"
    return render_template('submit.html', main_text=text)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)
