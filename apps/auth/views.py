from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user

from apps.app import db
from apps.auth.forms import LoginForm
from apps.crud.forms import UserForm
from apps.crud.models import User

auth = Blueprint(
  "auth",
  __name__,
  template_folder="templates",
  static_folder="static"
)

@auth.route("/")
def index():
  return render_template('auth/index.html')

@auth.route('/signup', methods=["GET", "POST"])
def signup():
  form = UserForm()

  if form.validate_on_submit():
    user = User(
      username = form.username.data,
      email = form.email.data,
      password = form.password.data
    )
    # 회원가입 시 입력한 이메일이 DB에 있는지 검사
    # 메서드의 결과가 True : 중복된 이메일, False : 중복안된 이메일
    if user.is_duplicate_email():
      flash('중복된 이메일은 사용이 불가능합니다.')
      return redirect(url_for('auth.signup'))
    
    db.session.add(user)
    db.session.commit()

    login_user(user)

    return redirect(url_for('detector.index'))

  return render_template('auth/signup.html', form=form)

@auth.route('/login', methods=["GET", "POST"])
def login():
  form = LoginForm()

  if form.validate_on_submit():
    user = User.query.filter_by(username = form.username.data).first()
    
    if user is not None and user.verify_password(form.password.data):
      login_user(user)
      return redirect(url_for('detector.index'))

    flash("아이디 또는 비밀번호가 일치하지 않습니다.")
  return render_template('auth/login.html', form=form)

@auth.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('auth.login'))