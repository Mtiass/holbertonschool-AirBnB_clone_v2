#!/usr/bin/python3
from models.city import City
from models.state import State
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.base_model import BaseModel, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        user = os.environ.get("HBNB_MYSQL_USER")
        password = os.environ.get("HBNB_MYSQL_PWD")
        host = os.environ.get("HBNB_MYSQL_HOST")
        database = os.environ.get("HBNB_MYSQL_DB")
        env = os.environ.get("HBNB_ENV")
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}:3306/{}".
                                      format(user, password, host, database),
                                      pool_pre_ping=True)

        Session = sessionmaker(bind=self.__engine)
        Session.configure(bind=self.__engine)
        self.__session = Session()

        if env == "test":
            Base.metadata.drop_all(self.__engine)
        Base.metadata.create_all(self.__engine)

    def new(self, obj):
        """new method"""
        self.__session.add(obj)

    def save(self):
        """save method"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete method"""
        if obj is None:
            return
        else:
            self.__session.delete(obj)

    def reload(self):
        """reload method"""
        from sqlalchemy.ext.declarative import declarative_base

        Base = declarative_base()
        s = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(s)
        Base.metadata.create_all(self.__engine)
