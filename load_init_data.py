from utils import exchange

import requests

FILE_PATH = '/Users/pmzz/dev/codingworks/3+1标签demo.xlsx'
# FILE_PATH = './utils/hhhh.xlsx'

labels = exchange.parse_xlsx_get_label(FILE_PATH)

names_paths = exchange.parse_xlsx_get_name_path(FILE_PATH)

print(names_paths)


def insert_file(name, path):
    url = "http://127.0.0.1:5000/file/insert1"

    payload = {'name': name}
    headers = {}
    try:
        files = [
            ('file', ('{}'.format(path.split('/')[-1]), open(path, 'rb'), 'application/octet-stream'))
        ]
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
    except:
        response = requests.request("POST", url, headers=headers, data=payload,)
    print(response.text)


def update_labels(name, labelk, labelv):
    import requests

    url = "http://127.0.0.1:5000/file/update_label/{}".format(name)

    payload = {'labelk': labelk,
               'labelv': labelv
               }
    files = [

    ]
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload, files=files)

    print(response.text)


def insert_files():
    for i in names_paths.values:
        insert_file(i[0], i[1])


def insert_labels():
    for i in labels.values:
        update_labels(i[0], i[1], i[2])
    print(labels)


insert_files()
insert_labels()
#
if __name__ == '__main__':
    print(names_paths)
