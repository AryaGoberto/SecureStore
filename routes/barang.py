from flask import Blueprint
from controllers.barang import barang_list_controller, tambah_barang_controller, edit_barang_controller, hapus_barang_controller
from flask_login import login_required

barangapp = Blueprint('barangapp', __name__)

@barangapp.route('/barang/')
@login_required
def barang_list():
    return barang_list_controller()

@barangapp.route('/barang/tambah/', methods=['GET', 'POST'])
@login_required
def tambah_barang():
    return tambah_barang_controller()

@barangapp.route('/barang/edit/<int:id>/', methods=['GET', 'POST'])
@login_required
def edit_barang(id):
    return edit_barang_controller(id)

@barangapp.route('/barang/hapus/<int:id>/', methods=['POST'])
@login_required
def hapus_barang(id):
    return hapus_barang_controller(id)