# Sistem Klasifikasi Gizi Ibu Hamil (Flask & Machine Learning)

Sistem berbasis web yang dibangun menggunakan **Flask** untuk mengklasifikasikan status gizi ibu hamil menggunakan algoritma **XGBoost** dan **CatBoost**.

## 📁 Struktur Proyek
* `app.py`: Entry point aplikasi Flask.
* `models/`: Folder untuk menyimpan model hasil training (XGBoost/CatBoost).
* `templates/` & `static/`: Frontend (HTML, CSS, JS).
* `requirements.txt`: Daftar library (Scikit-learn, Pandas, dll).

## 🚀 Cara Menjalankan dengan Docker
Karena sudah tersedia file `Dockerfile` dan `docker-compose.yml`, kamu bisa langsung menjalankan sistem tanpa instal Python di laptop:

1.  **Buka Terminal** (PowerShell/CMD) di folder proyek.
2.  **Jalankan Docker Compose:**
    ```bash
    docker-compose up --build
    ```
3.  **Akses Aplikasi:**
    Buka browser dan ketik: `http://localhost:5000`

4. **Login Aplikasi**
    Username: `admin@gmail.com`
    Password: `admin123`

## 🛠️ Cara Menjalankan Tanpa Docker (Local venv)
Jika ingin menjalankan manual lewat terminal:

1.  **Buat Virtual Environment:**
    ```bash
    python -m venv venv
    ```
2.  **Aktifkan venv:**
    * Windows: `.\venv\Scripts\activate`
    * Linux/Mac: `source venv/bin/activate`

3.  **Instal Library:**
    ```bash
    pip install "setuptools<70.0.0" "wheel<0.44.0"
    ```
    ```bash
    pip install -r requirements.txt
    ```
4.  **Running:**
    ```bash
    python app.py
    ```

## 📦 Tech Stack
* **Backend:** Python 3.12 (Slim Image)
* **ML Libraries:** `xgboost`, `catboost`, `scikit-learn`, `imbalanced-learn`
* **Data:** `pandas`, `numpy`
* **Container:** Docker & Docker Compose

(venv) kumo@vmi3335119:~/kumo-project/website-klasifikasi$ ps aux | grep -i 'gunicorn\|flask'
kumo      239987  0.0  0.3 110704 26416 ?        Ssl  Jun19   1:20 /home/kumo/kumo-project/website-klasifikasi/venv/bin/python3 /home/kumo/kumo-project/website-klasifikasi/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 -m 007 app:app
kumo      239990  0.0  3.2 2586300 261732 ?      Sl   Jun19   0:14 /home/kumo/kumo-project/website-klasifikasi/venv/bin/python3 /home/kumo/kumo-project/website-klasifikasi/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 -m 007 app:app
kumo      239991  0.0  3.2 2587360 262584 ?      Sl   Jun19   0:14 /home/kumo/kumo-project/website-klasifikasi/venv/bin/python3 /home/kumo/kumo-project/website-klasifikasi/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 -m 007 app:app
kumo      239992  0.0  3.1 2585240 260204 ?      Sl   Jun19   0:14 /home/kumo/kumo-project/website-klasifikasi/venv/bin/python3 /home/kumo/kumo-project/website-klasifikasi/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 -m 007 app:app
kumo      290232  0.0  0.0   7084  2260 pts/0    S+   10:20   0:00 grep --color=auto -i gunicorn\|flask
(venv) kumo@vmi3335119:~/kumo-project/website-klasifikasi$ 

