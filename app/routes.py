from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
import bcrypt
import os
import shutil
import time

bp = Blueprint('routes', __name__)

# Dictionary untuk menyimpan waktu permintaan terakhir dari masing-masing IP pengguna
last_request_times = {}

# Simulasikan basis data pengguna
users_db = {
    "admin": bcrypt.hashpw("ganteng".encode('utf-8'), bcrypt.gensalt())  # Password di-hash
}

def clean_folders(folders):
    """
    Menghapus folder secara rekursif jika ada.
    """
    for folder in folders:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
                print(f"Folder '{folder}' berhasil dihapus.")
            except Exception as e:
                print(f"Gagal menghapus folder '{folder}': {e}")

# Endpoint untuk login dan menghasilkan token JWT
@bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    # Validasi username dan password
    if username not in users_db:
        return jsonify({
            "status": "error",
            "message": "Username atau password salah.",
            "data": None
        }), 401
    
    # Verifikasi password yang di-hash dengan bcrypt
    stored_password_hash = users_db[username]
    if not bcrypt.checkpw(password.encode('utf-8'), stored_password_hash):
        return jsonify({
            "status": "error",
            "message": "Username atau password salah.",
            "data": None
        }), 401

    # Membuat token JWT jika autentikasi berhasil
    access_token = create_access_token(identity=username)
    return jsonify({
        "status": "success",
        "message": "Login berhasil.",
        "data": {
            "access_token": access_token
        }
    }), 200

# Endpoint untuk deteksi, dengan validasi JWT
@bp.route('/detect', methods=['POST'])
@jwt_required()
def detect():
    user_ip = request.remote_addr  # Mengambil alamat IP pengguna

    # Periksa apakah pengguna telah membuat permintaan dalam 5 detik terakhir
    current_time = time.time()
    if user_ip in last_request_times:
        time_difference = current_time - last_request_times[user_ip]
        if time_difference < 5:
            return jsonify({
                "status": "error",
                "message": "Tunggu beberapa detik sebelum mencoba lagi.",
                "data": None
            }), 429  # Status code untuk terlalu banyak permintaan (Too Many Requests)

    # Simpan waktu permintaan terakhir dari pengguna
    last_request_times[user_ip] = current_time

    if 'image' not in request.files:
        return jsonify({
            "status": "error",
            "message": "Gambar tidak ditemukan.",
            "data": None
        }), 400

    # Simpan gambar yang diunggah
    image = request.files['image']
    image_path = f'./static/uploads/{image.filename}'
    os.makedirs('./static/uploads', exist_ok=True)
    image.save(image_path)

    # Jalankan deteksi menggunakan YOLOv5
    detections = detect_padi(image_path)

    if detections:
        # Jalankan identifikasi penyakit pada setiap deteksi
        label, confidence = classify_disease(image_path)

        # Bersihkan folder setelah proses selesai
        clean_folders(['./static/uploads', './static/results'])

        if label == 'healthy':
            return jsonify({
                "status": "success",
                "message": "Padi yang dipindai sehat.",
                "data": None
            }), 201

        return jsonify({
            "status": "success",
            "message": "Padi yang dipindai memiliki penyakit.",
            "data": {
                "label": label,
                "confidence": confidence
            }
        }), 200
    else:
        # Bersihkan folder jika tidak ada deteksi
        clean_folders(['./static/uploads', './static/results'])

        return jsonify({
            "status": "error",
            "message": "Tidak dapat mendeteksi daun padi pada foto.",
            "data": None
        }), 202
