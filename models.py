from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
import os
import sys
import csv

engine = create_engine('sqlite:///data.db')
Base = declarative_base()


# class User(Base):
#     __tablename__ = "user"
#     username = Column(Integer, primary_key=True)
#     password = Column(Text)
#     email = Column(Text)
#     role = Column(Text)
#
#     def __init__(self, username, password, email, role):
#         self.username = username
#         self.password = password
#         self.email = email
#         self.role = role
#
#     def is_authenticated(self):
#         return True
#
#     def is_active(self):
#         return True
#
#     def is_anonymous(self):
#         return False
#
#     def get_id(self):
#         return self.username


class request_list(Base):
    __tablename__ = 'request'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text)
    address = Column(Text)
    room_num = Column(Integer)
    start_date = Column(Text)
    end_date = Column(Text)
    message = Column(String(250))
    # user = relationship(User)


class System(object):

    def create_table(self):
        Base.metadata.create_all(engine)

    def post_request(self, title, address, room_num, start_date, end_date, message):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        new_request = request_list(title=title, address=address, room_num=room_num, start_date=start_date,
                                   end_date=end_date,
                                   message=message)
        session.add(new_request)
        session.commit()

    def get_request_message(self, title):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        arequests = session.query(request_list).filter(request_list.title == title).all()
        arequest = [arequest.message for arequest in arequests]
        session.commit()
        return arequest

    def get_request_address(self, title):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        arequests = session.query(request_list).filter(request_list.title == title).all()
        arequest = [arequest.address for arequest in arequests]
        session.commit()
        return arequest

    def get_request_roomnum(self, title):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        arequests = session.query(request_list).filter(request_list.title == title).all()
        arequest = [arequest.room_num for arequest in arequests]
        session.commit()
        return arequest

    def get_request_start(self, title):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        arequests = session.query(request_list).filter(request_list.title == title).all()
        arequest = [arequest.start_date for arequest in arequests]
        session.commit()
        return arequest

    def get_request_end(self, title):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        arequests = session.query(request_list).filter(request_list.title == title).all()
        arequest = [arequest.end_date for arequest in arequests]
        session.commit()
        return arequest

    def list_request(self):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        finds = session.query(request_list).all()
        requests = []
        for find in finds:
            re = find.title
            requests.append(re)
        session.commit()
        return requests
