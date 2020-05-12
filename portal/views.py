from flask import Blueprint, render_template, request, redirect, session, jsonify, flash, url_for, abort
from functools import wraps
import hashlib
import json

#custom imports
from .models import Users

user_object = Users()

portal = Blueprint("portal", __name__, template_folder='template', static_folder='static/portal',
                   static_url_path='static/portal')


@portal.errorhandler(404)
def page_not_found(error):
    return render_template('portal/404.html'), 404


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


@portal.route('/')
def index():
    print('called')
    return render_template('portal/home.html'),404

@portal.route('/dashboard')
def dashboard():
    print('called')
    return render_template('portal/dashboard.html'),404

@portal.route('/profile')
def profile():
    print('called')
    return render_template('portal/profile.html'),404

@portal.route('/test')
def test():
    print('called')
    return render_template('portal/test.html'),404

@portal.route('/signup')
def signup():
    print('called')
    return render_template('portal/signup.html'),404

@portal.route('/signin')
def signin():
    print('called')
    return render_template('portal/signin.html'),404

