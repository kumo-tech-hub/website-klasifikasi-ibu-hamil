from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'nutricheck-secret-key-2026'

# ============================================================
# Dummy Credentials
# ============================================================
DUMMY_USER = {
    'email': 'admin@gmail.com',
    'password': 'admin123',
    'nama': 'Annisa Auliya R.',
    'nim': 'E1E122003',
    'role': 'Administrator'
}

# ============================================================
# Auth Decorator
# ============================================================
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


# ============================================================
# Data dummy riwayat pemeriksaan
# ============================================================
RIWAYAT = [
    {'id': 1, 'nama': 'Siti Nurhaliza', 'umur': 25, 'bb_awal': 49, 'bb_sekarang': 56, 'tinggi_badan': 155, 'lila': 25.5, 'trimester': 2, 'imt': 20.40, 'status': 'Normal',   'tanggal': '15 Jan 2026', 'algoritma': 'XGBoost'},
    {'id': 2, 'nama': 'Rina Wati',       'umur': 32, 'bb_awal': 42, 'bb_sekarang': 48, 'tinggi_badan': 150, 'lila': 21.0, 'trimester': 1, 'imt': 18.67, 'status': 'Kurang',   'tanggal': '18 Jan 2026', 'algoritma': 'CatBoost'},
    {'id': 3, 'nama': 'Dewi Anggraini',  'umur': 28, 'bb_awal': 72, 'bb_sekarang': 80, 'tinggi_badan': 158, 'lila': 30.0, 'trimester': 3, 'imt': 28.84, 'status': 'Lebih',    'tanggal': '22 Jan 2026', 'algoritma': 'XGBoost'},
    {'id': 4, 'nama': 'Fatimah Zahra',   'umur': 35, 'bb_awal': 85, 'bb_sekarang': 93, 'tinggi_badan': 160, 'lila': 33.0, 'trimester': 2, 'imt': 33.20, 'status': 'Obesitas', 'tanggal': '25 Jan 2026', 'algoritma': 'CatBoost'},
    {'id': 5, 'nama': 'Amira Putri',     'umur': 22, 'bb_awal': 50, 'bb_sekarang': 58, 'tinggi_badan': 162, 'lila': 26.0, 'trimester': 3, 'imt': 19.05, 'status': 'Normal',   'tanggal': '28 Jan 2026', 'algoritma': 'XGBoost'},
]

# Data dummy perbandingan algoritma
PERBANDINGAN = {
    'XGBoost':  {'accuracy': 96.5, 'precision': 95.8, 'recall': 96.2, 'f1': 96.0},
    'CatBoost': {'accuracy': 97.2, 'precision': 96.9, 'recall': 97.0, 'f1': 96.9},
}

TIPS = {
    'Kurang': [
        'Tingkatkan asupan kalori harian dengan makanan bergizi seimbang.',
        'Konsumsi protein hewani dan nabati secara teratur.',
        'Perbanyak makan sayuran hijau dan buah-buahan segar.',
        'Minum susu ibu hamil untuk menambah asupan nutrisi.',
        'Konsumsi makanan tinggi zat besi untuk mencegah anemia.',
        'Rutin melakukan pemeriksaan kehamilan sesuai jadwal.'
    ],
    'Normal': [
        'Konsumsi makanan bergizi seimbang dengan porsi yang cukup.',
        'Perbanyak sayuran, buah-buahan, protein, dan karbohidrat kompleks.',
        'Minum air putih 8-10 gelas per hari.',
        'Istirahat yang cukup dan hindari stres berlebihan.',
        'Olahraga ringan seperti jalan santai atau senam hamil.',
        'Rutin melakukan pemeriksaan kehamilan sesuai jadwal.'
    ],
    'Lebih': [
        'Kurangi makanan tinggi lemak dan gula berlebih.',
        'Perbanyak konsumsi sayur dan buah rendah kalori.',
        'Pilih karbohidrat kompleks (nasi merah, oat, roti gandum).',
        'Tetap aktif dengan olahraga ringan sesuai anjuran dokter.',
        'Hindari makanan cepat saji dan minuman manis.',
        'Pantau kenaikan berat badan secara berkala.'
    ],
    'Obesitas': [
        'Konsultasikan pola makan dengan ahli gizi secara intensif.',
        'Batasi asupan kalori berlebih tanpa mengurangi nutrisi penting.',
        'Hindari makanan tinggi gula, garam, dan lemak jenuh.',
        'Lakukan aktivitas fisik ringan secara teratur.',
        'Pantau tekanan darah dan kadar gula darah secara rutin.',
        'Waspadai tanda-tanda diabetes gestasional dan preeklamsia.'
    ]
}

REKOMENDASI_BB = {
    'Kurang':  '12,5 - 18 Kg',
    'Normal':  '11,5 - 16 Kg',
    'Lebih':   '7 - 11,5 Kg',
    'Obesitas': '5 - 9 Kg'
}


# ============================================================
# Auth Routes
# ============================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('dashboard'))

    error = None
    if request.method == 'POST':
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if email == DUMMY_USER['email'] and password == DUMMY_USER['password']:
            session['user'] = {
                'email': DUMMY_USER['email'],
                'nama':  DUMMY_USER['nama'],
                'nim':   DUMMY_USER['nim'],
                'role':  DUMMY_USER['role'],
            }
            return redirect(url_for('dashboard'))
        else:
            error = 'Email atau password salah. Silakan coba lagi.'

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


# ============================================================
# Main Routes (protected)
# ============================================================

@app.route('/')
@login_required
def dashboard():
    total    = len(RIWAYAT)
    normal   = sum(1 for r in RIWAYAT if r['status'] == 'Normal')
    kurang   = sum(1 for r in RIWAYAT if r['status'] == 'Kurang')
    lebih    = sum(1 for r in RIWAYAT if r['status'] == 'Lebih')
    obesitas = sum(1 for r in RIWAYAT if r['status'] == 'Obesitas')

    ringkasan = {
        'total': total, 'normal': normal,
        'kurang': kurang, 'lebih': lebih, 'obesitas': obesitas
    }

    return render_template('dashboard.html',
        riwayat=RIWAYAT,
        ringkasan=ringkasan,
        perbandingan=PERBANDINGAN,
        user=session.get('user')
    )


@app.route('/klasifikasi')
@login_required
def input_data():
    return render_template('input.html', user=session.get('user'))


@app.route('/klasifikasi/proses', methods=['POST'])
@login_required
def klasifikasi():
    nama          = request.form.get('nama')
    umur          = float(request.form.get('umur'))
    bb_awal       = float(request.form.get('bb_awal'))
    bb_sekarang   = float(request.form.get('bb_sekarang'))
    tinggi_badan  = float(request.form.get('tinggi_badan'))
    lila          = float(request.form.get('lila'))
    trimester     = int(request.form.get('trimester'))

    tinggi_m = tinggi_badan / 100
    imt      = round(bb_awal / (tinggi_m ** 2), 2)

    if imt < 18.5:
        status = 'Kurang'
    elif imt <= 24.9:
        status = 'Normal'
    elif imt <= 29.9:
        status = 'Lebih'
    else:
        status = 'Obesitas'

    hasil = {
        'nama': nama, 'umur': umur, 'bb_awal': bb_awal,
        'bb_sekarang': bb_sekarang, 'tinggi_badan': tinggi_badan,
        'lila': lila, 'trimester': trimester, 'imt': imt,
        'status': status,
        'tips': TIPS.get(status, []),
        'rekomendasi_bb': REKOMENDASI_BB.get(status, '-')
    }

    return render_template('hasil.html', hasil=hasil, user=session.get('user'))


@app.route('/riwayat/<int:id>')
@login_required
def detail_riwayat(id):
    data = next((r for r in RIWAYAT if r['id'] == id), None)
    if data is None:
        return redirect(url_for('dashboard'))
    data['tips']          = TIPS.get(data['status'], [])
    data['rekomendasi_bb'] = REKOMENDASI_BB.get(data['status'], '-')
    return render_template('detail.html', data=data, user=session.get('user'))


@app.route('/riwayat/<int:id>/edit')
@login_required
def edit_riwayat(id):
    data = next((r for r in RIWAYAT if r['id'] == id), None)
    if data is None:
        return redirect(url_for('dashboard'))
    return render_template('edit.html', data=data, user=session.get('user'))


if __name__ == '__main__':
    app.run(debug=True)