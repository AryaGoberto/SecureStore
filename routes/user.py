import os
from flask import Blueprint, current_app, send_file, abort
from controllers.user import user_list_controller, tambah_user_controller, edit_user_controller, hapus_user_controller
from flask_login import login_required
from models.user import User
import io

userapp = Blueprint('userapp', __name__)

@userapp.route('/user/')
@login_required
def user_list():
    return user_list_controller()

@userapp.route('/user/tambah/', methods=['GET', 'POST'])
@login_required
def tambah_user():
    return tambah_user_controller()

@userapp.route('/user/edit/<int:id>/', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    return edit_user_controller(id)

@userapp.route('/user/hapus/<int:id>/', methods=['POST'])
@login_required
def hapus_user(id):
    return hapus_user_controller(id)

@userapp.route('/user/profile_pic/<int:user_id>')
def profile_pic(user_id):
    user = User.get_by_id(user_id)
    
    if user and user.profile_pic and user.profile_pic_mimetype:
        return send_file(
            io.BytesIO(user.profile_pic),
            mimetype=user.profile_pic_mimetype
        )
    else:
        try:
            default_image_path = os.path.abspath(os.path.join(current_app.root_path, '..', 'static', 'profile_pics', 'default_profile.png'))
            return send_file(default_image_path, mimetype='image/png')
        except FileNotFoundError:
            abort(404)