from flask import Blueprint, render_template, request, redirect, session, jsonify, flash, url_for, abort
from functools import wraps
import hashlib
import json
from datetime import datetime

#custom imports
from .models import Users
from .models import Jobs

user_object = Users()
jobs=Jobs()
admin = Blueprint("admin", __name__, template_folder='templates', static_folder='static/admin',
                   static_url_path='static/admin')


@admin.errorhandler(404)
def page_not_found(error):
    return render_template('admin/404.html'), 404

@admin.route('/add_job',methods=['POST','GET'])
def add_job():
    try:
        if request.method == 'POST':
            job={}
            job['category']=request.form.get('category')
            job['title']=request.form.get('description')
            job['description']=request.form.get('description')
            job['skills']= request.form.get('skills')
            job['aptitude']=[]
            job['personality']=[]
            job['created_on']= datetime.now()
            result=jobs.put_job(job)
            return render_template('admin/index.html')
        else:
            return render_template('admin/index.html')
    except Exception as error:
        print(error)
        return render_template('admin/index.html')

@admin.route('/add_aptitude',methods=['POST','GET'])
def add_aptitude():
    try:
        if request.method == 'POST':
            apti=[]
            for i in range(10):
                tmp={}
                tmp['question']=request.form.get('question'+str(i+1))
                tmp['options']=request.form.get('options'+str(i+1)).split(',')
                tmp['answer']=request.form.get('answer'+str(i+1))
                apti.append(tmp)
            jobs.put_aptitude("5ebc58c43932aa87a84389a8",apti)
            return render_template('admin/test.html')
        else:
            return render_template('admin/test.html')

    except Exception as error:
        print(error)
        return render_template('admin/test.html')


