from datetime import datetime

from apps.app import db

class UserImage(db.Model):
  __tablename__ = 'user_image'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
  image_path = db.Column(db.String(255))
  is_detected = db.Column(db.Boolean, default=False)
  created_at = db.Column(db.DateTime, default=datetime.now)
  updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)