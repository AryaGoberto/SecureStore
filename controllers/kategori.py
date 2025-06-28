from flask import request, redirect, render_template, url_for, flash
from flask_login import login_required
from models.kategori import KategoriBarang
from models import db

@login_required
def kategori_list_controller():
    kategori_list = KategoriBarang.get_all()
    search_query = request.args.get('search', '')

    if search_query:
        kategori_list = KategoriBarang.query.filter(
            KategoriBarang.nama_kategori.ilike(f'%{search_query}%')
        ).all()
    else:
        kategori_list = KategoriBarang.get_all()

    return render_template('kategori/datakategori.html', kategoris=kategori_list, search_query=search_query)

@login_required
def tambah_kategori_controller():
    if request.method == 'POST':
        nama_kategori = request.form.get('nama_kategori')
        
        kategori_exists = KategoriBarang.query.filter_by(nama_kategori=nama_kategori).first()
        if kategori_exists:
            flash('Kategori with that name already exists!', 'error')
        else:
            new_kategori = KategoriBarang(nama_kategori=nama_kategori)
            new_kategori.save()
            flash('Kategori added successfully!', 'success')
            return redirect(url_for('kategoriapp.kategori_list'))
            
    return render_template('kategori/tambah-kategori.html')

@login_required
def hapus_kategori_controller(id):
    kategori = KategoriBarang.get_by_id(id)
    if kategori:
        if kategori.items:
            flash(f"Cannot delete category '{kategori.nama_kategori}' because it contains items. Please re-assign or delete the items first.", 'error')
        else:
            kategori.delete()
            flash('Kategori deleted successfully!', 'success')
    else:
        flash('Kategori not found!', 'error')
        
    return redirect(url_for('kategoriapp.kategori_list'))