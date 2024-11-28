# Gunakan Python 3.8 sebagai base image
FROM python:3.8-slim

# Set work directory
WORKDIR /app

# Install dependensi sistem yang diperlukan untuk Torch dan lainnya
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    libomp-dev \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    wget \
    libc6-dev \
    gfortran \
    libatlas-base-dev && \
    apt-get clean && \
    apt-get install -f  # Memperbaiki ketergantungan yang hilang

# Salin file requirements.txt
COPY requirements.txt /app/requirements.txt

# Install dependensi dari requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Torch dan TensorFlow secara terpisah
RUN pip install --no-cache-dir torch==1.10.2+cpu torchvision==0.11.3+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install --no-cache-dir tensorflow==2.12.0  # Sesuaikan dengan versi yang dibutuhkan

# Salin seluruh file proyek ke dalam kontainer
COPY . /app

# Expose port Flask
EXPOSE 5000

# Perintah untuk menjalankan aplikasi
CMD ["python", "app.py"]
