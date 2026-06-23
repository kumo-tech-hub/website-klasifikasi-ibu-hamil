from database.db import db
from datetime import datetime


class Riwayat(db.Model):
    __tablename__ = "riwayat"

    id             = db.Column(db.Integer, primary_key=True)
    id_ibu_hamil   = db.Column(db.Integer, db.ForeignKey('ibu_hamil.id'), nullable=False)
    kecamatan      = db.Column(db.String(100), nullable=False)
    kelurahan      = db.Column(db.String(100), nullable=False)
    umur           = db.Column(db.Integer,     nullable=False)
    bb_awal        = db.Column(db.Float,       nullable=False)
    bb_sekarang    = db.Column(db.Float,       nullable=False)
    tinggi_badan   = db.Column(db.Float,       nullable=False)
    lila           = db.Column(db.Float,       nullable=False)
    trimester      = db.Column(db.Integer,     nullable=False)
    imt            = db.Column(db.Float,       nullable=False)
    status         = db.Column(db.String(20),  nullable=False)
    algoritma      = db.Column(db.String(50),  nullable=False)
    tanggal        = db.Column(db.DateTime,    default=datetime.now)

    def to_dict(self):
        return {
            'id':           self.id,
            'nama':         self.ibu_hamil.nama if self.ibu_hamil else '',
            'nik':          self.ibu_hamil.nik if self.ibu_hamil else '',
            'kecamatan':    self.kecamatan,
            'kelurahan':    self.kelurahan,
            'tanggal_lahir': self.ibu_hamil.tanggal_lahir.strftime('%Y-%m-%d') if (self.ibu_hamil and self.ibu_hamil.tanggal_lahir) else '',
            'umur':         self.umur,
            'bb_awal':      self.bb_awal,
            'bb_sekarang':  self.bb_sekarang,
            'tinggi_badan': self.tinggi_badan,
            'lila':         self.lila,
            'trimester':    self.trimester,
            'imt':          self.imt,
            'status':       self.status,
            'algoritma':    self.algoritma,
            'tanggal':      self.tanggal.strftime('%d %b %Y') if self.tanggal else '-',
        }

    def __repr__(self):
        nama = self.ibu_hamil.nama if self.ibu_hamil else 'Unknown'
        return f"<Riwayat {nama} - {self.status}>"
