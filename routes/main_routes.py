from flask import Blueprint
from controllers.klasifikasi_controller import (
    dashboard,
    input_data,
    klasifikasi,
    detail_riwayat,
    edit_riwayat
)

main_routes = Blueprint('main_routes', __name__)

main_routes.route('/')(dashboard)

main_routes.route('/klasifikasi')(input_data)

main_routes.route('/klasifikasi/proses', methods=['POST'])(klasifikasi)

main_routes.route('/riwayat/<int:id>')(detail_riwayat)

main_routes.route('/riwayat/<int:id>/edit')(edit_riwayat)