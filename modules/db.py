import pymongo
from entities.fileEntity import File
from entities.knowledgeEntity import Knowledge


class MyDb:
    def __init__(self):
        self.client = None
        pass

    def connect(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")

    def add_file(self, file: File):
        x = self.client.Knowledge.files.insert_one(file.show())
        return x

    def add_file1(self, file: File):
        x = self.client.Knowledge.files.insert_one(file.show1())
        return x

    def save_file(self, file: File):
        x = self.client.Knowledge.files.save(file.show())
        return x

    def find_file(self, query):
        x = self.client.Knowledge.files.find(query)
        return x

    def add_knowledge(self, knowledge: Knowledge):
        x = self.client.Knowledge.knowledge.insert_one(knowledge.show())

    def find_knowledge(self, query):
        x = self.client.Knowledge.knowledge.find(query)
        return x


if __name__ == '__main__':
    db = MyDb()
    db.connect()
    db.add_file(File(_id='F0001', name='数据分析', url='www.baidu.com', labels=[]))
