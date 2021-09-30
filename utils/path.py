import jsonpath

all_path = []


def get_path(head, data, path=[]):
    """
    返回所有路径
    :param path: 初始化路径
    :param head: 头部的名称
    :param data: 所有的数据
    :return: 所有的路径
    """
    x = get_data_by_name(head, data)
    path.append(x)
    if path[-1] is None:
        all_path.append([i for i in path[:-1]])
        return
    elif not ('next' in path[-1].keys()):
        all_path.append([i for i in path[:-1]])
        return
    elif not path[-1]['next']:
        all_path.append([i for i in path[:-1]])
        return
    else:
        for i in path[-1]['next']:
            get_path(i, data, path)
            path.pop()


def get_path1(head, data, path=[]):
    """
    返回所有路径
    :param path: 初始化路径
    :param head: 头部的名称
    :param data: 所有的数据
    :return: 所有的路径
    """
    x = get_data_by_name(head, data)
    path.append(x)
    if path[-1] is None:
        all_path.append([i for i in path[:-1]])
        return
    elif not jsonpath.jsonpath(path[-1], '$..next'):
        all_path.append([i for i in path[:-1]])
        return
    elif not jsonpath.jsonpath(path[-1], '$..next')[0]:
        all_path.append([i for i in path[:-1]])
        return
    else:
        for i in jsonpath.jsonpath(path[-1], '$..next')[0]:
            get_path1(i, data, path)
            path.pop()


def get_path2(head, data, path=[]):
    """
    返回所有路径
    :param path: 初始化路径
    :param head: 头部的名称
    :param data: 所有的数据
    :return: 所有的路径
    """
    x = get_data_by_name(head, data)
    path.append(x)
    if path[-1] is None:
        all_path.append([i for i in path[:-1]])
        return
    elif not get_next(path[-1]):
        all_path.append([i for i in path[:-1]])
        return
    # elif not :
    #     all_path.append([i for i in path[:-1]])
    #     return
    else:
        for i in get_next(path[-1]):
            get_path2(i, data, path)
            path.pop()


def get_next(d):
    res = None
    for i in d['labels']:
        if i['type'] == 'next':
            res = i['value']
    # print('nxdfss',res)
    return res


def get_data_by_name(name, data):
    res = None
    for i in data:
        if i['name'] == name:
            res = i
    return res
