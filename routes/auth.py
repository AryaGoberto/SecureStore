from flask import Blueprint
from controllers.auth import login_controller, register_controller, logout_controller, dashboard_controller
from flask_login import login_required

authapp = Blueprint('authapp', __name__)

@authapp.route('/login/', methods=['GET', 'POST'])
def login():
    return login_controller()

@authapp.route('/register/', methods=['GET', 'POST'])
def register():
    return register_controller()

@authapp.route('/logout/')
@login_required
def logout():
    return logout_controller()

@authapp.route('/dashboard/')
@login_required
def dashboard():
    return dashboard_controller()