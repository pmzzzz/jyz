import random

from utils.exchange import prefix


class Knowledge:
    def __init__(self, _id='', name='', file=None, sub=None):
        self._id = _id
        self.name = name
        self.file = file
        self.sub = sub

    def show(self):
        if self._id == "":
            self._id = prefix(6, random.randint(1, 99999), 'L')
        data = {
            "_id": self._id,
            "name": self.name,
            "file": [i.show() for i in self.file],
            "sub": [i.show() for i in self.sub]
        }
        return data

    def load(self, data: dict):
        self._id = data['_id']
        self.name = data['name']
        self.file = data['file']
        self.sub = data['sub']
