#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    """When a state object is deleted, all linked City objects are deleted"""
    cities = relationship("City",
                          backref="state",
                          cascade="all, delete-orphan")

    @property
    def cities(self):
        """Getter attribute that returns the list of City objects from storage
        linked to the current State"""
        city_instances = storage.all("City").values()
        return [city for city in city_instances if city.state.id == self.id]
