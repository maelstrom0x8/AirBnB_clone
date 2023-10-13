#!/usr/bin/env python3
"""A module that defines the storage class"""
import json


class FileStorage():
    """File storage class"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns list of data"""
        return FileStorage.__objects

    def new(self, obj):
        """adds new data to the list"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """saves data to fille storage"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)

            for i in temp:
                temp[i] = temp[i].to_dict()
            json.dump(temp, f)

    def reload(self):
        """reloads previously stored data to the list of objects"""
        from models.base_model import BaseModel
        from models.city import City
        from models.place import Place
        from models.state import State
        from models.user import User

        class_map = {
            'BaseModel': BaseModel,
            'City': City,
            'place': Place,
            'state': State,
            'User': User
        }
        try:
            with open(self.__file_path, 'r') as f:
                result = json.load(f)
                for (key, value) in result.items():
                    FileStorage.__objects[key] = class_map[value["__class__"]](
                        **value)
        except FileNotFoundError:
            pass
