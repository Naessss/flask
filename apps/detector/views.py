from flask import Blueprint, render_template, current_app, send_from_directory, redirect, url_for, flash
from flask_login import login_required, current_user
import uuid
from pathlib import Path
import random
import cv2
import torch
import torchvision
from PIL import Image
import numpy as np
import torchvision.transforms.functional
from flask_wtf.csrf import generate_csrf

from apps.detector.forms import UploadImageForm
from apps.app import db
from apps.detector.models import UserImage, UserImageTag
from apps.crud.models import User

dt = Blueprint(
  "detector",
  __name__,
  template_folder="templates"
)

@dt.route('/')
def index():
  images = (
    db.session.query(User, UserImage)
              .join(UserImage)
              .filter(User.id == UserImage.user_id)
              .all()
  )

  csrf_token = generate_csrf()

  user_image_tag_dict = {}

  for image in images:
    user_image_tags = (
      db.session.query(UserImageTag)
        .filter(UserImageTag.user_image_id == image.UserImage.id)
        .all()
    )
    user_image_tag_dict[image.UserImage.id] = user_image_tags

  return render_template('detector/index.html', images = images, user_image_tag_dict=user_image_tag_dict, csrf_token=csrf_token)

@dt.route('/images/<path:filename>')
def image_file(filename):
  return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@dt.route('/upload', methods=["GET", "POST"])
@login_required
def upload_image():
  form = UploadImageForm()

  if form.validate_on_submit():
    # 전송받은 파일을 저장
    file = form.image.data
    
    # 이미지 파일의 확장자 추출
    ext = Path(file.filename).suffix
    uuid_file_name = str( uuid.uuid4() ) + ext

    # 이미지를 저장
    image_path = Path(current_app.config['UPLOAD_FOLDER'], uuid_file_name)
    file.save(image_path)

    # DB에 저장
    user_image = UserImage(user_id=current_user.id, image_path=uuid_file_name)
    db.session.add(user_image)
    db.session.commit()
    
    # 저장이 끝나면 index페이지로 이동
    return redirect(url_for('detector.index'))

  return render_template('detector/upload.html', form=form)


# 랜덤 색상 리턴
def make_color(labels):
  colors = [[random.randint(0,255) for _ in range(3)] for _ in labels]
  color = random.choice(colors)
  return color

# 선 두께 생성
def make_line(result_image):
  line = round(max(result_image.shape[0:2]) * 0.002) + 1
  return line

# 이미지에 선을 그려주는 함수
def draw_lines(c1, c2, result_image, line, color):
  cv2.rectangle(result_image, c1, c2, color, thickness=line)
  return cv2


def draw_texts(result_image, line, c1, cv2, color, labels, label):
  display_text = f'{labels[label]}'
  font = max(line - 1, 1)
  t_size = cv2.getTextSize(display_text, 0, fontScale=line / 3, thickness=font)[0]
  c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
  cv2.rectangle(result_image, c1, c2, color, -1)
  cv2.putText(
    result_image, display_text, (c1[0], c1[1] - 2),
    0, line / 3, [255, 255, 255], thickness=font, lineType=cv2.LINE_AA
  )

  return cv2

def exec_detect(target_image_path):
  labels = current_app.config['LABELS']
  image = Image.open(target_image_path)

  image_tensor = torchvision.transforms.functional.to_tensor(image)
  model = torch.load(Path(current_app.root_path, 'detector', 'model.pt'))

  model = model.eval()

  output = model([image_tensor])[0]
  tags = []
  result_image = np.array(image.copy())

  for box, label, score in zip(output['boxes'], output['labels'], output['scores']):
    if score > 0.5 and labels[label] not in tags:
      color = make_color(labels)
      line = make_line(result_image)
      c1 = ( int(box[0]), int(box[1]) )
      c2 = ( int(box[2]), int(box[3]) )
      cv2 = draw_lines(c1, c2, result_image, line, color)
      cv2 = draw_texts(result_image, line, c1, cv2, color, labels, label)
      tags.append(labels[label])

  if tags:
    detected_image = str(uuid.uuid4()) + '.jpg'

    detected_image_path = str( 
      Path(current_app.config['UPLOAD_FOLDER'], detected_image)
    )

    cv2.imwrite(detected_image_path, cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR))
    return tags, detected_image
  else:
    return tags, None
  
def save_detected_image_tags(user_image, tags, detected_image):
  user_image.image_path = detected_image
  user_image.is_detected = True
  db.session.add(user_image)

  for tag in tags:
    user_image_tag = UserImageTag(user_image_id=user_image.id, tag_name=tag)
    db.session.add(user_image_tag)
  
  db.session.commit()

@dt.route('/detect/<string:image_id>', methods=["POST"])
@login_required
def detect(image_id):
  user_image = db.session.query(UserImage).filter(UserImage.id == image_id).first()

  if user_image is None:
    flash('해당 이미지가 존재하지 않습니다.')
    return redirect(url_for('detector.index'))

  target_image_path = Path(current_app.config['UPLOAD_FOLDER'], user_image.image_path)
  tags, detected_image = exec_detect(target_image_path)

  if not tags:
    flash('감지된 물체가 없습니다.')
    return redirect(url_for('detector.index'))
  
  try:
    save_detected_image_tags(user_image, tags, detected_image)
  except Exception as e:
    flash('물체 감지 결과 저장 중 오류가 발생')
    db.session.rollback()

  return redirect(url_for('detector.index'))