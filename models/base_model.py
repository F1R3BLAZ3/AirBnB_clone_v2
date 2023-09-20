#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
import models
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.utcnow()
        else:
            if '__class__' in kwargs:
                del kwargs['__class__']
                
            for key, value in kwargs.items():
                if key != '__class__':
                    setattr(self, key, value)
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())
            if 'created_at' not in kwargs:
                self.created_at = self.updated_at = datetime.utcnow()

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.save()
    
    def to_dict(self):
        dictionary = dict(self.__dict__)
        dictionary['__class__'] = self.__class__.__name__

        if 'created_at' in dictionary and \
                isinstance(dictionary['created_at'], datetime):
            dictionary['created_at'] = dictionary['created_at'].isoformat()

        if 'updated_at' in dictionary and \
                isinstance(dictionary['updated_at'], datetime):
            dictionary['updated_at'] = dictionary['updated_at'].isoformat()

        if '_sa_instance_state' in dictionary:
            del dictionary['_sa_instance_state']
        return dictionary

    def delete(self):
        """ Deletes the current instance from storage """
        models.storage.delete(self)
