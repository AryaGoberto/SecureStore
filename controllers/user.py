from flask import request, redirect, render_template, url_for, flash, abort
from flask_login import login_required, current_user
from models.user import User
from models import db
from werkzeug.security import generate_password_hash

@login_required
def user_list_controller():
    if current_user.role != 'admin':
        # flash('You do not have permission to view user data.', 'error')
        return redirect(url_for('authapp.dashboard'))

    users = User.get_all()

    search_query = request.args.get('search', '')

    if search_query:
        users = User.query.filter(
            User.nama_lengkap.ilike(f'%{search_query}%')
        ).all()
    else:
        users = User.get_all()

    return render_template('user/datauser.html', users=users, search_query=search_query)

@login_required
def tambah_user_controller():
    if current_user.role != 'admin':
        # flash('You do not have permission to add users.', 'error')
        return redirect(url_for('authapp.dashboard'))

    if request.method == 'POST':
        nama_lengkap = request.form.get('nama_lengkap')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        konf_password = request.form.get('konf_password')
        role = request.form.get('role_user')

        user_exists_username = User.query.filter_by(username=username).first()
        user_exists_email = User.query.filter_by(email=email).first()

        if user_exists_username:
            flash('Username already exists.', 'error')
        elif user_exists_email:
            flash('Email already exists.', 'error')
        elif password != konf_password:
            flash('Passwords do not match.', 'error')
        else:
            new_user = User(
                nama_lengkap=nama_lengkap,
                username=username,
                email=email,
                role=role
            )
            new_user.set_password(password)
            new_user.save()
            # flash('User added successfully!', 'success')
            return redirect(url_for('userapp.user_list'))
    
    return render_template('user/tambah-user.html')

@login_required
def edit_user_controller(id):
    if current_user.role != 'admin':
        # flash('You do not have permission to edit users.', 'error')
        return redirect(url_for('authapp.dashboard'))

    user = User.get_by_id(id)
    if not user:
        # flash('User not found!', 'error')
        return redirect(url_for('userapp.user_list'))

    if request.method == 'POST':
        user.nama_lengkap = request.form.get('nama_lengkap')
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        new_password = request.form.get('password')
        konf_password = request.form.get('konf_password')
        user.role = request.form.get('role_user')

        if new_password:
            if new_password != konf_password:
                # flash('Passwords do not match!', 'error')
                return render_template('user/edit-user.html', user=user)
            user.set_password(new_password)

        user.save()
        # flash('User updated successfully!', 'success')
        return redirect(url_for('userapp.user_list'))

    return render_template('user/edit-user.html', user=user)

@login_required
def hapus_user_controller(id):
    if current_user.role != 'admin':
        # flash('You do not have permission to delete users.', 'error')
        return redirect(url_for('authapp.dashboard'))

    user = User.get_by_id(id)
    if user:
        if str(user.id) == current_user.get_id():
            flash('You cannot delete your own account!', 'error')
        else:
            user.delete()
            # flash('User deleted successfully!', 'success')
    else:
        flash('User not found!', 'error')

    return redirect(url_for('userapp.user_list'))