import os
from app import app
from database.db import db
from database.table.kecamatan import Kecamatan
from database.table.kelurahan import Kelurahan

with app.app_context():
    kec = Kecamatan.query.filter(Kecamatan.nama.ilike('%ABELI%')).first()
    if kec:
        print(f"Kecamatan: {kec.nama}")
        kelurahans = [k.nama.title() for k in kec.kelurahans]
        print("|".join(kelurahans))
    else:
        print("Kecamatan Abeli tidak ditemukan")
