from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import SubmitField

class UploadImageForm(FlaskForm):
  image = FileField(
    validators=[
      FileRequired('업로드할 이미지를 선택하세요'),
      FileAllowed(["jpg", "jpeg", "png"], "지원되지 않는 확장자입니다.")
    ]
  )
  submit = SubmitField("업로드")