from flask import Flask
from config import Config
from routes.main_routes import main_routes
from database.db import db
from database.table.user import User
from database.table.riwayat import Riwayat


app = Flask(__name__)
app.config.from_object(Config)

# register blueprint
app.register_blueprint(main_routes)

db.init_app(app)

# Buat semua tabel jika belum ada
with app.app_context():
    db.create_all()
    
    # Cek apakah user sudah ada di database, jika tidak buat otomatis
    admin_user = User.query.filter_by(username='annisa').first()
    if not admin_user:
        new_admin = User(username='annisa', password='annisa123')
        db.session.add(new_admin)
        db.session.commit()
        print("✅ User 'annisa' berhasil ditambahkan ke database!")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)