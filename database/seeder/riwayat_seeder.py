import os
import re
import pandas as pd
from datetime import datetime


def seed_riwayat(db, Riwayat):
    """
    Seeder data riwayat klasifikasi dari file Excel data ANC Bumil.
    Hanya berjalan jika tabel riwayat masih kosong.
    """

    if Riwayat.query.count() > 0:
        print("Seeder Riwayat: Sudah ada data, seeder dilewati.")
        return

    # Path file Excel (relatif dari root project)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    excel_path = os.path.join(base_dir, "ml", "Data ANC Bumil - NEWW fb - Copy - Copy.xlsx")

    if not os.path.exists(excel_path):
        print(f"Seeder Riwayat: File Excel tidak ditemukan di {excel_path}")
        return

    try:
        df = pd.read_excel(excel_path)
    except Exception as e:
        print(f"Seeder Riwayat: Gagal membaca file Excel — {e}")
        return

    def minggu_ke_trimester(usia_str):
        """Konversi string 'X Minggu' ke nomor trimester (1, 2, atau 3)."""
        try:
            match = re.search(r'\d+', str(usia_str))
            if not match:
                return 1
            minggu = int(match.group())
            if minggu <= 13:
                return 1
            elif minggu <= 26:
                return 2
            else:
                return 3
        except Exception:
            return 1

    def bersihkan_nik(nik):
        """Bersihkan karakter aneh dari NIK (misal karakter unknown di akhir)."""
        if pd.isna(nik):
            return "000000000000000"
        nik_str = str(nik).strip()
        # Ambil hanya angka, maksimal 16 digit
        angka = re.sub(r'[^\d]', '', nik_str)
        return angka[:16] if angka else "000000000000000"

    def parse_tanggal(tanggal_val):
        """Parse kolom tanggal, return datetime atau now jika gagal."""
        if pd.isna(tanggal_val):
            return datetime.now()
        if isinstance(tanggal_val, datetime):
            return tanggal_val
        try:
            return pd.to_datetime(tanggal_val).to_pydatetime()
        except Exception:
            return datetime.now()

    inserted = 0
    skipped  = 0

    for _, row in df.iterrows():
        try:
            # Validasi kolom wajib tidak kosong
            if pd.isna(row.get('Nama')) or pd.isna(row.get('Status Gizi')):
                skipped += 1
                continue

            status_gizi = str(row['Status Gizi']).strip()
            if status_gizi not in ('Normal', 'Kurang', 'Lebih', 'Obesitas'):
                skipped += 1
                continue

            # Ambil nilai — gunakan default aman jika kolom kosong
            nama          = str(row['Nama']).strip()
            nik           = bersihkan_nik(row.get('NIK'))
            umur          = int(row['Umur']) if not pd.isna(row.get('Umur')) else 0
            bb_awal       = float(row['Berat Badan Awal'])     if not pd.isna(row.get('Berat Badan Awal'))     else 0.0
            bb_sekarang   = float(row['Berat Badan Sekarang']) if not pd.isna(row.get('Berat Badan Sekarang')) else bb_awal
            tinggi_badan  = float(row['Tinggi'])               if not pd.isna(row.get('Tinggi'))               else 0.0
            lila          = float(row['LiLA'])                 if not pd.isna(row.get('LiLA'))                 else 0.0
            imt           = float(row['IMT Sebelum Hamil'])    if not pd.isna(row.get('IMT Sebelum Hamil'))    else 0.0
            trimester     = minggu_ke_trimester(row.get('Usia Kehamilan'))
            tanggal       = parse_tanggal(row.get('Tanggal ANC'))

            # Kecamatan & kelurahan dari kolom "Desa/Kel Domisili"
            # Data hanya punya 1 kolom wilayah, kita pakai sebagai kelurahan
            # dan isi kecamatan dengan "Kendari" sebagai default
            kelurahan  = str(row['Desa/Kel Domisili']).strip() if not pd.isna(row.get('Desa/Kel Domisili')) else 'Tidak Diketahui'
            kecamatan  = 'Abeli'   # default kota karena data tidak mencantumkan kecamatan

            riwayat = Riwayat(
                nama         = nama,
                nik          = nik,
                kecamatan    = kecamatan,
                kelurahan    = kelurahan,
                umur         = umur,
                bb_awal      = bb_awal,
                bb_sekarang  = bb_sekarang,
                tinggi_badan = tinggi_badan,
                lila         = lila,
                trimester    = trimester,
                imt          = imt,
                status       = status_gizi,
                algoritma    = 'Data Historis (Excel)',
                tanggal      = tanggal,
            )
            db.session.add(riwayat)
            inserted += 1

        except Exception as e:
            print(f"Seeder Riwayat: Baris gagal diproses — {e}")
            skipped += 1
            continue

    try:
        db.session.commit()
        print(f"Seeder Riwayat: Berhasil memasukkan {inserted} data. ({skipped} baris dilewati)")
    except Exception as e:
        db.session.rollback()
        print(f"Seeder Riwayat: Gagal commit ke database — {e}")
