import os
# import flask
from flask import Flask, render_template, session, request, flash, jsonify, redirect, url_for
import collections, operator, re, uuid, sqlite3
# from Models import *
from datetime import datetime

now = datetime.now()
#############################彭霄汉start###############################
# 1.userid -> username
# 2.route /
# 3.base website name
# 4.password password_hash 128
# from app import app, db
# import os
# from flask import render_template, flash, redirect, request, url_for
# from app.forms import LoginForm, RegistrationForm
import uuid
from flask_bootstrap import Bootstrap
from flask_login import current_user, login_user, logout_user, login_required, LoginManager, UserMixin
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


#############################彭霄汉end###############################

class dict2object(object):
    def __init__(self, map):
        self.map = map

    def __setattr__(self, name, value):
        if name == 'map':
            object.__setattr__(self, name, value)
            return
        print('set attr called ', name, value)
        self.map[name] = value

    def __getattr__(self, name):
        if name not in self.map:
            return None
        v = self.map[name]
        if isinstance(v, (dict)):
            return dict2object(v)
        if isinstance(v, (list)):
            r = []
            for i in v:
                r.append(dict2object(i))
            return r
        else:
            return self.map[name]

    def __getitem__(self, name):
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


def update(sql):
    conn = sqlite3.connect('small.db', detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    cur = conn.cursor()
    print(sql)
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
Bootstrap = Bootstrap(app)
login.login_view = 'login'


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Account Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    full_name = StringField('Full Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        sql = 'select username from users'
        cur = query(sql)
        res = cur.fetchall()
        if (username.data,) in res:
            raise ValidationError('Please use a different account name.')

    def validate_email(self, email):
        sql = 'select email from users'
        cur = query(sql)
        res = cur.fetchall()
        if (email.data,) in res:
            raise ValidationError('Please use a different email address.')


class Profile_edit_Form(FlaskForm):
    username = StringField('Update Account Name', \
                           render_kw={'placeholder': 'current_user.username'})

    email = StringField('Update Email Address', \
                        render_kw={'placeholder': 'current_user.email'})

    full_name = StringField('Update Full Name', \
                            render_kw={'placeholder': 'current_user.full_name'})

    home_suburb = StringField('Home Suburb (optional)')

    home = StringField('Home address (optional)')

    password = PasswordField('New Password')

    password2 = PasswordField(
        'Repeat Password', validators=[EqualTo('password')])

    submit = SubmitField('Update Profile')

    def validate_username(self, username):
        sql = 'select username from users'
        cur = query(sql)
        res = cur.fetchall()
        res.remove((current_user.username,))
        if (username.data,) in res:
            raise ValidationError('Please use a different account name.')

    def validate_email(self, email):
        sql = 'select email from users'
        cur = query(sql)
        res = cur.fetchall()
        res.remove((current_user.email,))
        if (email.data,) in res:
            raise ValidationError('Please use a different email address.')


sql = 'select ID from users order by ID DESC limit 1'
cur = query(sql)
res = cur.fetchall()
if len(res) > 0:
    Usercount = res[0][0]
else:
    Usercount = 0


class User(UserMixin):
    id = Usercount

    def __init__(self, Username):
        self.username = None
        sql = 'select * from users where username = "' + Username + '"'
        cur = query(sql)
        res = cur.fetchall()
        if len(res) == 1:
            self.ID = res[0][0]
            User.id = self.ID
            self.username = res[0][1]
            self.password_hash = res[0][2]
            self.full_name = res[0][3]
            self.email = res[0][4]
            self.home = res[0][5]
            self.home_latitude = res[0][6]
            self.home_longitude = res[0][7]
            self.home_suburb = res[0][8]

    def add_user(self, Username, Password, Full_name, Email, \
                 Home='None', Home_latitude='None', Home_longitude='None', Home_suburb='None'):
        global Usercount
        Usercount += 1
        password_hash = generate_password_hash(Password)

        key = '"ID", "username", "password_hash", "full_name", "email", \
        "home", "home_latitude", "home_longitude", "home_suburb"'

        # value = 'User.Usercount, Username, password_hash, Full_name, Email, \
        # Home, Home_latitude, Home_longitude, Home_suburb'

        sql = "insert into users (" + key + ") values ({},'{}','{}','{}','{}','{}','{}','{}','{}')".format \
            (Usercount, Username, password_hash, Full_name, Email, Home, Home_latitude, Home_longitude, Home_suburb)
        insert(sql)

    def update_user(self, Username, Password, Full_name, Email, \
                    Home, Home_suburb, New_password, Home_latitude='None', Home_longitude='None'):
        if (New_password):
            password_hash = generate_password_hash(Password)
        else:
            password_hash = Password

        sql = 'UPDATE users SET username = "' + Username + '", password_hash = "' + password_hash + '",\
        full_name = "' + Full_name + '", email = "' + Email + '", home = "' + Home + '",\
        home_suburb = "' + Home_suburb + '" WHERE ID = ' + str(current_user.ID)

        update(sql)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    sql = 'select * from users where ID = ' + str(id)
    cur = query(sql)
    res = cur.fetchall()
    user = User(res[0][1])
    return user


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/mainpage', methods=['GET', 'POST'])
def mainpage():
    p_path = os.path.join('static', 'pictures', 'background', '4.jpg')

    # key = '"ID", "username", "password", "full_name", "email"'
    # value = '1, "1", "isis", "5", "4"'
    # sql = 'insert into users (' + key + ') values (' + value + ')'
    # insert(sql)

    sql = 'select * from users'
    cur = query(sql)
    res = cur.fetchall()
    for i in res:
        print(i)
    return render_template('mainpage.html', picture_path=p_path)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('mainpage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User(Username=form.username.data)
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

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html', title='profile')

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if current_user.is_anonymous:
        return redirect(url_for('login'))

    current = {
        'username': current_user.username,
        'full_name': current_user.full_name,
        'email': current_user.email,
        'home': current_user.home,
        'home_suburb': current_user.home_suburb,
        'password': current_user.password_hash
    }
    new_password = 0
    form = Profile_edit_Form()
    print('before')
    if form.validate_on_submit():
        print('submit')
        update = {
            'username': form.username.data,
            'full_name': form.full_name.data,
            'email': form.email.data,
            'home': form.home.data,
            'home_suburb': form.home_suburb.data,
            'password': form.password.data
        }
        L = ['', '', '', '', '', '']
        if (list(update.values()) == L):
            flash('Please fill in the form to update your profile.')
            return redirect(url_for('edit_profile'))
        else:
            for i in range(len(update.values()) - 1):
                # if the input data is different from the current and input data is not empty:
                # update information except for password
                if (list(update.values())[i] != list(current.values())[i] and len(list(update.values())[i]) > 0):
                    current[list(current.keys())[i]] = update[list(update.keys())[i]]
            # if the user input none-empty password and is not using the same old password:
            if (len(form.password.data) > 0 and not current_user.check_password(form.password.data)):
                current['password'] = update['password']
                new_password = 1
            # elif the user filled the old same password in the form:
            elif (current_user.check_password(form.password.data)):
                flash('Password is same as the current one, please use a different password.')
                return redirect(url_for('edit_profile'))

            current_user.update_user(current['username'], current['password'], \
                                     current['full_name'], current['email'], current['home'], current['home_suburb'],
                                     new_password)
            flash('User profile update was successful.')

        if (len(update['password']) > 0 or len(update['username']) > 0):
            flash('Please sign in with your new account name and password.')
            logout_user()
            return redirect(url_for('login'))
    return render_template('edit_profile.html', title='Edit Profile', form=form)


############################彭霄汉end###############################
##################Yongxi start#################
from form import PersonForm
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'upload'


def tupletodict(keys, tup):
    return dict(zip(keys, tup))


def comd_gen(Pform, Image_dir):
    Userid = current_user.id
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

    Booking_state = False
    Full_address = ' '.join([Rooms + '/' + Streets, Suburb, State, Postcode])

    cmd = f"""INSERT INTO hotel VALUES (
        "{Userid}",
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
        "{Post_time}",
        "{Booking_state}",
        "{Full_address}"
        )"""
    return cmd


@app.route("/showAll")
# @login_required
def showAll():
    conn = sqlite3.connect("small.db")
    cur = conn.cursor()
    keys = [
        "UserID",
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
        "Post_time",
        "Booking_state",
        "Full_address"
    ]
    info_tuples = cur.execute("""SELECT * FROM hotel;""")
    posts = [tupletodict(keys, tup) for tup in info_tuples]
    conn.close()
    return render_template('showdb.html', posts=posts)


@app.route("/show")
# @login_required
def show():
    conn = sqlite3.connect("small.db")
    cur = conn.cursor()
    keys = [
        "UserID",
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
        "Post_time",
        "Booking_state",
        "Full_address"
    ]
    info_tuples = cur.execute("""SELECT * FROM hotel order by Post_time desc limit 1;""")
    posts = [tupletodict(keys, tup) for tup in info_tuples]
    conn.close()
    return render_template('show.html', posts=posts)


@app.route("/add", methods=['GET', "POST"])
@login_required
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
    return render_template('add.html', title='Add', form=AcForm)

@app.route("/ShowBooking", methods=['GET', "POST"])
def ShowBooking():
    showNum = 3
    conn = sqlite3.connect("small.db")
    cur = conn.cursor()
    keys = [
        "UserID",
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
        "Post_time",
        "Booking_state",
        "Full_address"
    ]
    info_tuples = cur.execute(f"""SELECT * FROM hotel where booking = 'False' order by price desc limit {showNum};""")
    # info_tuples = cur.execute(f"""SELECT * FROM hotel where booking = 'False';""")
    posts = [tupletodict(keys, tup) for tup in info_tuples]
    conn.close()
    return render_template('showBooking.html', posts=posts)

@app.route('/my_postings', methods=['GET', 'POST'])
@login_required
def my_postings():
    House_ID = request.args.get('HouseID')
    showNum = 3
    conn = sqlite3.connect("small.db")
    cur = conn.cursor()
    if House_ID != None:
        # print(f" the house ID :{House_ID}")
        pic_path = cur.execute(f"SELECT Image FROM hotel WHERE HouseID = '{House_ID}';")
        pic_path = list(pic_path)
        # print(pic_path)
        if pic_path != []:
            os.remove(pic_path[0][0][1:])
            cur.execute(f"DELETE FROM hotel WHERE HouseID = '{House_ID}';")
            conn.commit()

    keys = [
        "UserID",
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
        "Post_time",
        "Booking_state",
        "Full_address"
    ]
    info_tuples = cur.execute(f"""SELECT * FROM hotel where userid = {current_user.ID} order by price desc limit {showNum};""")
    # info_tuples = cur.execute(f"""SELECT * FROM hotel where booking = 'False';""")
    posts = [tupletodict(keys, tup) for tup in info_tuples]
    conn.close()
    return render_template('my_postings.html', title='my_postings', posts=posts)


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
        "message",
        "user_id"
    ]
    info_tuples = cur.execute("""SELECT * FROM requests;""")
    posts = [tupletodict(keys, tup) for tup in info_tuples]
    conn.close()
    return posts


@app.route('/request')
def request_index():
    # init.create_table()
    # user_id = session["users.id"]
    posts = getRequest()
    return render_template('request_index.html', request1=posts)


def load_requests(title, address, room_num, start_date, end_date, message):
    conn = sqlite3.connect('small.db', detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    posts = getRequest()
    count = 0
    for _ in posts:
        count = count + 1

    user_id = current_user.ID
    sql = "insert into requests values ('" + str(
        count) + "','" + title + "','" + address + "', '" + room_num + "', '" + start_date + "','" + end_date + "','" + message + "','" + str(user_id) + "') "
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


def getComment():
    conn = sqlite3.connect('small.db', detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    cur = conn.cursor()
    keys = [
        "ID",
        "message",
        "requestID",
        "userID"
        "time"
    ]
    info_tuples = cur.execute("""SELECT * FROM comments;""")
    comments = [tupletodict(keys, tup) for tup in info_tuples]
    conn.close()
    return comments


def load_comment(comment, requestID):
    conn = sqlite3.connect('small.db', detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    com = getComment()
    count = 0
    for _ in com:
        count = count + 1

    user_id = current_user.ID
    sql = "insert into comments values ('" + str(
        count) + "','" + comment + "','" + requestID + "', '" + str(user_id) + " ','" + str(now) + "') "
    conn.execute(sql)
    conn.commit()
    pass


@app.route('/view_request/<string:requestID>', methods=["GET", "POST"])
def view_request(requestID):
    posts = getRequest()
    if request.method == 'POST':
        comment = request.form["comment"]
        load_comment(comment, requestID)

    comments = getComment()
    return render_template('view_request.html', posts=posts, comments=comments, requestID=requestID)


##################Zeng End#################

@app.route('/my_bookings', methods=['GET', 'POST'])
@login_required
def my_bookings():
    booking_detail = load_booking(current_user.ID)
    return render_template('my_bookings.html', title='my_bookings', booking_detail = booking_detail)

class house_info():
    def __init__(self, each_house):
        self.userid = each_house[0]
        self.useremail = each_house[1]
        self.HouseID = each_house[2]
        self.RoomNo = each_house[3]
        self.Street = each_house[4]
        self.Suburb = each_house[5]
        self.State = each_house[6]
        self.Postcode = each_house[7]
        self.RoomType = each_house[8]
        self.Star = each_house[9]
        self.check_in_date = each_house[10]
        self.check_out_date = each_house[11]
        self.price = each_house[12]
        self.description = each_house[13]
        self.Image = each_house[14]
        self.post_time = each_house[15]
        self.booking = each_house[16]
        self.full_address = each_house[17]

class user_info():
    def __init__(self, user):
        self.ID = user[0]
        self.username = user[1]
        self.full_name = user[3]
        self.email = user[4]

class booking_info():
    def __init__(self, booking):
        self.HouseID = booking[1]
        self.img = booking[2]
        self.address = booking[3]
        self.roomtype = booking[4]
        self.price = booking[5]
        self.userid = booking[6]
        self.start_time = booking[7]
        self.end_time = booking[8]

@app.route('/search_init', methods =['GET','POST'])
def search_init():
    placeholder = ['hotel class', 'suburb', 'room type', 'sort choice']
    return render_template('noresult.html', placeholder = placeholder)

@app.route('/search', methods = ['POST'])
def search():
    Star = request.form.get('hotelclass')
    Suburb = request.form.get('suburb')
    RoomType = request.form.get('roomtype')
    sortchoice = request.form.get('sortchoice')
    check_in_date = request.form.get('start-date')
    check_out_date = request.form.get('end-date')
    placeholder, result_list = load_search_result(Star, Suburb, RoomType, sortchoice, check_in_date, check_out_date)
    if result_list == []:
        return render_template('noresult.html', placeholder = ['hotel class', 'suburb', 'room type', 'sort choice'])
    return render_template('search_result.html', placeholder = placeholder, results = result_list)

@app.route('/detail', methods = ['GET','POST'])
def detail():
    if current_user.is_authenticated:
        house_id = request.args.get('HouseID')
        print(house_id)
        house_detail, user_detail = load_house_info(house_id)
        print('booking',house_detail.booking)
        return render_template('house_detail.html', house_detail = house_detail, user_detail = user_detail)
    else:
        flash('You need login first')
        return redirect(url_for('login'))

@app.route('/booking', methods = ['GET','POST'])
def booking():
    house_id = request.args.get('HouseID')
    print(house_id)
    house_detail, user_detail = load_house_info(house_id)
    return render_template('booking_house.html', house_detail = house_detail, user_detail = user_detail)

@app.route('/order', methods=['GET','POST'])
def order():
    print(request.form)
    start_date = request.form.get('start-date')
    end_date = request.form.get('end-date')
    house_address = request.form.get('house_address')
    house_star = request.form.get('house_star')
    house_price = request.form.get('house_price')
    house_roomtype = request.form.get('house_roomtype')
    house_id = request.form.get('house_id')
    house_img = request.form.get('house_img')
    startdate = datetime.strptime(start_date, '%Y-%m-%d')
    enddate = datetime.strptime(end_date, '%Y-%m-%d')
    rentday = (enddate-startdate).days + 1
    total_price = float(rentday)*float(house_price)
    deposit = total_price * 0.2
    flash('Congratulations on your successful booking')
    # update date
    update_order(house_id, house_address, house_img, house_price, house_roomtype ,start_date, end_date)
    return render_template('show_book.html', house_address=house_address, house_star=house_star,
                           house_price=house_price, house_roomtype=house_roomtype,
                           start_date = start_date, end_date = end_date, total_price=total_price,
                           deposit=deposit)

def update_order(house_id, house_address, house_img, house_price, house_roomtype ,start_date, end_date):

    print('current_user',current_user.ID)
    sql = 'update hotel set booking = "False" where HouseID = "' + house_id + '"'
    update(sql)
    key = '"ID", "HouseID", "Img", "Address", "Roomtype", "Price", "userid", "start_time", "end_time"'
    sql = "insert into booking (" + key + ") values ({},'{}','{}','{}','{}','{}','{}','{}')".format \
        (uuid.uuid4(), house_id, house_img, house_address, house_roomtype, house_price, current_user.ID, start_date, end_date)
    insert(sql)

    house_detail, user_detail = load_house_info(id)
    print('nb',house_detail.booking)

def load_booking(id):
    sql = 'select * from booking where userid = "' + current_user.ID + '" order by start_time desc'
    cur = query(sql)
    t_list = []
    for h_tuple in cur.fetchall():
        booking_detail = booking_info(h_tuple)
        t_list.append(booking_detail)
    return t_list

def load_house_info(id):
    sql = 'select * from hotel where HouseID = "' + id + '"'
    print(sql)
    cur = query(sql)
    h_tuple = cur.fetchone()
    house = house_info(h_tuple)
    sql = 'select * from users where ID = "' + house.userid + '"'
    print(sql)
    cur = query(sql)
    h_tuple = cur.fetchone()
    user = user_info(h_tuple)
    return house, user

def load_search_result(Star, Suburb, RoomType, sortchoice, check_in_date, check_out_date):
    # booking = "False" and
    sql = 'select * from hotel where booking = "False" and'
    temp = ''
    hotelplaceholder = ''
    if operator.eq(Star, None):
        hotelsearch = 'Star != -1'
        hotelplaceholder = 'Star'
    elif operator.eq(Star,'2'):
        hotelsearch = '(Star = 2 or Star = 1 or Star = 0)'
        hotelplaceholder = '0-2 starts'
    else:
        hotelsearch = 'Star =' + Star
        hotelplaceholder = Star+ ' starts'

    suburbsearch = ''
    if operator.eq(Suburb, None):
        suburbsearch = 'Suburb != "None"'
        suburbplaceholder = 'suburb'
    else:
        suburbsearch = 'Suburb = ' + Suburb
        suburbplaceholder = 'suburb'
    print(suburbsearch)

    roomsearch = ''
    if operator.eq(RoomType, None):
        roomsearch = 'RoomType != "None"'
        roomplaceholder = 'room type'
    else:
        roomsearch = 'RoomType= "' + RoomType + '"'
        roomplaceholder = 'RoomType' + ' room'

    sortsearch = ''
    if operator.eq(sortchoice, None):
        sortsearch = 'Star'
    else:
        sortsearch = sortchoice
    check_in_search = ''
    if operator.eq(check_in_date, ''):
        check_in_search = 'check_in_date > ""'
    else:
        check_in_search = 'check_in_date < "' + check_in_date + '"'

    check_out_search = ''
    if operator.eq(check_out_date, ''):
        check_out_search = 'check_out_date > ""'
    else:
        check_out_search = 'check_out_date > "' + check_out_date + '"'

    placeholder = [hotelplaceholder, suburbplaceholder, roomplaceholder, sortchoice]
    sql = sql + hotelsearch + ' and '+ roomsearch + ' and ' + suburbsearch + ' and ' + check_in_search + ' and ' + check_out_search + ' order by ' + sortsearch + ' desc'
    print(sql)
    cur = query(sql)
    t_list = []
    for h_tuple in cur.fetchall():
        house = house_info(h_tuple)
        t_list.append(house)
    return placeholder, t_list

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
