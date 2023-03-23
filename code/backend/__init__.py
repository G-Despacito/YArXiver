from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from .db_models import db
from flask_login import LoginManager
from flask_cors import CORS
import os
import pickle

app = Flask(__name__,
            static_folder = "../dist/assets",
            template_folder = "../dist")
CORS(app)

app.config['SECRET_KEY'] = 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:1234@localhost/yarxiver"

db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'user_signin'
login_manager.login_message_category = 'danger'
login_manager.login_message = 'Login is required for this function.'

abspath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

with open("backend/utils/models/category_tf.pkl", "rb") as handle:
    vector_dictionary = pickle.load(handle)

with open("backend/utils/models/article_cat_info.pkl", "rb") as handle:
    article_cat_info = pickle.load(handle)


from backend import routes
