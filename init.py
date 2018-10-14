import os, re, sqlite3, uuid

conn = sqlite3.connect('small.db',detect_types=sqlite3.PARSE_DECLTYPES,check_same_thread=False)

def create_table():
    conn.execute("drop table if exists users")
    conn.execute('''create table users (
                    ID int primary key not null,
                    username char(50) not null,
                    password_hash char(128) not null,
                    full_name char(50) not null,
                    email char(50) not null,
                    home char(50),
                    home_latitude char(50),
                    home_longitude char(50),
                    home_suburb char(50));
                ''')

    conn.execute("drop table if exists hotel")
    conn.execute('''create table hotel (
                    userid char(50),
                    useremail char(50),
                    HouseID char(50) primary key not null,
                    RoomNo char(50),
                    Street char(50),
                    Suburb char(50),
                    State char(50),
                    Postcode char(50),
                    RoomType char(50),
                    Star char(50),
                    check_in_date char(50),
                    check_out_date char(50),
                    price int(50),
                    description char(255),
                    Image char(50),
                    post_time char(50),
                    booking char(50),
                    full_address char(255)
                    );
                    ''')

    conn.execute("drop table if exists booking")
    conn.execute('''create table booking (
                    ID primary key not null,
                    HouseID char(50),
                    Img char(50),
                    Address char(50),
                    Roomtype char(50),
                    Price char(50),
                    userid char(50),
                    start_time char(50),
                    end_time char(50));
                ''')

    conn.execute("drop table if exists messages")
    conn.execute('''create table messages (
                    ID int primary key not null,
                    mid char(50) not null,
                    userid char(50) not null,
                    message char(50) not null,
                    time char(50));
                ''')

    conn.execute("drop table if exists comments")
    conn.execute('''create table comments (
                   ID int primary key not null,
                   message char(50),
                   requestID int not null,
                   userID char(50) not null,
                   time char(50));
                ''')

    conn.execute("drop table if exists requests")
    conn.execute('''create table requests(
                    ID int primary key not null,
                    title char(50) not null,
                    address char(50) not null,
                    room_num int not null,
                    start_date char(50) not null,
                    end_date char(50) not null,
                    message char(250) not null,
                    user_id int );
                ''')


if __name__ == '__main__':
    create_table()

