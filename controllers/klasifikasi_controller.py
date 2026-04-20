from flask import render_template, request, redirect, url_for, session,current_app
from database.db import db
from database.table.riwayat import Riwayat
from database.table.user import User
from collections import Counter
from datetime import datetime
from database.table.kecamatan import Kecamatan
from database.table.kelurahan import Kelurahan
import os

# ─────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────

def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Mengecek user ke database
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('main_routes.dashboard'))
        else:
            return render_template('login.html', error='Username atau password salah')
    return render_template('login.html')

def logout():
    session.clear()
    return redirect(url_for('main_routes.login'))

# ─────────────────────────────────────────────
# Lookup tables (tetap di memori, tidak perlu DB)
# ─────────────────────────────────────────────

PERBANDINGAN = {
    'XGBoost': {
        'accuracy':  round((94.2 + 91.8) / 2, 1),
        'precision': round((93.8 + 92.1) / 2, 1),
        'recall':    round((93.5 + 94.7) / 2, 1),
        'f1':        round((93.6 + 93.4) / 2, 1),
    },
    'CatBoost': {
        'accuracy':  round((95.1 + 93.0) / 2, 1),
        'precision': round((94.6 + 93.5) / 2, 1),
        'recall':    round((94.2 + 96.1) / 2, 1),
        'f1':        round((94.4 + 94.8) / 2, 1),
    },
}

# Detail tiap variant (untuk referensi / pengembangan)
PERBANDINGAN_DETAIL = {
    'XGBoost Baseline': {'accuracy': 94.2, 'precision': 93.8, 'recall': 93.5, 'f1': 93.6},
    'XGBoost SMOTE':    {'accuracy': 91.8, 'precision': 92.1, 'recall': 94.7, 'f1': 93.4},
    'CatBoost Baseline':{'accuracy': 95.1, 'precision': 94.6, 'recall': 94.2, 'f1': 94.4},
    'CatBoost SMOTE':   {'accuracy': 93.0, 'precision': 93.5, 'recall': 96.1, 'f1': 94.8},
}

TIPS = {
    'Normal': [
        'Mempertahankan pola makan yang sehat dan seimbang (karbohidrat, protein, lemak, vitamin, dan mineral).',
        'Mengonsumsi makanan bergizi seperti sayur, buah, protein hewani, dan nabati.',
        'Tetap rutin melakukan pemeriksaan kehamilan.',
        'Menjaga aktivitas fisik ringan seperti jalan santai atau senam ibu hamil.',
        'Memastikan asupan air putih cukup setiap hari.'
    ],
    'Kurang': [
        'Meningkatkan asupan kalori dan protein (misalnya dari telur, ikan, daging, susu).',
        'Mengonsumsi makanan tambahan atau suplemen sesuai anjuran tenaga kesehatan.',
        'Makan dengan porsi kecil tetapi lebih sering.',
        'Memperhatikan asupan zat besi dan asam folat.',
        'Segera berkonsultasi dengan bidan atau ahli gizi untuk penanganan lebih lanjut.'
    ],
    'Lebih': [
        'Mengontrol pola makan dengan mengurangi makanan tinggi gula dan lemak.',
        'Memperbanyak konsumsi makanan berserat seperti sayur dan buah.',
        'Mengatur porsi makan agar tidak berlebihan.',
        'Melakukan aktivitas fisik ringan secara rutin.',
        'Konsultasi dengan tenaga kesehatan untuk menjaga kenaikan berat badan tetap ideal.'
    ],
    'Obesitas': [
        'Melakukan pengaturan pola makan secara ketat namun tetap memenuhi kebutuhan nutrisi ibu dan janin.',
        'Menghindari makanan cepat saji, tinggi gula, dan lemak berlebih.',
        'Rutin melakukan aktivitas fisik sesuai anjuran (misalnya senam hamil).',
        'Melakukan pemantauan berat badan secara berkala.',
        'Wajib berkonsultasi secara intensif dengan tenaga kesehatan (dokter, bidan, atau ahli gizi).'
    ]
}

REKOMENDASI_BB = {
    'Kurang': '12,5 - 18 Kg',
    'Normal': '11,5 - 16 Kg',
    'Lebih': '7 - 11,5 Kg',
    'Obesitas': '5 - 9 Kg'
}


CONFUSION = {
    'XGBoost': [
        [45, 3, 2],
        [1, 38, 4],
        [2, 1, 44],
    ],
    'CatBoost': [
        [42, 5, 3],
        [2, 35, 6],
        [3, 2, 42],
    ],
}

def dashboard():
    bulan = request.args.get('bulan')
    tahun = request.args.get('tahun')
    page  = request.args.get('page', 1, type=int)
    per_page = 8

    query = Riwayat.query

    if tahun:
        query = query.filter(db.extract('year', Riwayat.tanggal) == int(tahun))
    if bulan:
        query = query.filter(db.extract('month', Riwayat.tanggal) == int(bulan))

    # Pagination — 8 data per halaman
    pagination  = query.order_by(Riwayat.tanggal.desc()).paginate(page=page, per_page=per_page, error_out=False)
    riwayat_page = [r.to_dict() for r in pagination.items]

    # Statistik dihitung dari SEMUA data (bukan hanya halaman ini)
    semua        = query.all()
    riwayat_list = [r.to_dict() for r in semua]

    total    = len(riwayat_list)
    normal   = sum(1 for r in riwayat_list if r['status'] == 'Normal')
    kurang   = sum(1 for r in riwayat_list if r['status'] == 'Kurang')
    lebih    = sum(1 for r in riwayat_list if r['status'] == 'Lebih')
    obesitas = sum(1 for r in riwayat_list if r['status'] == 'Obesitas')
    wilayah  = len(set(r['kelurahan'] for r in riwayat_list))

    ringkasan = {
        'total': total,
        'normal': normal,
        'kurang': kurang,
        'lebih': lebih,
        'obesitas': obesitas,
        'wilayah': wilayah,
    }

    wilayah_data = {}
    for r in riwayat_list:
        kel = r.get('kelurahan', 'Lainnya')
        if kel not in wilayah_data:
            wilayah_data[kel] = {'jumlah': 0, 'status_list': []}
        wilayah_data[kel]['jumlah'] += 1
        wilayah_data[kel]['status_list'].append(r['status'])

    segmentasi_wilayah = []
    for kel, info in wilayah_data.items():
        counter = Counter(info['status_list'])
        dominan = counter.most_common(1)[0][0]
        segmentasi_wilayah.append({
            'kelurahan': kel,
            'jumlah':    info['jumlah'],
            'dominan':   dominan,
            'normal':    counter.get('Normal', 0),
            'kurang':    counter.get('Kurang', 0),
            'lebih':     counter.get('Lebih', 0),
            'obesitas':  counter.get('Obesitas', 0),
        })

    folder_path = os.path.join(current_app.root_path,'static','kelurahan_geojson')

    daftar_file_geojson = []
    if os.path.exists(folder_path):
        daftar_file_geojson = [f for f in os.listdir(folder_path) if f.endswith('.geojson')]

    return render_template(
        'dashboard.html',
        riwayat=riwayat_page,
        pagination=pagination,
        ringkasan=ringkasan,
        perbandingan=PERBANDINGAN,
        segmentasi_wilayah=segmentasi_wilayah,
        daftar_file_geojson=daftar_file_geojson,
        bulan=bulan,
        tahun=tahun,
    )



# ─────────────────────────────────────────────
# INPUT FORM
# ─────────────────────────────────────────────

def input_data():
    kecamatans = Kecamatan.query.all()

    data_wilayah = {}
    for kec in kecamatans:
        # Asumsi Anda menggunakan db.relationship('Kelurahan') dengan backref='kecamatan'
        data_wilayah[kec.nama] = [kel.nama for kel in kec.kelurahan_list]
    return render_template(
        'input.html',
        kecamatans=kecamatans, 
        data_wilayah=data_wilayah
        )


# ─────────────────────────────────────────────
# KLASIFIKASI — proses ML + simpan ke DB
# ─────────────────────────────────────────────

def klasifikasi():
    nama         = request.form.get('nama')
    nik          = request.form.get('nik', '')
    kecamatan    = request.form.get('kecamatan', '')
    kelurahan    = request.form.get('kelurahan', '')
    umur         = float(request.form.get('umur'))
    bb_awal      = float(request.form.get('bb_awal'))
    bb_sekarang  = float(request.form.get('bb_sekarang'))
    tinggi_badan = float(request.form.get('tinggi_badan'))
    lila         = float(request.form.get('lila'))
    trimester    = int(request.form.get('trimester'))

    tinggi_m = tinggi_badan / 100
    imt = round(bb_awal / (tinggi_m ** 2), 2)

    import joblib
    import pandas as pd

    input_df = pd.DataFrame(
        [[umur, bb_awal, tinggi_badan, imt, lila]],
        columns=['umur', 'berat_badan_awal', 'tinggi', 'imt_sebelum_hamil', 'lila']
    )

    predictions = {}
    mapping_status = {0: 'Kurang', 1: 'Normal', 2: 'Lebih', 3: 'Obesitas'}
    nama_algoritma = None   # akan diisi otomatis oleh model dengan confidence tertinggi
    status = 'Normal'

    try:
        import numpy as np
        import joblib
        import os

        model_paths = {
            'XGBoost (SMOTE)': 'ml/model_xgb_smote.pkl',
            'XGBoost (Baseline)': 'ml/model_xgb_baseline.pkl',
            'CatBoost (SMOTE)': 'ml/model_cat_smote.pkl',
            'CatBoost (Baseline)': 'ml/model_cat_baseline.pkl'
        }

        for m_name, rel_path in model_paths.items():
            try:
                abs_path = os.path.join(current_app.root_path, rel_path)
                if not os.path.exists(abs_path):
                    print(f"DEBUG: File model tidak ditemukan: {abs_path}")
                    continue
                
                model = joblib.load(abs_path)
                
                # Gunakan values untuk menghindari masalah nama kolom pada XGBoost
                pred = model.predict(input_df.values)
                
                prob = None
                try:
                    proba = model.predict_proba(input_df.values)
                    if proba is not None and len(proba) > 0:
                        prob = round(float(np.max(proba[0])) * 100, 2)
                except Exception as prob_e:
                    print(f"DEBUG: Error proba {m_name}: {prob_e}")

                # Ambil nilai tunggal hasil prediksi
                temp_pred = pred
                if isinstance(temp_pred, (list, tuple, np.ndarray)):
                    if isinstance(temp_pred, np.ndarray):
                        temp_pred = temp_pred.flatten()[0]
                    else:
                        temp_pred = temp_pred[0]

                # Konversi ke status teks
                if str(temp_pred).isdigit() or isinstance(temp_pred, (int, float, np.integer)):
                    m_status = mapping_status.get(int(temp_pred), 'Normal')
                else:
                    m_status = str(temp_pred).strip("[]'\" ")

                predictions[m_name] = {
                    'status': m_status,
                    'probability': prob
                }

                print(f"DEBUG: Model {m_name} berhasil: {m_status} ({prob}%)")
            except Exception as inner_e:
                error_msg = str(inner_e)
                print(f"DEBUG: Error pada model {m_name}: {error_msg}")
                predictions[m_name] = {
                    'status': 'Error',
                    'error': error_msg
                }
                import traceback
                traceback.print_exc()

        # ── Pilih model dengan confidence (probability) tertinggi ──────
        best_prob = -1
        for m_name, m_data in predictions.items():
            if m_data.get('status') != 'Error' and m_data.get('probability') is not None:
                if m_data['probability'] > best_prob:
                    best_prob      = m_data['probability']
                    status         = m_data['status']
                    nama_algoritma = m_name

        # Fallback jika semua model error atau tidak punya probability
        if nama_algoritma is None:
            for m_name, m_data in predictions.items():
                if m_data.get('status') != 'Error':
                    status         = m_data['status']
                    nama_algoritma = m_name
                    break

        if nama_algoritma is None:
            nama_algoritma = 'Tidak Diketahui'

        print(f"DEBUG: Semua predictions: {list(predictions.keys())}")
        print(f"DEBUG: Model terpilih: {nama_algoritma} — {status} ({best_prob}%)")

    except Exception as e:
        print("Error utama saat prediksi:", e)

    # ── Simpan ke database ──────────────────────
    baru = Riwayat(
        nama=nama,
        nik=nik,
        kecamatan=kecamatan,
        kelurahan=kelurahan,
        umur=int(umur),
        bb_awal=bb_awal,
        bb_sekarang=bb_sekarang,
        tinggi_badan=tinggi_badan,
        lila=lila,
        trimester=trimester,
        imt=imt,
        status=status,
        algoritma=nama_algoritma,
        tanggal=datetime.now(),
    )
    db.session.add(baru)
    db.session.commit()
    # ────────────────────────────────────────────

    hasil = {
        'nama':             nama,
        'nik':              nik,
        'kecamatan':        kecamatan,
        'kelurahan':        kelurahan,
        'umur':             umur,
        'bb_awal':          bb_awal,
        'bb_sekarang':      bb_sekarang,
        'tinggi_badan':     tinggi_badan,
        'lila':             lila,
        'trimester':        trimester,
        'imt':              imt,
        'status':           status,
        'algoritma_dipakai': nama_algoritma,
        'tips':             TIPS.get(status, []),
        'rekomendasi_bb':   REKOMENDASI_BB.get(status, '-'),
        'predictions':      predictions
    }

    return render_template('hasil.html', hasil=hasil)


# ─────────────────────────────────────────────
# DETAIL RIWAYAT
# ─────────────────────────────────────────────

def detail_riwayat(id):
    data = Riwayat.query.get(id)

    if data is None:
        return redirect(url_for('main_routes.dashboard'))

    detail = data.to_dict()
    detail['tips'] = TIPS.get(detail['status'], [])
    detail['rekomendasi_bb'] = REKOMENDASI_BB.get(detail['status'], '-')

    return render_template('detail.html', data=detail)


# ─────────────────────────────────────────────
# EDIT RIWAYAT
# ─────────────────────────────────────────────

def edit_riwayat(id):
    data = Riwayat.query.get(id)

    if data is None:
        return redirect(url_for('main_routes.dashboard'))

    return render_template('edit.html', data=data.to_dict())


# ─────────────────────────────────────────────
# HAPUS RIWAYAT
# ─────────────────────────────────────────────

def hapus_riwayat(id):
    data = Riwayat.query.get(id)
    if data:
        db.session.delete(data)
        db.session.commit()
    return redirect(url_for('main_routes.dashboard'))


# ─────────────────────────────────────────────
# PERBANDINGAN ALGORITMA
# ─────────────────────────────────────────────

def perbandingan_algoritma():
    xgb = PERBANDINGAN['XGBoost']
    cat = PERBANDINGAN['CatBoost']

    # Hitung pemenang tiap metrik
    metrik_list = ['accuracy', 'precision', 'recall', 'f1']
    metrik_label = {
        'accuracy':  'Accuracy',
        'precision': 'Precision',
        'recall':    'Recall',
        'f1':        'F1-Score',
    }

    xgb_wins = 0
    cat_wins = 0
    detail_metrik = []

    for m in metrik_list:
        xgb_val = xgb[m]
        cat_val = cat[m]
        if xgb_val >= cat_val:
            winner = 'XGBoost'
            xgb_wins += 1
        else:
            winner = 'CatBoost'
            cat_wins += 1
        detail_metrik.append({
            'nama':    metrik_label[m],
            'key':     m,
            'xgb':     xgb_val,
            'cat':     cat_val,
            'winner':  winner,
            'selisih': round(abs(xgb_val - cat_val), 1),
        })

    # Pemenang keseluruhan (berdasarkan jumlah metrik lebih unggul)
    if xgb_wins > cat_wins:
        overall_winner        = 'XGBoost'
        overall_winner_color  = 'xgb'
        runner_up             = 'CatBoost'
    elif cat_wins > xgb_wins:
        overall_winner        = 'CatBoost'
        overall_winner_color  = 'cat'
        runner_up             = 'XGBoost'
    else:
        # Seri — bandingkan F1 sebagai tie-breaker
        overall_winner        = 'XGBoost' if xgb['f1'] >= cat['f1'] else 'CatBoost'
        overall_winner_color  = 'xgb' if overall_winner == 'XGBoost' else 'cat'
        runner_up             = 'CatBoost' if overall_winner == 'XGBoost' else 'XGBoost'

    # Kalimat deskripsi dinamis berdasarkan pemenang
    winner_data   = xgb if overall_winner == 'XGBoost' else cat
    runnerup_data = cat if overall_winner == 'XGBoost' else xgb

    # Metrik apa yang paling dominan perbedaannya?
    largest = max(detail_metrik, key=lambda x: x['selisih'])

    kesimpulan = {
        'winner':              overall_winner,
        'winner_color':        overall_winner_color,
        'runner_up':           runner_up,
        'xgb_wins':            xgb_wins,
        'cat_wins':            cat_wins,
        'detail_metrik':       detail_metrik,
        'winner_accuracy':     winner_data['accuracy'],
        'runnerup_accuracy':   runnerup_data['accuracy'],
        'winner_f1':           winner_data['f1'],
        'largest_diff_metric': largest['nama'],
        'largest_diff_val':    largest['selisih'],
    }

    return render_template(
        'algoritma.html',
        perbandingan=PERBANDINGAN,
        confusion=CONFUSION,
        kesimpulan=kesimpulan,
    )