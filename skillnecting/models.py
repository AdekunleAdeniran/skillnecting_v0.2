#!/usr/bin/python3
from datetime import datetime
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as TJS
from skillnecting import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    """Function to reload user_id stored in db"""
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """ Create User instance for db"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    github_username = db.Column(db.String(30), unique=True, nullable=False)

    
    def get_reset_token(self, expires_sec=1800):
        """Function to generate timed token for password reset"""
        s = TJS(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        """FUnction to verify token"""
        s = TJS(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return "User '{}', '{}', '{}', '{}' ".format(
            self.username, self.email, self.image_file, self.github_username)


class Post(db.Model):
    """DB class for posts"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Post {} {}".format(self.title, self.date_posted)
