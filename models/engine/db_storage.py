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
        
    def all(self, cls=None):
        """ query on the current database session """
        dic = {}
        if os.getenv("HBNB_ENV") == "test":
            xd = self.__session.query(State).all()
        else:
            if cls is None:
                xd = self.__session.query(State, City, Place,
                                         Review, User, Amenity).all()
            else:
                xd = self.__session.query(cls).all()

        for obj in xd:
            # delattr(obj,"_sa_instance_state") sert à rien
            dic[f"{obj.__class__.__name__}.{obj.id}"] = obj

        return dic


    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj is None:
            return
        else:
            self.__session.delete(obj)

    def reload(self):
        from sqlalchemy.ext.declarative import declarative_base

        Base = declarative_base()
        s = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(s)
        Base.metadata.create_all(self.__engine)
