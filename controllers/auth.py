from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from models.kategori import KategoriBarang
from models.barang import DataBarang
from models import db

def login_controller():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember_me')
        remember_me = True if remember else False

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user, remember=remember_me)
            # flash('Logged in successfully.', 'success')
            return redirect(url_for('authapp.dashboard'))
        # else:
            # flash('Invalid username or password.', 'error')

    return render_template('login-register.html')

def register_controller():
    if request.method == 'POST':
        nama_lengkap = request.form.get('nama_lengkap')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        konf_password = request.form.get('konf_password')

        user_exists_username = User.query.filter_by(username=username).first()
        user_exists_email = User.query.filter_by(email=email).first()

        if user_exists_username:
            flash('Username already exists.', 'error')
        elif user_exists_email:
            flash('Email already exists.', 'error')
        elif password != konf_password:
            flash('Passwords do not match.', 'error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
        else:
            new_user = User(
                nama_lengkap=nama_lengkap,
                username=username,
                email=email,
                role='user'
            )
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            # flash('Account created successfully! You can now log in.', 'success')
            return redirect(url_for('authapp.login'))

    return render_template('login-register.html')

def logout_controller():
    logout_user()
    return redirect(url_for('authapp.login'))

def dashboard_controller():
    total_users = 0
    if current_user.role == 'admin':
        total_users = User.get_total_users()

    total_kategori = KategoriBarang.get_total_kategori()
    total_barang = DataBarang.get_total_barang()

    return render_template('dashboard.html',
                           total_users=total_users,
                           total_kategori=total_kategori,
                           total_barang=total_barang)