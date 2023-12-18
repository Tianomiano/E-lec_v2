from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
from flask_login import logout_user
import json
import jwt
from flask import jsonify
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from datetime import datetime
from flask_migrate import Migrate
import time
from flask import session
from flask_login import user_logged_in, user_loaded_from_cookie
from models.engine.db_storage import db, Question
from models.engine.db_storage import Users, Articles
from config import Config
from flask_cors import CORS
from api.v1.views import app_views

app = Flask(__name__)
app.config.from_object("config.Config")
db.init_app(app)
app.secret_key = 'miano123'
CORS(app, origins="*")
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
login_manager = LoginManager(app)
login_manager.init_app(app)
app.register_blueprint(app_views)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)


@app.route('/', methods=['GET'])
def landing():
    return render_template('landing.html')

@app.route('/home', methods=['GET'])
def home():
    # this is my homepage with posted questions and replies

    token = session.get('user_token')
    logged_in = bool(token) 

    return render_template('index.html', logged_in=logged_in, token=token)


@app.route('/articles', methods=['GET', 'POST'])
def articles():
    # this is the articles page for all posted articles
    articles = Articles.query.all()
    token = session.get('user_token')
    logged_in = bool(token) 

    return render_template('articles.html', logged_in=logged_in, token=token, articles=articles)


@app.route('/videos', methods=['GET', 'POST'])
def videos():
    # this is the videos page for all posted videos
    token = session.get('user_token')
    logged_in = bool(token) 

    return render_template('videos.html', logged_in=logged_in, token=token)


@app.route('/about', methods=['GET'])
def about():
    # a page describing what the site offers

    token = session.get('user_token')
    logged_in = bool(token) 

    return render_template('about.html', logged_in=logged_in, token=token)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    # a page that allows contact between users and the web application owner

    token = session.get('user_token')
    logged_in = bool(token) 
    
    return render_template('contact.html', logged_in=logged_in, token=token)

@app.route('/register', methods=['GET', 'POST'])
def register():
    # a page from which new users can sign up

    token = session.get('user_token')
    logged_in = bool(token) 
    return render_template('register.html', logged_in=logged_in)

@login_manager.user_loader
def load_user(user_id):
    user = Users.query.get(user_id)
    if user:
        return user

class User(UserMixin):
    def __init__(self, users):
        self.id = users.user_id
        self.username = users.username
        self.email = users.email

    def get_id(self):
        return str(self.id)

@app.route('/login', methods=['POST', 'GET'])
def login():
    # handles user login

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = Users.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.passwd, password):
            user_obj = User(user)
            login_user(user_obj)
            session.permanent = True
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Please check your email and password.', 'danger')
            # Add the 'not_registered' message to the session
            if not user:
                flash('User not registered.', 'not_registered')
            return redirect(url_for('login'))
    return render_template('login.html',logged_in=False)

@user_logged_in.connect_via(app)
def track_user_logged_in(sender, user, **extra):
    session['last_activity'] = time.time()

@user_loaded_from_cookie.connect_via(app)
def track_user_loaded_from_cookie(sender, user, **extra):
    session['last_activity'] = time.time()

def check_user_activity():
    last_activity = session.get('last_activity', 0)
    current_time = time.time()
    if current_user.is_authenticated and (current_time - last_activity) > 3600:  # 1 hour
        flash('You have been logged out due to inactivity.', 'info')
        logout_user()
        return redirect(url_for('login'))
    session['last_activity'] = current_time

@app.route('/protected_route')
@login_required
def protected_route():
    check_user_activity()

@app.route('/api/v1/logout', methods=['GET', 'POST'])
def logout():
    # handle user logout and redirect after logout
    
    token = session.get('user_token')
    session.pop('user_token', None)
    logged_in = bool(token) 

    return redirect(url_for('home', logged_in=logged_in))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.debug = True
    app.run()