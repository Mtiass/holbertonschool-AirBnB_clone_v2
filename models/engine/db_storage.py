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
    """This class manages storage of hbnb models in a SQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the SQL database storage"""
        user = os.getenv('HBNB_MYSQL_USER')
        pword = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db_name = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')
        DATABASE_URL = "mysql+mysqldb://{}:{}@{}:3306/{}".format(
            user, pword, host, db_name
        )
        self.__engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True
        )
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

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
