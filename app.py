from flask import Flask
from config import Config
from routes.main_routes import main_routes
from database.db import db
from database.table.user import User
from database.table.riwayat import Riwayat
from database.table.kecamatan import Kecamatan
from database.table.kelurahan import Kelurahan
from database.seeder.kelurahan_seeder import seed_wilayah_kendari
from flask_migrate import Migrate
from sqlalchemy.exc import OperationalError


app = Flask(__name__)
app.config.from_object(Config)

# register blueprint
app.register_blueprint(main_routes)

db.init_app(app)

migrate = Migrate(app, db)

# Buat semua tabel jika belum ada
with app.app_context():
    try:
        # 1. Seeder Admin
        admin_user = User.query.filter_by(username='annisa').first()
        if not admin_user:
            new_admin = User(username='annisa', password='annisa123')
            db.session.add(new_admin)
            db.session.commit()
            print("User 'annisa' berhasil ditambahkan!")
            
        # 2. Seeder Wilayah Kendari
        seed_wilayah_kendari()

    except OperationalError:
        print("Menunggu migrasi tabel selesai...")
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)