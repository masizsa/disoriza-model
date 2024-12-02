from flask import Blueprint, request, jsonify
from .yolov5_model import detect_padi
from .cnn_model import classify_disease
import os
import shutil

bp = Blueprint('routes', __name__)

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

@bp.route('/detect', methods=['POST'])
def detect():
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
