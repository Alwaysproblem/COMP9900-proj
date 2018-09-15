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


# def load_hotel_info():
#     conn.execute("delete from hotel")
#     key = '"useremail", "HouseID", "RoomNo", "hotel_class", "guest_renting", "room_type", "price"'
#     value = '"1", "1", "isis", "5", "4", "single", 500'
#     sql = 'insert into hotel (' + key + ') values (' + value + ')'
#     conn.execute(sql)
#     value = '"2", "2", "saf", "4", "3", "double", 400'
#     sql = 'insert into hotel (' + key + ') values (' + value + ')'
#     conn.execute(sql)
#     value = '"3", "3", "afea", "3", "5", "family", 600'
#     sql = 'insert into hotel (' + key + ') values (' + value + ')'
#     conn.execute(sql)
#     value = '"4", "4", "afafe", "2", "4", "multiple", 600'
#     sql = 'insert into hotel (' + key + ') values (' + value + ')'
#     conn.execute(sql)
#     value = '"5", "5", "aeaeae", "1", "1", "double", 200'
#     sql = 'insert into hotel (' + key + ') values (' + value + ')'
#     conn.execute(sql)
#     value = '"6", "6", "isisas", "5", "3", "multiple", 350'
#     sql = 'insert into hotel (' + key + ') values (' + value + ')'
#     conn.execute(sql)
#     conn.commit()
#     # key += ', "' + match.group(1) + '"'
#     # value += ', "' + match.group(2) + '"'
#     # sql = 'insert into students (' + key + ') values (' + value + ')'
# # print(sql)
# #     conn.execute(sql)
# #     conn.commit()

# create_table()
# load_hotel_info()
# detial = str(5)
# # sql = 'select * from hotel where hotel_class = 5'
# hotelclass = '-1'
# guestrenting = '-1'
# roomtype = ''
# # sql = 'select ID, hotelid, hotel, hotel_class, guest_renting from hotel '
# sql = 'select * from hotel where '+'(hotel_class = 2 or hotel_class = 1 or hotel_class = 0) and (guest_renting = 2 or guest_renting = 1 or guest_renting = 0) and room_type = "double" order by price desc'
# print(sql)
# # sql = 'select ID, hotelid, hotel, hotel_class from hotel '
# cursor = conn.execute(sql)
# for row in cursor:
#     print(row)
#     # cid = row[0]
#     # mid = row[1]