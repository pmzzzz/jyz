import os
import time
from flask import (
    Blueprint, request, send_from_directory, jsonify
)
from pymongo.errors import DuplicateKeyError
from werkzeug.utils import secure_filename

from labelEntity import Label
from modules.db import MyDb
from entities.fileEntity import File

bp = Blueprint('file', __name__, url_prefix='/file')
bp.config = {'UPLOAD_FOLDER': 'upload/'}


@bp.route('/insert', methods=['POST'])
def insert_file():
    form = request.form
    _id = ''
    name = form['name']
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
    label = Label(k=labelk, v=[i for i in labelv.split(',')])
    db = MyDb()
    db.connect()
    db.client.Knowledge.files.update({'name': name}, {'$push': {'labels': label.show()}})
    return 'x'
