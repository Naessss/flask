from flask import Blueprint, render_template

from apps.crud.forms import UserForm
from apps.crud.models import User
from apps.app import db

crud = Blueprint(
  "crud",
  __name__,
  template_folder="templates",
  static_folder="static"
)

@crud.route('/')
def index():
  return render_template('crud/index.html')

@crud.route('/users/new', methods=["GET", "POST"])
def create_user():
  form = UserForm()

  if form.validate_on_submit():
    # db에 저장할 객체 설정
    # db에 insert 시키고
    # 회원가입 완료 페이지 이동
    pass
  
  return render_template('crud/create.html', form=form)