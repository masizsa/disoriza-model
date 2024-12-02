from flask import Blueprint, request, jsonify
from .yolov5_model import detect_padi
from .cnn_model import classify_disease
import os
import shutil

bp = Blueprint('routes', __name__)

@bp.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return jsonify({"status": "error","message": "Gambar tidak ditemukan.","data": None}), 400

    # Simpan gambar yang diunggah
    image = request.files['image']
    image_path = f'./static/uploads/{image.filename}'
    os.makedirs('./static/uploads', exist_ok=True)
    image.save(image_path)

    # Jalankan deteksi menggunakan YOLOv5
    detections = detect_padi(image_path)

    if detections:
        # disease_results = []

        # Jalankan identifikasi penyakit pada setiap deteksi
        label, confidence = classify_disease(image_path)

        # disease_results.append({'label': label, 'confidence': confidence})

        # Hapus folder ./static/uploads/ dan ./static/results/
        for folder in ['./static/uploads', './static/results']:
            if os.path.exists(folder):
                shutil.rmtree(folder)

        if (label=='healthy'):
            return jsonify({"status": "success", "message": "Padi yang dipindai sehat.", "data": None}), 201

        return jsonify({"status": "success", "message": "Padi yang dipindai memiliki penyakit.", 
                        "data": { 
                            "label": label, 
                            "confidence": confidence }
                        })
    else:
        for folder in ['./static/uploads', './static/results']:
            if os.path.exists(folder):
                shutil.rmtree(folder)

        return jsonify({"status": "error", "message": "Tidak dapat mendeteksi daun padi pada foto.", "data": None}), 202
