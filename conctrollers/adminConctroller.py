import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/mind')
def a():
    return 'x'
