# Gunakan Python 3.8 sebagai base image
FROM python:3.8-slim

# Set work directory
WORKDIR /app

# Install dependensi sistem yang diperlukan untuk Torch, OpenCV, dan lainnya
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    libomp-dev \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    wget \
    libgl1-mesa-glx \
    libc6-dev \
    gfortran \
    libatlas-base-dev && \
    apt-get clean

# Salin file requirements.txt
COPY requirements.txt /app/requirements.txt

# Install dependensi dari requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh file proyek ke dalam kontainer
COPY . /app

# Expose port Flask
EXPOSE 5000

# Perintah untuk menjalankan aplikasi
CMD ["python3", "app.py"]
