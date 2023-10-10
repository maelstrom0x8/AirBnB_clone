#!/usr/bin/env python3
import json
class FileStorage():
    __file_path = "file.json"
    __objects = {}

    def all(self):
        return self.__objects
    
    def new(self, obj):
        key = f"{obj.__class__.__name__}.{obj.id}"
        data = obj.to_dict()
        self.__objects[key] = data

    def save(self):
        with open(self.__file_path, 'a', encoding="utf-8") as f:
            json.dump(self.__objects, f)
    
    def reload(self):
        try:
            with open(self.__file_path) as f:
                data = json.load(f)
                self.new(data)
        except Exception:
            pass
