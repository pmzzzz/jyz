import pandas as pd
import numpy as np


def xxx(l, i):
    """
    从l中取出i传入的区间 例如[1,2,3],[0,1]---->[1]
    :param l: 要分割的列表
    :param i: 区间的前后索引
    :return: l中i区间的值
    """
    x = l[i[0]:i[1]]
    if len(x) > 0:
        return x


def w2(l):
    """
    将列表拆成两两组合的列表，例如[1,2,3] ----> [[1,2],[2,3]]
    :param l: 列表
    :return: 列表两两组合的列表
    """
    res = []
    for i, j in enumerate(l):
        if i < len(l) - 1:
            tem = []
            tem.append(j)
            tem.append(l[i + 1])
            res.append(tem)
    return res


def super_split(l: list, i: list) -> list:
    """
    将l按照i的值分割，例如[1,2,3,4,5,6] [3] --->[[1,2,3],[4,5]]
    :param l: 被分割的列表
    :param i: 分割的index列表
    :return: 分割好的列表
    """
    i.insert(0, 0)
    i.append(-1)
    res = []
    for xxxx in w2(i):
        x = xxx(l, xxxx)
        if x:
            res.append(x)
    return res


# 定义前缀补充方法
def prefix(max_len, number, pre):
    str_len = len(str(number))
    if max_len > str_len:
        return pre + '0' * (max_len - str_len) + str(number)


def parse_xlsx_get_label(fp):
    x = pd.read_excel(fp)
    for i in range(len(x)):
        if x.iloc[i, 0] is np.nan:
            x.iloc[i, :2] = x.iloc[i - 1, :2]
    return x.iloc[:, [0, 2, 3]]


def parse_xlsx_get_name_path(fp):
    x = pd.read_excel(fp)
    x = x.dropna(subset=['name'])
    return x.iloc[:,:2]


if __name__ == '__main__':
    x = parse_xlsx_get_label('/Users/pmzz/dev/codingworks/3+1标签demo.xlsx')
    y = parse_xlsx_get_name_path('/Users/pmzz/dev/codingworks/3+1标签demo.xlsx')
    print(y)
