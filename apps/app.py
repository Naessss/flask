from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_login import LoginManager

from apps.config import config
import os

config_key = os.environ.get('FLASK_CONFIG_KEY')

# SQLAlchemy 객체 생성
db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = '로그인 후 사용 가능 합니다.'

def create_app():
  app = Flask(__name__)

  app.config.from_object(config[config_key])

  db.init_app(app)
  Migrate(app, db)
  login_manager.init_app(app)

  from apps.crud import views as crud_views
  from apps.auth import views as auth_views
  from apps.detector import views as dt_views

  app.register_blueprint(crud_views.crud, url_prefix='/crud')
  app.register_blueprint(auth_views.auth, url_prefix='/auth')
  app.register_blueprint(dt_views.dt)

  return app