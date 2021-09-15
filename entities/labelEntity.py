import random
from utils.exchange import prefix


class Label:
    def __init__(self, _id='', k='', v=[]):
        self._id = _id
        self.k = k
        self.v = v

    def show(self):
        if self._id == "":
            self._id = prefix(6, random.randint(1, 99999), 'L')
        data = {
            '_id': self._id,
            'type': self.k,
            'value': self.v
        }
        return data

    def load(self, data: dict):
        self._id = data['_id']
        self.k = data['k']
        self.v = data['v']
