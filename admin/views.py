from flask import Blueprint, render_template, request, redirect, session, jsonify, flash, url_for, abort
from functools import wraps
import hashlib
import json

#custom imports
from .models import Users

user_object = Users()

admin = Blueprint("admin", __name__, template_folder='templates', static_folder='static/admin',
                   static_url_path='static/admin')


@admin.errorhandler(404)
def page_not_found(error):
    return render_template('admin/404.html'), 404


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        print('into login required')
        try:
            if session["user_type"] == "parent" or session["user_type"] == "student":
                return f(*args, **kwargs)
            else:
                flash("You need to login first")
                return redirect(url_for("portal.login"))
        except Exception as e:
            print(e)
            return redirect(url_for("portal.login"))
    return wrap


@admin.route('/users/profile',methods=['POST'])
def index():
    if request.method == 'POST':
        x = request.get_json(force=True)
    user_object.save_user(x)
    if True:
        print('ho gaya')

    if user_object.is_admin(x['username']):
        pass
    # result = user_object.check_user_exists("q@yahoo.com")
    # print(result)
    return x

