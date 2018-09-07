import os

from flask import Flask, request, redirect, render_template, url_for, flash
from models import System

app = Flask(__name__)


@app.route('/')
def request_index():
    # return redirect(url_for('post_request'))
    system = System()
    system.create_table()
    return render_template('request_index.html')


@app.route('/post_request', methods=["GET", "POST"])
def post_request():
    system = System()
    if request.method == 'POST':
        title = request.form["title"]
        address = request.form["address"]
        room_num = request.form["room_num"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        message = request.form["message"]
        system.post_request(title, address, room_num, start_date, end_date, message)
        return redirect(url_for("request_index"))
    else:
        return render_template("post_request.html")


@app.route('/requestList', methods=["GET", "POST"])
def requestList():
    system = System()
    requests = system.list_request()
    return render_template('request.html', request1=requests)


@app.route('/view_quest/<string:title>')
def view_request(title):
    system = System()
    request_message = system.get_request_message(title)
    request_address = system.get_request_address(title)
    request_roomnum = system.get_request_roomnum(title)
    request_start = system.get_request_start(title)
    request_end = system.get_request_end(title)
    return render_template('view_request.html', title=title, request_mesaage=request_message,
                           request_address=request_address, request_roomnum= request_roomnum,
                           request_start=request_start, request_end=request_end)


if __name__ == '__main__':
    app.run()
