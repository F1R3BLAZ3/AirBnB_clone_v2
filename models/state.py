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
        """
        Getter for the cities linked to the state
        """
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            from models import storage
            from models.city import City

            # Get the related City objects using a list comprehension
            city_instances = [city for city in storage.all(City).values()
                              if city.state_id == self.id]
            return city_instances
        else:
            # In case of FileStorage, you can keep the existing code
            return [city for city in models.storage.all(models.City).values()
                    if city.state_id == self.id]
