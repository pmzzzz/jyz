import random

import jsonpath

from db import MyDb
from entities.fileEntity import File

# 添加
from utils.exchange import prefix


def add_file(file: File):
    """
    插入新的file
    :param file:
    :return:
    """
    db = MyDb()
    db.connect()
    db.client.Knowledg.files.insert_one(file.show())


def add_file_name_path(name, url):
    _id = prefix(6, random.randint(1, 99999), 'F')
    data = {"_id": _id,
            'name': name,
            'url': url,
            'labels': []
            }


# 修改
def add_label(id_, k, v):
    """
    向指定file添加一个标签
    :param id_:
    :param k: 标签类型
    :param v: 标签值，以逗号隔开
    :return:
    """
    db = MyDb()
    db.connect()
    db.client.Knowledge.files.update_one({'_id': id_}, {'$push': {'labels': {'type': k, 'value': v.split(',')}}})


def add_label_by_name(name, k, v):
    """
    向指定file添加一个标签
    :param id_:
    :param k: 标签类型
    :param v: 标签值，以逗号隔开
    :return:
    """
    db = MyDb()
    db.connect()
    db.client.Knowledge.files.update_one({'name': name}, {'$push': {'labels': {'type': k, 'value': v.split(',')}}})


def add_next(id_, v):
    """
    添加next标签
    :param id_: 需要添加的id
    :param v: next的id，以逗号隔开
    :return:
    """
    db = MyDb()
    db.connect()

    db.client.Knowledge.files.update_one({'_id': id_}, )


def remove_next(pre_id, next_id):
    pass


def push_file_label_by_name(name, type_, value):
    """
    向指定file指定标签插入新的值
    :param name: 修改file的名称
    :param type_:标签类型
    :param value:push的值
    :return:
    """
    db = MyDb()
    db.connect()
    x = db.client.Knowledge.files.find_one({'$and': [{'name': name}, {'labels.type': type_}]})
    print('scssds', x)
    if x:
        db.client.Knowledge.files.update_one({'$and': [{'name': name}, {'labels.type': type_}]},
                                             {'$push': {'labels.$.value': value}})
    else:
        print('已创建新的标签{}、{}、{}'.format(name, type_, value))
        add_label_by_name(name, type_, value)
    return True


def push_file_label_by_id(id_, type_, value):
    """
    向指定file指定标签插入新的值
    :param id_: 修改file的_id
    :param type_:标签类型
    :param value:push的值
    :return:
    """
    db = MyDb()
    db.connect()
    y = db.client.Knowledge.files.find_one({'$and': [{'_id': id_}, {'labels.type': type_}]})
    if y:
        db.client.Knowledge.files.update_one({'$and': [{'_id': id_}, {'labels.type': type_}]},
                                             {'$push': {'labels.$.value': value}})
    else:
        print('已创建新的标签{}、{}、{}'.format(id_, type_, value))
        add_label_by_name(id_, type_, value)
    return True


def push_file_labels_by_id(id_, type_, values):
    """
    向指定file指定标签插入新的值(多个)
    :param id_: 修改file的_id
    :param type_:标签类型
    :param values:push的值
    :return:
    """
    for i in values.split():
        push_file_label_by_id(id_, type_, i)
    return True


def push_file_labels_by_name(name, type_, values):
    """
    向指定file指定标签插入新的值(多个)
    :param name: 修改file的名称
    :param type_:标签类型
    :param values:push的值
    :return:
    """
    for i in values.split():
        push_file_label_by_name(name, type_, i)
    return True


# 查询
def __all_file() -> list:
    """
    查询所有文件
    :return:
    """
    db = MyDb()
    db.connect()
    files = db.client.Knowledge.files.find({})
    return [i for i in files]


def __all_file_id() -> list:
    """
    查询所有文件
    :return:
    """
    db = MyDb()
    db.connect()
    files = db.client.Knowledge.files.find({})
    return [i['_id'] for i in files]


def __all_file_name():
    files = __all_file()
    return [i['name'] for i in files]


def get_file_by_id(id_):
    db = MyDb()
    db.connect()
    return [i for i in db.client.Knowledge.files.find({'_id': id_})][0]


def search_file_by_label(value):
    db = MyDb()
    db.connect()
    vs = [i for i in value.split(',')]
    x = [i for i in db.client.Knowledge.files.find({'labels': {'$elemMatch': {'value': {'$in': vs}}}})]
    return x


def search_file_by_label_type(type_, value):
    db = MyDb()
    db.connect()
    vs = [i for i in value.split(',')]
    y = db.client.Knowledge.files.find({'labels.type': type_})
    print(y)
    x = [i for i in y]
    res = []
    for i in x:
        for j in i['labels']:
            if j['type'] == type_ and value in j['value']:
                res.append(i)
    return res


def get_next(id_):
    """
    返回所有next的file对象
    :param id_:要查询的file的id
    :return:
    """
    db = MyDb()
    db.connect()
    file = [i for i in db.client.Knowledge.files.find({'_id': id_})]
    print(type(file[0]))
    if file is not None:
        labels = file[0]['labels']
        next_ = [i for i in labels if i['type'] == 'next']
        if next_:
            ids = next_[0]['value']
            res = []
            for i in ids:
                res.append(get_file_by_id(i))
            return res
    else:
        return '文件不存在'


# 删除
def delete_file(name):
    db = MyDb()
    db.connect()
    db.client.Knowledge.files.remove({'name': name})


if __name__ == '__main__':
    # x = search_file_by_label('python')
    # for i in x:
    #     print(i)
    #
    # # add_label('F059322','next','F041076,F062153')
    # print(get_next('F059322'))
    # # print(get_file_by_id('F059322'))
    # print(__all_file_id())
    for i in __all_file():
        print(i)
    # # # print(__all_file_name())
    # for i in search_file_by_label_type('能力', '通识知识与技能'):
    #     print(i)
    #     print(jsonpath.jsonpath(i, '$..labels[type=next]'))
    a = {"name": 'a123', 'next': ['a124']}
    b = {"name": 'a124', 'next': ['a125']}
    c = {"name": 'a125', 'next': ['a126', 'a127']}
    d = {"name": 'a126', 'next': ['a127']}
    e = {"name": 'a127', 'next': ['a128']}
    test_data = [a, c, d, e, b]
    # import jsonpath

    # x = jsonpath.jsonpath(test_data[0], '$..next')
    # print(x)
    for i in __all_file():
        print(i)
