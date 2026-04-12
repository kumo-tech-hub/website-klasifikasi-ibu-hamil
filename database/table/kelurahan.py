from database.db import db
from datetime import datetime


class Kelurahan(db.Model):
    __tablename__ = 'kelurahan'

    id             = db.Column(db.Integer, primary_key=True)
    nama           = db.Column(db.String(100), nullable=False)
    kecamatan_id   = db.Column(db.Integer,db.ForeignKey('kecamatan.id'), nullable=False)