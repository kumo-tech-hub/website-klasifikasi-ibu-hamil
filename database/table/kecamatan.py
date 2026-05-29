from database.db import db
from datetime import datetime


class Kecamatan(db.Model):
    __tablename__ = 'kecamatan'

    id             = db.Column(db.Integer, primary_key=True)
    nama           = db.Column(db.String(100), nullable=False)
    kelurahan_list = db.relationship('Kelurahan', backref='kecamatan', lazy=True)