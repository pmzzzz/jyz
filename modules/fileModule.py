from db import MyDb
from entities.fileEntity import File


# 添加
def add_file(file: File):
    """
    插入新的file
    :param file:
    :return:
    """
    db = MyDb()
    db.connect()
    db.client.Knowledg.files.insert_one(file.show())


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
    db.client.Knowledge.files.update_one({'$and': [{'name': name}, {'labels.type': type_}]},
                                         {'$push': {'labels.$.value': value}})
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
    db.client.Knowledge.files.update_one({'$and': [{'_id': id_}, {'labels.type': type_}]},
                                         {'$push': {'labels.$.value': value}})
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


if __name__ == '__main__':
    x = search_file_by_label('python')
    for i in x:
        print(i)

    # add_label('F059322','next','F041076,F062153')
    print(get_next('F059322'))
    # print(get_file_by_id('F059322'))
