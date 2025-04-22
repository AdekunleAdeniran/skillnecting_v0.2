# Starting point
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from authlib.integrations.flask_client import OAuth
from skillnecting.config import Config
from flasgger import Swagger

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
swagger = Swagger()
oauth = OAuth()

# We'll store github globally so it's accessible later
github = None

def create_app(config_class=Config):
    """Function to create multiple instance of run"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    swagger.init_app(app)
    oauth.init_app(app)

    # Register GitHub OAuth inside the app context
    global github
    github = oauth.register(
        name='github',
        client_id=app.config['GITHUB_CLIENT_ID'],
        client_secret=app.config['GITHUB_CLIENT_SECRET'],
        access_token_url='https://github.com/login/oauth/access_token',
        access_token_params=None,
        authorize_url='https://github.com/login/oauth/authorize',
        authorize_params=None,
        api_base_url='https://api.github.com/',
        client_kwargs={'scope': 'user:email'}
    )

    from skillnecting.users.routes import users
    from skillnecting.posts.routes import posts
    from skillnecting.main.routes import main
    from skillnecting.errors.handlers import errors
    from skillnecting.api.routes import api

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(api)

    return app
