import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from app import mail
from flask_login import login_user, current_user, logout_user, login_required

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    #把照片缩小
    #output_size = (125, 125)
    #i = Image.open(form_picture)
    #i.thumbnail(output_size)
    #删除原先照片，除了default
    form_picture.save(picture_path)
    if current_user.image_file != "default.jpg":
        os.remove(os.path.join(current_app.root_path, 'static/profile_pics', current_user.image_file))

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)