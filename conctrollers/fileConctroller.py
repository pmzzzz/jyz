import os
import time
from flask import (
    Blueprint, request, send_from_directory, jsonify
)
from pymongo.errors import DuplicateKeyError
from werkzeug.utils import secure_filename

from fileModule import push_file_label_by_name, __all_file_name, search_file_by_label_type, delete_file, \
    push_file_labels_by_name, __all_file
from labelEntity import Label
from modules.db import MyDb
from entities.fileEntity import File
from utils import assemble
from utils import path
from utils.exchange import prefix

bp = Blueprint('file', __name__, url_prefix='/file')
bp.config = {'UPLOAD_FOLDER': 'upload/'}


@bp.route('/insert', methods=['POST'])
def insert_file():
    form = request.form
    _id = ''
    name = form['name'].strip()
    file = request.files['file']
    url = ''
    if file:
        url = ''.join([str(int(time.time())), '.', file.filename.split('.')[1]])
        file.save(os.path.join(bp.config['UPLOAD_FOLDER'], secure_filename(url)))
    labelk = form['labelk']
    labelv = form['labelv']

    label = Label(k=labelk, v=[labelv])
    labels = [label]
    f = File(_id, name, url, labels)
    print(f.show())
    db = MyDb()
    db.connect()
    try:
        db.add_file(f)
    except DuplicateKeyError as e:
        return jsonify({'msg': 'error', 'result': 'id已存在'})
    return jsonify({'msg': 'success', 'filename': url})


@bp.route('/insert1', methods=['POST'])
def insert_super():
    form = request.form
    _id = ''
    name = form['name'].strip()
    url = ''
    f = File(_id, name, url)
    print(f.show1())
    db = MyDb()
    db.connect()
    try:
        db.add_file1(f)
    except DuplicateKeyError as e:
        db.add_file1(f)
        print({'msg': 'error', 'result': 'id已存在'})
    return jsonify({'msg': 'success', 'filename': url})


@bp.route('/')
def insex_file():
    db = MyDb()
    db.connect()
    x = [i for i in db.client.Knowledge.files.find()]
    return {'result': x}


@bp.route('/search')
def search_file():
    kw = request.args.get('kw')

    db = MyDb()
    db.connect()
    vs = [i for i in kw.split(',')]
    x = [i for i in db.client.Knowledge.files.find({'labels': {'$elemMatch': {'value': {'$in': vs}}}})]
    return {'result': x}


@bp.route('/update_label/<string:name>', methods=['GET', 'POST'])
def add_label(name):
    form = request.form
    labelk = form['labelk']
    labelv = form['labelv']
    push_file_labels_by_name(name, labelk, labelv)
    return {'msg': 'success'}


@bp.route('/push_label', methods=['GET', 'POST'])
def push_label():
    form = request.form
    name = form['name']
    type_ = form['labelk']
    value = form['labelv']
    push_file_label_by_name(name, type_, value)
    return {'msg', 'success'}


@bp.route('/add_next_from_xmind', methods=['POST', 'GET'])
def add_next_from_xmind():
    fp = None
    try:
        f = request.files['file']
        fp = './temp/' + str(int(time.time())) + '.' + f.filename.split('.')[-1]
        f.save(fp)
        pairs, all_last_name = assemble.parse_xmind_next(fp)
        # 验证是否全部存在
        notin = []
        for i in all_last_name:
            if i not in __all_file_name():
                notin.append(i)
        if not notin:
            for i in pairs:
                push_file_label_by_name(i[0], 'next', i[1])
        else:
            return {'msg': "错误", 'notin': notin}
    except Exception as e:
        return {"msg": 'error', 'excption': str(e)}
    finally:
        if fp is not None:
            os.remove(fp)
    return {'msg': 'success', 'pairs': pairs}


@bp.route('/get_path')
def get_path_by_domain():
    domain_type = request.args.get('type')
    domain_value = request.args.get('value')
    data = search_file_by_label_type(type_=domain_type, value=domain_value)
    head = 'python是什么'
    path.get_path2(head, data, [])
    x = path.all_path
    path.all_path = []
    return jsonify({'total':len(x),'result': x, 'data': data})


@bp.route('/delete/<string:name>')
def delete(name):
    delete_file(name)
    return {'msg': 'success'}


@bp.route('/all_path')
def get_all_path():
    data = __all_file()
    names = __all_file_name()
    max_path_length = 0
    res = []
    for i in names:
        print(i)
        path.get_path2(i, data, [])
        all_path = path.all_path
        path.all_path = []
        a_path_max_length = max(list(map(lambda x: len(x), all_path)))
        print(i, a_path_max_length)
        if a_path_max_length > max_path_length:
            max_path_length = a_path_max_length
            res = all_path
        result = [[j['name'] for j in i] for i in res]
    return jsonify({'total': len(result), 'result': result})


if __name__ == '__main__':
    pass
