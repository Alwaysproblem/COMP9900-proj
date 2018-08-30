#!/bin/python3.6
# view functions 
# written by z5106189 August 2018

from app import app
import os
from flask import render_template, flash, redirect, request
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse

@app.route('/', methods=['GET','POST'])
@app.route('/mainpage', methods=['GET','POST'])
# @login_required 
def mainpage():
    p_path = os.path.join('static','pictures','background','4.jpg')

    return render_template('mainpage.html', picture_path=p_path)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('mainpage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('mainpage'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('mainpage'))


@app.route('/sign_up', methods=['POST'])
def sign_up():
    return render_template('sign_up.html')



@app.route('/search', methods=['POST'])
def search():
    return render_template('search.html')
    
