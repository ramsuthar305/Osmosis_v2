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
				return True
			else:
				return False
		except Exception as error:
			print(error)
			return "something went wrong"

	def put_aptitude(self,job_id,apti):
		try:
			result=mongo.db.jobs.update_one({"_id":ObjectId("5ebc58c43932aa87a84389a8")},{"$set":{"aptitude":apti}})
			if result:
				return True
			else:
				return False
		except Exception as error:
			print(error)
			return "something went wrong"

	def put_personality(self,job_id,personality):
		try:
			result=mongo.db.jobs.update_one({"_id":job_id},{"$set":{personality:personality}})
			if result:
				return True
			else:
				return False
		except Exception as error:
			print(error)
			return "something went wrong"
