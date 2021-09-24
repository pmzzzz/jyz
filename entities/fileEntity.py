import random

from utils.exchange import prefix
from labelEntity import Label


class File:
    def __init__(self, _id='', name='', url='', labels=[]):
        self._id = _id
        self.name = name
        self.url = url
        self.labels = labels

    def load(self, data: dict):
        """
        从字典加载File对象（从数据库中获取）
        :param data: 字典类型对象
        :return:
        """
        self._id = data['_id']
        self.name = data['name']
        self.url = data['url']
        self.labels = data['labels']

    def show(self):
        """

        :return: 能够存入mongodb的字典对象
        """
        if self._id == "":
            self._id = prefix(6, random.randint(1, 99999), 'F')
        data = {
            "_id": self._id,
            "name": self.name,
            "url": self.url,
            "labels": [i.show() for i in self.labels]
        }
        return data

    def show1(self):
        """

        :return: 能够存入mongodb的字典对象
        """
        if self._id == "":
            self._id = prefix(6, random.randint(1, 99999), 'F')
        data = {
            "_id": self._id,
            "name": self.name,
            "url": self.url,
            "labels": []
        }
        return data

    def add_label(self, label: Label):
        self.labels.append(label)
