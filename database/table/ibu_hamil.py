from database.db import db

class IbuHamil(db.Model):
    __tablename__ = "ibu_hamil"

    id = db.Column(db.Integer, primary_key=True)
    nik = db.Column(db.String(16), nullable=False, unique=True)
    nama = db.Column(db.String(100), nullable=False)
    tanggal_lahir = db.Column(db.Date)

    # Relationship back to Riwayat
    riwayat_list = db.relationship('Riwayat', backref='ibu_hamil', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<IbuHamil {self.nik} - {self.nama}>"
