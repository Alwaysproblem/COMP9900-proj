import os
# import flask
from flask import Flask, render_template, session, request, flash, jsonify, redirect, url_for
import collections, operator, re, uuid, sqlite3
# from Models import *
from datetime import datetime

class dict2object(object):
    def __init__(self,map):
        self.map = map

    def __setattr__(self, name, value):
        if name == 'map':
             object.__setattr__(self, name, value)
             return
        print('set attr called ',name,value)
        self.map[name] = value

    def __getattr__(self,name):
        if name not in self.map:
            return None
        v = self.map[name]
        if isinstance(v,(dict)):
            return dict2object(v)
        if isinstance(v, (list)):
            r = []
            for i in v:
                r.append(dict2object(i))
            return r
        else:
            return self.map[name]

    def __getitem__(self,name):
        return self.map[name]
def query(sql):
    conn = sqlite3.connect('small.db', detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    cur = conn.cursor()
    cur.execute(sql)
    return cur

def insert(sql):
    conn = sqlite3.connect('small.db', detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    cur = conn.cursor()
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()

def current_time():
    now = datetime.now()
    current_time = now.strftime('%Y-%m-%dT%H:%M:%S+0000')
    return current_time
app = Flask(__name__, static_folder='', static_url_path='')

@app.route('/', methods =['GET','POST'])
def init():
    placeholder = ['hotel class', 'guest renting', 'room type', 'sort choice']
    return render_template('noresult.html', placeholder = placeholder)

@app.route('/search', methods = ['POST'])
def search():
    hotelclass = request.form.get('hotelclass')
    guestrenting = request.form.get('guestrenting')
    roomtype = request.form.get('roomtype')
    sortchoice = request.form.get('sortchoice')
    check_in = request.form.get('check_in')
    check_out = request.form.get('check_out')
    print(check_in)
    # result_list = []
    placeholder, result_list = load_search_result(hotelclass, guestrenting, roomtype, sortchoice)
    if result_list == []:
        return render_template('noresult.html')
    return render_template('search_result.html', placeholder = placeholder, results = result_list)

# @app.route('/search_result', methods = ['POST'])
# def search_result():
#     return render_template('search_result.html')

def load_search_result(hotelclass, guestrenting, roomtype, sortchoice):
    # sql = 'select * from hotel where hotel_class="' + detail + '"'
    sql = 'select * from hotel where '
    temp = ''
    hotelplaceholder = ''
    if operator.eq(hotelclass, None):
        hotelsearch = 'hotel_class != -1'
        hotelplaceholder = 'hotel class'
    elif operator.eq(hotelclass,'2'):
        hotelsearch = '(hotel_class = 2 or hotel_class = 1 or hotel_class = 0)'
        hotelplaceholder = '0-2 starts'
    else:
        hotelsearch = 'hotel_class =' + hotelclass
        hotelplaceholder = hotelclass+ ' starts'

    guestsearch = ''
    if operator.eq(guestrenting, None):
        guestsearch = 'guest_renting != -1'
        guestplaceholder = 'guest renting'
    elif operator.eq(guestrenting,'2'):
        guestsearch = '(guest_renting = 2 or guest_renting = 1 or guest_renting = 0)'
        guestplaceholder = '0-2 starts'
    else:
        guestsearch = 'guest_renting = ' + guestrenting
        guestplaceholder = guestrenting + ' starts'

    roomsearch = ''
    if operator.eq(roomtype, None):
        roomsearch = 'room_type != "None"'
        roomplaceholder = 'room type'
    else:
        roomsearch = 'room_type= "' + roomtype + '"'
        roomplaceholder = 'room type' + ' room'

    placeholder = [hotelplaceholder, guestplaceholder, roomplaceholder, sortchoice]
    sql = sql + hotelsearch + ' and '+ guestsearch + ' and ' + roomsearch + 'order by ' + sortchoice + ' desc'
    print(sql)
    # return sql

    cur = query(sql)
    t_list = []
    for h_tuple in cur.fetchall():
        t_list.append(h_tuple)
        print(h_tuple)

    return placeholder, t_list
    pass



if __name__ == '__main__':

    app.secret_key = os.urandom(12)
    app.run(debug=True)
    # print(load_search_result('2','2','mutl','price'))