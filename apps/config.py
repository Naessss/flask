import secrets
import os
from pathlib import Path

dir = os.path.dirname(__file__)
image_dir = Path(__file__).parent.parent

class BaseConfig:
  SECRET_KEY = secrets.token_urlsafe(32)
  WTF_CSRF_SECRET_KEY = secrets.token_urlsafe(32)
  UPLOAD_FOLDER = str(Path(image_dir, "apps", "images"))

# 로컬환경 
class LocalConfig(BaseConfig):
  SQLALCHEMY_DATABASE_URI=f'sqlite:///{os.path.join(dir,"test.db")}'
  SQLALCHEMY_TRACK_MODIFICATIONS=False
  SQLALCHEMY_ECHO=True

# 테스트환경
class TestingConfig(BaseConfig):
  SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://root:1234@localhost:3306/flaskdb'
  SQLALCHEMY_TRACK_MODIFICATIONS=False
  SQLALCHEMY_ECHO=True

# 배포
class ProductionConfig(BaseConfig):
  SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://root:1234@localhost:3306/flaskdb'
  SQLALCHEMY_TRACK_MODIFICATIONS=False
  SQLALCHEMY_ECHO=True

config = {
  "local" : LocalConfig,
  "testing" : TestingConfig,
  "production" : ProductionConfig
}