from flask import request, redirect, render_template, url_for, flash, current_app
from flask_login import login_required, current_user
from models.user import User
from models import db
from werkzeug.security import generate_password_hash

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@login_required
def user_list_controller():
    if current_user.role != 'admin':
        flash('Anda tidak memiliki izin untuk mengakses halaman ini.', 'error')
        return redirect(url_for('authapp.dashboard'))

    search_query = request.args.get('search', '')
    if search_query:
        # Mengambil data dari query langsung untuk pencarian
        users_query = User.query.filter(User.nama_lengkap.ilike(f'%{search_query}%')).all()
        users = [user.data for user in users_query] # Mengubah ke format dictionary
    else:
        # Mengambil semua user jika tidak ada pencarian
        users = User.get_all()

    return render_template('user/datauser.html', users=users, search_query=search_query)

@login_required
def tambah_user_controller():
    if current_user.role != 'admin':
        flash('Anda tidak memiliki izin untuk menambah user.', 'error')
        return redirect(url_for('authapp.dashboard'))

    if request.method == 'POST':
        nama_lengkap = request.form.get('nama_lengkap')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        konf_password = request.form.get('konf_password')
        role = request.form.get('role_user')
        
        profile_pic_data = None
        profile_pic_mimetype = None

        user_exists_username = User.query.filter_by(username=username).first()
        user_exists_email = User.query.filter_by(email=email).first()

        if user_exists_username:
            flash('Username sudah digunakan.', 'error')
        elif user_exists_email:
            flash('Email sudah terdaftar.', 'error')
        elif password != konf_password:
            flash('Password dan konfirmasi password tidak cocok.', 'error')
        else:
            file = request.files.get('foto-profil')
            if file and file.filename != '' and allowed_file(file.filename):
                try:
                    profile_pic_data = file.read()
                    profile_pic_mimetype = file.mimetype
                except Exception as e:
                    flash(f'Gagal membaca file: {e}', 'error')
                    return render_template('user/tambah-user.html')

            new_user = User(
                nama_lengkap=nama_lengkap,
                username=username,
                email=email,
                role=role,
                profile_pic=profile_pic_data,
                profile_pic_mimetype=profile_pic_mimetype
            )
            
            new_user.set_password(password)
            new_user.save()
            flash('User berhasil ditambahkan!', 'success')
            return redirect(url_for('userapp.user_list'))
    
    return render_template('user/tambah-user.html')

@login_required
def edit_user_controller(id):
    if current_user.role != 'admin':
        flash('Anda tidak memiliki izin untuk mengedit user.', 'error')
        return redirect(url_for('authapp.dashboard'))

    user = User.get_by_id(id)
    if not user:
        flash('User tidak ditemukan!', 'error')
        return redirect(url_for('userapp.user_list'))

    if request.method == 'POST':
        user.nama_lengkap = request.form.get('nama_lengkap')
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        new_password = request.form.get('password')
        konf_password = request.form.get('konf_password')
        user.role = request.form.get('role_user')

        file = request.files.get('foto-profil')

        if file and file.filename != '' and allowed_file(file.filename):
            try:
                user.profile_pic = file.read()
                user.profile_pic_mimetype = file.mimetype
            except Exception as e:
                flash(f'Gagal membaca file: {e}', 'error')
                return render_template('user/edit-user.html', user=user)
        elif file and not allowed_file(file.filename):
            flash('Jenis file tidak valid. Gunakan png, jpg, atau jpeg.', 'error')
            return render_template('user/edit-user.html', user=user)

        if new_password:
            if new_password != konf_password:
                flash('Password baru dan konfirmasi tidak cocok!', 'error')
                return render_template('user/edit-user.html', user=user)
            user.set_password(new_password)

        user.save()
        flash('Data user berhasil diperbarui!', 'success')
        return redirect(url_for('userapp.user_list'))

    return render_template('user/edit-user.html', user=user)

@login_required
def hapus_user_controller(id):
    if current_user.role != 'admin':
        flash('Anda tidak memiliki izin untuk menghapus user.', 'error')
        return redirect(url_for('authapp.dashboard'))

    user = User.get_by_id(id)
    if user:
        if str(user.id) == current_user.get_id():
            flash('Anda tidak dapat menghapus akun Anda sendiri!', 'error')
        else:
            user.delete()
            flash('User berhasil dihapus!', 'success')
    else:
        flash('User tidak ditemukan!', 'error')

    return redirect(url_for('userapp.user_list'))