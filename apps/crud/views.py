from flask import Blueprint, render_template, redirect, url_for

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
    user = User(
      username = form.username.data,
      email = form.email.data,
      password = form.password.data
    )

    # db에 insert 시키고
    db.session.add(user)
    db.session.commit()

    # 회원가입 완료 페이지 이동
    return redirect(url_for('crud.users'))
  
  return render_template('crud/create.html', form=form)

@crud.route('/users')
def users():
  # 회원정보들을 db에서 가져오는 코드
  users = User.query.all()

  return render_template('crud/index.html', users=users)