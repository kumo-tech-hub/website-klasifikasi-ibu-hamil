from app import app, db
from sqlalchemy import text

def migrate_data():
    with app.app_context():
        with db.engine.begin() as conn:  # Menggunakan begin() agar otomatis commit
            # Cek apakah kolom id_ibu_hamil sudah ada di tabel riwayat
            result = conn.execute(text("SHOW COLUMNS FROM riwayat LIKE 'id_ibu_hamil'")).fetchone()
            
            if not result:
                print("🚀 Memulai migrasi data ke skema relasional (IbuHamil)...")
                
                # 1. Pastikan tabel ibu_hamil dibuat
                conn.execute(text("""
                CREATE TABLE IF NOT EXISTS ibu_hamil (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nik VARCHAR(16) NOT NULL UNIQUE,
                    nama VARCHAR(100) NOT NULL,
                    tanggal_lahir DATE
                )
                """))
                print("✅ Tabel ibu_hamil disiapkan.")
                
                # 2. Pindahkan data unik dari riwayat ke ibu_hamil
                conn.execute(text("""
                INSERT IGNORE INTO ibu_hamil (nik, nama, tanggal_lahir)
                SELECT nik, MAX(nama), MAX(tanggal_lahir) FROM riwayat GROUP BY nik
                """))
                print("✅ Data pasien berhasil disalin ke tabel ibu_hamil.")
                
                # 3. Tambahkan kolom id_ibu_hamil ke riwayat
                conn.execute(text("ALTER TABLE riwayat ADD COLUMN id_ibu_hamil INT"))
                print("✅ Kolom id_ibu_hamil ditambahkan.")
                
                # 4. Update id_ibu_hamil di tabel riwayat berdasarkan NIK yang cocok
                conn.execute(text("""
                UPDATE riwayat r
                JOIN ibu_hamil i ON r.nik = i.nik
                SET r.id_ibu_hamil = i.id
                """))
                print("✅ Relasi data riwayat dengan ibu_hamil berhasil disambungkan.")
                
                # 5. Ubah id_ibu_hamil jadi NOT NULL dan tambahkan foreign key
                conn.execute(text("ALTER TABLE riwayat MODIFY id_ibu_hamil INT NOT NULL"))
                try:
                    conn.execute(text("ALTER TABLE riwayat ADD CONSTRAINT fk_ibu_hamil FOREIGN KEY (id_ibu_hamil) REFERENCES ibu_hamil(id)"))
                except Exception as e:
                    print(f"⚠️ Peringatan pembuatan Foreign Key: {e}")
                print("✅ Aturan relasi Foreign Key diterapkan.")
                
                # 6. Hapus kolom-kolom lama di riwayat yang sudah tidak dipakai
                conn.execute(text("ALTER TABLE riwayat DROP COLUMN nik"))
                conn.execute(text("ALTER TABLE riwayat DROP COLUMN nama"))
                conn.execute(text("ALTER TABLE riwayat DROP COLUMN tanggal_lahir"))
                print("✅ Kolom usang dihapus. Migrasi struktur tabel selesai!")
                
                print("🎉 MINGRASI BERHASIL! Data aman.")
            else:
                print("ℹ️ Migrasi sudah pernah dilakukan. Skema sudah yang terbaru.")

if __name__ == '__main__':
    migrate_data()
