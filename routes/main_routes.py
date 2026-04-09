from flask import Blueprint
from controllers.klasifikasi_controller import (
    dashboard,
    input_data,
    klasifikasi,
    detail_riwayat,
    edit_riwayat,
    hapus_riwayat,
    perbandingan_algoritma,
    login,
    logout
)

main_routes = Blueprint('main_routes', __name__)

main_routes.route('/login', methods=['GET', 'POST'])(login)
main_routes.route('/logout')(logout)

main_routes.route('/')(dashboard)

main_routes.route('/klasifikasi')(input_data)

main_routes.route('/klasifikasi/proses', methods=['POST'])(klasifikasi)

main_routes.route('/riwayat/<int:id>')(detail_riwayat)

main_routes.route('/riwayat/<int:id>/edit')(edit_riwayat)

main_routes.route('/riwayat/<int:id>/hapus', methods=['POST'])(hapus_riwayat)

main_routes.route('/algoritma')(perbandingan_algoritma)