from entities.fileEntity import File
from entities.labelEntity import Label

l1 = Label('L00001', '类型', '视频')
l2 = Label('L00002', '时长', '80')
l3 = Label('L00003', '难度', '4')
l4 = Label('L00004', '时长', '40')
l5 = Label('L0005', '领域', '新零售')

f1 = File('F00001', '数据采集', 'WWW.baidu.com', [l1, l2, l3])
f2 = File('F00002', '数据存储', 'www.googel.com', [l1, l4])
f3 = File('F00003', '数据分析', 'www.bilibili.com', [l1, l2, l4, l5])
f4 = File('F00004', '数据预处理', 'www.bilibili.com', [l2, l5])
f5 = File('F00005', '可视化', 'www.googel.com', [l1, l4])

print(f1.show())
