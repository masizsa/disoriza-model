# Disoriza API (Python 3.8)

<a href='https://play.google.com/store/apps/details?id=com.disoriza.app'>Link Application</a>

Disoriza is a system for classifying diseases on the leaves of rice plants. This system uses a 2 layer model mechanism. The first layer as object detection, the second layer as disease classification.

## 🎯 Features

- User authentication and profile management
- Rice leaf detection using 2 layer model mechanism (YoloV5 & CNN)
- Scan history tracking
- Community forum

## 🌿 Supported Rice Leaf Disease Categories

- Bacterial Leaf Blight
- Brown Spot
- Leaf Blast
- Leaf Scald
- Narrow Brown Spot
- Healthy

## 🚀 Getting Started

1. Clone this repository
   ```
   git clone https://github.com/masizsa/disoriza-model.git
   ```
2. <a href="https://drive.google.com/drive/folders/1LxhGZavLygNl6xyF8wyBnViaVVPkOjM9?usp=sharing">Download</a> required model
3. Put the downloaded model in the “models” folder
4. Create _virtualenv_

   ```
   python -m venv "name_virtual_env"
   ```

5. Run to activate _virtual environment_

   ```
   "name_virtual_env"/Scripts/activate
   ```

6. Install semua requirement dengan menggunakan
   ```
   pip install -r requirements.txt
   ```
7. Run application

   ```
   python app.py
   ```

8. Use Postman or other alternatives to test the API that has been created

## Test API

_API Endpoint_

```
http://127.0.0.1:5000/detect
```

_Request Body_

```json
{
   "image": File
}
```

_Success Response (200)_

```json
{
  "status": "success",
  "message": "Padi yang dipindai memiliki penyakit.",
  "data": {
    "label": "Brown Spot",
    "confidence": "0.9876457"
  }
}
```

_Success Response (201)_

```json
{
  "status": "success",
  "message": "Padi yang dipindai sehat.",
  "data": null
}
```

_Success Response (202)_

```json
{
  "status": "error",
  "message": "Tidak dapat mendeteksi daun padi pada foto.",
  "data": null
}
```

**Error Response (400)**

```json
{
  "status": "error",
  "message": "Gambar tidak ditemukan.",
  "data": null
}
```
