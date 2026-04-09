from flask import render_template, request, redirect, url_for, session
from database.db import db
from database.table.riwayat import Riwayat
from database.table.user import User
from collections import Counter
from datetime import datetime

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
    'XGBoost': {'accuracy': 96.5, 'precision': 95.8, 'recall': 96.2, 'f1': 96.0},
    'CatBoost': {'accuracy': 97.2, 'precision': 96.9, 'recall': 97.0, 'f1': 96.9},
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

# ─────────────────────────────────────────────
# Confusion matrix dummy
# ─────────────────────────────────────────────

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


# ─────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────

def dashboard():
    semua = Riwayat.query.order_by(Riwayat.tanggal.desc()).all()
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

    # Segmentasi per kelurahan untuk treemap
    wilayah_data = {}
    for r in riwayat_list:
        kel = r.get('kelurahan', 'Lainnya')
        if kel not in wilayah_data:
            wilayah_data[kel] = {'jumlah': 0, 'status_list': []}
        wilayah_data[kel]['jumlah'] += 1
        wilayah_data[kel]['status_list'].append(r['status'])

    segmentasi_wilayah = []
    for kel, info in wilayah_data.items():
        dominan = Counter(info['status_list']).most_common(1)[0][0]
        segmentasi_wilayah.append({
            'kelurahan': kel,
            'jumlah': info['jumlah'],
            'dominan': dominan
        })

    return render_template(
        'dashboard.html',
        riwayat=riwayat_list,
        ringkasan=ringkasan,
        perbandingan=PERBANDINGAN,
        segmentasi_wilayah=segmentasi_wilayah
    )


# ─────────────────────────────────────────────
# INPUT FORM
# ─────────────────────────────────────────────

def input_data():
    return render_template('input.html')


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
    algoritma    = request.form.get('algoritma', 'xgboost')

    tinggi_m = tinggi_badan / 100
    imt = round(bb_awal / (tinggi_m ** 2), 2)

    import joblib
    import pandas as pd

    input_df = pd.DataFrame(
        [[umur, bb_awal, tinggi_badan, imt, lila]],
        columns=['umur', 'berat_badan_awal', 'tinggi', 'imt_sebelum_hamil', 'lila']
    )

    status = 'Normal'
    nama_algoritma = 'XGBoost (SMOTE)'

    try:
        if algoritma == 'catboost':
            model = joblib.load('ml/model_cat_smote.pkl')
            nama_algoritma = 'CatBoost (SMOTE)'
        else:
            model = joblib.load('ml/model_xgb_smote.pkl')
            nama_algoritma = 'XGBoost (SMOTE)'

        pred = model.predict(input_df)

        import numpy as np
        while isinstance(pred, (list, tuple, np.ndarray)) and (isinstance(pred, (list, tuple)) and len(pred) > 0 or isinstance(pred, np.ndarray) and pred.size > 0):
            if isinstance(pred, np.ndarray) and getattr(pred, 'ndim', 0) == 0:
                pred = pred.item()
                break
            pred = pred[0]

        pred_class = pred

        mapping_status = {0: 'Kurang', 1: 'Normal', 2: 'Lebih', 3: 'Obesitas'}

        if isinstance(pred_class, (int, float)) or str(pred_class).isdigit():
            status = mapping_status.get(int(pred_class), 'Normal')
        else:
            status = str(pred_class).strip("[]'\" ")

    except Exception as e:
        print("Error saat prediksi:", e)

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
        'rekomendasi_bb':   REKOMENDASI_BB.get(status, '-')
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
    return render_template(
        'algoritma.html',
        perbandingan=PERBANDINGAN,
        confusion=CONFUSION
    )