from flask import Blueprint
from controllers.klasifikasi_controller import (
    dashboard,
    input_data,
    klasifikasi,
    detail_riwayat,
    edit_riwayat,
    hapus_riwayat,
    perbandingan_algoritma,
    pesan_gizi,
    login,
    logout
)

from flask import request, redirect, url_for, session

main_routes = Blueprint('main_routes', __name__)

@main_routes.before_request
def require_login():
    allowed_routes = ['main_routes.login', 'static']
    if request.endpoint not in allowed_routes and 'user_id' not in session:
        return redirect(url_for('main_routes.login'))

main_routes.route('/login', methods=['GET', 'POST'])(login)
main_routes.route('/logout')(logout)

main_routes.route('/')(dashboard)

main_routes.route('/klasifikasi')(input_data)

main_routes.route('/klasifikasi/proses', methods=['POST'])(klasifikasi)

main_routes.route('/riwayat/<int:id>')(detail_riwayat)

main_routes.route('/riwayat/<int:id>/edit', methods=['GET', 'POST'])(edit_riwayat)

main_routes.route('/riwayat/<int:id>/hapus', methods=['POST'])(hapus_riwayat)

main_routes.route('/algoritma')(perbandingan_algoritma)

main_routes.route('/pesan-gizi')(pesan_gizi)