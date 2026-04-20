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