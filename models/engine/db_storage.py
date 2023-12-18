from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Users(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    passwd = db.Column(db.String(255), nullable=False)
    deletion_requested = db.Column(db.DateTime)

class Articles(db.Model):
    article_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    author = db.relationship('Users', backref=db.backref('articles', lazy=True))
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Articles('{self.title}', '{self.date_posted}')"
    
class Question(db.Model):
    question_id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50), nullable=False)
    question = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    author = db.relationship('Users', backref=db.backref('questions', lazy=True))
    replies = db.relationship('Reply', backref='question', lazy=True, cascade='all, delete')

class Reply(db.Model):
    reply_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    author = db.relationship('Users', backref=db.backref('replies', lazy=True))
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'), nullable=False)

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    author = db.relationship('Users', backref=db.backref('videos', lazy=True))