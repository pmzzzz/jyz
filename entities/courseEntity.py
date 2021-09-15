import random

from utils.exchange import prefix


class Course:
    def __init__(self, _id, name, knowledge, labels):
        self._id = _id
        self.name = name
        self.knowledge = knowledge
        self.labels = labels

    def show(self):
        if self._id == "":
            self._id = prefix(6, random.randint(1, 99999), 'L')
        data = {
            "_id": self._id,
            "name": self.name,
            "knowledge": [i.show() for i in self.knowledge],
            "labels": [i.show() for i in self.labels]
        }
        return data

    def load(self, data: dict):
        self._id = data['_id']
        self.name = data['name']
        self.knowledge = data['knowledge']
        self.labels = data['labels']
