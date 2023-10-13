#!/usr/bin/env python3
"""Module that defines a class `Review`"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Review class inheriting from BaseModel"""
    place_id = ""
    user_id = ""
    text = ""
