from flask import Blueprint, render_template, request, redirect, session, jsonify, flash, url_for, abort
from functools import wraps
from flask import session
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




@portal.route('/')
def index():
    print('called')
    return render_template('portal/home.html')

@portal.route('/dashboard')
def dashboard():
    try:
        print(session['logged_in'])
        if session["logged_in"]:
            return render_template('portal/dashboard.html')
        else:
            return redirect(url_for('portal.signin'))
    except Exception as error:
        print(error)
        return render_template('portal/signin.html')


@portal.route('/profile')
def profile():
    user=user_object.get_user_profile()
    return render_template('portal/profile.html',user=user)

@portal.route('/test')
def test():
    return render_template('portal/test.html')

@portal.route('/signup', methods=['POST','GET'])
def signup():
    try:
        if session['logged_in']==True:
            return redirect(url_for("portal.dashboard"))
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
                return redirect(url_for("portal.dashboard"))
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
        print(session['logged_in'])

        if session['logged_in']==False:
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
        else:
                return redirect(url_for('portal.dashboard'))
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

