from flask import Blueprint
from controllers.user import user_list_controller, tambah_user_controller, edit_user_controller, hapus_user_controller
from flask_login import login_required

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