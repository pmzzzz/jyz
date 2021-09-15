import os
import time
from flask import (
    Blueprint, request, send_from_directory, jsonify, render_template
)
from modules.db import MyDb

bp = Blueprint('course', __name__, url_prefix='/course')


@bp.route('/search')
def search_course():
    label = request.args.get("label")
    db = MyDb()
    db.connect()
    course_collection = db.client.Knowledge.courseCollections
    x = course_collection.find({'label': {'$in': [label]}})
    if x is not None:
        return {'courses': [{'course': i['course'], 'label': i['label']} for i in x]}


# @bp.route('/get')
# def search_course():
#     label = request.form.get("label")
#     db = MyDb()
#     db.connect()
#     course_collection = db.client.Knowledge.courseCollections
#     x = course_collection.find_one({'label': {'$in': [label]}})
#     print(x)
#     return {'course': x['course'], 'label': x['label']}


@bp.route('/')
def course_index():
    return render_template('index.html')
