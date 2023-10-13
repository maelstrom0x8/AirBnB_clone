#!/usr/bin/env python3
"""Module that defines a class `City`"""
from models.base_model import BaseModel


class City(BaseModel):
    """City class inheriting from the Base Model"""
    state_id = ""
    name = ""
