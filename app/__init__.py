import os
import random
import time

from flask import Flask, render_template, request, send_from_directory, redirect, jsonify, url_for
from werkzeug.utils import secure_filename

from conctrollers.adminConctroller import bp
from conctrollers.fileConctroller import bp as bpf
from conctrollers.labelConctroller import bp as bpl
from conctrollers.userConctroller import bp as bpu
from conctrollers.courseConctroller import bp as cpu
from utils import assemble
from modules.db import MyDb
from utils.exchange import prefix

app = Flask(__name__, template_folder='../templates', static_folder="../static", static_url_path="")

UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # 设置文件上传的目标文件夹
basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前项目的绝对路径
# ALLOWED_EXTENSIONS = {'txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF'}  # 允许上传的文件后缀


# app.config['MONGODB_SETTINGS'] = {
#     'db': 'Knowledge',
#     'host': '127.0.0.1',
#     'port': 27017
# }
app.config["MONGO_URI"] = "mongodb://localhost:27017/Knowledge"

# mongo = PyMongo(app)

app.register_blueprint(bp)

app.register_blueprint(bpf)

app.register_blueprint(bpl)

app.register_blueprint(bpu)

app.register_blueprint(cpu)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/file/upload', methods=['POST'])
def upload_file():
    f = request.files['file']
    print(request.files)
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
    return {'msg': 'success', 'url': ''}


@app.route("/file/download/<filename>", methods=['GET'])
def downloader(filename):
    print(filename)
    dirpath = os.path.join(app.root_path, '../upload')  # 这里是下在目录，从工程的根目录写起，比如你要下载static/js里面的js文件，这里就要写“static/js”
    # dirpath = app.config['UPLOAD_FOLDER']
    print(dirpath)
    return send_from_directory(dirpath, filename, as_attachment=True)  # as_attachment=True 一定要写，不然会变成打开，而不是下载


@app.route('/api/parsexmind', methods=['POST', 'GET'])
def parse_xmind():
    fp = None
    try:
        f = request.files['file']
        fp = './temp/' + str(int(time.time())) + '.' + f.filename.split('.')[-1]
        f.save(fp)
        res = assemble.parse_xmind(fp)
    except:
        return '错误'
    finally:
        if fp is not None:
            os.remove(fp)
    return res


@app.route('/api/insertxmind', methods=['POST', 'GET'])
def insrt_xmind():
    fp = None
    try:
        f = request.files['file']
        fp = './temp/' + str(int(time.time())) + '.' + f.filename.split('.')[-1]
        f.save(fp)
        res = assemble.parse_xmind(fp)
        myset = set()
        res = assemble.parse_xmind(fp)
        assemble.course_label(res, myset)  # xmind导入
        labels = list(myset)
        db = MyDb()
        db.connect()
        course_collection = db.client.Knowledge.courseCollections
        id_ = prefix(6, random.randint(1, 99999), 'C')
        course = {'_id': id_, 'course': res, 'label': labels}
        if course_collection.find_one({'label': labels}) is None:
            course_collection.insert_one(course)  # xmind导入
        else:
            print('xxxx')
    except:
        return '错误'
    finally:
        if fp is not None:
            os.remove(fp)
    return {'course': res, 'label': labels}
