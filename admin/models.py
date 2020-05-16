import hashlib
from app import *
from flask import session
from bson import ObjectId

class Users:
	def __init__(self):
		self.mongo = mongo.db

	def check_user_exists(self, username):
		result = self.mongo.users.find_one({"$or": [{"username": username}, {"phone": username}]})
		if result:
			return True
		else:
			return False

	def save_user(self,x):
		result = mongo.db.users.insert_one({"username":x['username'],"password":x['password'],"phno":x['phno'],"address":x['address'],"user_type":"normal"})
		if result:
			return True
		else:
			return False


	def is_admin(self,x):
		result = mongo.db.users.find_one({"$and":[{"username":x},{"user_type":"admin"}]})
		if result:
			return True
		else:
			return False

	def get_user_by_id(self,id):
		try:
			user = mongo.db.users.find_one({"username":id})
			return user
		except Exception as error:
			print(error)

	def login_user(self, username, password):
		result = self.check_user_exists(username)
		if result:
			login_result = self.mongo.users.find_one(
				{"$and": [{"$or": [{"username": username}, {"phone": username}]},
						  {"password": password}]})
			if login_result is not None:
				session["username"] = login_result["username"]
				session["logged_in"] = True

				session["user_type"] = login_result['user_type']
				session['id'] = str(login_result["user_id"])
				return login_result
			else:
				return 1
		else:
			return 0

class Jobs:
	def __init__(self):
		self.mongo =mongo.db
	
	def put_job(self,job):
		try:
			result=mongo.db.jobs.insert_one(job)
			
			if result:
				return result.inserted_id
			else:
				return False
		except Exception as error:
			print(error)
			return "something went wrong"

	def put_aptitude(self,job_id,apti):
		try:
			result=mongo.db.jobs.update_one({"_id":ObjectId(job_id)},{"$set":{"aptitude":apti}})
			if result:
				return True
			else:
				return False
		except Exception as error:
			print(error)
			return "something went wrong"

	def put_personality(self,job_id,personality):
		try:
			result=mongo.db.jobs.update_one({"_id":ObjectId(job_id)},{"$set":{"personality":personality}})
			if result:
				return True
			else:
				return False
		except Exception as error:
			print(error)
			return "something went wrong"

	def get_all_jobs(self):
		try:
			result= mongo.db.jobs.find({})
			print('This is rresult: ',result)
			return result
		except Exception as error:
			print(error)
			return "something went wrong"

	def get_job(self,job_id):
		try:
			result=mongo.db.jobs.find_one({"_id":ObjectId(job_id)})
			return result
		except Exception as error:
			print(error)
			return "something went wrong"

class Shortlist:
	def __init__(self):
		self.mongo = mongo.db

	def get_profiles(self,job_id):
		profiles=mongo.db.shortlist.find({"job_id":job_id})
		users=Users()
		all_profiles=[]
		for profile in profiles:
			user=users.get_user_by_id(profile['user_id'])
			user['score']=profile['aptiscore']+profile['personalityscore']+profile['skillscore']
			user['outoff']=profile['totalScore']
			all_profiles.append(user)
		print(all_profiles)
		return all_profiles