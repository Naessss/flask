from flask import Blueprint, render_template, current_app, send_from_directory
from flask_login import login_required

from apps.detector.forms import UploadImageForm

dt = Blueprint(
  "detector",
  __name__,
  template_folder="templates"
)

@dt.route('/')
def index():
  return render_template('detector/index.html')

@dt.route('/images/<path:filename>')
def image_file(filename):
  return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@dt.route('/upload', methods=["GET", "POST"])
@login_required
def upload_image():
  form = UploadImageForm()

  return render_template('detector/upload.html', form=form)