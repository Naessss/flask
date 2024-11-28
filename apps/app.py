from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy 객체 생성
db = SQLAlchemy()

def create_app():
  app = Flask(__name__)

  # MySQL 연결
  app.config.from_mapping(
    SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://root:1234@localhost:3306/flaskdb',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_EHCO=True
  )

  db.init_app(app)
  Migrate(app, db)

  from apps.crud import views as crud_views

  app.register_blueprint(crud_views.crud, url_prefix='/crud')

  return app