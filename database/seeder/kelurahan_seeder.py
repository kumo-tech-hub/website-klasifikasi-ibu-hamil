from database.db import db
from database.table.kecamatan import Kecamatan
from database.table.kelurahan import Kelurahan

def seed_wilayah_kendari():
    # Data Master 11 Kecamatan & 65 Kelurahan Kota Kendari
    data_kendari = {
        "Abeli": ["Abeli", "Anggolomelai", "Benua Nirae", "Lapulu", "Poasia", "Pudai", "Talia", "Tobimeita"],
        "Baruga": ["Baruga", "Lepo-Lepo", "Watubangga", "Wundudopi"],
        "Kadia": ["Anaiwoi", "Bende", "Kadia", "Pondambea", "Wawanggu"],
        "Kambu": ["Kambu", "Lalolara", "Mokoau", "Padaleu"],
        "Kendari": ["Gunung Jati", "Jati Mekar", "Kampungsalo", "Kandai", "Kassilampe", "Kendari Caddi", "Mangga Dua", "Mata", "Purirano"],
        "Kendari Barat": ["Benu-Benua", "Dapu-Dapura", "Kemaraya", "Lahundape", "Punggaloba", "Sadoha", "Sanua", "Tipulu", "Watu-Watu"],
        "Mandonga": ["Alolama", "Anggilowu", "Korumba", "Labibia", "Mandonga", "Wawombalata"],
        "Nambo": ["Bungkutoko", "Nambo", "Petoaha", "Sambuli", "Tondonggeu"],
        "Poasia": ["Anduonohu", "   Anggoeya", "Matabubu", "Rahandouna", "Wundumbatu"],
        "Puuwatu": ["Abeli Dalam", "Lalodati", "Punggolaka", "Puuwatu", "Tobuuha", "Watulondo"],
        "Wua-Wua": ["Anawai", "Bonggoeya", "Mataiwoi", "Wua-Wua"]
    }

    # Variabel penanda apakah ada data baru yang dimasukkan
    ada_data_baru = False

    for kec_nama, kel_list in data_kendari.items():
        # 1. Cek apakah Kecamatan sudah ada
        kecamatan = Kecamatan.query.filter_by(nama=kec_nama).first()
        
        if not kecamatan:
            kecamatan = Kecamatan(nama=kec_nama)
            db.session.add(kecamatan)
            db.session.commit() # Commit langsung agar kita mendapatkan ID kecamatannya
            ada_data_baru = True

        # 2. Loop dan cek masing-masing kelurahannya
        for kel_nama in kel_list:
            kelurahan = Kelurahan.query.filter_by(nama=kel_nama, kecamatan_id=kecamatan.id).first()
            if not kelurahan:
                kelurahan = Kelurahan(nama=kel_nama, kecamatan_id=kecamatan.id)
                db.session.add(kelurahan)
                ada_data_baru = True

    # 3. Commit semua data kelurahan yang baru ditambahkan
    if ada_data_baru:
        db.session.commit()
        print("Data 11 Kecamatan dan 65 Kelurahan Kota Kendari berhasil di-seed!")