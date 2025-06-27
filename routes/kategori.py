from flask import Blueprint
from controllers.kategori import kategori_list_controller, tambah_kategori_controller, hapus_kategori_controller
from flask_login import login_required

kategoriapp = Blueprint('kategoriapp', __name__)

@kategoriapp.route('/kategori/')
@login_required
def kategori_list():
    return kategori_list_controller()

@kategoriapp.route('/kategori/tambah/', methods=['GET', 'POST'])
@login_required
def tambah_kategori():
    return tambah_kategori_controller()

@kategoriapp.route('/kategori/hapus/<int:id>/', methods=['POST'])
@login_required
def hapus_kategori(id):
    return hapus_kategori_controller(id)