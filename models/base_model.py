#!/usr/bin/env python3
"""A module that defines the BaseModel Class"""
import uuid
from datetime import datetime
from models import storage
class BaseModel():
    """The baseModel class"""
    
    def __init__(self, *args, **kwargs):
        """Initialization function"""
        valid_keys = ["created_at", "updated_at"]
        if (kwargs is None or len(kwargs) == 0):
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)
        else:
            self.id = kwargs.get("id", str(uuid.uuid4()))
            for i in valid_keys:
                setattr(self, i, datetime.fromisoformat(kwargs[i]))

    def __str__(self):
        """custom str function"""
        return (f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}")

    def save(self):
        "updates 'updated_at' with current datetime"
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values of __dict__"""
        keys = ['created_at', 'updated_at']
        result = {}

        for (key, value) in self.__dict__.items():
            if (key == "created_at" or key == "updated_at"):
                value = value.isoformat()
            result[key] = value
        
        return result
