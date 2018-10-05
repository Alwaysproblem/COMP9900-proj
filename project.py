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
    Usercount = 1


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
# import datetime
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
        "{Post_time}"
        )"""
    return cmd


@app.route("/showAll")
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
        "Post_time"
    ]
    info_tuples = cur.execute("""SELECT * FROM hotel;""")
    posts = [tupletodict(keys, tup) for tup in info_tuples]
    conn.close()
    return render_template('show.html', posts=posts)


@app.route("/show")
def show():
    print(current_user.ID)
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
    return render_template('add.html', title='Add', form=AcForm)


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


@app.route('/view_quest/<string:requestID>', methods=["GET", "POST"])
def view_request(requestID):
    posts = getRequest()
    if request.method == 'POST':
        comment = request.form["comment"]
        load_comment(comment, requestID)

    comments = getComment()
    return render_template('view_request.html', posts=posts, comments=comments, requestID=requestID)


##################Zeng End#################

# @app.route('/', methods =['GET','POST'])
# def init():
#     placeholder = ['hotel class', 'guest renting', 'room type', 'sort choice']
#     return render_template('noresult.html', placeholder = placeholder)

@app.route('/search', methods=['POST'])
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
    return render_template('search_result.html', placeholder=placeholder, results=result_list)


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
    elif operator.eq(hotelclass, '2'):
        hotelsearch = '(hotel_class = 2 or hotel_class = 1 or hotel_class = 0)'
        hotelplaceholder = '0-2 starts'
    else:
        hotelsearch = 'hotel_class =' + hotelclass
        hotelplaceholder = hotelclass + ' starts'

    guestsearch = ''
    if operator.eq(guestrenting, None):
        guestsearch = 'guest_renting != -1'
        guestplaceholder = 'guest renting'
    elif operator.eq(guestrenting, '2'):
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
    sql = sql + hotelsearch + ' and ' + guestsearch + ' and ' + roomsearch + 'order by ' + sortchoice + ' desc'
    print(sql)
    # return sql

    cur = query(sql)
    t_list = []
    for h_tuple in cur.fetchall():
        t_list.append(h_tuple)
        print(h_tuple)

    return placeholder, t_list
    pass


@app.route('/post', methods=['POST'])
def post():
    pass


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
    # print(load_search_result('2','2','mutl','price'))
