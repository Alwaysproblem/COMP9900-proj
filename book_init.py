import os, re, sqlite3, uuid

conn = sqlite3.connect('book.db',detect_types=sqlite3.PARSE_DECLTYPES,check_same_thread=False)

def create_table():
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


# if __name__ == '__main__':
    # create_table()

cur = conn.cursor()


house_id = house_img = house_address = house_roomtype = house_price = current_user = start_date = end_date = None
# sql = 'select * from booking'
key = '"ID", "HouseID", "Img", "Address", "Roomtype", "Price", "userid", "start_time", "end_time"'
sql = "insert into booking (" + key + ") values ('{}','{}','{}','{}','{}','{}','{}','{}','{}')".format \
    (uuid.uuid4(), house_id, house_img, house_address, house_roomtype, house_price, current_user, start_date,
     end_date)
print(sql)
cur.execute(sql)
# cur.close()
conn.commit()
sql = 'select * from booking'
cur.execute(sql)
t_list = []
for h_tuple in cur.fetchall():
    t_list.append(h_tuple)
print('tlist', t_list)


