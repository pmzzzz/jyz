from entities.labelEntity import Label
import xmindparser  # xmind解析器


def stick_label_and_update(label_collection, material, collection):
    """
    将material中的标签贴给file
    :param label_collection:
    :param material: xmind解析的目录
    :param collection: 存file的collection
    :return:
    """
    if type(material) == str or not material:
        for label in label_collection:
            if collection.find_one({'$and': [{'labels.value': {'$in': [label]}}, {'name': material}]}) is None:
                print(label_collection)
                collection.update_one({'$and': [{'name': material}, {'labels.type': '领域'}]},
                                      {'$push': {'labels.$.value': label}})
        return

    for material_k, material_v in material.items():
        label_collection.append(material_k)
        for item in material_v:  # 进入内层。内层material_v是一个列表（内部的值有三种情况：字典、字符串、空），因此需要依次遍历。
            stick_label_and_update(label_collection, item, collection)
        label_collection.pop()  # 最后记得回溯一下，把之前的标签清空


def parse_xmind(x: str):
    """
    返回解析xmin后的结果
    :param x: xmind文件的目录
    :return: 解析的结果
    """
    xmindparser.config = {
        'showTopicId': True,  # 是否展示主题ID
        'hideEmptyValue': True  # 是否隐藏空值
    }
    file_path = x
    content = xmindparser.xmind_to_dict(file_path)
    print(content)
    data = content[0]['topic']
    res = get_course_from_xmind(data)
    return res


def get_course_from_xmind(data: dict):
    if 'topics' not in data:
        return data['title']
    return {data['title']: [get_course_from_xmind(i) for i in data['topics']]}


def course_label(material, label_of_path):
    # 如果item不是字典，则说明已经走到最底层了，应该输出打印并返回上层。
    if type(material) == str or not material:
        label_of_path.add(material)
        return
    # 进入外层的字典，并获取外层的键作为共有标签
    for material_k, material_v in material.items():
        label_of_path.add(material_k)
        # 进入内层。内层material_v是一个列表（内部的值有三种情况：字典、字符串、空），因此需要依次遍历。
        for item in material_v:
            course_label(item, label_of_path)


if __name__ == '__main__':
    from modules.db import MyDb

    db = MyDb()
    db.connect()
    collection = db.client.Knowledge.files
    x = '/Users/pmzz/Documents/茜总框架/数据分析体系.xmind'
    print([i for i in collection.find()])
    res = parse_xmind(x)
    print(res)
