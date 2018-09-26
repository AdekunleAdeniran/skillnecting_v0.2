# starting point of the entire app
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from skillnecting.config import Config



db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()




def create_app(config_class=Config):
	"""Function to create multiple instance of run"""
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	from skillnecting.users.routes import users
	from skillnecting.posts.routes import posts
	from skillnecting.main.routes import main
	from skillnecting.debugme.routes import debugme
	from skillnecting.errors.handlers import errors


	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(main)
	app.register_blueprint(debugme)
	app.register_blueprint(errors)

	return app