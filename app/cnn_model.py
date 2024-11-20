import tensorflow as tf
import numpy as np
from PIL import Image

def classify_disease( image_path,model_path='./models/cnn_model.tflite',):
    """
    Melakukan klasifikasi penyakit pada daun padi menggunakan model TFLite.
    
    Args:
        model_path (str): Path ke model TFLite.
        image_path (str): Path ke gambar input.
        
    Returns:
        tuple: (label_prediksi, confidence) dalam bentuk string dan float.
    """
    # Label penyakit (sesuaikan dengan urutan kelas di model Anda)
    labels = [
        "bacterial_leaf_blight",
        "brown_spot",
        "healthy",
        "leaf_blast",
        "leaf_scald",
        "narrow_brown_spot",
    ]
    
    # Memuat model TFLite
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    
    # Mendapatkan informasi tensor input dan output
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    # Menentukan ukuran input yang diharapkan oleh model
    input_shape = input_details[0]['shape']
    input_size = tuple(input_shape[1:3])  # Mengambil dimensi tinggi dan lebar
    
    # Memuat dan memproses gambar
    image = Image.open(image_path)
    image = image.resize(input_size)
    image = np.array(image, dtype=np.float32)
    
    # Jika gambar RGB, normalisasi dan ubah bentuknya
    if image.shape[-1] == 3:
        image = image / 255.0  # Normalisasi ke rentang [0, 1]
    image = np.expand_dims(image, axis=0)  # Menambah dimensi batch
    
    # Memasukkan gambar ke dalam input tensor
    interpreter.set_tensor(input_details[0]['index'], image)
    
    # Menjalankan inferensi
    interpreter.invoke()
    
    # Mendapatkan hasil dari output tensor
    output_data = interpreter.get_tensor(output_details[0]['index'])
    
    # Menentukan prediksi label dan confidence tertinggi
    predicted_index = np.argmax(output_data)
    confidence = float(output_data[0][predicted_index])
    label_prediksi = labels[predicted_index]

    print(predicted_index)
    
    # Mengembalikan hasil dalam format JSON-friendly
    return label_prediksi, confidence
