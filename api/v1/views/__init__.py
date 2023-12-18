from flask import Blueprint

# this file imports and registers blueprints for our api endpoints
# allowing access to endpoints through importation a single file

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.articles import *
from api.v1.views.login import login_bp
from api.v1.views.questions import questions_bp
from api.v1.views.register import register_bp
from api.v1.views.users import users_bp
from api.v1.views.articles import articles_bp
from api.v1.views.contact import contact_bp
from api.v1.views.videos import videos_bp


app_views.register_blueprint(register_bp)
app_views.register_blueprint(login_bp)
app_views.register_blueprint(questions_bp)
app_views.register_blueprint(users_bp)
app_views.register_blueprint(articles_bp)
app_views.register_blueprint(contact_bp)
app_views.register_blueprint(videos_bp)