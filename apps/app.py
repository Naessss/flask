from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from apps.config import config
import os

config_key = os.environ.get('FLASK_CONFIG_KEY')

# SQLAlchemy 객체 생성
db = SQLAlchemy()

csrf = CSRFProtect()

def create_app():
  app = Flask(__name__)

  app.config.from_object(config[config_key])

  db.init_app(app)
  Migrate(app, db)

  from apps.crud import views as crud_views

  app.register_blueprint(crud_views.crud, url_prefix='/crud')

  return app