# Gunakan base image Python
FROM python:3.9-slim

# Set work directory
WORKDIR /app

# Install dependencies sistem
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    wget && \
    apt-get clean

# Salin file requirements.txt
COPY requirements.txt /app/requirements.txt

# Install torch dari URL PyTorch
RUN pip install --no-cache-dir torch torchvision -f https://download.pytorch.org/whl/torch_stable.html

# Install dependensi lain
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file proyek
COPY . /app

# Expose port Flask
EXPOSE 5000

# Perintah untuk menjalankan aplikasi
CMD ["python", "app.py"]
