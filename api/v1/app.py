from flask import Flask
from views import app_views
from models.engine.db_storage import db, Users
from config import Config
from flask_login import LoginManager
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object("config.Config")
db.init_app(app)
app.secret_key = 'miano123'

CORS(app, origins="*")

login_manager = LoginManager(app)
login_manager.init_app(app)
app.register_blueprint(app_views)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

if __name__ == '__main__':
    app.run()
