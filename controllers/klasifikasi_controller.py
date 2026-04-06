from flask import render_template, request, redirect, url_for

# Dummy data
RIWAYAT = [
    {'id': 1, 'nama': 'Siti Nurhaliza', 'umur': 25, 'bb_awal': 49, 'bb_sekarang': 56, 'tinggi_badan': 155, 'lila': 25.5, 'trimester': 2, 'imt': 20.40, 'status': 'Normal', 'tanggal': '15 Jan 2026', 'algoritma': 'XGBoost'},
    {'id': 2, 'nama': 'Rina Wati', 'umur': 32, 'bb_awal': 42, 'bb_sekarang': 48, 'tinggi_badan': 150, 'lila': 21.0, 'trimester': 1, 'imt': 18.67, 'status': 'Kurang', 'tanggal': '18 Jan 2026', 'algoritma': 'CatBoost'},
]

PERBANDINGAN = {
    'XGBoost': {'accuracy': 96.5, 'precision': 95.8, 'recall': 96.2, 'f1': 96.0},
    'CatBoost': {'accuracy': 97.2, 'precision': 96.9, 'recall': 97.0, 'f1': 96.9},
}

TIPS = {
    'Kurang': ['Tingkatkan asupan kalori.', 'Konsumsi protein lebih banyak.'],
    'Normal': ['Pertahankan pola makan sehat.'],
    'Lebih': ['Kurangi makanan tinggi lemak.'],
    'Obesitas': ['Konsultasi dengan ahli gizi.']
}

REKOMENDASI_BB = {
    'Kurang': '12,5 - 18 Kg',
    'Normal': '11,5 - 16 Kg',
    'Lebih': '7 - 11,5 Kg',
    'Obesitas': '5 - 9 Kg'
}


def dashboard():

    total = len(RIWAYAT)
    normal = sum(1 for r in RIWAYAT if r['status'] == 'Normal')
    kurang = sum(1 for r in RIWAYAT if r['status'] == 'Kurang')
    lebih = sum(1 for r in RIWAYAT if r['status'] == 'Lebih')
    obesitas = sum(1 for r in RIWAYAT if r['status'] == 'Obesitas')

    ringkasan = {
        'total': total,
        'normal': normal,
        'kurang': kurang,
        'lebih': lebih,
        'obesitas': obesitas
    }

    return render_template(
        'dashboard.html',
        riwayat=RIWAYAT,
        ringkasan=ringkasan,
        perbandingan=PERBANDINGAN
    )


def input_data():
    return render_template('input.html')


def klasifikasi():

    nama = request.form.get('nama')
    umur = float(request.form.get('umur'))
    bb_awal = float(request.form.get('bb_awal'))
    bb_sekarang = float(request.form.get('bb_sekarang'))
    tinggi_badan = float(request.form.get('tinggi_badan'))
    lila = float(request.form.get('lila'))
    trimester = int(request.form.get('trimester'))

    tinggi_m = tinggi_badan / 100
    imt = round(bb_awal / (tinggi_m ** 2), 2)

    if imt < 18.5:
        status = 'Kurang'
    elif imt <= 24.9:
        status = 'Normal'
    elif imt <= 29.9:
        status = 'Lebih'
    else:
        status = 'Obesitas'

    hasil = {
        'nama': nama,
        'umur': umur,
        'bb_awal': bb_awal,
        'bb_sekarang': bb_sekarang,
        'tinggi_badan': tinggi_badan,
        'lila': lila,
        'trimester': trimester,
        'imt': imt,
        'status': status,
        'tips': TIPS.get(status, []),
        'rekomendasi_bb': REKOMENDASI_BB.get(status, '-')
    }

    return render_template('hasil.html', hasil=hasil)


def detail_riwayat(id):

    data = next((r for r in RIWAYAT if r['id'] == id), None)

    if data is None:
        return redirect(url_for('main_routes.dashboard'))

    data['tips'] = TIPS.get(data['status'], [])
    data['rekomendasi_bb'] = REKOMENDASI_BB.get(data['status'], '-')

    return render_template('detail.html', data=data)


def edit_riwayat(id):

    data = next((r for r in RIWAYAT if r['id'] == id), None)

    if data is None:
        return redirect(url_for('main_routes.dashboard'))

    return render_template('edit.html', data=data)