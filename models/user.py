#!/usr/bin/env python3

from models.base_model import BaseModel
"""Module that defines a class `User`"""


class User(BaseModel):
    """User class inheriting from the BaseModel"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
