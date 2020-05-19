from flask import Blueprint, render_template, request, redirect, session, jsonify, flash, url_for, abort
from functools import wraps
import hashlib
import json
from datetime import datetime

#custom imports
from .models import Users, Shortlist
from .models import Jobs
shorlist_obj=Shortlist()
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
            job['skills']= request.form.get('skills').split(',')
            job['aptitude']=[]
            job['personality']=[]
            job['created_on']= datetime.now()
            result=jobs.put_job(job)
            return redirect(url_for('admin.add_aptitude',job_id=result))
        else:
            return render_template('admin/index.html')
    except Exception as error:
        print(error)
        return render_template('admin/index.html')

@admin.route('/add_aptitude/<job_id>',methods=['POST','GET'])
def add_aptitude(job_id):
    print(job_id)
    try:
        job={}
        job['job_id']=job_id
        job['is_apti']=True
        if request.method == 'POST':
            apti=[]
            for i in range(10):
                tmp={}
                tmp['question']=request.form.get('question'+str(i+1))
                tmp['options']=request.form.get('options'+str(i+1)).split(',')
                tmp['answer']=request.form.get('answer'+str(i+1))
                apti.append(tmp)
            print(apti)
            jobs.put_aptitude(job_id,apti)
            return redirect(url_for('admin.add_personality',job_id=job_id))
        else:
            return render_template('admin/test.html',job=job)

    except Exception as error:
        job={}
        job['job_id']=job_id
        job['is_apti']=False
        print('In exception: ',error)
        return render_template('admin/test.html',job=job)

@admin.route('/dashboard')
def dashboard():
    alljobs=jobs.get_all_jobs()
    print('\n\nall jobs: ',alljobs)
    return render_template('admin/dashboard.html',alljobs=alljobs)

@admin.route('/shortlist')
def shortlist():
    print(request.args.get('job_id'))
    profiles=shorlist_obj.get_profiles(request.args.get('job_id'))
    print('\n\nall jobs: ',profiles)
    return render_template('admin/shortlist.html',profiles=profiles)

@admin.route('/delete/<job_id>',methods=['POST','GET'])
def delete(job_id):
    try:
        print("Im here"*100,job_id)
        jobs.delete_job(job_id)
        
        return redirect(url_for('admin.dashboard'))
    except Exception as error:
        
        return redirect(url_for('admin.dashboard'))

@admin.route('/add_personality/<job_id>',methods=['POST','GET'])
def add_personality(job_id):
    print(job_id)
    try:
        job={}
        job['job_id']=job_id
        job['is_apti']=False
        if request.method == 'POST':
            apti=[]
            for i in range(10):
                tmp={}
                tmp['question']=request.form.get('question'+str(i+1))
                tmp['options']=request.form.get('options'+str(i+1)).split(',')
                tmp['answer']=request.form.get('answer'+str(i+1))
                apti.append(tmp)
            print(apti)
            jobs.put_personality(job_id,apti)
            return redirect(url_for('admin.dashboard'))
        else:
            return render_template('admin/test.html',job_id=job_id)

    except Exception as error:
        print('In exception: ',error)

        job={}
        job['job_id']=job_id
        job['is_apti']=False
        
        return render_template('admin/test.html',job=job)

