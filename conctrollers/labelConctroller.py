from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

from entities.labelEntity import Label

bp = Blueprint('label', __name__, url_prefix='/label')


@bp.route('/insert', methods=('GET', 'POST'))
def insert_label():
    if request.method == 'POST':
        key = request.form['key']
        value = request.form['value']
        label = Label()
        label.k = key
        label.v = value
        label.save()
        return jsonify({'label': Label.objects.all()}), 201
    else:
        return '弄好'


@bp.route('/delete/<label_id>', methods=('GET', 'POST'))
def delete_label(label_id):
    print(label_id)
    if request.method == 'POST':
        return jsonify({'label': Label.objects.all()}), 201
    else:
        return label_id
