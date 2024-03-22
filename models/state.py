#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"

    name = Column(
        String(128),
        nullable=False
    )

    state_id = Column(
        String(60),
        ForeignKey('states.id'),
        nullable=False
    )

    cities = relationship(
        "City",
        backref="state",
        cascade="all, delete",
        passive_deletes=True
    )

    @property
    def cities(self):
        """Getter for cities in FileStorage"""
        acities = self.cities
        filtercit = [city for city in acities if city.state_id == self.id]
        return filtercit
