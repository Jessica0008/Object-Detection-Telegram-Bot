from flask import Flask, render_template
from flask import request, redirect
import os
import requests
import business_logic
from business_logic import detect, count

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
app = Flask(__name__, static_url_path='/static')
    

def process_file(request):
    file = request.files['file']
    if file:
        os.makedirs("static", exist_ok=True)
        file_name = os.path.join("static", file.filename)
        file.save(file_name)
        return file_name


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
        file_name = process_file(request)
        if file_name is None:
            return error()
        answer = count(file_name)
        return render_template('show_result.html', main_img="/" + file_name, answer=answer)
    return render_template('submit.html', main_text="Count cars")


@app.route('/defects/',methods = ['GET', 'POST'])
def detect_defects():
    if request.method =='POST':
        file_name = process_file(request)
        if file_name is None:
            return error()
        answer = detect(file_name)
        return render_template('show_result.html', main_img="/" + file_name, answer=answer)
    return render_template('submit.html', main_text="Detect defects")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)
