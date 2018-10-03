import os
# import flask
from flask import Flask, render_template, session, request, flash, jsonify, redirect, url_for
import collections, operator, re, uuid, sqlite3
# from Models import *
from datetime import datetime


#############################彭霄汉start###############################
#1.userid -> username
#2.route / 
#3.base website name
# 4.password password_hash 128
# from app import app, db
# import os
# from flask import render_template, flash, redirect, request, url_for
# from app.forms import LoginForm, RegistrationForm
import uuid
from flask_login import current_user, login_user, logout_user, login_required, LoginManager, UserMixin
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
#############################彭霄汉end###############################

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

#############################彭霄汉start###############################
login = LoginManager(app)
login.login_view = 'login'


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    full_name = StringField('Full Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        sql = 'select username from users'
        cur = query(sql)#Cursor object
        res = cur.fetchall()
        if (username.data,) in res:
            raise ValidationError('Please use a different username.')

        
        # user = User.query.filter_by(username=username.data).first()
        # if user is not None:
            # raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        sql = 'select email from users'
        cur = query(sql)#Cursor object
        if email.data in cur.fetchall():
        # user = User.query.filter_by(email=email.data).first()
        # if user is not None:
            raise ValidationError('Please use a different email address.')


class User(UserMixin):
    sql = 'select ID from users order by ID DESC limit 1'
    cur = query(sql)
    res = cur.fetchall()
    if len(res) > 0:
        Usercount = res[0][0]
    else:
        Usercount = 0
    id = Usercount
    def __init__(self, Username):
        self.username = None
        sql = 'select * from users where username = "' + Username + '"'
        cur = query(sql)
        res = cur.fetchall()
        if len(res) == 1:
            self.ID = res[0][0]
            self.username = res[0][1]
            self.password_hash = res[0][2] 
            self.full_name = res[0][3]
            self.email = res[0][4]
            self.home = res[0][5]
            self.home_latitude = res[0][6]
            self.home_longitude = res[0][7]
            self.home_suburb = res[0][8]

    def add_user(self,Username, Password, Full_name, Email,\
     Home = 'None', Home_latitude = 'None', Home_longitude = 'None', Home_suburb = 'None'):

        User.Usercount += 1
        password_hash = generate_password_hash(Password)

        key = '"ID", "username", "password_hash", "full_name", "email", \
        "home", "home_latitude", "home_longitude", "home_suburb"'

        # value = 'User.Usercount, Username, password_hash, Full_name, Email, \
        # Home, Home_latitude, Home_longitude, Home_suburb'

        sql = "insert into users (" + key + ") values ({},'{}','{}','{}','{}','{}','{}','{}','{}')".format\
        (User.Usercount, Username, password_hash, Full_name, Email, Home, Home_latitude, Home_longitude, Home_suburb)
        insert(sql)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username) 


@login.user_loader
def load_user(id):
    sql = 'select * from users where ID = ' + str(id)
    cur = query(sql)
    res = cur.fetchall()
    print(id)
    print(res)
    return res[0]
    # return User.query.get(int(id))


# @app.route('/', methods=['GET','POST'])
@app.route('/mainpage', methods=['GET','POST'])
# @login_required 
def mainpage():
    p_path = os.path.join('static','pictures','background','4.jpg')

    # key = '"ID", "username", "password", "full_name", "email"'
    # value = '1, "1", "isis", "5", "4"'
    # sql = 'insert into users (' + key + ') values (' + value + ')'
    # insert(sql)

    # sql = 'select * from users'
    # cur = query(sql)
    # res = cur.fetchall()
    # for i in res:
    #     print(i)

    return render_template('mainpage.html', picture_path=p_path)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('mainpage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User(Username = form.username.data)
        if user.username is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('mainpage'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('mainpage'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('mainpage'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(form.username.data)
        user.add_user(form.username.data, form.password.data, form.full_name.data, form.email.data)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

############################彭霄汉end###############################
##################Yongxi start#################
from form import PersonForm
# import datetime
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'upload'

def tupletodict(keys, tup):
    return dict(zip(keys, tup))

def comd_gen(Pform, Image_dir):
    UserEmail = Pform.UserEmail.data
    HouseID = str(uuid.uuid4())
    Rooms = Pform.Room.data.strip()
    Streets = Pform.Street.data.strip()
    Suburb = Pform.Suburb.data.strip()
    State = Pform.State.data.strip()
    Postcode = Pform.Postcode.data.strip()
    RoomType = Pform.RoomType.data
    Star = Pform.Star.data
    CheckIn = Pform.check_in_date.data
    CheckOut = Pform.check_out_date.data
    Price = Pform.Price.data
    Description = Pform.Description.data.strip()

    # save the Image directory and Image data
    picture = Pform.Image.data
    filename = secure_filename(picture.filename)
    cur_dir = os.getcwd()
    Image = os.path.join(cur_dir, Image_dir, filename)
    picture.save(Image)
    Image = "../" + UPLOAD_FOLDER + '/' + filename
    # save post time
    Post_time = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.now())


    cmd = f"""INSERT INTO hotel VALUES (
                    "{UserEmail}",
                    "{HouseID}",
                    "{Rooms}",
                    "{Streets}",
                    "{Suburb}",
                    "{State}",
                    "{Postcode}",
                    "{RoomType}",
                    "{Star}",
                    "{CheckIn}",
                    "{CheckOut}",
                    "{Price}",
                    "{Description}",
                    "{Image}",
                    "{Post_time}"
                )"""
    return cmd

@app.route("/showAll")
def showAll():
    conn = sqlite3.connect("small.db")
    cur = conn.cursor()
    keys = [
        "UserEmail", 
        "HouseID", 
        "RoomNo",
        "Street",
        "Suburb",
        "State",
        "Postcode",
        "RoomType",
        "Star",
        "CheckIn",
        "CheckOut",
        "Price",
        "Description",
        "Image",
        "Post_time"
        ]
    info_tuples = cur.execute("""SELECT * FROM hotel;""")
    posts = [tupletodict(keys, tup) for tup in info_tuples]
    conn.close()
    return render_template('show.html', posts=posts)

@app.route("/show")
def show():
    conn = sqlite3.connect("small.db")
    cur = conn.cursor()
    keys = [
        "UserEmail", 
        "HouseID", 
        "RoomNo",
        "Street",
        "Suburb",
        "State",
        "Postcode",
        "RoomType",
        "Star",
        "CheckIn",
        "CheckOut",
        "Price",
        "Description",
        "Image",
        "Post_time"
        ]
    info_tuples = cur.execute("""SELECT * FROM hotel order by Post_time desc limit 1;""")
    posts = [tupletodict(keys, tup) for tup in info_tuples]
    conn.close()
    return render_template('show.html', posts=posts)


@app.route("/add", methods=['GET', "POST"])
def add():
    AcForm = PersonForm()
    if AcForm.validate_on_submit():
        cmd_db = comd_gen(AcForm, UPLOAD_FOLDER)
        conn = sqlite3.connect("small.db")
        cur = conn.cursor()
        with conn:
            cur.execute(cmd_db)
        conn.close()
        flash("the information is added", "success")
        return redirect(url_for('show'))
    return render_template('add.html', title='Add', form = AcForm)

##################Yongxi End#################

##################Zeng Start#################

def getRequest():
    conn = sqlite3.connect('small.db', detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    cur = conn.cursor()
    keys = [
        "ID",
        "title",
        "address",
        "room_num",
        "start_date",
        "end_date",
        "message"
    ]
    info_tuples = cur.execute("""SELECT * FROM requests;""")
    posts = [tupletodict(keys, tup) for tup in info_tuples]
    conn.close()
    return posts


@app.route('/request')
def request_index():
    return render_template('request_index.html')


def load_requests(title, address, room_num, start_date, end_date, message):
    conn = sqlite3.connect('small.db', detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    posts = getRequest()
    count = 0
    for _ in posts:
        count = count + 1

    sql = "insert into requests values ('" + str(count) + "','" + title + "','" + address + "', '" + room_num + "', '" + start_date + "','" + end_date + "','" + message + "','1') "
    conn.execute(sql)
    conn.commit()
    pass


@app.route('/post_request', methods=["GET", "POST"])
def post_request():

    if request.method == 'POST':
        title = request.form["title"]
        address = request.form["address"]
        room_num = request.form["room_num"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        message = request.form["message"]
        load_requests(title, address, room_num, start_date, end_date, message)
        return redirect(url_for("request_index"))
    else:
        return render_template("post_request.html")


@app.route('/requestList', methods=["GET", "POST"])
def requestList():
    posts = getRequest()
    return render_template('request.html', request1=posts)


@app.route('/view_quest/<string:title>')
def view_request(title):
    posts = getRequest()
    return render_template('view_request.html', posts=posts, title1=title)

##################Zeng End#################

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

@app.route('/post', methods = ['POST'])
def post():
    pass

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
    # print(load_search_result('2','2','mutl','price'))