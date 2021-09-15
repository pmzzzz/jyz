from db import MyDb


def all_course():
    db = MyDb()
    db.connect()
    course_collection = db.client.Knowledge.courseCollections
    x = [i for i in course_collection.find({})]
    print(x[1])
    return x


def get_course_by_id(id_):
    db = MyDb()
    db.connect()
    course_collection = db.client.Knowledge.courseCollections


if __name__ == '__main__':
    all_course()
