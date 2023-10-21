#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import os


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship(
            'City', back_populates='state',
            cascade='all, delete, delete-orphan')

    else:
        name = ""

    @property
    def cities(self):
        """Getter attribute that returns the list of City objects from storage
        linked to the current State"""
        city_instances = self.cities
        return [city for city in city_instances if city.state_id == self.id]
