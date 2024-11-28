import os
import sys
import json
import torch
import time
import cv2

# Masukkan path YOLOv5
yolov5_path = os.path.join(os.getcwd(), 'yolov5')
sys.path.append(yolov5_path)

from yolov5.detect import run

def detect_padi(image_path):
    results_path = './static/results'
    os.makedirs(results_path, exist_ok=True)
    
    # Menentukan nama folder eksperimen secara dinamis menggunakan timestamp
    timestamp = time.strftime('%Y%m%d-%H%M%S')
    experiment_name = f"exp_{timestamp}"

    # Melakukan deteksi dengan YOLOv5
    run(weights='./models/best.pt', 
        source=image_path, 
        project=results_path, 
        save_txt=True, 
        save_conf=True, 
        conf_thres=0.2, 
        name=experiment_name)

    exts = ['.jpg', '.webp', '.jpeg']
    results_file = os.path.join(results_path, experiment_name, 'labels', os.path.basename(image_path))
    
    # Ganti ekstensi file dengan '.txt'
    for ext in exts:
        if results_file.endswith(ext):
            results_file = results_file.replace(ext, '.txt')
            break
        results_file = results_file.replace(os.sep, '/')

    # print(f"Path hasil deteksi: {results_file}")
    
    # Pastikan file hasil deteksi ada
    if os.path.exists(results_file):
        with open(results_file, 'r') as f:
            detections = [line.strip().split() for line in f.readlines()]
    else:
        print(f"File {results_file} tidak ditemukan.")
        return None

    # Membaca gambar asli untuk proses cropping
    image = cv2.imread(image_path)
    if image is None:
        print(f"Gambar {image_path} tidak ditemukan.")
        return None

    # Dimensi gambar
    h, w, _ = image.shape

    # Proses cropping berdasarkan kontur terbesar
    largest_bbox = None
    largest_area = 0

    for detection in detections:
        _, x_center, y_center, width, height, *_ = map(float, detection)
        x1 = int((x_center - width / 2) * w)
        y1 = int((y_center - height / 2) * h)
        x2 = int((x_center + width / 2) * w)
        y2 = int((y_center + height / 2) * h)

        # Hitung area bounding box
        area = (x2 - x1) * (y2 - y1)
        if area > largest_area:
            largest_area = area
            largest_bbox = (x1, y1, x2, y2)

    if largest_bbox:
        x1, y1, x2, y2 = largest_bbox
        # Pastikan koordinat tetap berada dalam batas gambar
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)

        # Crop gambar berdasarkan bounding box terbesar
        cropped_image = image[y1:y2, x1:x2]

        # Simpan gambar hasil cropping ke folder exp
        cropped_image_path = os.path.join(results_path, experiment_name, f"cropped_{os.path.basename(image_path)}")
        os.makedirs(os.path.dirname(cropped_image_path), exist_ok=True)
        cv2.imwrite(cropped_image_path, cropped_image)

        print(f"Gambar berhasil dipotong dan disimpan di: {cropped_image_path}")
        return cropped_image_path

    print("Tidak ada bounding box yang ditemukan.")
    return None
