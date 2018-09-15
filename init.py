import os, re, sqlite3, uuid

conn = sqlite3.connect('small.db',detect_types=sqlite3.PARSE_DECLTYPES,check_same_thread=False)

def create_table():
    with conn:
        conn.execute("drop table if exists users")
        conn.execute('''create table users (
                        ID int primary key not null,
                        userid char(50) not null,
                        password char(50) not null,
                        full_name char(50) not null,
                        email char(50) not null,
                        home char(50),
                        home_latitude char(50),
                        home_longitude char(50),
                        home_suburb char(50));
                    ''')

        conn.execute("drop table if exists hotel")
        conn.execute('''create table hotel (
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
                        price int(50));
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
                    cid char(50) not null,
                    mid char(50) not null,
                    message char(50),
                    userid char(50) not null,
                    muserid char(50) not null,
                    time char(50));
                    ''')

    conn.close()

def main():
    create_table()

if __name__ == '__main__':
    main()