# Gunakan base image Python
FROM python:3.9-slim

# Set work directory
WORKDIR /app

# Salin semua file proyek ke container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port Flask
EXPOSE 5000

# Perintah untuk menjalankan aplikasi
CMD ["python", "app.py"]
