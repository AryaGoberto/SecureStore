from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required
from controllers.auth import login_controller, register_controller, logout_controller, dashboard_controller
from models.user import User
from . import oauth

authapp = Blueprint('authapp', __name__)

@authapp.route('/')
def index():
    return redirect(url_for('authapp.login'))

@authapp.route('/register/google/')
def google_register():
    google = oauth.google
    redirect_uri = url_for('authapp.google_register_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@authapp.route('/register/google/authorized')
def google_register_authorize():
    google = oauth.google
    token = google.authorize_access_token()
    user_info = google.userinfo()
    
    user_email = user_info['email']
    user = User.query.filter_by(email=user_email).first()
    
    if user:
        login_user(user)
        flash('Akun Anda sudah terdaftar. Anda berhasil login.', 'info')
        return redirect(url_for('authapp.dashboard'))

    user_name = user_info['name']
    new_user = User(
        email=user_email,
        nama_lengkap=user_name,
        username=user_email.split('@')[0],
        role='user'
    )
    new_user.set_password('google_oauth_user')
    new_user.save()
    
    login_user(new_user)
    flash('Pendaftaran dengan akun Google berhasil!', 'success')
    return redirect(url_for('authapp.dashboard'))

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