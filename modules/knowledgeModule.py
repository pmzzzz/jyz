from db import MyDb
from entities.knowledgeEntity import Knowledge


class KnowledgeModule:
    def __init__(self):
        pass

    def add_knowledge(self, knowledge: Knowledge):
        md = MyDb()
        md.connect()
        md.client.files.insert_one(knowledge.show())
        print(self)
        pass
