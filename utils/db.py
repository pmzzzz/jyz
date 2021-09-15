import pymongo
from bson import ObjectId


# client = pymongo.MongoClient('mongodb://localhost:27017/')

class MyDb:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.client = pymongo.MongoClient()

    def connect(self):
        self.client = pymongo.MongoClient('mongodb://{}:{}/'.format(self.host, self.port))

    def close(self):
        if self.client:
            self.client.close()
        else:
            raise Exception('还没连接')

    def insert_file(self, file: dict):
        col = self.client['Knowledge']['files']
        try:
            col.insert_one(file)
            return True
        except:
            raise Exception('插入失败')

    def search_file_by_id(self, _id):
        col = self.client['Knowledge']['files']
        try:
            x = col.find_one({'_id': _id})
        except:
            raise Exception('搜索失败')

    def insert_knowledge(self, knowledge: dict):
        col = self.client['Knowledge']['knowledge']
        try:
            col.insert_one(knowledge)
            return True
        except:
            raise Exception('插入失败')


if __name__ == '__main__':
    db = MyDb('localhost', 27017)
    db.connect()
    # db.insert_file({'name': 'anaconda的安装', 'url': 'www.baidu.com', 'labels': []})
    col = db.client['Knowledge']['files']
    x = col.find_one()
    print(x)
    db.close()
