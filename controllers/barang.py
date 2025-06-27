from flask import request, redirect, render_template, url_for, flash
from flask_login import login_required
from models.barang import DataBarang
from models.kategori import KategoriBarang
from models import db

@login_required
def barang_list_controller():
    barang_list = DataBarang.get_all()

    search_query = request.args.get('search', '')

    if search_query:
        barang_list = DataBarang.query.filter(
            DataBarang.nama_barang.ilike(f'%{search_query}%')
        ).all()
    else:
        barang_list = DataBarang.get_all()

    return render_template('barang/databarang.html', barangs=barang_list, search_query=search_query)

@login_required
def tambah_barang_controller():
    kategori_list = KategoriBarang.get_all()
    if request.method == 'POST':
        nama_barang = request.form.get('nama_barang')
        stok = request.form.get('stok_barang')
        kategori_id = request.form.get('kategori_barang')

        if not nama_barang or not stok or not kategori_id:
            # flash('All fields are required!', 'error')
            return render_template('barang/tambah-barang.html', kategori_list=kategori_list)
        
        new_barang = DataBarang(
            nama_barang=nama_barang,
            stok=int(stok),
            kategori_id=kategori_id
        )
        new_barang.save()
        # flash('Barang added successfully!', 'success')
        return redirect(url_for('barangapp.barang_list'))
    
    return render_template('barang/tambah-barang.html', kategori_list=kategori_list)

@login_required
def edit_barang_controller(id):
    barang = DataBarang.get_by_id(id)
    if not barang:
        # flash('Barang not found!', 'error')
        return redirect(url_for('barangapp.barang_list'))

    if request.method == 'POST':
        stok = request.form.get('stok_barang')
        
        if not stok:
            # flash('Stok field is required!', 'error')
            return render_template('barang/edit-barang.html', barang=barang)
            
        barang.stok = int(stok)
        barang.save()
        # flash('Stok updated successfully!', 'success')
        return redirect(url_for('barangapp.barang_list'))

    return render_template('barang/edit-barang.html', barang=barang)

@login_required
def hapus_barang_controller(id):
    barang = DataBarang.get_by_id(id)
    if barang:
        barang.delete()
        # flash('Barang deleted successfully!', 'success')
    # else:
        # flash('Barang not found!', 'error')

    return redirect(url_for('barangapp.barang_list'))