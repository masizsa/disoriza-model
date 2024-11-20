from flask import Blueprint, request, jsonify
from .yolov5_model import detect_padi
from .cnn_model import classify_disease
import os

bp = Blueprint('routes', __name__)

@bp.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    # Simpan gambar yang diunggah
    image = request.files['image']
    image_path = f'./static/uploads/{image.filename}'
    os.makedirs('./static/uploads', exist_ok=True)
    image.save(image_path)

    # Jalankan deteksi menggunakan YOLOv5
    detections = detect_padi(image_path)

    if detections:
        disease_results = []

        # Jalankan identifikasi penyakit pada setiap deteksi
        label, confidence = classify_disease( image_path)
        disease_results.append({'label': label, 'confidence': confidence})

        return ({'detections': detections, 'disease_results': disease_results})
    else:
        return jsonify({'message': 'No rice leaf detected'}), 200
    