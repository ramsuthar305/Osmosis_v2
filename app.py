from flask import Flask,request
from flask_pymongo import PyMongo
# from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object("config.Config")
mongo = PyMongo(app)
# csrf = CSRFProtect(app)

from admin.views import admin
from portal.views import portal

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(portal, url_prefix='')


if __name__ == '__main__':
    app.run(debug=True)



#
#
# app = flask.Flask(__name__)
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/myDatabase'
# mongo = PyMongo(app)
#
#
# @app.route('/', methods=['GET', 'POST'])
# def home():
# 	if request.method == 'POST':
# 		sent = request.get_json(force=True)
# 		return jsonify({'sent': f'{sent}'}), 201
# 	else:
# 		return jsonify({'about': 'server'})
#
#
# app.run(debug=True)