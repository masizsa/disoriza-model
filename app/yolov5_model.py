import os
import sys
import json
import torch

# Masukkan path YOLOv5
yolov5_path = os.path.join(os.getcwd(), 'yolov5')
sys.path.append(yolov5_path)

from yolov5.detect import run

def detect_padi(image_path):
    results_path = './static/results'
    os.makedirs(results_path, exist_ok=True)
    
    run(weights='./models/best.pt', 
        source=image_path, 
        project=results_path, 
        save_txt=True, 
        save_conf=True,
        conf_thres=0.1)

    # Load hasil deteksi
    results_file = os.path.join(results_path, 'exp', 'labels', os.path.basename(image_path).replace('.jpg', '.txt'))
    if os.path.exists(results_file):
        with open(results_file, 'r') as f:
            detections = [line.strip().split() for line in f.readlines()]
        return detections  # Format: [class, x_center, y_center, width, height, confidence]
    return None
