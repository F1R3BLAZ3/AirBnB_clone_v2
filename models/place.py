#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from models.review import Review
from sqlalchemy.orm import relationship
from os import getenv

database_type = getenv("HBNB_TYPE_STORAGE")

place_amenity = Table(
    "place_amenity",
    Base.metadata,
    Column(
        "place_id",
        String(60),
        ForeignKey("places.id"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "amenity_id",
        String(60),
        ForeignKey("amenities.id"),
        primary_key=True,
        nullable=False,
    ),
)


class Place(BaseModel, Base):
    """
    Place class representing the 'places' table.

    Attributes:
        __tablename__ (str): The table name in the database.
        city_id (str): The ID of the associated city (foreign key).
        user_id (str): The ID of the associated user (foreign key).
        name (str): The name of the place.
        description (str): A description of the place.
        number_rooms (int): The number of rooms in the place.
        number_bathrooms (int): The number of bathrooms in the place.
        max_guest (int): The maximum number of guests the place can
        accommodate.
        price_by_night (int): The price per night for the place.
        latitude (float): The latitude coordinate of the place.
        longitude (float): The longitude coordinate of the place.
    """

    __tablename__ = 'places'

    if database_type == "db":
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        place_amenities = relationship(
            "Amenity",
            secondary=place_amenity,
            backref="places",
        )
        reviews = relationship(
            "Review", backref="place", cascade="all, delete-orphan")
        amenity_ids = []

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    @property
    def amenities(self):
        """Getter document"""
        from models import storage
        amenitiesList = []
        amenitiesAll = storage.all(Amenity)
        for amenity in amenitiesAll.values():
            if amenity.id in self.amenity_ids:
                amenitiesList.append(amenity)
        return amenitiesList

    @property
    def reviews(self):
        """Getter document"""
        from models import storage
        reviewsList = []
        reviewsAll = storage.all(Review)
        for review in reviewsAll.values():
            if review.place_id == self.id:
                reviewsList.append(review)
        return reviewsList

    @amenities.setter
    def amenities(self, amenity):
        """Setter document"""
        if isinstance(amenity, Amenity):
            self.amenity_ids.append(amenity.id)
