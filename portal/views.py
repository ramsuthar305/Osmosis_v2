from flask import Blueprint, render_template, request, redirect, session, jsonify, flash, url_for, abort
from functools import wraps
from flask import session
import hashlib
import json
from datetime import datetime
#custom imports
from .models import Users, Shortlist
from admin.models import Jobs

user_object = Users()
jobs = Jobs()
shortlist= Shortlist()
portal = Blueprint("portal", __name__, template_folder='template', static_folder='static/portal',
                   static_url_path='static/portal')


@portal.errorhandler(404)
def page_not_found(error):
    return render_template('portal/404.html'), 404




@portal.route('/')
def index():
    print('called')
    return render_template('portal/home.html')

@portal.route('/dashboard')
def dashboard():
    try:
        alljobs=jobs.get_all_jobs()
        if session["logged_in"]:
            return render_template('portal/dashboard.html',alljobs=alljobs)
        else:
            return redirect(url_for('portal.signin'))
    except Exception as error:
        print(error)
        return render_template('portal/signin.html')


@portal.route('/profile')
def profile():
    user=user_object.get_user_profile()
    return render_template('portal/profile.html',user=user)

@portal.route('/test',methods=['POST','GET'])
def test():
    try:
        if request.method=='POST':
            job=jobs.get_job(request.args.get('job_id'))
            apti=[]
            #print(job)
            print(request.form.get('name'))
            aptitude_sum=0
            for question in job['aptitude']:
                if question['answer']==request.form.get(question['question']):
                    aptitude_sum+=1
            shortlist_profile={}
            shortlist_profile['job_id']=request.args.get('job_id')
            shortlist_profile['user_id']=session['id']
            shortlist_profile['aptiscore']=aptitude_sum
            shortlist_profile['personalityscore']=None
            print('this is job skills',job['skills'])
            job_skills=job['skills']
            shortlist_profile['skillscore']=skillscore(job)
            print('this is job skills herer',job['skills'])
            shortlist_profile['createdOn']=datetime.now()
            shortlist_profile['totalScore']=10+len(job['skills'])+10
            result=shortlist.save_profile(shortlist_profile)
            print(result)
            job['is_apti']=False
            job['test_id']=result
            return redirect(url_for('portal.personality_test',job_id=job['_id'],test_id=result))
        else:
            print(request.args.get('job_id'))
            job=jobs.get_job(request.args.get('job_id'))
            job['is_apti']=True
            return render_template('portal/test.html',job=job)
    except Exception as error:
        print('this is exception here',error)

def skillscore(jobskills):
    print('calleddd')
    user=user_object.get_user_profile()
    print('i am herer',user)
    user_skills=[x.lower() for x in user['skills']]
    skill_score=0
    print(user_skills)
    print(jobskills)
    for skill in jobskills:
        if skill.lower() in user_skills:
            skill_score+=1
    return skill_score

@portal.route('/personality_test',methods=['POST','GET'])
def personality_test():
    try:
        if request.method=='POST':
            job=jobs.get_job(request.args.get('job_id'))
            apti=[]
            #print(job)
            print(request.form.get('name'))
            personality_sum=0
            for question in job['personality']:
                if question['answer']==request.form.get(question['question']):
                    personality_sum+=1 
            print('this is test_id ',personality_sum)
            shortlist.update_personality(request.args.get('test_id'),personality_sum)
            return redirect(url_for('portal.dashboard'))
            
        else:
            print(request.args.get('test_id'))
            job=jobs.get_job(request.args.get('job_id'))
            print(job)
            return render_template('portal/personality.html',job=job,test_id=request.args.get('test_id'))
            
    except Exception as error:
        print('this is exception',error)

@portal.route('/signup', methods=['POST','GET'])
def signup():
    try:
        if request.method == 'POST':
            #x = request.get_json(force=True)
            email= request.form.get('email')
            name= request.form.get('name')
            password= request.form.get('password')
            user={
                "username":email,
                "name":name,
                "password":password,
                "phone":None,
                "resume":None,
                "profile_picture":None,
                "address":None
            }
            registration_status = user_object.save_user(user)
            if registration_status == True:
                flash("User registered Successfully!!!")
                return render_template('portal/signin.html', TOPIC_DICT = TOPIC_DICT)
            else:
                flash(registration_status)
                return render_template('portal/signup.html', TOPIC_DICT = TOPIC_DICT)
        else:
            return render_template('portal/signup.html')
    except Exception as error:
        print(error)
        return render_template('portal/signup.html')


@portal.route('/signin', methods = ['GET', 'POST'])
def signin():
    try:
        if request.method == 'POST':
            #x = request.get_json(force=True)
            email= request.form.get('email')
            password= request.form.get('password')
            
            login_status = user_object.login_user(email,password)
            if login_status==True:
                return redirect(url_for("portal.dashboard"))
            else:
                flash(login_status)
                return render_template('portal/signin.html', TOPIC_DICT = TOPIC_DICT)
        else:
            return render_template('portal/signin.html')
    except Exception as error:
        print(error)
        return render_template('portal/signin.html')


@portal.route('/logout', methods=['POST','GET'])
def logout():
    try:
        session['logged_in']=False
        session["username"] = None
        session["name"] = None
        session["user_type"] = None
        session['id'] = None
        return redirect(url_for('portal.signin'))
    except Exception as error:
        print(error)
        return redirect(url_for('portal.signin'))

@portal.route('/edit_profile', methods=['POST','GET'])
def edit_profile():
    try:
        if request.method=='POST':
            #print("in request files", request.files)
            if not request.files.get('profile_picture', None):
                pass
            else:
                file=request.files['profile_picture']
                if file:
                    profile_pic = {}
                    profile_pic["filename"] = file.filename
                    profile_pic["directory"] = session['id'] + "/profile_picture" + "/"
                    print(file.filename)
                    user_object.upload_file(profile_pic, file,"pic")

            if not request.files.get('resume', None):
                pass
            else:
                cv=request.files['resume']
                print('resume :',cv)
                if cv:
                    resume = {}
                    resume["filename"] = cv.filename
                    resume["directory"] = session['id'] + "/resume" + "/"
                    print(cv.filename)
                    user_object.upload_file(resume, cv,"resume")
            update_data={}
            
            if request.form.get('phone'):
                update_data['phone']=request.form.get('phone')
            
            if request.form.get('name'):
                update_data['name']=request.form.get('name')
            
            if request.form.get('email'):
                update_data['email']=request.form.get('email')
            
            if request.form.get('address'):
                update_data['address']=request.form.get('address') 
            
            if update_data:
                user_object.user_edit(update_data)


        return redirect(url_for('portal.profile'))
    except Exception as error:
        return redirect(url_for('portal.profile'))

